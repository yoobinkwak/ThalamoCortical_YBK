subj=${1}
side=${2}
voxel_size=${3}         #e.g., 3

if [ ${side} == 'left' ] ; then
    hemi=lh
elif [ ${side} == 'right' ] ; then
    hemi=rh
fi

RS=${subj}/REST_for_OM2015
if [ ! -e ${RS} ] ; then
    mkdir ${RS}
    RS_dataLoc=/Volume/CCNC_BI_3T/Thalamus_rsFC_20171104
    RS_subj_data=${RS_dataLoc}/${subj}/REST/Preprocess
    cp -r ${RS_subj_data}/hp2mni.nii.gz ${RS}/
    cp -r ${RS_subj_data}/hp*.txt ${RS}/
    cp -r ${RS_subj_data}/rsfMRI_raw_mcf.par ${RS}/
fi
rs=${RS}/hp2mni.nii.gz
rs_ds3=${RS}/hp2mni_ds3.nii.gz
if [ ! -e ${rs_ds3} ] ; then  
    flirt -in ${rs} -ref ${rs} -applyisoxfm 3 -out ${rs_ds3}
fi
thal=${hemi}_thalamus_HOSC_60.nii.gz
thald_ds3=${hemi}_thalamus_HOSC_60_ds3.nii.gz

out_dir=${subj}/34FEP68CHR69HC/${side}_ds${voxel_size}_thalamusICs_rsFC
if [ ! -e ${out_dir} ] ; then
    mkdir ${out_dir}
fi
ts_dir=${out_dir}/Timeseries
if [ ! -e ${ts_dir} ] ; then
    mkdir ${ts_dir}
fi
reg_dir=${out_dir}/Regressed
if [ ! -e ${reg_dir} ] ; then
    mkdir ${reg_dir}
fi

in_dir=${subj}/34FEP68CHR69HC/${side}_ds${voxel_size}_mICA_dual_regression
NumICs=`ls ${in_dir}/${subj}_thresh_zstat00*stage2.nii.gz | wc -l`

for num in $(seq -w 01 ${NumICs})
do
    subj_ic_ts=${ts_dir}/${subj}_thresh_zstat00${num}_ts
    if [ ! -e ${subj_ic_ts} ] ; then
        input=${in_dir}/${subj}_thresh_zstat00${num}_stage2.nii.gz
        fsl_glm -i ${rs_ds3} -d ${input} -o ${subj_ic_ts}
        count_ts=`cat ${subj_ic_ts} | wc -l`
        correct_ts=112
        if [ ! ${count_ts} -eq ${correct_ts} ] ; then
            echo ${subj_ic_ts} >> ${out_dir}/error_ts.txt
        fi
    fi

    base=`basename ${subj_ic_ts}`
    design_subj_ic_ts=${reg_dir}/${base}.mat
    if [ ! -e ${design_subj_ic_ts} ] ; then
        paste ${subj_ic_ts} ${RS}/rsfMRI_raw_mcf.par ${RS}/hp_WM_noise.txt ${RS}/hp_CSF_noise.txt > ${ts_dir}/design_${base}.txt
        Text2Vest ${ts_dir}/design_${base}.txt ${design_subj_ic_ts}
    fi
    
    regressed_subj_ic_ts=${reg_dir}/${base}_regressed.nii.gz
    if [ ! -e ${regressed_subj_ic_ts} ] ; then
        fsl_glm -i ${rs_ds3} -d ${design_subj_ic_ts} -o ${regressed_subj_ic_ts}
    fi

    extract_map1=${reg_dir}/split_${base}_regressed0000.nii.gz
    if [ ! -e ${extract_map1} ] ; then
        fslsplit ${regressed_subj_ic_ts} ${reg_dir}/split_${base}_regressed
    fi

    rm -rf ${reg_dir}/split_${subj}*regressed000[12345678].nii.gz

    
    z_subj_ic_ts=${ts_dir}/znorm_${subj}_thresh_zstat00${num}_ts
    if [ ! -e ${z_subj_ic_ts} ] ; then
        z_input=${in_dir}/znorm_${subj}_thresh_zstat00${num}_stage2.nii.gz
        fsl_glm -i ${rs_ds3} -d ${z_input} -o ${z_subj_ic_ts}
        z_count_ts=`cat ${z_subj_ic_ts} | wc -l`
        correct_ts=112
        if [ ! ${z_count_ts} -eq ${correct_ts} ] ; then
            echo ${z_subj_ic_ts} >> ${out_dir}/error_ts.txt
        fi
    fi

    z_base=`basename ${z_subj_ic_ts}`
    z_design_subj_ic_ts=${reg_dir}/${z_base}.mat
    if [ ! -e ${z_design_subj_ic_ts} ] ; then
        paste ${z_subj_ic_ts} ${RS}/rsfMRI_raw_mcf.par ${RS}/hp_WM_noise.txt ${RS}/hp_CSF_noise.txt > ${ts_dir}/design_${z_base}.txt
        Text2Vest ${ts_dir}/design_${z_base}.txt ${z_design_subj_ic_ts}
    fi

    z_regressed_subj_ic_ts=${reg_dir}/${z_base}_regressed.nii.gz
    if [ ! -e ${z_regressed_subj_ic_ts} ] ; then
        fsl_glm -i ${rs_ds3} -d ${z_design_subj_ic_ts} -o ${z_regressed_subj_ic_ts}
    fi

    z_extract_map1=${reg_dir}/split_${z_base}_regressed0000.nii.gz
    if [ ! -e ${z_extract_map1} ] ; then
        fslsplit ${z_regressed_subj_ic_ts} ${reg_dir}/split_${z_base}_regressed
    fi

    rm -rf ${reg_dir}/split_znorm_${subj}*regressed000[12345678].nii.gz

done















