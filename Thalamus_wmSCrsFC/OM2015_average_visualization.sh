dir=OM2015_Averaged_rsFC
out_dir=${dir}/visualization
if [ ! -e ${out_dir} ] ; then
    mkdir ${out_dir}
fi
noZnorm_dir=${dir}/noZnorm
noZnorm_out_dir=${noZnorm_dir}/visualization
if [ ! -e ${noZnorm_out_dir} ] ; then
    mkdir ${noZnorm_out_dir}
fi

mni=mni_ds3.nii.gz

for inputs in ${dir}/*nii.gz
do
    input=`basename ${inputs}`
    img=`remove_ext ${input}`
    overlayOut=${out_dir}/overlay_${img}.nii.gz
    slicerOut=${out_dir}/slicer_${img}
    pngOut=${out_dir}/sliced_${img}.png
    overlay 1 0 ${mni} -A ${inputs} 2.5 10 ${overlayOut}
    slicer ${overlayOut} -A 1200 ${slicerOut}
    convert ${slicerOut} ${pngOut}
done

for noZinputs in ${noZnorm_dir}/*nii.gz
do
    input=`basename ${noZinputs}`
    img=`remove_ext ${input}`
    overlayOut=${noZnorm_out_dir}/overlay_${img}.nii.gz
    slicerOut=${noZnorm_out_dir}/slicer_${img}
    pngOut=${noZnorm_out_dir}/sliced_${img}.png
    overlay 1 0 ${mni} -A ${noZinputs} 2.5 10 ${overlayOut}
    slicer ${overlayOut} -A 1200 ${slicerOut}
    convert ${slicerOut} ${pngOut}
done


