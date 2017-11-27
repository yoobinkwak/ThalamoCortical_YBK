side=${1}
voxel_size=${2}
smoothing=${3}

input_dir=OM2015_group_rsFC/output_group_rsFC/tfce/fwe_corrected_p/mc_95thr_${side}_${voxel_size}_${smoothing}
output_dir=OM2015_group_rsFC/output_group_rsFC/tfce/fwe_corrected_p/visualize_mc_95thr_${side}_${voxel_size}_${smoothing}
if [ ! -e ${output_dir} ] ; then
    mkdir ${output_dir}
fi
mni=mni_ds3.nii.gz

for inputs in ${input_dir}/*
do
    input=`basename ${inputs}`
    img=`remove_ext ${input}`
    overlayOut=${output_dir}/overlay_${img}.nii.gz
    slicesOut=${output_dir}/slices_${img}.gif
    slicerOut=${output_dir}/slicer_${img}
    pngOut=${output_dir}/sliced_${img}.png
    if [ ! -e ${pngOut} ] || [ ! -e ${slicesOut} ] ; then
        overlay 1 0 ${mni} -A ${inputs} 0.95 1 ${overlayOut}
        slices ${overlayOut} -o ${slicesOut}
        slicer ${overlayOut} -A 1200 ${slicerOut}
        convert ${slicerOut} ${pngOut}
    fi
    rm -rf ${overlayOut}
    rm -rf ${slicerOut}
done





INPUTDIR=OM2015_group_rsFC/noZnorm_output_group_rsFC/tfce/fwe_corrected_p/mc_95thr_${side}_${voxel_size}_${smoothing}
OUTPUTDIR=OM2015_group_rsFC/noZnorm_output_group_rsFC/tfce/fwe_corrected_p/visualize_mc_95thr_${side}_${voxel_size}_${smoothing}
if [ ! -e ${OUTPUTDIR} ] ; then
    mkdir ${OUTPUTDIR}
fi

for INPUTs in ${INPUTDIR}/*
do
    INPUT=`basename ${INPUTs}`
    img=`remove_ext ${INPUT}`
    overlayOUT=${OUTPUTDIR}/overlay_${img}.nii.gz
    slicesOUT=${OUTPUTDIR}/slices_${img}.gif
    slicerOUT=${OUTPUTDIR}/slicer_${img}
    pngOUT=${OUTPUTDIR}/sliced_${img}.png
    if [ ! -e ${pngOUT} ] || [ ! -e ${slicesOUT} ] ; then
        overlay 1 0 ${mni} -A ${INPUTs} 0.95 1 ${overlayOUT}
        slices ${overlayOUT} -o ${slicesOUT}
        slicer ${overlayOUT} -A 1200 ${slicerOUT}
        convert ${slicerOUT} ${pngOUT}
    fi
    rm -rf ${overlayOUT}
    rm -rf ${slicerOUT}
done
