input=${1}

dir_thr=re_OM2012_tensor_stats/noZnorm_outputs/voxel_wise/fwe_corrected_p/95thr_${input}
if [ ! -e ${dir_thr} ] ; then
    mkdir ${dir_thr}
fi

dir_thr_mc=re_OM2012_tensor_stats/noZnorm_outputs/voxel_wise/fwe_corrected_p/mc_95thr_${input}
if [ ! -e ${dir_thr_mc} ] ; then
    mkdir ${dir_thr_mc}
fi

dir_in=re_OM2012_tensor_stats/noZnorm_outputs/voxel_wise/fwe_corrected_p/${input}

mc_correct=`ls ${dir_in}/*tstat1.nii.gz | wc -l`
sig_level=0.05
mc_corrected_sig=`echo "scale=6; 1 - (${sig_level} / ${mc_correct})" | bc -l`
echo ${mc_corrected_sig}


for tstat1 in ${dir_in}/*tstat1.nii.gz
do
    base=`basename ${tstat1}`
    tstat1_out=${dir_thr}/95thr_${base}
    if [ ! -e ${tstat1_out} ] ; then
        fslmaths ${tstat1} -thr 0.95 ${tstat1_out}
    elif [ -e ${tstat1_out} ] ; then
        val=`fslstats ${tstat1_out} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} -eq ${zero} ] ; then
            echo ${tstat1_out} >> re_OM2012_tensor_stats/noZnorm_outputs/voxel_wise/fwe_corrected_p/survive_95.txt
        fi
    fi

    tstat1_mc=${dir_thr_mc}/mc_95thr_${base}
    if [ ! -e ${tstat1_mc} ] ; then
        fslmaths ${tstat1} -thr ${mc_corrected_sig} ${tstat1_mc}
    elif [ -e ${tstat1_mc} ] ; then
        val=`fslstats ${tstat1_mc} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} == ${zero} ] ; then
            echo ${tstat1_mc} >> re_OM2012_tensor_stats/noZnorm_outputs/voxel_wise/fwe_corrected_p/survive_mc_95.txt
        fi
    fi

done

for tstat2 in ${dir_in}/*tstat2.nii.gz
do
    base=`basename ${tstat2}`
    tstat2_out=${dir_thr}/95thr_${base}
    if [ ! -e ${tstat2_out} ] ; then
        fslmaths ${tstat2} -thr 0.95 ${tstat2_out}
    elif [ -e ${tstat2_out} ] ; then
        val=`fslstats ${tstat2_out} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} -eq ${zero} ] ; then
            echo ${tstat2_out} >> re_OM2012_tensor_stats/noZnorm_outputs/voxel_wise/fwe_corrected_p/survive_95.txt
        fi
    fi
    
    tstat2_mc=${dir_thr_mc}/mc_95thr_${base}
    if [ ! -e ${tstat2_mc} ] ; then
        fslmaths ${tstat2} -thr ${mc_corrected_sig} ${tstat2_mc}
    elif [ -e ${tstat2_mc} ] ; then
        val=`fslstats ${tstat2_mc} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} == ${zero} ] ; then
            echo ${tstat2_mc} >> re_OM2012_tensor_stats/noZnorm_outputs/voxel_wise/fwe_corrected_p/survive_mc_95.txt
        fi
    fi

done







