for isoLevel in 3 4 5
do
    # Downsample the masks
    flirt \
        -in masks/atlasHO_bilateral_thalamus.nii.gz \
        -ref masks/atlasHO_bilateral_thalamus.nii.gz \
        -out masks/${isoLevel}/ds_atlasHO_bilateral_thalamus.nii.gz \
        -applyisoxfm ${isoLevel}/ \
        -interp nearestneighbour

    for i in [CFN]*
    do
        dsFcMap=${i}/downsampled/${isoLevel}ds_filtered_func_data.nii.gz
        # Masked meants
        fslmeants \
            -i ${dsFcMap} \
            -m masks/${isoLevel}ds_atlasHO_bilateral_thalamus.nii.gz \
            --showall >> ${i}/timeSeries/${isoLevel}ds_B_thalamus_masked_showall.txt
        # wholebrain meants
        fslmeants \
            -i ${dsFcMap} \
            --showall >> ${i}/timeSeries/${isoLevel}ds_filtered_func_showall.txt
    done
done
