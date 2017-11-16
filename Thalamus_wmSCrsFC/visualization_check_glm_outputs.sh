mICA=${1}
hemi=${2}
subj=${3}

mni=/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/mni_ds3.nii.gz
thalamus=/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/${hemi}_thalamus_HOSC_60_ds3.nii.gz

glm_dir=${mICA}/dim0/glm_out
vis_dir=${glm_dir}/visualization
if [ ! -e ${vis_dir} ] ; then
    mkdir ${vis_dir}
fi


for inputs_noZnorm in ${glm_dir}/${subj}_stage2_thresh_zstat*.nii.gz
do
    input_noZnorm=`basename ${inputs_noZnorm}`
    img_noZnorm=`remove_ext ${input_noZnorm}`
    overlayOut=${vis_dir}/overlay_${img_noZnorm}.nii.gz
    slicerOut=${vis_dir}/slicer_${img_noZnorm}
    pngOut=${vis_dir}/sliced_${img_noZnorm}.png
    if [ ! -e ${pngOut} ] ; then
        overlay 1 0 ${thalamus} -A ${inputs_noZnorm} 2.5 10 ${overlayOut}
        slicer ${overlayOut} -A 1200 ${slicerOut}
        convert ${slicerOut} ${pngOut}
    fi
done








