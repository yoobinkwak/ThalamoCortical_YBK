for i in [CFN]*
do
    

###### head motion correction, slice timing 
#    mkdir ${i}/feat

    ### run feat (FSL GUI)

#    mv ${i}/registration/*.feat ${i}/feat/

    
####### Temporal filtering

#    mkdir ${i}/post_feat
    
#    fslmaths ${i}/feat/rs_ref_registered3.feat/filtered_func_data.nii.gz -bptf 28.5714286 -1 ${i}/post_feat/temporal_filtered.nii.gz


###### CSF, WM, motion regressors

#    mkdir ${i}/nuisance

#    fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o ${i}/nuisance/ ${i}/bet/2nd_bet_neck_T1_co

#    flirt -in ${i}/nuisance/_pve_0.nii.gz -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -out ${i}/nuisance/registered_pve_0_CSF.nii.gz -applyxfm -init ${i}/registration/t1_ref_registered1.mat -interp trilinear

#    flirt -in ${i}/nuisance/_pve_2.nii.gz -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -out ${i}/nuisance/registered_pve_2_WM.nii.gz -applyxfm -init ${i}/registration/t1_ref_registered1.mat -interp trilinear

#    fslmaths ${i}/nuisance/registered_pve_0_CSF.nii.gz -thr 0.50 ${i}/nuisance/thr_registered_pve_0_CSF.nii.gz
#    fslmaths ${i}/nuisance/registered_pve_2_WM.nii.gz -thr 0.75 ${i}/nuisance/thr_registered_pve_2_WM.nii.gz

    
#    fslmeants -i ${i}/feat/rs_ref_registered3.feat/filtered_func_data.nii.gz -o ${i}/nuisance/CSF_noise.txt -m ${i}/nuisance/thr_registered_pve_0_CSF.nii.gz       #### CHECK IF INPUT IS CORRECT

#    fslmeants -i ${i}/feat/rs_ref_registered3.feat/filtered_func_data.nii.gz -o ${i}/nuisance/WM_noise.txt -m ${i}/nuisance/thr_registered_pve_2_WM.nii.gz        #### CHECK IF INPUT IS CORRECT


#    mkdir ${i}/motion

#    fsl_motion_outliers -i ${i}/bet/bet_rsfMRI.nii.gz -o ${i}/motion/mot -s ${i}/motion/mn.txt --dvars --fd 


####### dual regression 1 -- spatial regression (output: thalamic ts)

#    mkdir ${i}/dual_regression

##    fsl_glm -i ${i}/post_feat/temporal_filtered.nii.gz -d <indiv IC input, i.e., run this command for each IC separately; x runs for x no. of ICs> -o ${i}/dual_regression/thalamic_ts_ICno.txt


#    fsl_glm -i ${i}/post_feat/temporal_filtered.nii.gz -d ICs_for_prac/prac_IC7.nii.gz -o ${i}/dual_regression/thalamic_ts_IC7.txt
#    fsl_glm -i ${i}/post_feat/temporal_filtered.nii.gz -d ICs_for_prac/prac_IC6.nii.gz -o ${i}/dual_regression/thalamic_ts_IC6.txt
    fsl_glm -i ${i}/post_feat/temporal_filtered.nii.gz -d ICs_for_prac/prac_IC5.nii.gz -o ${i}/dual_regression/thalamic_ts_IC5.txt
    fsl_glm -i ${i}/post_feat/temporal_filtered.nii.gz -d ICs_for_prac/prac_IC4.nii.gz -o ${i}/dual_regression/thalamic_ts_IC4.txt
    fsl_glm -i ${i}/post_feat/temporal_filtered.nii.gz -d ICs_for_prac/prac_IC3.nii.gz -o ${i}/dual_regression/thalamic_ts_IC3.txt
    fsl_glm -i ${i}/post_feat/temporal_filtered.nii.gz -d ICs_for_prac/prac_IC2.nii.gz -o ${i}/dual_regression/thalamic_ts_IC2.txt
    fsl_glm -i ${i}/post_feat/temporal_filtered.nii.gz -d ICs_for_prac/prac_IC1.nii.gz -o ${i}/dual_regression/thalamic_ts_IC1.txt
    
    #### design_matrix.py       NEED EDIT TO INCORPORATE THALAMIC TS





done

