#mkdir RS
#mkdir T1
#mv 20140701_114912RESTfMRIPHASE1161s005a1001.nii.gz RS/
#mv 20140701_114912TFL3D208SLABs004a1001.nii.gz o20140701_114912TFL3D208SLABs004a1001.nii.gz co20140701_114912TFL3D208SLABs004a1001.nii.gz T1/

rsfMRI_raw=RS/20140701_114912RESTfMRIPHASE1161s005a1001.nii.gz
t1_data=T1/o20140701_114912TFL3D208SLABs004a1001.nii.gz

preproc_dir=Preprocess
if [ ! -d ${preproc_dir} ]
then
	mkdir ${preproc_dir}
fi

fslroi ${rsfMRI_raw} ${preproc_dir}/rs.nii.gz  4 112
rsfMRI=${preproc_dir}/rs.nii.gz 

mc_dir=${preproc_dir}/Motion_Correction
if [ ! -d ${mc_dir} ]
then
	mkdir ${mc_dir}
fi
mcflirt -in ${rsfMRI} -out ${mc_dir}/motion_corrected -mats -plots -rmsrel -rmsabs -spline_final

slicetimer -i ${mc_dir}/motion_corrected --out=${preproc_dir}/slice_time_corrected -r 3.500000 --odd

bet_dir=${preproc_dir}/Brain_Extract
if [ ! -d ${bet_dir} ]
then
	mkdir ${bet_dir}
fi
fslmaths ${preproc_dir}/slice_time_corrected -Tmean ${bet_dir}/mean_func
bet2 ${bet_dir}/mean_func ${bet_dir}/mask -f 0.3 -n -m
fslmaths ${preproc_dir}/slice_time_corrected -mas ${bet_dir}/mask_mask ${bet_dir}/rs_brain


##mkdir trial_bandpass
##cp -r Brain_extract/rs_brain.nii.gz trial_banpass/prac.nii.gz
##3dBandpass 0.01 0.1 prac.nii.gz 	
##3dresample -orient RPI -inset bandpass+orig -prefix 3dresample.nii
##OR 
##3dAFNItoNIFTI bandpass+orig -prefix bandpass.nii
##
##3dBandpass -band 0 0.1 -prefix higpass prac.nii.gz
##3dAFNItoNIFTI higpass+orig. -prefix highpass.nii


## dpabi used for temporal bandpass filtering (0.01 ~0.1 Hz)
#cp -r dpabi_temporal_bp/FunImgARF/NOR89/Filtered_4DVolume.nii dpabi_temporal_bp/FunImgARF/NOR89/bp.nii
#cp -r dpabi_temporal_bp/FunImgARF/NOR89/bp.nii ${preproc_dir}/bp.nii
#mri_convert ${preproc_dir}//bp.nii ${preproc_dir}//bp.nii.gz

cp -r T1/o20140701_114912TFL3D208SLABs004a1001.nii.gz ${bet_dir}/T1.nii.gz
bet ${bet_dir}/T1.nii.gz ${bet_dir}/T1_brain.nii.gz -m -f 0.3 -B

reg_dir=${preproc_dir}/Registration
if [ ! -d ${reg_dir} ]
then
	mkdir ${reg_dir}
fi
EPI_image=${bet_dir}/rs_brain.nii.gz
EPI_bp_imgage=${preproc_dir}/bp.nii.gz
T1=${bet_dir}/T1.nii.gz
T1_brain=${bet_dir}/T1_brain.nii.gz
MNI_brain=/usr/local/fsl/data/standard/MNI152_T1_2mm_brain
MNI=/usr/local/fsl/data/standard/MNI152_T1_2mm
epi_reg --noclean --epi=${EPI_image} --t1=${T1} --t1brain=${T1_brain} --out=${reg_dir}/rs_to_t1
convert_xfm -inverse -omat ${reg_dir}/t1_to_rs.mat ${reg_dir}/rs_to_t1.mat
flirt -in ${T1_brain} -ref ${MNI_brain} -out ${reg_dir}/t1_to_mni_flirt -omat ${reg_dir}/t1_to_mni_flirt.mat -cost corratio -dof 12 -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -interp trilinear
convert_xfm -inverse -omat ${reg_dir}/mni_to_t1_flirt.mat ${reg_dir}/t1_to_mni_flirt.mat
convert_xfm -omat ${reg_dir}/rs_to_mni.mat -concat ${reg_dir}/t1_to_mni_flirt.mat ${reg_dir}/rs_to_t1.mat
convert_xfm -inverse -omat ${reg_dir}/mni_to_rs.mat ${reg_dir}/rs_to_mni.mat
fnirt --iout=${reg_dir}/t1_to_mni_head_fnirt --in=${T1} --aff=${reg_dir}/t1_to_mni_flirt.mat --cout=${reg_dir}/t1_to_mni_warp --iout=${reg_dir}/t1_to_mni_fnirt --jout=${reg_dir}/t1_to_t1_jac --ref=${MNI} --refmask=/usr/local/fsl/data/standard/MNI152_T1_2mm_brain_mask_dil
applywarp -i ${T1_brain} -r ${MNI_brain} -o ${reg_dir}/t1_to_mni_brain_fnirt -w ${reg_dir}/t1_to_mni_warp
convertwarp --ref=${MNI_brain} --premat=${reg_dir}/rs_to_t1.mat --warp1=${reg_dir}/t1_to_mni_warp --out=${reg_dir}/rs_to_mni_warp
applywarp -r ${MNI_brain} -i ${EPI_image} -o ${reg_dir}/rs_to_mni -w ${reg_dir}/rs_to_mni_warp

