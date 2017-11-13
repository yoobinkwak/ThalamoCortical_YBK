mni=/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz
mni_ds3=/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/mni_ds3.nii.gz
if [ ! -e ${mni_ds3} ] ; then
	flirt -in ${mni}  -ref ${mni} -applyisoxfm 3 -out ${mni_ds3}
fi
lh_thal=/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/lh_thalamus_HOSC_60.nii.gz
lh_thal_ds3=/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/lh_thalamus_HOSC_60_ds3.nii.gz  
if [ ! -e ${lh_thal_ds3} ] ; then
	flirt -in ${lh_thal} -ref ${lh_thal} -applyisoxfm 3 -out ${lh_thal_ds3}
fi
rh_thal=/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/rh_thalamus_HOSC_60.nii.gz
rh_thal_ds3=/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/rh_thalamus_HOSC_60_ds3.nii.gz  
if [ ! -e ${rh_thal_ds3} ] ; then
	flirt -in ${rh_thal} -ref ${rh_thal} -applyisoxfm 3 -out ${rh_thal_ds3}
fi


lh_melodic_dir=tica_results/mICA_HCvsFEP_left_ds3/dim0
lh_melodic_ic=${lh_melodic_dir}/melodic_IC.nii.gz
lh_glm_out_dir=${lh_melodic_dir}/glm_out
for i in $@
do
	lh_subject_map=${i}/YB*/left/fdt_matrix2_reconstructed_ds3.nii.gz
	lh_glm_stage1=${lh_glm_out_dir}/${i}_stage1
	lh_glm_stage2=${lh_glm_out_dir}/${i}_stage2

	fsl_glm -i ${lh_subject_map} -d ${lh_melodic_ic} -o ${lh_glm_stage1}
	fsl_glm -i ${lh_subject_map} -d ${lh_glm_stage1} -m ${lh_thal_ds3} -o ${lh_glm_stage2}

done

rh_melodic_dir=tica_results/mICA_HCvsFEP_right_ds3/dim0
rh_melodic_ic=${rh_melodic_dir}/melodic_IC.nii.gz
rh_glm_out_dir=${rh_melodic_dir}/glm_out
for i in $@
do
	rh_subject_map=${i}/YB*/right/fdt_matrix2_reconstructed_ds3.nii.gz
	rh_glm_stage1=${rh_glm_out_dir}/${i}_stage1
	rh_glm_stage2=${rh_glm_out_dir}/${i}_stage2

	fsl_glm -i ${rh_subject_map} -d ${rh_melodic_ic} -o ${rh_glm_stage1}
	fsl_glm -i ${rh_subject_map} -d ${rh_glm_stage1} -m ${rh_thal_ds3} -o ${rh_glm_stage2}

done





