img=${1}

input_dir=37FEP36HC_randomise_wmSC/inputs
output_dir=37FEP36HC_randomise_wmSC/outputs
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

input=${input_dir}/${img}
output_name=`remove_ext ${input}`

val=`fslval ${input} dim4`
correct_val=73
if [ ! ${val} = ${correct_val} ] ; then
    echo ${input} >> 37FEP36HC_randomise_wmSC/error_inputs.txt
fi

base=`basename ${input}`
output_name=`remove_ext ${base}`
if [ ! -e ${out_tfce}/${output_name}_tfce_corrp_tstat1.nii.gz ] ; then
    randomise -i ${input} -o ${out_tfce}/${output_name} -d 37FEP36HC_randomise_wmSC/design.mat -t 37FEP36HC_randomise_wmSC/design.con -T --uncorrp
fi

if [ ! -e ${out_voxel}/${output_name}_vox_corrp_tstat1.nii.gz ] ; then
    randomise -i ${input} -o ${out_voxel}/${output_name} -d 37FEP36HC_randomise_wmSC/design.mat -t 37FEP36HC_randomise_wmSC/design.con -x --uncorrp
fi



z_input_dir=37FEP36HC_randomise_wmSC/znorm_inputs
z_output_dir=37FEP36HC_randomise_wmSC/znorm_outputs
if [ ! -e ${z_output_dir} ] ; then
    mkdir ${z_output_dir}
fi
z_out_voxel=${z_output_dir}/voxel_wise
if [ ! -e ${z_out_voxel} ] ; then
    mkdir ${z_out_voxel}
fi
z_out_tfce=${z_output_dir}/tfce
if [ ! -e ${z_out_tfce} ] ; then
    mkdir ${z_out_tfce}
fi

z_input=${z_input_dir}/${img}
z_output_name=`remove_ext ${z_input}`

z_val=`fslval ${z_input} dim4`
correct_val=73
if [ ! ${z_val} = ${correct_val} ] ; then
    echo ${z_input} >> 37FEP36HC_randomise_wmSC/error_znorm_inputs.txt
fi

z_base=`basename ${z_input}`
z_output_name=`remove_ext ${z_base}`
if [ ! -e ${z_out_tfce}/${z_output_name}_tfce_corrp_tstat1.nii.gz ] ; then
    randomise -i ${z_input} -o ${z_out_tfce}/${z_output_name} -d 37FEP36HC_randomise_wmSC/design.mat -t 37FEP36HC_randomise_wmSC/design.con -T --uncorrp
fi

if [ ! -e ${z_out_voxel}/${z_output_name}_vox_corrp_tstat1.nii.gz ] ; then
    randomise -i ${z_input} -o ${z_out_voxel}/${z_output_name} -d 37FEP36HC_randomise_wmSC/design.mat -t 37FEP36HC_randomise_wmSC/design.con -x --uncorrp
fi

