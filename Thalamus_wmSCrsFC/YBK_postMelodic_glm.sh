melodic_dir=tica_results/all_right_ds3
melodic_ic=${melodic_dir}/melodic_IC.nii.gz
glm_out_dir=${melodic_dir}/glm_out

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









fsl_glm -i ${rh_thal_ds3} -d ${melodic_ic} -o ${glm_out_dir}/rh_thal_melodic_IC

for map in ${melodic_dir}/stats/thresh_zstat*
do
	outputname=`cat remove_ext ${map}`
	fsl_glm -i ${rh_thal_ds3} -d ${map} -o -o ${glm_out_dir}/rh_thal_${outputname}
done





#for i in $@
#do
#	subject_map=${i}/YB*/left/fdt_matrix2_reconstructed_4s.nii.gz
#	fsl_reg_out=${melodic_dir}/fsl_glm_output_${i}
#
#	if [ ! -e ${fsl_reg_out} ] ; then
#		echo " Running GLM for ${i}"
#		fsl_glm -i ${subject_map} -d ${melodic_ic} -o ${fsl_reg_out}
#	else
#		echo " GLM completed for ${i}"
#	fi
#
#done
















