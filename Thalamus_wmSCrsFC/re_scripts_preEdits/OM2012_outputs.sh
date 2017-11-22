input=${1}

input_dir=OM2012_tensor_stats_inputs
output_dir=OM2012_tensor_stats_outputs
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
    
randomise -i ${input_dir}/${input} -o ${out_voxel}/${output_name} -d ${input_dir}/design.mat -t ${input_dir}/design.con -x --uncorrp
randomise -i ${input_dir}/${input} -o ${out_tfce}/${output_name} -d ${input_dir}/design.mat -t ${input_dir}/design.con -T --uncorrp
