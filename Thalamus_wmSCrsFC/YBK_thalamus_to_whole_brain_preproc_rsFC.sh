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

	raw=${REST}/raw/*REST*.nii.gz
	if [ ! -e ${raw} ] ; then
		echo "${i} HAS NO RAW REST FILE"
	fi

    #### discard initial 4 ts ####
	if [ ! -e ${RS_preproc}/rsfMRI_raw.nii.gz ] ; then
	    fslroi ${raw} ${RS_preproc}/rsfMRI_raw.nii.gz 4 112
    fi
    #### motion correction ####
	if [ ! -e ${RS_preproc}/rsfMRI_raw_mcf.nii.gz ] ; then
	    mcflirt -in ${RS_preproc}/rsfMRI_raw -out ${RS_preproc}/rsfMRI_raw_mcf -mats -plots -rmsrel -rmsabs -spline_final
    fi
    #### slice time correction ####
    if [ ! -e ${RS_preproc}/rsfMRI_raw_mcf_st.nii.gz ] ; then	
        slicetimer -i ${RS_preproc}/rsfMRI_raw_mcf --out=${RS_preproc}/rsfMRI_raw_mcf_st -r 3.500000 --odd
    fi
    ##### brain extraction #####
	if [ ! -e ${RS_preproc}/rsfMRI_raw_mcf_st_bet.nii.gz ] ; then
	    fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st -Tmean ${RS_preproc}/mean_func
	    bet2 ${RS_preproc}/mean_func ${RS_preproc}/mask -f 0.3 -n -m
	    fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st -mas ${RS_preproc}/mask_mask ${RS_preproc}/rsfMRI_raw_mcf_st_bet
    fi
    #### temporal high pass filter (0.01Hz=100s) and bandpass filter (0.1Hz high pass, 0.01Hz low pass) ####
    ## sigma[vol] = filter_width[secs]/(2*TR)      0.1Hz=10secs, 0.01Hz=100secs
    ## highpass for seeb-based connectivity
    if [ ! -e ${RS_preproc}/tempMean.nii.gz ] ; then
	    fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st_bet -Tmean ${RS_preproc}/tempMean
    fi
	if [ ! -e ${RS_preproc}/rsfMRI_temp_hp.nii.gz ] ; then
	    fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st_bet -bptf 14.2857142857 -1 -add ${RS_preproc}/tempMean ${RS_preproc}/rsfMRI_temp_hp
	    fslmaths ${RS_preproc}/rsfMRI_temp_hp -Tmean ${RS_preproc}/mean_func_hp	
    fi
    ## bandpass for correlation between 2 voxels/s timeseries
	if [ ! -e ${RS_preproc}/rsfMRI_temp_bp.nii.gz ] ; then
	    fslmaths ${RS_preproc}/rsfMRI_raw_mcf_st_bet -bptf 1.42857142857 14.2857142857  -add ${RS_preproc}/tempMean ${RS_preproc}/rsfMRI_temp_bp
	    fslmaths ${RS_preproc}/rsfMRI_temp_bp -Tmean ${RS_preproc}/mean_func_bp	
    fi

    #### rsfMRI, T1, & MNI 2mm registration ####
	EPI_hp=${RS_preproc}/rsfMRI_temp_hp.nii.gz
    EPI_bp=${RS_preproc}/rsfMRI_temp_bp.nii.gz
	T1=${i}/T1/reorient_rawT1.nii.gz
	T1_brain=${i}/T1/reorient_rawT1_brain.nii.gz
	MNI=/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm
	MNI_brain=/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain
	MNI_brain_mask=/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain_mask_dil
	
	if [ ! -e ${RS_preproc}/hp2t1w.mat ] ; then
	    epi_reg --noclean --epi=${EPI_hp} --t1=${T1} --t1brain=${T1_brain} --out=${RS_preproc}/hp2t1w
	    convert_xfm -inverse -omat ${RS_preproc}/t1w2hp.mat ${RS_preproc}/hp2t1w.mat
    fi
	if [ ! -e ${RS_preproc}/bp2t1w.mat ] ; then
	    epi_reg --noclean --epi=${EPI_bp} --t1=${T1} --t1brain=${T1_brain} --out=${RS_preproc}/bp2t1w
	    convert_xfm -inverse -omat ${RS_preproc}/t1w2bp.mat ${RS_preproc}/bp2t1w.mat
    fi
    
    if [ ! -e ${RS_preproc}/t1w2mni_flirt.mat  ] ; then
        flirt -in ${T1_brain} -ref ${MNI_brain} -out ${RS_preproc}/t1w2mni_flirt -omat ${RS_preproc}/t1w2mni_flirt.mat -cost corratio -dof 12 -searchrx -180 180 -searchry -180 180 -searchrz -180 180 -interp trilinear
	    convert_xfm -inverse -omat ${RS_preproc}/mni2t1w_flirt.mat ${RS_preproc}/t1w2mni_flirt.mat
    fi

    if [ ! -e ${RS_preproc}/hp2mni.mat ] ; then
        convert_xfm -omat ${RS_preproc}/hp2mni.mat -concat ${RS_preproc}/t1w2mni_flirt.mat ${RS_preproc}/hp2t1w.mat
	    convert_xfm -inverse -omat ${RS_preproc}/mni2hp.mat ${RS_preproc}/hp2mni.mat
    fi
    if [ ! -e ${RS_preproc}/bp2mni.mat ] ; then
	    convert_xfm -omat ${RS_preproc}/bp2mni.mat -concat ${RS_preproc}/t1w2mni_flirt.mat ${RS_preproc}/bp2t1w.mat
	    convert_xfm -inverse -omat ${RS_preproc}/mni2bp.mat ${RS_preproc}/bp2mni.mat
    fi

    if [ ! -e ${RS_preproc}/t1w2mni_warp.nii.gz ] ; then 
        fnirt --in=${T1} --aff=${RS_preproc}/t1w2mni_flirt.mat --cout=${RS_preproc}/t1w2mni_warp --iout=${RS_preproc}/t1w2mni_fnirt --jout=${RS_preproc}/t1w2mni_jac --ref=${MNI} --refmask=${MNI_brain_mask}
	    applywarp -i ${T1_brain} -r ${MNI_brain} -o ${RS_preproc}/t1w2mni_brain_fnirt -w ${RS_preproc}/t1w2mni_warp
    fi

    if [ ! -e ${RS_preproc}/hp2mni.nii.gz ] ; then
        convertwarp --ref=${MNI_brain} --premat=${RS_preproc}/hp2t1w.mat --warp1=${RS_preproc}/t1w2mni_warp --out=${RS_preproc}/hp2mni_warp
	    applywarp -i ${EPI_hp} -r ${MNI_brain} -o ${RS_preproc}/hp2mni -w ${RS_preproc}/hp2mni_warp
    fi
    if [ ! -e ${RS_preproc}/bp2mni.nii.gz ] ; then
	    convertwarp --ref=${MNI_brain} --premat=${RS_preproc}/bp2t1w.mat --warp1=${RS_preproc}/t1w2mni_warp --out=${RS_preproc}/bp2mni_warp
	    applywarp -i ${EPI_bp} -r ${MNI_brain} -o ${RS_preproc}/bp2mni -w ${RS_preproc}/bp2mni_warp
    fi

    #### Nuisance Regression for Temporally Bandpass Filtered #####
    if [ ! -e ${RS_preproc}/bp_nuisance_design.mat ] ; then
        applywarp -r ${MNI_brain} -i ${RS_preproc}/bp2t1w_fast_pve_0.nii.gz -w ${RS_preproc}/t1w2mni_warp -o ${RS_preproc}/bp_fnirted_CSF.nii.gz
	    applywarp -r ${MNI_brain} -i ${RS_preproc}/bp2t1w_fast_pve_2.nii.gz -w ${RS_preproc}/t1w2mni_warp -o ${RS_preproc}/bp_fnirted_WM.nii.gz
	    fslmaths ${RS_preproc}/bp_fnirted_CSF.nii.gz -thr 0.50 ${RS_preproc}/bp_50thr_fnirted_CSF.nii.gz
	    fslmaths ${RS_preproc}/bp_fnirted_WM.nii.gz -thr 0.75 ${RS_preproc}/bp_75thr_fnirted_WM.nii.gz
	    fslmeants -i ${RS_preproc}/bp2mni.nii.gz -o ${RS_preproc}/bp_CSF_noise.txt -m ${RS_preproc}/bp_50thr_fnirted_CSF.nii.gz
	    fslmeants -i ${RS_preproc}/bp2mni.nii.gz -o ${RS_preproc}/bp_WM_noise.txt -m ${RS_preproc}/bp_75thr_fnirted_WM.nii.gz
	    paste ${RS_preproc}/rsfMRI_raw_mcf.par ${RS_preproc}/bp_CSF_noise.txt ${RS_preproc}/bp_WM_noise.txt > ${RS_preproc}/bp_nuisance_design.txt
	    Text2Vest ${RS_preproc}/bp_nuisance_design.txt ${RS_preproc}/bp_nuisance_design.mat
    fi

    if [ ! -e ${RS_preproc}/bp_nuisance_regressed.nii.gz ] ; then
	    fsl_regfilt -i ${RS_preproc}/bp2mni.nii.gz -d ${RS_preproc}/bp_nuisance_design.mat -o ${RS_preproc}/bp_nuisance_regressed -f 1,2,3,4,5,6,7,8
    fi

    #### Prepare Later Nuisance Regression for Temporally Highpass Filtered ####
    if [ ! -e ${RS_preproc}/hp_CSF_noise.txt ] ; then
        applywarp -r ${MNI_brain} -i ${RS_preproc}/hp2t1w_fast_pve_0.nii.gz -w ${RS_preproc}/t1w2mni_warp -o ${RS_preproc}/hp_fnirted_CSF.nii.gz
	    fslmaths ${RS_preproc}/hp_fnirted_CSF.nii.gz -thr 0.50 ${RS_preproc}/hp_50thr_fnirted_CSF.nii.gz
	    fslmeants -i ${RS_preproc}/hp2mni.nii.gz -o ${RS_preproc}/hp_CSF_noise.txt -m ${RS_preproc}/hp_50thr_fnirted_CSF.nii.gz
    fi
    if [ ! -e ${RS_preproc}/hp_WM_noise.txt ] ; then
	    applywarp -r ${MNI_brain} -i ${RS_preproc}/hp2t1w_fast_pve_2.nii.gz -w ${RS_preproc}/t1w2mni_warp -o ${RS_preproc}/hp_fnirted_WM.nii.gz
	    fslmaths ${RS_preproc}/hp_fnirted_WM.nii.gz -thr 0.75 ${RS_preproc}/hp_75thr_fnirted_WM.nii.gz
	    fslmeants -i ${RS_preproc}/hp2mni.nii.gz -o ${RS_preproc}/hp_WM_noise.txt -m ${RS_preproc}/hp_75thr_fnirted_WM.nii.gz
    fi

done








#	fsl_glm -i ${EPI_hp} -d <each thalamic IC> -o <ts of each thalamic IC>
#	paste <ts of each thalamic IC> <expanded motion parameters> <scans with excessive motion> <WM noise> <CSF noise> > <each_IC_design.txt>
#	Text2Vest <each_IC_design.txt> <each_IC_design.mat>
#	fsl_glm -i ${EPI_hp} -d <each_IC_design.mat> -o <each_IC_FCmap>

