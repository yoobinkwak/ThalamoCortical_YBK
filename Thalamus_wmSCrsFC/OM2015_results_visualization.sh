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
    slicerOut=${output_dir}/slicer_${img}
    pngOut=${output_dir}/sliced_${img}.png
    if [ ! -e ${pngOut} ] ; then
        overlay 1 0 ${mni} -A ${inputs} 0.95 1 ${overlayOut}
        slicer ${overlayOut} -A 1200 ${slicerOut}
        convert ${slicerOut} ${pngOut}
    fi
done





