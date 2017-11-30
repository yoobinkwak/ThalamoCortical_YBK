img=${1}


input_dir=37FEP36HC_randomise/input
output_dir=37FEP36HC_randomise/output
if [ ! -e ${output_dir} ] ; then
    mkdir ${output_dir}
fi
out_tfce=${output_dir}/tfce
if [ ! -e ${out_tfce} ] ; then
    mkdir ${out_tfce}
fi

input=${input_dir}/${img}

val=`fslval ${input} dim4`
correct_val=72
if [ ! ${val} = ${correct_val} ] ; then
    echo ${input} >> 37FEP36HC_randomise/error_inputs.txt
fi
   
base=`basename ${input}`
output_name=`remove_ext ${base}`
if [ ! -e ${out_tfce}/${output_name}_tfce_corrp_tstat1.nii.gz ] ; then
    randomise -i ${input} -o ${out_tfce}/${output_name} -d 37FEP36HC_randomise/design.mat -t 37FEP36HC_randomise/design.con -T --uncorrp
fi

znorm_input_dir=37FEP36HC_randomise/znorm_input
znorm_output_dir=37FEP36HC_randomise/znorm_output
if [ ! -e ${znorm_output_dir} ] ; then
    mkdir ${znorm_output_dir}
fi
znorm_out_tfce=${znorm_output_dir}/tfce
if [ ! -e ${znorm_out_tfce} ] ; then
    mkdir ${znorm_out_tfce}
fi

znorm_input=${znorm_input_dir}/${img}

val=`fslval ${znorm_input} dim4`
correct_val=72
if [ ! ${val} = ${correct_val} ] ; then
    echo ${znorm_input} >> 37FEP36HC_randomise/error_znorm_inputs.txt
fi
   
base=`basename ${znorm_input}`
znorm_output_name=`remove_ext ${base}`
if [ ! -e ${z_left_ds3}/${znorm_output_name}_tfce_corrp_tstat1.nii.gz ] ; then
    randomise -i ${znorm_input} -o ${z_left_ds3}/${znorm_output_name} -d 37FEP36HC_randomise/design.mat -t 37FEP36HC_randomise/design.con -T --uncorrp
fi




