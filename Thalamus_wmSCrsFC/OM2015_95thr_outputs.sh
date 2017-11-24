input=${1}

dir_thr=OM2015_group_rsFC/output_group_rsFC/tfce/fwe_corrected_p/95thr_${input}
if [ ! -e ${dir_thr} ] ; then
    mkdir ${dir_thr}
fi

dir_thr_mc=OM2015_group_rsFC/output_group_rsFC/tfce/fwe_corrected_p/mc_95thr_${input}
if [ ! -e ${dir_thr_mc} ] ; then
    mkdir ${dir_thr_mc}
fi

dir_in=OM2015_group_rsFC/output_group_rsFC/tfce/fwe_corrected_p/${input}

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
            echo ${tstat1_out} >> OM2015_group_rsFC/output_group_rsFC/tfce/fwe_corrected_p/survive_95.txt
        fi
    fi

    tstat1_mc=${dir_thr_mc}/mc_95thr_${base}
    if [ ! -e ${tstat1_mc} ] ; then
        fslmaths ${tstat1} -thr ${mc_corrected_sig} ${tstat1_mc}
    elif [ -e ${tstat1_mc} ] ; then
        val=`fslstats ${tstat1_mc} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} == ${zero} ] ; then
            echo ${tstat1_mc} >> OM2015_group_rsFC/output_group_rsFC/tfce/fwe_corrected_p/survive_mc_95.txt
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
            echo ${tstat2_out} >> OM2015_group_rsFC/output_group_rsFC/tfce/fwe_corrected_p/survive_95.txt
        fi
    fi
    
    tstat2_mc=${dir_thr_mc}/mc_95thr_${base}
    if [ ! -e ${tstat2_mc} ] ; then
        fslmaths ${tstat2} -thr ${mc_corrected_sig} ${tstat2_mc}
    elif [ -e ${tstat2_mc} ] ; then
        val=`fslstats ${tstat2_mc} -V | head -n1 | sed -e 's/\s.*$//'`
        zero=0
        if [ ! ${val} == ${zero} ] ; then
            echo ${tstat2_mc} >> OM2015_group_rsFC/output_group_rsFC/tfce/fwe_corrected_p/survive_mc_95.txt
        fi
    fi

done







#dir_thr_L34=OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/95thr_left_3mm_4fwhm
#if [ ! -e ${dir_thr_L34} ] ; then
#    mkdir ${dir_thr_L34}
#fi
#dir_input_L34=OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/left_3mm_4fwhm
#for tstat1 in ${dir_input_L34}/*tstat1.nii.gz
#do
#    base=`basename ${tstat1}`
#    tstat1_out=${dir_thr_L34}/95thr_${base}
#    if [ ! -e ${tstat1_out} ] ; then
#        fslmaths ${tstat1} -thr 0.95 ${tstat1_out}
#    elif [ -e ${tstat1_out} ] ; then
#        val=`fslstats ${tstat1_out} -V | head -n1 | sed -e 's/\s.*$//'`
#        zero=0
#        if [ ! ${val} -eq ${zero} ] ; then
#            echo ${tstat1_out} >> OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/survive_95.txt
#        fi
#    fi
#done
#for tstat2 in ${dir_input_L34}/*tstat2.nii.gz
#do
#    base=`basename ${tstat2}`
#    tstat2_out=${dir_thr_L34}/95thr_${base}
#    if [ ! -e ${tstat2_out} ] ; then
#        fslmaths ${tstat2} -thr 0.95 ${tstat2_out}
#    elif [ -e ${tstat2_out} ] ; then
#        val=`fslstats ${tstat2_out} -V | head -n1 | sed -e 's/\s.*$//'`
#        zero=0
#        if [ ! ${val} -eq ${zero} ] ; then
#            echo ${tstat2_out} >> OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/survive_95.txt
#        fi
#    fi
#done
#
#dir_thr_R34=OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/95thr_right_3mm_4fwhm
#if [ ! -e ${dir_thr_R34} ] ; then
#    mkdir ${dir_thr_R34}
#fi
#dir_input_R34=OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/right_3mm_4fwhm
#for tstat1 in ${dir_input_R34}/*tstat1.nii.gz
#do
#    base=`basename ${tstat1}`
#    tstat1_out=${dir_thr_R34}/95thr_${base}
#    if [ ! -e ${tstat1_out} ] ; then
#        fslmaths ${tstat1} -thr 0.95 ${tstat1_out}
#    elif [ -e ${tstat1_out} ] ; then
#        val=`fslstats ${tstat1_out} -V | head -n1 | sed -e 's/\s.*$//'`
#        zero=0
#        if [ ! ${val} -eq ${zero} ] ; then
#            echo ${tstat1_out} >> OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/survive_95.txt
#        fi
#    fi
#done
#for tstat2 in ${dir_input_R34}/*tstat2.nii.gz
#do
#    base=`basename ${tstat2}`
#    tstat2_out=${dir_thr_R34}/95thr_${base}
#    if [ ! -e ${tstat2_out} ] ; then
#        fslmaths ${tstat2} -thr 0.95 ${tstat2_out}
#    elif [ -e ${tstat2_out} ] ; then
#        val=`fslstats ${tstat2_out} -V | head -n1 | sed -e 's/\s.*$//'`
#        zero=0
#        if [ ! ${val} -eq ${zero} ] ; then
#            echo ${tstat2_out} >> OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/survive_95.txt
#        fi
#    fi
#done
#
#dir_thr_L3n=OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/95thr_left_3mm_nosmooth
#if [ ! -e ${dir_thr_L3n} ] ; then
#    mkdir ${dir_thr_L3n}
#fi
#dir_input_L3n=OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/left_3mm_nosmooth
#for tstat1 in ${dir_input_L3n}/*tstat1.nii.gz
#do
#    base=`basename ${tstat1}`
#    tstat1_out=${dir_thr_L3n}/95thr_${base}
#    if [ ! -e ${tstat1_out} ] ; then
#        fslmaths ${tstat1} -thr 0.95 ${tstat1_out}
#    elif [ -e ${tstat1_out} ] ; then
#        val=`fslstats ${tstat1_out} -V | head -n1 | sed -e 's/\s.*$//'`
#        zero=0
#        if [ ! ${val} -eq ${zero} ] ; then
#            echo ${tstat1_out} >> OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/survive_95.txt
#        fi
#    fi
#done
#for tstat2 in ${dir_input_L3n}/*tstat2.nii.gz
#do
#    base=`basename ${tstat2}`
#    tstat2_out=${dir_thr_L3n}/95thr_${base}
#    if [ ! -e ${tstat2_out} ] ; then
#        fslmaths ${tstat2} -thr 0.95 ${tstat2_out}
#    elif [ -e ${tstat2_out} ] ; then
#        val=`fslstats ${tstat2_out} -V | head -n1 | sed -e 's/\s.*$//'`
#        zero=0
#        if [ ! ${val} -eq ${zero} ] ; then
#            echo ${tstat2_out} >> OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/survive_95.txt
#        fi
#    fi
#done
#
#dir_thr_R3n=OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/95thr_right_3mm_nosmooth
#if [ ! -e ${dir_thr_R3n} ] ; then
#    mkdir ${dir_thr_R3n}
#fi
#dir_input_R3n=OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/right_3mm_nosmooth
#for tstat1 in ${dir_input_R3n}/*tstat1.nii.gz
#do
#    base=`basename ${tstat1}`
#    tstat1_out=${dir_thr_R3n}/95thr_${base}
#    if [ ! -e ${tstat1_out} ] ; then
#        fslmaths ${tstat1} -thr 0.95 ${tstat1_out}
#    elif [ -e ${tstat1_out} ] ; then
#        val=`fslstats ${tstat1_out} -V | head -n1 | sed -e 's/\s.*$//'`
#        zero=0
#        if [ ! ${val} -eq ${zero} ] ; then
#            echo ${tstat1_out} >> OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/survive_95.txt
#        fi
#    fi
#done
#for tstat2 in ${dir_input_R3n}/*tstat2.nii.gz
#do
#    base=`basename ${tstat2}`
#    tstat2_out=${dir_thr_R3n}/95thr_${base}
#    if [ ! -e ${tstat2_out} ] ; then
#        fslmaths ${tstat2} -thr 0.95 ${tstat2_out}
#    elif [ -e ${tstat2_out} ] ; then
#        val=`fslstats ${tstat2_out} -V | head -n1 | sed -e 's/\s.*$//'`
#        zero=0
#        if [ ! ${val} -eq ${zero} ] ; then
#            echo ${tstat2_out} >> OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/survive_95.txt
#        fi
#    fi
#done
#
#
#
#
#
