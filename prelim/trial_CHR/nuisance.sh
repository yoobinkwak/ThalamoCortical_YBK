for i in $@
do

    applywarp -r /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain -i ${i}/preprocess/registration/tr_fixed_ra* -o ${i}/preprocess/registration/rs_to_mni -w ${i}/preprocess/registration/rs_to_mni_warp


    mkdir ${i}/preprocess/nuisance

    cp -r preprocess_dpabi/RealignParameter/${i}/rp* ${i}/preprocess/nuisance/rp.txt
    cp -r missed_preprocess_dpabi/RealignParameter/${i}/rp* ${i}/preprocess/nuisance/rp.txt
    
    fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o ${i}/preprocess/nuisance/ ${i}/bet/*T1_co.nii.gz


    flirt -in ${i}/preprocess/nuisance/_pve_0.nii.gz -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -out ${i}/preprocess/nuisance/flirted_pve_0_CSF.nii.gz -applyxfm -init ${i}/preprocess/registration/t1_to_mni_flirt.mat -interp trilinear
    flirt -in ${i}/preprocess/nuisance/_pve_2.nii.gz -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -out ${i}/preprocess/nuisance/flirted_pve_2_WM.nii.gz -applyxfm -init ${i}/preprocess/registration/t1_to_mni_flirt.mat -interp trilinear

    fslmaths ${i}/preprocess/nuisance/flirted_pve_0_CSF.nii.gz -thr 0.50 ${i}/preprocess/nuisance/thr_flirted_pve_0_CSF.nii.gz
    fslmaths ${i}/preprocess/nuisance/flirted_pve_2_WM.nii.gz -thr 0.75 ${i}/preprocess/nuisance/thr_flirted_pve_2_WM.nii.gz

    fslmeants -i ${i}/preprocess/registration/rs_to_mni.nii.gz -o ${i}/preprocess/nuisance/flirt_CSF_noise.txt -m ${i}/preprocess/nuisance/thr_flirted_pve_0_CSF.nii.gz
    fslmeants -i ${i}/preprocess/registration/rs_to_mni.nii.gz -o ${i}/preprocess/nuisance/flirt_WM_noise.txt -m ${i}/preprocess/nuisance/thr_flirted_pve_2_WM.nii.gz

    paste ${i}/preprocess/nuisance/flirt_CSF_noise.txt ${i}/preprocess/nuisance/flirt_WM_noise.txt ${i}/preprocess/nuisance/rp.txt > ${i}/preprocess/nuisance/flirt_nuisance_design.txt     
    Text2Vest ${i}/preprocess/nuisance/flirt_nuisance_design.txt ${i}/preprocess/nuisance/flirt_nuisance_design.mat

    fsl_regfilt -i ${i}/preprocess/registration/rs_to_mni.nii.gz -d ${i}/preprocess/nuisance/flirt_nuisance_design.mat -o ${i}/preprocess/nuisance/flirt_nuisance_regressed -f 1,2,3,4,5,6,7,8




    applywarp -r /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -i ${i}/preprocess/nuisance/_pve_0.nii.gz -w ${i}/preprocess/registration/t1_to_mni_warp -o ${i}/preprocess/nuisance/fnirted_pve_0_CSF.nii.gz   
    applywarp -r /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -i ${i}/preprocess/nuisance/_pve_2.nii.gz -w ${i}/preprocess/registration/t1_to_mni_warp -o ${i}/preprocess/nuisance/fnirted_pve_2_WM.nii.gz   

    fslmaths ${i}/preprocess/nuisance/fnirted_pve_0_CSF.nii.gz -thr 0.50 ${i}/preprocess/nuisance/thr_fnirted_pve_0_CSF.nii.gz
    fslmaths ${i}/preprocess/nuisance/fnirted_pve_2_WM.nii.gz -thr 0.75 ${i}/preprocess/nuisance/thr_fnirted_pve_2_WM.nii.gz

    fslmeants -i ${i}/preprocess/registration/rs_to_mni.nii.gz -o ${i}/preprocess/nuisance/fnirt_CSF_noise.txt -m ${i}/preprocess/nuisance/thr_fnirted_pve_0_CSF.nii.gz
    fslmeants -i ${i}/preprocess/registration/rs_to_mni.nii.gz -o ${i}/preprocess/nuisance/fnirt_WM_noise.txt -m ${i}/preprocess/nuisance/thr_fnirted_pve_2_WM.nii.gz

    paste ${i}/preprocess/nuisance/fnirt_CSF_noise.txt ${i}/preprocess/nuisance/fnirt_WM_noise.txt ${i}/preprocess/nuisance/rp.txt > ${i}/preprocess/nuisance/fnirt_nuisance_design.txt     
    Text2Vest ${i}/preprocess/nuisance/fnirt_nuisance_design.txt ${i}/preprocess/nuisance/fnirt_nuisance_design.mat

    fsl_regfilt -i ${i}/preprocess/registration/rs_to_mni.nii.gz -d ${i}/preprocess/nuisance/fnirt_nuisance_design.mat -o ${i}/preprocess/nuisance/fnirt_nuisance_regressed -f 1,2,3,4,5,6,7,8

done
   
    



