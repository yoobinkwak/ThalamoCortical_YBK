input=${1}

input_dir=re_OM2012_tensor_stats/noZnorm_inputs
output_dir=re_OM2012_tensor_stats/noZnorm_outputs
if [ ! -e ${output_dir} ] ; then
    mkdir ${output_dir}
fi
out_voxel=${output_dir}/voxel_wise
if [ ! -e ${out_voxel} ] ; then
    mkdir ${out_voxel}
fi
out_tfce=${output_dir}/tfce
if [ ! -e ${out_tfce} ] ; then
    mkdir ${out_tfce}
fi
output_name=`remove_ext ${input}`

val=`fslval ${input_dir}/${input} dim4`
correct_val=73
if [ ! ${val} = ${correct_val} ] ; then
    echo ${input} >> re_OM2012_tensor_stats/noZnorm_error_inputs.txt
fi

    
if [ ! -e ${out_voxel}/${output_name}_vox_corrp_tstat6.nii.gz ] ; then
    randomise -i ${input_dir}/${input} -o ${out_voxel}/${output_name} -d ${input_dir}/design.mat -t ${input_dir}/design.con -x --uncorrp
fi
if [ ! -e ${out_tfce}/${output_name}_tfce_corrp_tstat6.nii.gz ] ; then
    randomise -i ${input_dir}/${input} -o ${out_tfce}/${output_name} -d ${input_dir}/design.mat -t ${input_dir}/design.con -T --uncorrp
fi

