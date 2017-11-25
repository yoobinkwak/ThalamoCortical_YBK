subj=${1}
mICA=${2}
side=${3}
voxel_size=${4}
smoothing=${5}

if [ ${side} == 'left' ] ; then
    hemi=lh
elif [ ${side} == 'right' ] ; then
    hemi=rh
fi

orig_OM2015_subj=${subj}/OM2015
OM2015_subj=${subj}/OM2015/noZnorm
if [ ! -e ${OM2015_subj} ] ; then
    mkdir ${OM2015_subj}
fi

#RS_dataLoc=/Volume/CCNC_BI_3T/Thalamus_rsFC_20171104
#RS_subj_data=${RS_dataLoc}/${subj}/REST/Preprocess
#cp -r ${RS_subj_data}/hp2mni.nii.gz ${OM2015_subj}/
#cp -r ${RS_subj_data}/hp*.txt ${OM2015_subj}/
#cp -r ${RS_subj_data}/rsfMRI_raw_mcf.par ${OM2015_subj}/

rs=${orig_OM2015_subj}/hp2mni.nii.gz
rs_ds3=${orig_OM2015_subj}/hp2mni_ds3.nii.gz
if [ ! -e ${rs_ds3} ] ; then  
    flirt -in ${rs} -ref ${rs} -applyisoxfm 3 -out ${rs_ds3}
fi
thal=${hemi}_thalamus_HOSC_60.nii.gz
thald_ds3=${hemi}_thalamus_HOSC_60_ds3.nii.gz

glm_dir=tica_results/${mICA}/dim0/glm_out
melodicIC_map=tica_results/${mICA}/dim0/melodic_IC.nii.gz
NumICs=`fslval ${melodicIC_map} dim4`
ts_dir=${OM2015_subj}/Timeseries
if [ ! -e ${ts_dir} ] ; then
    mkdir ${ts_dir}
fi

for num in $(seq -w 01 ${NumICs})
#for (( num=1; num<${Num}; num++ ))
do
    subj_ic_ts=${ts_dir}/${side}_${voxel_size}_${smoothing}_IC${num}_ts
    if [ ! -e ${subj_ic_ts} ] ; then
        perSubj_perIC=${glm_dir}/${subj}_stage2_thresh_zstat00${num}.nii.gz
        fsl_glm -i ${rs_ds3} -d ${perSubj_perIC} -o ${subj_ic_ts}
    elif [ -e ${subj_ic_ts} ] ; then
        count_ts=`cat ${subj_ic_ts} | wc -l`
        correct_ts=112
        if [ ! ${count_ts} -eq ${correct_ts} ] ; then
            echo ${subj_ic_ts} >> error_ts_OM2015.txt
        fi
    fi
    regress=${OM2015_subj}/Regress
    if [ ! -e ${regress} ] ; then
        mkdir ${regress}
    fi
    base=`basename ${subj_ic_ts}`
    design_subj_ic_ts=${regress}/${base}.mat
    if [ ! -e ${design_subj_ic_ts} ] ; then
        paste ${subj_ic_ts} ${orig_OM2015_subj}/rsfMRI_raw_mcf.par ${orig_OM2015_subj}/hp_WM_noise.txt ${orig_OM2015_subj}/hp_CSF_noise.txt > ${ts_dir}/design_${base}.txt
        Text2Vest ${ts_dir}/design_${base}.txt ${design_subj_ic_ts}
    fi
    regressed_subj_ic_ts=${regress}/regressed_${base}.nii.gz
    if [ ! -e ${regressed_subj_ic_ts} ] ; then
        fsl_glm -i ${rs_ds3} -d ${design_subj_ic_ts} -o ${regressed_subj_ic_ts}
    fi

    extract_map1=${regress}/split_regressed_${base}0000.nii.gz
    if [ ! -e ${extract_map1} ] ; then
        fslsplit ${regressed_subj_ic_ts} ${regress}/split_regressed_${base}
    fi

## thal_subj_ic_ts is the same as subj_ic_ts
##    thal_subj_ic_ts=${thal_ts_dir}/thal_${side}_${voxel_size}_${smoothing}_IC${num}_ts
##    if [ ! -e ${thal_subj_ic_ts} ] ; then/noZnorm
##        perSubj_perIC=${glm_dir}/znorm_${subj}_stage2_thresh_zstat00${num}.nii.gz
##        fsl_glm -i ${rs_ds3} -d ${perSubj_perIC} -m ${thald_ds3} -o ${thal_subj_ic_ts}
##    elif [ -e ${thal_subj_ic_ts} ] ; then
##        count_ts=`cat ${thal_subj_ic_ts} | wc -l`
##        correct_ts=112
##        if [ ! ${count_ts} -eq ${correct_ts} ] ; then
##            echo ${thal_subj_ic_ts} >> error_thal_ts_OM2015.txt
##        fi
##    fi
 
#thal_regress=${OM2015_subj}/Regress_thalamus
#    if [ ! -e ${thal_regress} ] ; then
#        mkdir ${thal_regress}
#    fi
#    thal_regressed_subj_ic_ts=${thal_regress}/regressed_thal_${base}
#    if [ ! -e ${thal_regressed_subj_ic_ts} ] ; then
#        fsl_glm -i ${rs_ds3} -d ${design_subj_ic_ts} -m ${thald_ds3} -o ${thal_regressed_subj_ic_ts}
#    fi


done













