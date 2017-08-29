for i in [CFN]*
    do
#       mkdir ${i}/bet             
    ##              copied original REST, T1 (co*), outputs of "bet -m -f 0.30 -F" & "bet -m -f 0.30 -B" 
#       mkdir ${i}/registration
    ##              copied output of
    ###             flirt -in ${i}/2nd_preprocessed/2nd_bet_neck_T1_co.nii.gz -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain -omat ${i}/registered/t1_ref_registered1.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12 
    ###             flirt -in ${i}/preprocessed/bet_rsfMRI.nii.gz -ref ${i}/2nd_preprocessed/2nd_bet_neck_T1_co.nii.gz -omat ${i}/registered/rs_t1_registered2.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12 
    ###             convert_xfm -concat ${i}/registered/t1_ref_registered1.mat -omat ${i}/registered/rs_ref_registered3.mat ${i}/registered/rs_t1_registered2.mat
    ###             flirt -in ${i}/preprocessed/bet_rsfMRI.nii.gz -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain -out ${i}/registered/rs_ref_registered3 -applyxfm -init ${i}/registered/rs_ref_registered3.mat -interp trilinear
#       mkdir ${i}/feat_preSmoothing
#       mkdir ${i}/nuisance
#       mkdir ${i}/motion
#	mkdir ${i}/feat_postSmoothing    
#	mkdir ${i}/timeSeries 



####    FEAT -- motion correction, slice timing correction
## note: use "paste" to select inputs (In the X11 preferences under the "Input" tab you can turn on "Emulate three button mouse".  Now when you hold down the option key and click the left mouse button it will emulate the middle mouse click and paste the data on your clipboard.) 
    
#	mv ${i}/registration/*.feat ${i}/feat_preSmoothing/

#	fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o ${i}/nuisance/ ${i}/bet/2nd_bet_neck_T1_co

#	flirt -in ${i}/nuisance/_pve_0.nii.gz -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -out ${i}/nuisance/registered_pve_0_CSF.nii.gz -applyxfm -init ${i}/registration/t1_ref_registered1.mat -interp trilinear
#	flirt -in ${i}/nuisance/_pve_2.nii.gz -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -out ${i}/nuisance/registered_pve_2_WM.nii.gz -applyxfm -init ${i}/registration/t1_ref_registered1.mat -interp trilinear

#	fslmaths ${i}/nuisance/registered_pve_0_CSF.nii.gz -thr 0.99 ${i}/nuisance/thr_registered_pve_0_CSF.nii.gz  
#	fslmaths ${i}/nuisance/registered_pve_2_WM.nii.gz -thr 0.99 ${i}/nuisance/thr_registered_pve_2_WM.nii.gz  

#	fslmeants -i ${i}/feat_preSmoothing/rs_ref_registered3.feat/filtered_func_data.nii.gz -o ${i}/nuisance/CSF_noise.txt -m ${i}/nuisance/thr_registered_pve_0_CSF.nii.gz 
#	fslmeants -i ${i}/feat_preSmoothing/rs_ref_registered3.feat/filtered_func_data.nii.gz -o ${i}/nuisance/WM_noise.txt -m ${i}/nuisance/thr_registered_pve_2_WM.nii.gz 
	

#	fsl_motion_outliers -i ${i}/bet/bet_rsfMRI.nii.gz -o ${i}/motion/mot -s ${i}/motion/mn.txt --dvars --fd

#### nuisance_matrix.py
#### nuisance_glm.sh

#	fsl_regfilt -i ${i}/feat_preSmoothing/rs_ref_registered3.feat/filtered_func_data.nii.gz -d ${i}/nuisance/design.mat -o ${i}/feat_preSmoothing/regfilt_CSF_WM_regressed -f 1,2

#    fsl_regfilt -i ${i}/feat_preSmoothing/regfilt_CSF_WM_regressed -d ${i}/motion/design.mat -o ${i}/feat_preSmoothing/regfilt_motion_regressed_CSF_WM_regressed -f 1


	    #### GLM -- try 3 EVs
	
	    #	mkdir ${i}/try_3EVs
	    #	mv ${i}/try_3EVs.* ${i}/try_3EVs/
	    #	mv ${i}/try_3EVs_* ${i}/try_3EVs/

        #	fsl_regfilt -i ${i}/feat_preSmoothing/rs_ref_registered3.feat/filtered_func_data.nii.gz -d ${i}/try_3EVs/try_3EVs.mat -o ${i}/feat_preSmoothing/regfilt_CSF_WM_motion_regressed -f 1,2,3
	

## checked that signal are different after nuiance regression via fslmeants


#### FEAT -- smoothing, temporal filtering ("regfilt_motion_regressed_CSF_WM_regressed" as input)


#	mv ${i}/feat_preSmoothing/regfilt_motion_regressed_CSF_WM_regressed.feat ${i}/feat_postSmoothing/







done

