subj=${1}
side=${2}		#e.g., left or right
voxel_size=${3}         #e.g., ds3 or 2mm
fwhm=${4}		#e.g., 4fwhm, 6fwhm or nosmooth

if [ ${side} == 'left' ] ; then
    hemi=lh
elif [ ${side} == 'right' ] ; then
    hemi=rh
fi

if [ ${voxel_size} == 'ds3' ] ; then
	rs=${subj}/REST/Preprocess/hp2mni_ds3.nii.gz
	thal=masks/${hemi}_thalamus_HOSC_60_ds3.nii.gz
elif [ ${voxel_size} == '2mm' ] ; then
	rs=${subj}/REST/Preprocess/hp2mni/hp2mni.nii.gz
	thal=masks/${hemi}_thalamus_HOSC_60.nii.gz
fi


RS=${subj}/REST/Preprocess

out=${subj}/TensorIC_RSFC
if [ ! -e ${out} ] ; then
    mkdir ${out}
fi
out_dir=${out}/${voxel_size}_${side}_${fwhm}
if [ ! -e ${out_dir} ] ; then
    mkdir ${out_dir}
fi

ts_dir=${out_dir}/Timeseries
if [ ! -e ${ts_dir} ] ; then
    mkdir ${ts_dir}
fi
reg_dir=${out_dir}/SpatialMap
if [ ! -e ${reg_dir} ] ; then
    mkdir ${reg_dir}
fi


in_dir=${subj}/DualRegression_TensorICA/TemporalRegression_Stage2/${voxel_size}_${side}_${fwhm}
NumICs=`ls ${in_dir}/z2.3_${subj}*.nii.gz | wc -l`


for num in $(seq -w 01 ${NumICs})
do
    subj_ic_ts=${ts_dir}/${subj}_IC${num}_timeseries
    if [ ! -e ${subj_ic_ts} ] ; then
        input=${in_dir}/z2.3_${subj}_thresh_zstat00${num}*.nii.gz
        fsl_glm -i ${rs} -d ${input} -o ${subj_ic_ts}
        count_ts=`cat ${subj_ic_ts} | wc -l`
        correct_ts=112
        if [ ! ${count_ts} -eq ${correct_ts} ] ; then
            echo ${subj_ic_ts} >> ${out_dir}/error_ts.txt
        fi
    fi

    design_subj_ic_ts=${reg_dir}/${subj}_IC${num}.mat
    if [ ! -e ${design_subj_ic_ts} ] ; then
        paste ${subj_ic_ts} ${RS}/rsfMRI_raw_mcf.par ${RS}/WM_noise_hp.txt ${RS}/CSF_noise_hp.txt > ${ts_dir}/${subj}_IC${num}.txt
        Text2Vest ${ts_dir}/${subj}_IC${num}.txt ${design_subj_ic_ts}
    fi
    
    regressed_subj_ic_ts=${reg_dir}/${subj}_IC${num}_maps.nii.gz
    if [ ! -e ${regressed_subj_ic_ts} ] ; then
        fsl_glm -i ${rs} -d ${design_subj_ic_ts} -o ${regressed_subj_ic_ts}
    fi

    extract_map1=${reg_dir}/${subj}_IC${num}_map0000.nii.gz
    if [ ! -e ${extract_map1} ] ; then
        fslsplit ${regressed_subj_ic_ts} ${reg_dir}/${subj}_IC${num}_map
    fi

    #rm -rf ${reg_dir}/${subj}_IC${num}_map000[12345678].nii.gz

    
done









