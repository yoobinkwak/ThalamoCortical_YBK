subject_map=${i}/YB*/left/fdt_matrix2_reconstructed_4s.nii.gz
melodic_dir=tica_results/all_left_4s
melodic_ic=${melodic_dir}/melodic_IC.nii.gz
fsl_reg_out=${melodic_dir}/fsl_glm_output_${i}

fsl_glm -i ${subject_map} -d ${melodic_ic} -o ${fsl_reg_out}















