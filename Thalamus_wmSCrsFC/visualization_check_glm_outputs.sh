mICA=${1}
hemi=${2}
downsample=${3}
subj=${4}

if [ ! ${downsample} == '0' ] ; then
    ds=_ds${downsample}
    mni=/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/mni${ds}.nii.gz
elif [ ${downsample} == '0' ] ; then
    ds=""
    mni=/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz
fi
thalamus=/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/${hemi}_thalamus_HOSC_60${ds}.nii.gz

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
        #sips -s png ${slicerOut} --out ${pngOut}
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
        #sips -s png ${slicer_out} --out ${png_out}
    fi
done









