#flirt -in masks/atlasHO_left_thalamus.nii.gz -ref masks/atlasHO_left_thalamus.nii.gz -out masks/3ds_atlasHO_left_thalamus.nii.gz -applyisoxfm 3 -interp nearestneighbour -omat masks/L_mask_to_3mm.mat

#flirt -in masks/atlasHO_left_thalamus.nii.gz -ref masks/atlasHO_left_thalamus.nii.gz -out masks/4ds_atlasHO_left_thalamus.nii.gz -applyisoxfm 4 -interp nearestneighbour -omat masks/L_mask_to_4mm.mat
    

for i in $@
do
    mkdir ${i}/preprocess/ds_filter


    fslmaths ${i}/preprocess/nuisance/flirt_nuisance_regressed.nii.gz -bptf 28.5714286 -1 ${i}/preprocess/ds_filter/hp_flirt.nii.gz
    fslmaths ${i}/preprocess/nuisance/flirt_nuisance_regressed.nii.gz -bptf 28.5714286 2.85714286 ${i}/preprocess/ds_filter/bp_flirt.nii.gz

    fslmaths ${i}/preprocess/nuisance/fnirt_nuisance_regressed.nii.gz -bptf 28.5714286 -1 ${i}/preprocess/ds_filter/hp_fnirt.nii.gz
    fslmaths ${i}/preprocess/nuisance/fnirt_nuisance_regressed.nii.gz -bptf 28.5714286 2.85714286 ${i}/preprocess/ds_filter/bp_fnirt.nii.gz



    flirt -in ${i}/preprocess/nuisance/flirt_nuisance_regressed.nii.gz -ref ${i}/preprocess/nuisance/flirt_nuisance_regressed.nii.gz -out ${i}/preprocess/ds_filter/3ds_flirt_nuisance_regressed.nii.gz -applyisoxfm 3 -interp nearestneighbour -omat ${i}/preprocess/ds_filter/3ds_flirt.mat
    flirt -in ${i}/preprocess/nuisance/flirt_nuisance_regressed.nii.gz -ref ${i}/preprocess/nuisance/flirt_nuisance_regressed.nii.gz -out ${i}/preprocess/ds_filter/4ds_flirt_nuisance_regressed.nii.gz -applyisoxfm 4 -interp nearestneighbour -omat ${i}/preprocess/ds_filter/4ds_flirt.mat

    flirt -in ${i}/preprocess/nuisance/fnirt_nuisance_regressed.nii.gz -ref ${i}/preprocess/nuisance/fnirt_nuisance_regressed.nii.gz -out ${i}/preprocess/ds_filter/3ds_fnirt_nuisance_regressed.nii.gz -applyisoxfm 3 -interp nearestneighbour -omat ${i}/preprocess/ds_filter/3ds_fnirt.mat
    flirt -in ${i}/preprocess/nuisance/fnirt_nuisance_regressed.nii.gz -ref ${i}/preprocess/nuisance/fnirt_nuisance_regressed.nii.gz -out ${i}/preprocess/ds_filter/4ds_fnirt_nuisance_regressed.nii.gz -applyisoxfm 4 -interp nearestneighbour -omat ${i}/preprocess/ds_filter/4ds_fnirt.mat
    
    

    fslmaths ${i}/preprocess/ds_filter/3ds_flirt_nuisance_regressed.nii.gz -bptf 28.5714286 -1 ${i}/preprocess/ds_filter/3ds_hp_flirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/3ds_flirt_nuisance_regressed.nii.gz -bptf 28.5714286 2.85714286 ${i}/preprocess/ds_filter/3ds_bp_flirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/4ds_flirt_nuisance_regressed.nii.gz -bptf 28.5714286 -1 ${i}/preprocess/ds_filter/4ds_hp_flirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/4ds_flirt_nuisance_regressed.nii.gz -bptf 28.5714286 2.85714286 ${i}/preprocess/ds_filter/4ds_bp_flirt.nii.gz


    fslmaths ${i}/preprocess/ds_filter/3ds_fnirt_nuisance_regressed.nii.gz -bptf 28.5714286 -1 ${i}/preprocess/ds_filter/3ds_hp_fnirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/3ds_fnirt_nuisance_regressed.nii.gz -bptf 28.5714286 2.85714286 ${i}/preprocess/ds_filter/3ds_bp_fnirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/4ds_fnirt_nuisance_regressed.nii.gz -bptf 28.5714286 -1 ${i}/preprocess/ds_filter/4ds_hp_fnirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/4ds_fnirt_nuisance_regressed.nii.gz -bptf 28.5714286 2.85714286 ${i}/preprocess/ds_filter/4ds_bp_fnirt.nii.gz



    fslmaths ${i}/preprocess/ds_filter/hp_flirt.nii.gz -mas masks/atlasHO_left_thalamus.nii.gz ${i}/preprocess/ds_filter/L_thal_on_hp_flirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/bp_flirt.nii.gz -mas masks/atlasHO_left_thalamus.nii.gz ${i}/preprocess/ds_filter/L_thal_on_bp_flirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/hp_fnirt.nii.gz -mas masks/atlasHO_left_thalamus.nii.gz ${i}/preprocess/ds_filter/L_thal_on_hp_fnirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/bp_fnirt.nii.gz -mas masks/atlasHO_left_thalamus.nii.gz ${i}/preprocess/ds_filter/L_thal_on_bp_fnirt.nii.gz


    fslmaths ${i}/preprocess/ds_filter/3ds_hp_flirt.nii.gz -mas masks/3ds_atlasHO_left_thalamus.nii.gz ${i}/preprocess/ds_filter/L_thal_on_3ds_hp_flirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/3ds_bp_flirt.nii.gz -mas masks/3ds_atlasHO_left_thalamus.nii.gz ${i}/preprocess/ds_filter/L_thal_on_3ds_bp_flirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/4ds_hp_flirt.nii.gz -mas masks/4ds_atlasHO_left_thalamus.nii.gz ${i}/preprocess/ds_filter/L_thal_on_4ds_hp_flirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/4ds_bp_flirt.nii.gz -mas masks/4ds_atlasHO_left_thalamus.nii.gz ${i}/preprocess/ds_filter/L_thal_on_4ds_bp_flirt.nii.gz


    fslmaths ${i}/preprocess/ds_filter/3ds_hp_fnirt.nii.gz -mas masks/3ds_atlasHO_left_thalamus.nii.gz ${i}/preprocess/ds_filter/L_thal_on_3ds_hp_fnirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/3ds_bp_fnirt.nii.gz -mas masks/3ds_atlasHO_left_thalamus.nii.gz ${i}/preprocess/ds_filter/L_thal_on_3ds_bp_fnirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/4ds_hp_fnirt.nii.gz -mas masks/4ds_atlasHO_left_thalamus.nii.gz ${i}/preprocess/ds_filter/L_thal_on_4ds_hp_fnirt.nii.gz
    fslmaths ${i}/preprocess/ds_filter/4ds_bp_fnirt.nii.gz -mas masks/4ds_atlasHO_left_thalamus.nii.gz ${i}/preprocess/ds_filter/L_thal_on_4ds_bp_fnirt.nii.gz

done

