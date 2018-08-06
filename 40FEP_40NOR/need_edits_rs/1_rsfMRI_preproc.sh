for i in $@
do
	REST=${i}/REST
	if [ ! -d ${REST} ] ; then
		mkdir ${REST}
	fi

	RS_preproc=${REST}/Preprocess
	if [ ! -d ${RS_preproc} ] ; then
		mkdir ${RS_preproc}
	fi

	#raw=${REST}/2*.nii.gz
	raw=${REST}/*.nii.gz
	if [ ! -e ${raw} ] ; then
		echo "${i} HAS NO RAW REST FILE"
	fi

    if [ -e ${raw} ] ; then
        #### 1. Discard initial 4 ts ####
	    if [ ! -e ${RS_preproc}/rsfMRI_raw.nii.gz ] ; then
	        fslroi ${raw} ${RS_preproc}/rsfMRI_raw.nii.gz 4 112
        fi
        
        #### 2. Motion correction ####
	    if [ ! -e ${RS_preproc}/rsfMRI_raw_mcf.nii.gz ] ; then
	        mcflirt -in ${RS_preproc}/rsfMRI_raw -out ${RS_preproc}/rsfMRI_raw_mcf -mats -plots -rmsrel -rmsabs -spline_final
        fi
        #### 3. Slice time correction ####
        if [ ! -e ${RS_preproc}/rsfMRI_raw_mcf_st.nii.gz ] ; then	
            slicetimer -i ${RS_preproc}/rsfMRI_raw_mcf --out=${RS_preproc}/rsfMRI_raw_mcf_st -r 3.500000 --odd
        fi
    
        ##### 4. Brain extraction #####
	    if [ ! -e ${RS_preproc}/rsfMRI_raw_mcf_st_bet.nii.gz ] ; then
	        fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st -Tmean ${RS_preproc}/mean_func
	        bet2 ${RS_preproc}/mean_func ${RS_preproc}/mask -f 0.3 -n -m
	        fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st -mas ${RS_preproc}/mask_mask ${RS_preproc}/rsfMRI_raw_mcf_st_bet
        fi

        #### Steps included in FEAT (lines 41-67)
        ## Calculate the difference between the 98th and 2nd percentile (the region between the tails) and use that range as a threshold minimum on the prefiltered, motion corrected, masked functional data (i.e., eliminate intensities below 2nd percentile, and above 98th percentile)
	    if [ ! -e ${RS_preproc}/rsfMRI_raw_mcf_st_bet_thresh_intnorm.nii.gz ] ; then
	        lowerp=`fslstats ${RS_preproc}/rsfMRI_raw_mcf_st_bet -p 2`
            upperp=`fslstats ${RS_preproc}/rsfMRI_raw_mcf_st_bet -p 98`
            BBTHRESH=10       # Brain background threshold
            thresholdp=`echo "scale=6; ($upperp-$lowerp)/$BBTHRESH" | bc`
            
            ## Use fslmaths to threshold the brain extracted data based on the filter (use "mask" as a binary mask, and Tmin to specify we want the minimum across time)
            fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st_bet -thr $thresholdp -Tmin -bin ${RS_preproc}/mask_mask -odt char      

            ## Needed later to calculate the intensity scaling factor
            meanintensity=`fslstats ${RS_preproc}/rsfMRI_raw_mcf_st -k ${RS_preproc}/mask_mask -p 50`
        
            fslmaths ${RS_preproc}/mask_mask -dilF ${RS_preproc}/mask_mask

            ## Mask to produce functional data that is motion corrected and thresholded based on the 2-98% filter
            fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st -mas ${RS_preproc}/mask_mask ${RS_preproc}/rsfMRI_raw_mcf_st_bet_thresh 

            ## Create a "mean_func" image that is the mean across time (Tmean)
            fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st_bet_thresh -Tmean ${RS_preproc}/mean_func2

            ## Calculate the intensity scaling factor applied to the whole  4D dataset so that it's mean is 10000
            inscalefactor=`echo "scale=6; ((10000/$meanintensity))" | bc`

            ## Multiply the data by the intensity scaling factor to get the intensity normalized data
            fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st_bet_thresh -mul $inscalefactor ${RS_preproc}/rsfMRI_raw_mcf_st_bet_thresh_intnorm
        fi

        #### 5. Temporal high pass filter (0.01Hz=100s) and bandpass filter (0.1Hz high pass, 0.01Hz low pass) ####
            ## sigma[vol] = filter_width[secs]/(2*TR)      0.1Hz=10secs, 0.01Hz=100secs
        if [ ! -e ${RS_preproc}/tempMean.nii.gz ] ; then
	        fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st_bet_thresh_intnorm -Tmean ${RS_preproc}/tempMean
        fi
        ## Highpass for seeb-based connectivity
        if [ ! -e ${RS_preproc}/rsfMRI_temp_hp.nii.gz ] ; then
	            fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st_bet_thresh_intnorm -bptf 14.2857142857 -1 -add ${RS_preproc}/tempMean ${RS_preproc}/rsfMRI_temp_hp
	            fslmaths ${RS_preproc}/rsfMRI_temp_hp -Tmean ${RS_preproc}/mean_func_hp	
        fi
         ## Bandpass for correlation between 2 voxels/s timeseries
	    if [ ! -e ${RS_preproc}/rsfMRI_temp_bp.nii.gz ] ; then
	        fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st_bet_thresh_intnorm -bptf 1.42857142857 14.2857142857  -add ${RS_preproc}/tempMean ${RS_preproc}/rsfMRI_temp_bp
	        fslmaths ${RS_preproc}/rsfMRI_temp_bp -Tmean ${RS_preproc}/mean_func_bp	
	    fi

        #### 6. Nuisance Regression for BP, preparation for HP ####
	    EPI_hp=${RS_preproc}/rsfMRI_temp_hp.nii.gz
        EPI_bp=${RS_preproc}/rsfMRI_temp_bp.nii.gz
	    T1=${i}/T1/reorient_rawT1.nii.gz
	    T1_brain=${i}/T1/reorient_rawT1_brain.nii.gz
	    T1w2hp=${RS_preproc}/t1w2hp
	    if [ ! -e ${T1w2hp} ] ; then
	        mkdir ${T1w2hp} 
        fi
	    T1w2bp=${RS_preproc}/t1w2bp
        if [ ! -e ${T1w2bp} ] ; then
            mkdir ${T1w2bp} 
        fi

	    if [ ! -e ${T1w2hp}/hp2t1w.mat ] ; then
	        epi_reg --noclean --epi=${EPI_hp} --t1=${T1} --t1brain=${T1_brain} --out=${T1w2hp}/hp2t1w
	        convert_xfm -inverse -omat ${T1w2hp}/t1w2hp.mat ${T1w2hp}/hp2t1w.mat
        fi
	    if [ ! -e ${T1w2bp}/bp2t1w.mat ] ; then
	        epi_reg --noclean --epi=${EPI_bp} --t1=${T1} --t1brain=${T1_brain} --out=${T1w2bp}/bp2t1w
	        convert_xfm -inverse -omat ${T1w2bp}/t1w2bp.mat ${T1w2bp}/bp2t1w.mat
        fi

        if [ ! -e ${RS_preproc}/nuisance_bp.mat ] ; then
            flirt -in ${T1w2bp}/bp2t1w_fast_pve_0.nii.gz -ref ${EPI_bp} -applyxfm -init ${T1w2bp}/t1w2bp.mat -out ${T1w2bp}/csf2bp.nii.gz
            flirt -in ${T1w2bp}/bp2t1w_fast_pve_2.nii.gz -ref ${EPI_bp} -applyxfm -init ${T1w2bp}/t1w2bp.mat -out ${T1w2bp}/wm2bp.nii.gz
            fslmaths ${T1w2bp}/csf2bp.nii.gz -thr 0.50 ${T1w2bp}/50thr_csf2bp.nii.gz
            fslmaths ${T1w2bp}/wm2bp.nii.gz -thr 0.75 ${T1w2bp}/75thr_wm2bp.nii.gz
            fslmeants -i ${EPI_bp} -o ${RS_preproc}/CSF_noise_bp.txt -m ${T1w2bp}/50thr_csf2bp.nii.gz
            fslmeants -i ${EPI_bp} -o ${RS_preproc}/WM_noise_bp.txt -m ${T1w2bp}/75thr_wm2bp.nii.gz
            paste ${RS_preproc}/rsfMRI_raw_mcf.par ${RS_preproc}/CSF_noise_bp.txt ${RS_preproc}/WM_noise_bp.txt > ${RS_preproc}/nuisance_bp.txt
	        Text2Vest ${RS_preproc}/nuisance_bp.txt ${RS_preproc}/nuisance_bp.mat
        fi
        
        if [ ! -e ${RS_preproc}/nuisance_regressed_bp.nii.gz ] ; then
	        fsl_regfilt -i ${EPI_bp} -d ${RS_preproc}/nuisance_bp.mat -o ${RS_preproc}/nuisance_regressed_bp -f 1,2,3,4,5,6,7,8
        fi

        if [ ! -e ${RS_preproc}/CSF_noise_hp.txt ] ; then
            flirt -in ${T1w2hp}/hp2t1w_fast_pve_0.nii.gz -ref ${EPI_hp} -applyxfm -init ${T1w2hp}/t1w2hp.mat -out ${T1w2hp}/csf2hp.nii.gz
            fslmaths ${T1w2hp}/csf2hp.nii.gz -thr 0.50 ${T1w2hp}/50thr_csf2hp.nii.gz
            fslmeants -i ${EPI_hp} -o ${RS_preproc}/CSF_noise_hp.txt -m ${T1w2hp}/50thr_csf2hp.nii.gz
        fi
           
        if [ ! -e ${RS_preproc}/WM_noise_hp.txt ] ; then
            flirt -in ${T1w2hp}/hp2t1w_fast_pve_2.nii.gz -ref ${EPI_hp} -applyxfm -init ${T1w2hp}/t1w2hp.mat -out ${T1w2hp}/wm2hp.nii.gz
            fslmaths ${T1w2hp}/wm2hp.nii.gz -thr 0.75 ${T1w2hp}/75thr_wm2hp.nii.gz
            fslmeants -i ${EPI_hp} -o ${RS_preproc}/WM_noise_hp.txt -m ${T1w2hp}/75thr_wm2hp.nii.gz
        fi
        
        #### 7. Register rsfMRI, T1, & MNI 2mm ####
        MNI=/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm
	    MNI_brain=/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain
	    MNI_brain_mask=/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain_mask_dil
	    hp2mni=${RS_preproc}/hp2mni
	    if [ ! -e ${hp2mni} ] ; then
	        mkdir ${hp2mni} 
        fi
	    bp2mni=${RS_preproc}/bp2mni
        if [ ! -e ${bp2mni} ] ; then
            mkdir ${bp2mni} 
        fi

        if [ ! -e ${RS_preproc}/t1w2mni_flirt.mat  ] ; then
            flirt -in ${T1_brain} -ref ${MNI_brain} -out ${RS_preproc}/t1w2mni_flirt -omat ${RS_preproc}/t1w2mni_flirt.mat -cost corratio -dof 12 -searchrx -180 180 -searchry -180 180 -searchrz -180 180 -interp trilinear
	        convert_xfm -inverse -omat ${RS_preproc}/mni2t1w_flirt.mat ${RS_preproc}/t1w2mni_flirt.mat
        fi

        if [ ! -e ${hp2mni}/hp2mni.mat ] ; then
            convert_xfm -omat ${hp2mni}/hp2mni.mat -concat ${RS_preproc}/t1w2mni_flirt.mat ${T1w2hp}/hp2t1w.mat
	        convert_xfm -inverse -omat ${hp2mni}/mni2hp.mat ${hp2mni}/hp2mni.mat
        fi

        if [ ! -e ${bp2mni}/bp2mni.mat ] ; then
            convert_xfm -omat ${bp2mni}/bp2mni.mat -concat ${RS_preproc}/t1w2mni_flirt.mat ${T1w2bp}/bp2t1w.mat
	        convert_xfm -inverse -omat ${bp2mni}/mni2bp.mat ${bp2mni}/bp2mni.mat
        fi
        
        if [ ! -e ${RS_preproc}/t1w2mni_warp.nii.gz ] ; then 
            fnirt --in=${T1} --aff=${RS_preproc}/t1w2mni_flirt.mat --cout=${RS_preproc}/t1w2mni_warp --iout=${RS_preproc}/t1w2mni_fnirt --jout=${RS_preproc}/t1w2mni_jac --ref=${MNI} --refmask=${MNI_brain_mask}
	        applywarp -i ${T1_brain} -r ${MNI_brain} -o ${RS_preproc}/t1w2mni_brain_fnirt -w ${RS_preproc}/t1w2mni_warp
        fi

        if [ ! -e ${hp2mni}/hp2mni.nii.gz ] ; then
            convertwarp --ref=${MNI_brain} --premat=${T1w2hp}/hp2t1w.mat --warp1=${RS_preproc}/t1w2mni_warp --out=${hp2mni}/hp2mni_warp
	        applywarp -i ${EPI_hp} -r ${MNI_brain} -o ${hp2mni}/hp2mni -w ${hp2mni}/hp2mni_warp
        fi

        if [ ! -e ${bp2mni}/bp2mni.nii.gz ] ; then
            convertwarp --ref=${MNI_brain} --premat=${T1w2bp}/bp2t1w.mat --warp1=${RS_preproc}/t1w2mni_warp --out=${bp2mni}/bp2mni_warp
	        applywarp -i ${RS_preproc}/nuisance_regressed_bp -r ${MNI_brain} -o ${bp2mni}/bp2mni -w ${bp2mni}/bp2mni_warp
        fi

        #### 8. Downsample ####
        if [ ! -e ${RS_preproc}/bp2mni_ds3.nii.gz ] ; then 
            flirt -interp nearestneighbour -in ${bp2mni}/bp2mni -ref ${bp2mni}/bp2mni -applyisoxfm 3 -out ${RS_preproc}/bp2mni_ds3 
        fi
        if [ ! -e ${RS_preproc}/bp2mni_ds4.nii.gz ] ; then 
            flirt -interp nearestneighbour -in ${bp2mni}/bp2mni -ref ${bp2mni}/bp2mni -applyisoxfm 4 -out ${RS_preproc}/bp2mni_ds4 
        fi
        if [ ! -e ${RS_preproc}/hp2mni_ds3.nii.gz ] ; then 
            flirt -interp nearestneighbour -in ${hp2mni}/hp2mni -ref ${hp2mni}/hp2mni -applyisoxfm 3 -out ${RS_preproc}/hp2mni_ds3 
        fi
        if [ ! -e ${RS_preproc}/hp2mni_ds4.nii.gz ] ; then 
            flirt -interp nearestneighbour -in ${hp2mni}/hp2mni -ref ${hp2mni}/hp2mni -applyisoxfm 4 -out ${RS_preproc}/hp2mni_ds4 
        fi
        
        #### 9. Thalamus mask on WB ####
        if [ ! -e masks/lh_thalamus_HOSC_60_ds3.nii.gz ] ; then
            flirt -interp nearestneighbour -in masks/lh_thalamus_HOSC_60.nii.gz -ref masks/lh_thalamus_HOSC_60.nii.gz -applyisoxfm 3 -out masks/lh_thalamus_HOSC_60_ds3.nii.gz 
        fi
        if [ ! -e masks/lh_thalamus_HOSC_60_ds4.nii.gz ] ; then
            flirt -interp nearestneighbour -in masks/lh_thalamus_HOSC_60.nii.gz -ref masks/lh_thalamus_HOSC_60.nii.gz -applyisoxfm 4 -out masks/lh_thalamus_HOSC_60_ds4.nii.gz 
        fi
        if [ ! -e masks/rh_thalamus_HOSC_60_ds3.nii.gz ] ; then
            flirt -interp nearestneighbour -in masks/rh_thalamus_HOSC_60.nii.gz -ref masks/rh_thalamus_HOSC_60.nii.gz -applyisoxfm 3 -out masks/rh_thalamus_HOSC_60_ds3.nii.gz 
        fi
        if [ ! -e masks/rh_thalamus_HOSC_60_ds4.nii.gz ] ; then
            flirt -interp nearestneighbour -in masks/rh_thalamus_HOSC_60.nii.gz -ref masks/rh_thalamus_HOSC_60.nii.gz -applyisoxfm 4 -out masks/rh_thalamus_HOSC_60_ds4.nii.gz 
        fi


        if [ ! -e ${RS_preproc}/L_thal_on_bp.nii.gz ] ; then
            fslmaths ${bp2mni}/bp2mni.nii.gz -mas masks/lh_thalamus_HOSC_60.nii.gz ${RS_preproc}/L_thal_on_bp.nii.gz 
        fi
        if [ ! -e ${RS_preproc}/L_thal_on_bp_ds3.nii.gz ] ; then
            fslmaths ${RS_preproc}/bp2mni_ds3.nii.gz -mas masks/lh_thalamus_HOSC_60_ds3.nii.gz ${RS_preproc}/L_thal_on_bp_ds3.nii.gz 
        fi
        if [ ! -e ${RS_preproc}/L_thal_on_bp_ds4.nii.gz ] ; then
            fslmaths ${RS_preproc}/bp2mni_ds4.nii.gz -mas masks/lh_thalamus_HOSC_60_ds4.nii.gz ${RS_preproc}/L_thal_on_bp_ds4.nii.gz 
        fi
        
        if [ ! -e ${RS_preproc}/R_thal_on_bp.nii.gz ] ; then
            fslmaths ${bp2mni}/bp2mni.nii.gz -mas masks/rh_thalamus_HOSC_60.nii.gz ${RS_preproc}/R_thal_on_bp.nii.gz 
        fi
        if [ ! -e ${RS_preproc}/R_thal_on_bp_ds3.nii.gz ] ; then
            fslmaths ${RS_preproc}/bp2mni_ds3.nii.gz -mas masks/rh_thalamus_HOSC_60_ds3.nii.gz ${RS_preproc}/R_thal_on_bp_ds3.nii.gz 
        fi
        if [ ! -e ${RS_preproc}/R_thal_on_bp_ds4.nii.gz ] ; then
            fslmaths ${RS_preproc}/bp2mni_ds4.nii.gz -mas masks/rh_thalamus_HOSC_60_ds4.nii.gz ${RS_preproc}/R_thal_on_bp_ds4.nii.gz 
        fi

        if [ ! -e ${RS_preproc}/Bi_thal_on_bp_ds3.nii.gz ] ; then
            fslmaths ${RS_preproc}/L_thal_on_bp_ds3.nii.gz -add ${RS_preproc}/R_thal_on_bp_ds3.nii.gz ${RS_preproc}/Bi_thal_on_bp_ds3.nii.gz
        fi
        
        if [ ! -e ${RS_preproc}/Bi_thal_on_bp.nii.gz ] ; then
            fslmaths ${RS_preproc}/L_thal_on_bp.nii.gz -add ${RS_preproc}/R_thal_on_bp.nii.gz ${RS_preproc}/Bi_thal_on_bp.nii.gz
        fi
    fi
done






