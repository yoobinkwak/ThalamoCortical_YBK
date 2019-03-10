stat_dir=Tractography_Values/ds3_bi_nosmooth_20ICs
for i in [FN]*
do
    for thr in 5 10 20 90 95
    do
        for ic in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19
        do
            dir=${i}/rsFC_seed_tractography/ds3_bi_nosmooth_20ICs/nosmooth_IC${ic}_demeaned_tfce_corrp_tstat1
            
            if [ ! -e ${dir}/${thr}thrP_norm_fdt_paths.nii.gz ] ; then
                fslmaths ${dir}/fdt_paths.nii.gz -thrP ${thr} ${dir}/${thr}thrP_fdt_paths.nii.gz
                fslmaths ${dir}/norm_fdt_paths.nii.gz -thrP ${thr} ${dir}/${thr}thrP_norm_fdt_paths.nii.gz
                echo ${i} >> ${stat_dir}/thrP_subjs.txt 
                echo ${ic} >> ${stat_dir}/thrP_IC_numbs.txt
                fslstats ${dir}/${thr}thrP_fdt_paths.nii.gz -V >> ${stat_dir}/${thr}thrP.txt
                fslstats ${dir}/${thr}thrP_norm_fdt_paths.nii.gz -V >> ${stat_dir}/${thr}thrP_norm.txt
            fi

            if [ ! -f ${dir}/${thr}thrP_reg_MD_norm_fdt_paths.nii.gz ] ; then
                applywarp -i ${dir}/${thr}thrP_fdt_paths.nii.gz -r ${i}/DTI/dti_FA.nii.gz -w ${i}/DTI/Registration/mni2reorient_t1w2nodif_coeff.nii.gz -o ${dir}/${thr}thrP_reg_FA_fdt_paths.nii.gz
                applywarp -i ${dir}/${thr}thrP_norm_fdt_paths.nii.gz -r ${i}/DTI/dti_FA.nii.gz -w ${i}/DTI/Registration/mni2reorient_t1w2nodif_coeff.nii.gz -o ${dir}/${thr}thrP_reg_FA_norm_fdt_paths.nii.gz
                applywarp -i ${dir}/${thr}thrP_fdt_paths.nii.gz -r ${i}/DTI/dti_MD.nii.gz -w ${i}/DTI/Registration/mni2reorient_t1w2nodif_coeff.nii.gz -o ${dir}/${thr}thrP_reg_MD_fdt_paths.nii.gz
                applywarp -i ${dir}/${thr}thrP_norm_fdt_paths.nii.gz -r ${i}/DTI/dti_MD.nii.gz -w ${i}/DTI/Registration/mni2reorient_t1w2nodif_coeff.nii.gz -o ${dir}/${thr}thrP_reg_MD_norm_fdt_paths.nii.gz
                echo ${i} >> ${stat_dir}/thrP_FAMD_subjs.txt 
                echo ${ic} >> ${stat_dir}/thrP_FAMD_IC_numbs.txt
                fslstats ${i}/DTI/dti_FA.nii.gz -k ${dir}/${thr}thrP_reg_FA_fdt_paths.nii.gz -M >> ${stat_dir}/${thr}thrP_FA.txt
                fslstats ${i}/DTI/dti_FA.nii.gz -k ${dir}/${thr}thrP_reg_FA_norm_fdt_paths.nii.gz -M >> ${stat_dir}/${thr}thrP_norm_FA.txt
                fslstats ${i}/DTI/dti_MD.nii.gz -k ${dir}/${thr}thrP_reg_MD_fdt_paths.nii.gz -M >> ${stat_dir}/${thr}thrP_MD.txt
                fslstats ${i}/DTI/dti_MD.nii.gz -k ${dir}/${thr}thrP_reg_MD_norm_fdt_paths.nii.gz -M >> ${stat_dir}/${thr}thrP_norm_MD.txt
            fi

            if [ ! -f ${dir}/${thr}thrP_tract_reg_MD_norm_fdt_paths.nii.gz ] ; then
                seed=rsFC_Randomise_n80/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/t0.95_concatenated_ds3_bi_nosmooth_IC${ic}_demeaned_tfce_corrp_tstat1.nii.gz
                fslmaths ${dir}/${thr}thrP_fdt_paths.nii.gz -sub ${seed} -bin ${dir}/${thr}thrP_tract_fdt_paths.nii.gz
                fslmaths ${dir}/${thr}thrP_norm_fdt_paths.nii.gz -sub ${seed} -bin ${dir}/${thr}thrP_tract_norm_fdt_paths.nii.gz
                echo ${i} >> ${stat_dir}/thrP_tract_subjs.txt 
                echo ${ic} >> ${stat_dir}/thrP_tract_IC_numbs.txt
                fslstats ${dir}/${thr}thrP_tract_fdt_paths.nii.gz -V >> ${stat_dir}/${thr}thrP_tract.txt
                fslstats ${dir}/${thr}thrP_tract_norm_fdt_paths.nii.gz -V >> ${stat_dir}/${thr}thrP_tract_norm.txt
            fi








        done
    done
done






