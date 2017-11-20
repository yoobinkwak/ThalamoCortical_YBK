input=${1}

dir_thr=OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/95thr_${input}
if [ ! -e ${dir_thr} ] ; then
    mkdir ${dir_thr}
fi

dir_in=OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/${input}
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
            echo ${tstat1_out} >> OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/survive_95.txt
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
            echo ${tstat2_out} >> OM2012_tensor_stats_outputs/tfce/fwe_corrected_p/survive_95.txt
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
