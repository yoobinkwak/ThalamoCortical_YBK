for i in [CFN]*
do
    

###### head motion correction, slice timing 
#    mkdir ${i}/feat

    ### run feat (FSL GUI)

#    mv ${i}/registration/*.feat ${i}/feat/


    
###### CSF, WM, motion regressors

#    mkdir ${i}/nuisance

#    fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o ${i}/nuisance/ ${i}/bet/2nd_bet_neck_T1_co

#    flirt -in ${i}/nuisance/_pve_0.nii.gz -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -out ${i}/nuisance/registered_pve_0_CSF.nii.gz -applyxfm -init ${i}/registration/t1_ref_registered1.mat -interp trilinear

#    flirt -in ${i}/nuisance/_pve_2.nii.gz -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -out ${i}/nuisance/registered_pve_2_WM.nii.gz -applyxfm -init ${i}/registration/t1_ref_registered1.mat -interp trilinear

#    fslmaths ${i}/nuisance/registered_pve_0_CSF.nii.gz -thr 0.95 ${i}/nuisance/thr_registered_pve_0_CSF.nii.gz
#    fslmaths ${i}/nuisance/registered_pve_2_WM.nii.gz -thr 0.95 ${i}/nuisance/thr_registered_pve_2_WM.nii.gz

    
#    fslmeants -i ${i}/feat/rs_ref_registered3.feat/filtered_func_data.nii.gz -o ${i}/nuisance/CSF_noise.txt -m ${i}/nuisance/thr_registered_pve_0_CSF.nii.gz 

#    fslmeants -i ${i}/feat/rs_ref_registered3.feat/filtered_func_data.nii.gz -o ${i}/nuisance/WM_noise.txt -m ${i}/nuisance/thr_registered_pve_2_WM.nii.gz 


#    mkdir ${i}/motion

#    fsl_motion_outliers -i ${i}/bet/bet_rsfMRI.nii.gz -o ${i}/motion/mot -s ${i}/motion/mn.txt --dvars --fd 


    #### nuisance_matrix.py
    #### nuisance_glm.sh



#    mkdir ${i}/post_feat

#    fsl_regfilt -i ${i}/feat/rs_ref_registered3.feat/filtered_func_data.nii.gz -d ${i}/nuisance/design.mat -o ${i}/post_feat/regfilt_CSF_WM_regressed -f 1,2

#    fsl_regfilt -i ${i}/post_feat/regfilt_CSF_WM_regressed -d ${i}/motion/design.mat -o ${i}/post_feat/regfilt_motion_regressed_CSF_WM_regressed -f 1



###### 3mm downsampling (4mm just to try out)
    
#    flirt -in ${i}/post_feat/regfilt_motion_regressed_CSF_WM_regressed.nii.gz -ref ${i}/post_feat/regfilt_motion_regressed_CSF_WM_regressed.nii.gz -out ${i}/post_feat/3ds_preTemporalFilter.nii.gz -applyisoxfm 3 -interp nearestneighbour -omat ${i}/post_feat/3ds_preTemporalFilter.mat
    

##    flirt -in ${i}/post_feat/regfilt_motion_regressed_CSF_WM_regressed.nii.gz -ref ${i}/post_feat/regfilt_motion_regressed_CSF_WM_regressed.nii.gz -out ${i}/post_feat/4ds_preTemporalFilter.nii.gz -applyisoxfm 4 -interp nearestneighbour -omat ${i}/post_feat/4ds_preTemporalFilter.mat


###### Temporal filtering

#    fslmaths ${i}/post_feat/3ds_preTemporalFilter.nii.gz -bptf 28.5714286 -1 ${i}/post_feat/3ds_preprocessed.nii.gz


##    fslmaths ${i}/post_feat/4ds_preTemporalFilter.nii.gz -bptf 28.5714286 -1 ${i}/post_feat/4ds_preprocessed.nii.gz


###### for corrMap

#    mkdir ${i}/corr_map

#    flirt -in masks/atlasHO_bilateral_thalamus.nii.gz -ref masks/atlasHO_bilateral_thalamus.nii.gz -out masks/3ds_atlasHO_bilateral_thalamus.nii.gz -applyisoxfm 3 -interp nearestneighbour -omat masks/B_mask_to_3mm.mat

#    fslmaths ${i}/post_feat/3ds_preprocessed.nii.gz -mas masks/3ds_atlasHO_bilateral_thalamus.nii.gz ${i}/corr_map/3ds_B_thal_on_preprocessed.nii.gz



##    flirt -in masks/atlasHO_bilateral_thalamus.nii.gz -ref masks/atlasHO_bilateral_thalamus.nii.gz -out masks/4ds_atlasHO_bilateral_thalamus.nii.gz -applyisoxfm 4 -interp nearestneighbour -omat masks/B_mask_to_4mm.mat

##    fslmaths ${i}/post_feat/4ds_preprocessed.nii.gz -mas masks/4ds_atlasHO_bilateral_thalamus.nii.gz ${i}/corr_map/4ds_B_thal_on_preprocessed.nii.gz

done

