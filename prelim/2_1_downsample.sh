# Possible future changes
# - names should be shortened

for i in C*
do
    dsDir=${i}/downsampled
    postSmoothingDir=${i}/feat_postSmoothing
    preprocDir=${postSmoothingDir}/regfilt_motion_regressed_CSF_WM_regressed.feat
    filtered_data=${preprocDir}/filtered_func_data.nii.gz # fc map
    thal_mask=masks/atlasHo_bilateral_thalamus.nii.gz

    mkdir ${dsDir}

    # Mask fc map with the thalamus mask
    fslmaths  \
        ${filtered_data} \
        -mas ${thal_mask} \
        ${postSmoothingDir}/B_thal_on_filtered_func_data.nii.gz

    for isolevel in 3 4 5
    do
        # Downsampling the whole brain fc map
        flirt \
            -in ${filtered_data} \
            -ref ${filtered_data} \
            -out ${dsDir}/${isolevel}ds_filtered_func_data.nii.gz \
            -applyisoxfm ${isolevel} \
            -interp nearestneighbour \
            -omat ${dsDir}/filtered_funct_TO_${isolevel}mm.mat

        # Downsampling the thalamus fc map
        flirt \
            -in ${postSmoothingDir}/B_thal_on_filtered_func_data.nii.gz \
            -ref ${postSmoothingDir}/B_thal_on_filtered_func_data.nii.gz \
            -out ${dsDir}/${isolevel}ds_B_thal_on_filtered_func_data.nii.gz \
            -applyisoxfm ${isolevel} \
            -interp nearestneighbour \
            -omat ${dsDir}/B_thal_on_filtered_func_TO_${isolevel}mm.mat

        # estimating the matrix for
        # downsampled image --> original image
        convert_xfm \
            -omat ${dsDir}/${isolevel}mm_TO_filtered_func.mat \
            -inverse ${dsDir}/filtered_funct_TO_${isolevel}mm.mat

        # shouldn't this be same as the above?
        convert_xfm \
            -omat ${dsDir}/${isolevel}mmB_thal_TO_B_thal_on_filtered_func.mat \
            -inverse ${dsDir}/B_thal_on_filtered_func_TO_${isolevel}mm.mat
        
        # Registration back to original space (upsampling)
        flirt \
            -in ${dsDir}/${isolevel}ds_filtered_func_data.nii.gz \
            -ref ${preprocDir}/filtered_func_data.nii.gz \
            -applyxfm -init ${dsDir}/${isolevel}mm_TO_filtered_func.mat \
            -out ${dsDir}/${isolevel}ds_backTo_filtered_func.nii.gz 
    done
done
