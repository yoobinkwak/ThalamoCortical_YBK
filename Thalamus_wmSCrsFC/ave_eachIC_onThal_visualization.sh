side=${1}
voxel_size=${2}     #e.g., 3mm
smoothing=${3}      #e.g., 4fwhm, nosmooth

if [ ${side} == 'left' ] ; then
    hemi=lh
elif [ ${side} == 'right' ] ; then
    hemi=rh
fi


input_loc=OM2012_Averaged_eachIC_onThal
input_dir=${input_loc}/${side}_${voxel_size}_${smoothing}
if [ ! -e ${input_dir} ] ; then
    mkdir ${input_dir}
    mv ${input_loc}/${side}_${voxel_size}_${smoothing}_IC*.nii.gz ${input_dir}/
    mv ${input_loc}/bin_${side}_${voxel_size}_${smoothing}_IC*.nii.gz ${input_dir}/
fi
output_dir=OM2012_Averaged_eachIC_onThal/visualize_${side}_${voxel_size}_${smoothing}
if [ ! -e ${output_dir} ] ; then
    mkdir ${output_dir}
fi

thal=${hemi}_thalamus_HOSC_60_ds3.nii.gz

for inputs in ${input_dir}/*nii.gz
do
    input=`basename ${inputs}`
    img=`remove_ext ${input}`
    overlayOut=${output_dir}/overlay_${img}.nii.gz
    slicerOut=${output_dir}/slicer_${img}
    pngOut=${output_dir}/sliced_${img}.png
    slicesOut=${output_dir}/slices_${img}.gif
    if [ ! -e ${pngOut} ] || [ ! -e ${slicesOut} ] ; then
        overlay 1 0 ${thal} -A ${inputs} 0.1 1 ${overlayOut}
        slices ${overlayOut} -o ${slicesOut}
        slicer ${overlayOut} -A 1200 ${slicerOut}
        convert ${slicerOut} ${pngOut}
    fi
    rm -rf ${overlayOut}
    rm -rf ${slicerOut}
done



INPUT_loc=OM2012_Averaged_eachIC_onThal/noZnorm
INPUTDIR=${INPUT_loc}/${side}_${voxel_size}_${smoothing}
if [ ! -e ${INPUTDIR} ] ; then
    mkdir ${INPUTDIR}
    mv ${INPUT_loc}/${side}_${voxel_size}_${smoothing}_IC*.nii.gz ${INPUTDIR}/
    mv ${INPUT_loc}/bin_${side}_${voxel_size}_${smoothing}_IC*.nii.gz ${INPUTDIR}/
fi
OUTPUTDIR=OM2012_Averaged_eachIC_onThal/noZnorm/visualize_${side}_${voxel_size}_${smoothing}
if [ ! -e ${OUTPUTDIR} ] ; then
    mkdir ${OUTPUTDIR}
fi

thal=${hemi}_thalamus_HOSC_60_ds3.nii.gz

for INPUTs in ${INPUTDIR}/*nii.gz
do
    INPUT=`basename ${INPUTs}`
    img=`remove_ext ${INPUT}`
    overlayOUT=${OUTPUTDIR}/overlay_${img}.nii.gz
    slicerOUT=${OUTPUTDIR}/slicer_${img}
    pngOUT=${OUTPUTDIR}/sliced_${img}.png
    slicesOUT=${OUTPUTDIR}/slices_${img}.gif
    if [ ! -e ${pngOUT} ] || [ ! -e ${slicesOUT} ] ; then
        overlay 1 0 ${thal} -A ${INPUTs} 0.1 1 ${overlayOUT}
        slices ${overlayOUT} -o ${slicesOUT}
        slicer ${overlayOUT} -A 1200 ${slicerOUT}
        convert ${slicerOUT} ${pngOUT}
    fi
    rm -rf ${overlayOUT}
    rm -rf ${slicerOUT}
done




