dir=37FEP36HC_randomise/output/tfce

fwe=${dir}/fwe_corrected_p
if [ ! -e ${fwe} ] ; then
    mkdir ${fwe}
    mkdir ${fwe}/left_ds3
    mkdir ${fwe}/right_ds3
    mkdir ${dir}/uncorrected_p
    mkdir ${dir}/uncorrected_p/left_ds3
    mkdir ${dir}/uncorrected_p/right_ds3
    mkdir ${dir}/raw_stats
    mv ${dir}/concatenated_left_ds3_IC*tfce_corrp_tstat* ${fwe}/left_ds3/
    mv ${dir}/concatenated_right_ds3_IC*tfce_corrp_tstat* ${fwe}/right_ds3/
    mv ${dir}/concatenated_left_ds3_IC*tfce_p_tstat* ${dir}/uncorrected_p/left_ds3/
    mv ${dir}/concatenated_right_ds3_IC*tfce_p_tstat* ${dir}/uncorrected_p/right_ds3/
    mv ${dir}/concatenated_*_tstat* ${dir}/raw_stats/

fi

left_ds3=${fwe}/left_ds3
l_dir=`basename ${left_ds3}`
l_dir_thr=${fwe}/95thr_${l_dir}
if [ ! -e ${l_dir_thr} ] ; then
    mkdir ${l_dir_thr}
fi
l_dir_thr_mc=${fwe}/mc_95thr_${l_dir}
if [ ! -e ${l_dir_thr_mc} ] ; then
    mkdir ${l_dir_thr_mc}
fi

l_mc_correct=`ls ${left_ds3}/*tstat1.nii.gz | wc -l`
sig_level=0.05
l_mc_corrected_sig=`echo "scale=6; 1 - (${sig_level} / ${l_mc_correct})" | bc -l`
echo ${l_mc_corrected_sig}

for l_tstat1 in ${left_ds3}/*tstat1.nii.gz
do
    base=`basename ${l_tstat1}`
    tstat1_out=${l_dir_thr}/95thr_${base}
    if [ ! -e ${tstat1_out} ] ; then
        fslmaths ${l_tstat1} -thr 0.95 ${tstat1_out}
    elif [ -e ${tstat1_out} ] ; then
        val=`fslstats ${tstat1_out} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} -eq ${zero} ] ; then
            echo ${tstat1_out} >> ${fwe}/survive_95.txt
        fi
    fi

    tstat1_mc=${l_dir_thr_mc}/mc_95thr_${base}
    if [ ! -e ${tstat1_mc} ] ; then
        fslmaths ${l_tstat1} -thr ${l_mc_corrected_sig} ${tstat1_mc}
    elif [ -e ${tstat1_mc} ] ; then
        val=`fslstats ${tstat1_mc} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} == ${zero} ] ; then
            echo ${tstat1_mc} >> ${fwe}/survive_mc_95.txt
        fi
    fi

done

for l_tstat2 in ${left_ds3}/*tstat2.nii.gz
do
    base=`basename ${l_tstat2}`
    tstat2_out=${l_dir_thr}/95thr_${base}
    if [ ! -e ${tstat2_out} ] ; then
        fslmaths ${l_tstat2} -thr 0.95 ${tstat2_out}
    elif [ -e ${tstat2_out} ] ; then
        val=`fslstats ${tstat2_out} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} -eq ${zero} ] ; then
            echo ${tstat2_out} >> ${fwe}/survive_95.txt
        fi
    fi
    
    tstat2_mc=${l_dir_thr_mc}/mc_95thr_${base}
    if [ ! -e ${tstat2_mc} ] ; then
        fslmaths ${l_tstat2} -thr ${l_mc_corrected_sig} ${tstat2_mc}
    elif [ -e ${tstat2_mc} ] ; then
        val=`fslstats ${tstat2_mc} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} == ${zero} ] ; then
            echo ${tstat2_mc} >> ${fwe}/survive_mc_95.txt
        fi
    fi

done



right_ds3=${fwe}/right_ds3
r_dir=`basename ${right_ds3}`
r_dir_thr=${fwe}/95thr_${r_dir}
if [ ! -e ${r_dir_thr} ] ; then
    mkdir ${r_dir_thr}
fi
r_dir_thr_mc=${fwe}/mc_95thr_${r_dir}
if [ ! -e ${r_dir_thr_mc} ] ; then
    mkdir ${r_dir_thr_mc}
fi

r_mc_correct=`ls ${right_ds3}/*tstat1.nii.gz | wc -l`
sig_level=0.05
r_mc_corrected_sig=`echo "scale=6; 1 - (${sig_level} / ${r_mc_correct})" | bc -l`
echo ${r_mc_corrected_sig}

for r_tstat1 in ${right_ds3}/*tstat1.nii.gz
do
    base=`basename ${r_tstat1}`
    tstat1_out=${r_dir_thr}/95thr_${base}
    if [ ! -e ${tstat1_out} ] ; then
        fslmaths ${r_tstat1} -thr 0.95 ${tstat1_out}
    elif [ -e ${tstat1_out} ] ; then
        val=`fslstats ${tstat1_out} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} -eq ${zero} ] ; then
            echo ${tstat1_out} >> ${fwe}/survive_95.txt
        fi
    fi

    tstat1_mc=${r_dir_thr_mc}/mc_95thr_${base}
    if [ ! -e ${tstat1_mc} ] ; then
        fslmaths ${r_tstat1} -thr ${r_mc_corrected_sig} ${tstat1_mc}
    elif [ -e ${tstat1_mc} ] ; then
        val=`fslstats ${tstat1_mc} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} == ${zero} ] ; then
            echo ${tstat1_mc} >> ${fwe}/survive_mc_95.txt
        fi
    fi

done

for r_tstat2 in ${right_ds3}/*tstat2.nii.gz
do
    base=`basename ${r_tstat2}`
    tstat2_out=${r_dir_thr}/95thr_${base}
    if [ ! -e ${tstat2_out} ] ; then
        fslmaths ${r_tstat2} -thr 0.95 ${tstat2_out}
    elif [ -e ${tstat2_out} ] ; then
        val=`fslstats ${tstat2_out} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} -eq ${zero} ] ; then
            echo ${tstat2_out} >> ${fwe}/survive_95.txt
        fi
    fi
    
    tstat2_mc=${r_dir_thr_mc}/mc_95thr_${base}
    if [ ! -e ${tstat2_mc} ] ; then
        fslmaths ${r_tstat2} -thr ${r_mc_corrected_sig} ${tstat2_mc}
    elif [ -e ${tstat2_mc} ] ; then
        val=`fslstats ${tstat2_mc} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} == ${zero} ] ; then
            echo ${tstat2_mc} >> ${fwe}/survive_mc_95.txt
        fi
    fi

done

