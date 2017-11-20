subj=${1}
mICA=${2}
side=${3}
voxel_size=${4}
smoothing=${5}



OM2015_subj=${subj}/OM2015
if [ ! -e ${OM2015_subj} ] ; then
    mkdir ${OM2015_subj}
fi

#RS_dataLoc=/Volume/CCNC_BI_3T/Thalamus_rsFC_20171104
#RS_subj_data=${RS_dataLoc}/${subj}/REST/Preprocess
#cp -r ${RS_subj_data}/hp2mni.nii.gz ${OM2015_subj}/
#cp -r ${RS_subj_data}/hp*.txt ${OM2015_subj}/
#cp -r ${RS_subj_data}/rsfMRI_raw_mcf.par ${OM2015_subj}/

rs=${OM2015_subj}/hp2mni.nii.gz
rs_ds3=${OM2015_subj}/hp2mni_ds3.nii.gz
if [ ! -e ${rs_ds3} ] ; then  
    flirt -in ${rs} -ref ${rs} -applyisoxfm 3 -out ${rs_ds3}
fi

glm_dir=tica_results/${mICA}/dim0/glm_out
melodicIC_map=tica_results/${mICA}/dim0/melodic_IC.nii.gz
NumICs=`fslval ${melodicIC_map} dim4`
#Num=$((${NumICs} + 1))
ts_dir=${OM2015_subj}/Timeseries
if [ ! -e ${ts_dir} ] ; then
    mkdir ${ts_dir}
fi

for num in $(seq -w 01 ${NumICs})
#for (( num=1; num<${Num}; num++ ))
do
    echo $num
    subj_ic_ts=${ts_dir}/${side}_${voxel_size}_${smoothing}_IC${num}_ts
    if [ ! -e ${subj_ic_ts} ] ; then
        perSubj_perIC=${glm_dir}/znorm_${subj}_stage2_thresh_zstat00${num}.nii.gz
        fsl_glm -i ${rs_ds3} -d ${perSubj_perIC} -o ${subj_ic_ts}
    fi
done










