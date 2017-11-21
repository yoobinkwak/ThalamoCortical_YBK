input=${1}

input_dir=OM2015_group_rsFC/input_group_rsFC
output_dir=OM2015_group_rsFC/output_group_rsFC
if [ ! -e ${output_dir} ] ; then
    mkdir ${output_dir}
fi

val=`fslval ${input_dir}/${input} dim4`
correct_val=72
if [ ! ${val} = ${correct_val} ] ; then
    echo ${input} >> OM2015_group_rsFC/error_inputs.txt
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