applywarp -i ${EPI_bp_image} -o ${reg_dir}/bp_to_mni -r ${MNI_brain} -w ${reg_dir}/rs_to_mni_warp


nuisance_dir=${preproc_dir}/Nuisance
if [ ! -d ${nuisance_dir} ]
then
	mkdir ${nuisance_dir}
fi
cp -r ${mc_dir}/motion_corrected.par ${nuisance_dir}/motion_corrected.par
fast  -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o ${nuisance_dir}/ ${bet_dir}/T1_brain.nii.gz
applywarp -r ${MNI_brain} -i ${nuisance_dir}/_pve_0.nii.gz -w ${reg_dir}/t1_to_mni_warp -o ${nuisance_dir}/fnirted_pve_0_CSF.nii.gz
applywarp -r ${MNI_brain} -i ${nuisance_dir}/_pve_2.nii.gz -w ${reg_dir}/t1_to_mni_warp -o ${nuisance_dir}/fnirted_pve_2_WM.nii.gz
fslmaths ${nuisance_dir}/fnirted_pve_0_CSF.nii.gz -thr 0.50 ${nuisance_dir}/50thr_fnirted_pve_0_CSF.nii.gz
fslmaths ${nuisance_dir}/fnirted_pve_2_WM.nii.gz -thr 0.75 ${nuisance_dir}/75thr_fnirted_pve_2_WM.nii.gz
fslmeants -i ${reg_dir}/bp_to_mni.nii.gz -o ${nuisance_dir}/CSF_noise.txt -m ${nuisance_dir}/50thr_fnirted_pve_0_CSF.nii.gz
fslmeants -i ${reg_dir}/bp_to_mni.nii.gz -o ${nuisance_dir}/WM_noise.txt -m ${nuisance_dir}/75thr_fnirted_pve_2_WM.nii.gz
paste ${nuisance_dir}/motion_corrected.par ${nuisance_dir}/CSF_noise.txt ${nuisance_dir}/WM_noise.txt > ${nuisance_dir}/nuisance_design.txt
Text2Vest ${nuisance_dir}/nuisance_design.txt ${nuisance_dir}/nuisance_design.mat
fsl_regfilt -i ${reg_dir}/bp_to_mni.nii.gz -d ${nuisance_dir}/nuisance_design.mat -o ${nuisance_dir}/nuisance_regressed -f 1,2,3,4,5,6,7,8


downsample_dir=${preproc_dir}/Downsampled
if [ ! -d ${downsample_dir} ]
then
	mkdir ${downsample_dir}	
fi
flirt -in ${nuisance_dir}/nuisance_regressed.nii.gz -ref ${nuisance_dir}/nuisance_regressed.nii.gz -out ${downsample_dir}/WB_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour -omat ${downsample_dir}/WB_3mm.mat
flirt -in ${nuisance_dir}/nuisance_regressed.nii.gz -ref ${nuisance_dir}/nuisance_regressed.nii.gz -out ${downsample_dir}/WB_4mm.nii.gz -applyisoxfm 4 -interp nearestneighbour -omat ${downsample_dir}/WB_4mm.mat
flirt -in thalamus_mask/L_thal_MNI2mmBrain.nii.gz -ref thalamus_mask/L_thal_MNI2mmBrain.nii.gz -out ${downsample_dir}/L_thal_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour -omat ${downsample_dir}/L_thal_3mm.mat
flirt -in thalamus_mask/L_thal_MNI2mmBrain.nii.gz -ref thalamus_mask/L_thal_MNI2mmBrain.nii.gz -out ${downsample_dir}/L_thal_4mm.nii.gz -applyisoxfm 4 -interp nearestneighbour -omat ${downsample_dir}/L_thal_4mm.mat





