for i in [FN]*
do
    outDir=${i}/rsFC_ICA_1sample/nocov_1_sample_tfce/ds3_bi_nosmooth_20ICs/corr_measures
#    if [ ! -d ${outDir} ] ; then
#        mkdir ${outDir}
#    fi
#
#    for ic in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19
#    do
#        tstat1=rsFC_Randomise_n80/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/step2_2group_tfce/cluster_t0.95_corrp/t0.95_concatenated_ds3_bi_nosmooth_IC${ic}_demeaned_tfce_corrp_tstat1.nii.gz
#        if [ -f ${tstat1} ] ; then
#            output=${outDir}/IC${ic}_demeaned_tfce_corrp_tstat1
#            if [ ! -f ${output} ] ; then
#                subj_map=${i}/rsFC_ICA_1sample/nocov_1_sample_tfce/ds3_bi_nosmooth_20ICs/dual_regression/t0.95_concatenated_ds3_bi_nosmooth_IC${ic}_demeaned_tfce_corrp_tstat1/dr_stage2_subject00000.nii.gz
#                fslmeants -i ${subj_map} -o ${output} -m ${tstat1}
#                echo ${ic} >> ${outDir}/IC_numbs.txt
#                cat ${output} >> ${outDir}/values.txt
#            fi
#        fi
#    done

    if [ ! -f ${outDir}/${i}_for_corr.txt ] ; then
        paste ${outDir}/IC_numbs.txt ${outDir}/values.txt | expand -t $(($(wc -L <${outDir}/IC_numbs.txt) + 1)) >> ${outDir}/for_corr.txt
        sed "s/^/${i} /" ${outDir}/for_corr.txt > ${outDir}/${i}_for_corr.txt
    fi

    





done

