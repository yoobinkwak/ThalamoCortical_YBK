side=${1}
downsample=${2}
subj=${3}

if [ ${side} == 'left' ] ; then
    hemi=lh
elif [ ${side} == 'right' ] ; then
    hemi=rh
fi

if [ ! ${downsample} == '0' ] ; then
    ds=_ds${downsample}
elif [ ${downsample} == '0' ] ; then
    ds=""
fi

mni=/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz
mni_ds=/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/mni${ds}.nii.gz
thal_ds=/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/${hemi}_thalamus_HOSC_60${ds}.nii.gz  
if [ ! ${downsample} == '0' ] ; then
    if [ ! -e ${mni_ds} ] ; then
	    flirt -in ${mni}  -ref ${mni} -applyisoxfm ${downsample} -out ${mni_ds}
    fi
    if [ ! -e ${thal_ds} ] ; then
	    flirt -in ${thal} -ref ${thal} -applyisoxfm ${downsample} -out ${thal_ds}
    fi
fi

#melodic_dir=tica_results/mICA_HCvsFEP_${side}${ds}/dim0
melodic_dir=tica_results/mICA_HCvsFEP_${side}${ds}_nosmooth/dim0
melodic_ic=${melodic_dir}/melodic_IC.nii.gz
if [ ! -e ${melodic_dir}/split_melodic_IC0000.nii.gz ] ; then
    fslsplit ${melodic_ic} ${melodic_dir}/split_melodic_IC
fi
glm_out_dir=${melodic_dir}/glm_out
if [ ! -e ${glm_out_dir} ] ; then
	mkdir ${glm_out_dir}
fi

subject_map=${subj}/YB*/${side}/fdt_matrix2_reconstructed${ds}.nii.gz
glm_stage1=${glm_out_dir}/${subj}_stage1
glm_stage2=${glm_out_dir}/${subj}_stage2
if [ ! -e ${glm_stage1} ] ; then
    echo " running glm stage 1 for melodic_IC.nii.gz"
    fsl_glm -i ${subject_map} -d ${melodic_ic} -m ${thal_ds} -o ${glm_stage1}
else
    echo " completed glm stage 1 for melodic IC.nii.gz"
fi
if [ ! -e ${glm_stage2}.nii.gz ] ; then
    echo " running glm stage 2 for melodic_IC.nii.gz"
    fsl_glm -i ${subject_map} -d ${glm_stage1} -m ${thal_ds} -o ${glm_stage2}
else
    echo " completed glm stage 2 for melodic IC.nii.gz"
fi

for melodic_map in ${melodic_dir}/split_melodic_IC*
do
    base=`basename ${melodic_map}`
	outputname=`remove_ext ${base}`
	if [ ! -e ${glm_stage1}_${outputname} ] ; then
	    echo "running glm stage 1 for ${base}"
	    fsl_glm -i ${subject_map} -d ${melodic_map} -m ${thal_ds} -o ${glm_stage1}_${outputname}
    else
        echo "completed glm stage 1 for ${base}"
    fi

	if [ ! -e ${glm_stage2}_${outputname}.nii.gz ] ; then
	    echo "running glm stage 2 for ${base}"
	    fsl_glm -i ${subject_map} -d ${glm_stage1}_${outputname} -m ${thal_ds} -o ${glm_stage2}_${outputname}
    else
        echo "completed glm stage 2 for ${base}"
    fi
done




for map in ${melodic_dir}/stats/thresh_zstat*
do
    base=`basename ${map}`
	outputname=`remove_ext ${base}`
	if [ ! -e ${glm_stage1}_${outputname} ] ; then
	    echo "running glm stage 1 for ${base}"
	    fsl_glm -i ${subject_map} -d ${map} -m ${thal_ds} -o ${glm_stage1}_${outputname}
    else
        echo "completed glm stage 1 for ${base}"
    fi

	if [ ! -e ${glm_stage2}_${outputname}.nii.gz ] ; then
	    echo "running glm stage 2 for ${base}"
	    fsl_glm -i ${subject_map} -d ${glm_stage1}_${outputname} -m ${thal_ds} -o ${glm_stage2}_${outputname} 	
    else
        echo "completed glm stage 2 for ${base}"
    fi
done






