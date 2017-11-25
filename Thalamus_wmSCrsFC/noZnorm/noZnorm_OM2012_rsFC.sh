subj=${1}

OM2015_subj=${subj}/OM2015
OM2012_subj=${subj}/OM2012/noZnorm
if [ ! -e ${OM2012_subj} ] ; then
    mkdir ${OM2012_subj}
fi

rs_ds3=${OM2015_subj}/hp2mni_ds3.nii.gz
seed=re_OM2012_tensor_stats/noZnorm_outputs/tfce/fwe_corrected_p/mc_95thr_right_3mm_4fwhm/mc_95thr_right_3mm_4fwhm_IC12_tfce_corrp_tstat1.nii.gz

thal_ts=${OM2012_subj}/right_3mm_4fwhm_IC12
if [ ! -e ${thal_ts} ] ; then
    fsl_glm -i ${rs_ds3} -d ${seed} -o ${thal_ts}
fi

if [ ! -e ${OM2012_subj}/design.mat ] ; then
    paste ${thal_ts} ${OM2015_subj}/rsfMRI_raw_mcf.par ${OM2015_subj}/hp_WM_noise.txt ${OM2015_subj}/hp_CSF_noise.txt > ${OM2012_subj}/design.txt
    Text2Vest ${OM2012_subj}/design.txt ${OM2012_subj}/design.mat
fi

regressed_thal_ts=${OM2012_subj}/right_3mm_4fwhm_IC12_regressed.nii.gz
if [ ! -e ${regressed_thal_ts} ] ; then
    fsl_glm -i ${rs_ds3} -d ${OM2012_subj}/design.mat -o ${regressed_thal_ts}
fi

extract_map1=${OM2012_subj}/split_right_3mm_4fwhm_IC12_regressed0000.nii.gz
if [ ! -e ${extract_map1} ] ; then
    fslsplit ${regressed_thal_ts} ${OM2012_subj}/split_right_3mm_4fwhm_IC12_regressed
fi



