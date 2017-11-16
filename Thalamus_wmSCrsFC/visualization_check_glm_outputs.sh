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
    png_out=${vis_dir}/sliced_${img_Znorm}.png
    if [ ! -e ${png_out} ] ; then
        overlay 1 0 ${thalamus} -A ${inputs_Znorm} 2.5 10 ${overlay_out}
        slicer ${overlay_out} -A 1200 ${slicer_out}
        convert ${slicer_out} ${png_out}
    fi
done



for inputs_Znorm in ${glm_dir}/znorm_${subj}_stage2_thresh_zstat*.nii.gz
do
    input_Znorm=`basename ${inputs_Znorm}`
    img_Znorm=`remove_ext ${input_Znorm}`
    overlay_out=${vis_dir}/overlay_${img_Znorm}.nii.gz
    slicer_out=${vis_dir}/slicer_${img_Znorm}
    png_out=${vis_dir}/sliced_${img_Znorm}.png
    if [ ! -e ${png_out} ] ; then
        overlay 1 0 ${thalamus} -A ${inputs_Znorm} 2.5 10 ${overlay_out}
        slicer ${overlay_out} -A 1200 ${slicer_out}
        convert ${slicer_out} ${png_out}
    fi
done









