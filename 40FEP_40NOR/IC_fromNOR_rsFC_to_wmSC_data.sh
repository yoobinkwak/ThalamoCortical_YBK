mkdir IC_fromNOR_IC_fromNOR_rsFC_to_wmSC

#for i in [FN]*
#do
#    mkdir IC_fromNOR_rsFC_to_wmSC/${i}
#    cp -r ${i}/DTI* IC_fromNOR_rsFC_to_wmSC/${i}/
#    mkdir IC_fromNOR_rsFC_to_wmSC/${i}/T1
#    cp -r ${i}/T1/reorient*gz IC_fromNOR_rsFC_to_wmSC/${i}/T1/
#
#done


#mkdir -p IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6preproc_10ICs/two_step_randomise/1_sample_tfce/sig_clusters
#mkdir -p IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6preproc_20ICs/two_step_randomise/1_sample_tfce/sig_clusters
#mkdir -p IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6_10ICs/two_step_randomise/1_sample_tfce/sig_clusters
#mkdir -p IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6_20ICs/two_step_randomise/1_sample_tfce/sig_clusters
#mkdir -p IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_nosmooth_10ICs/two_step_randomise/1_sample_tfce/sig_clusters
#mkdir -p IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_nosmooth_20ICs/two_step_randomise/1_sample_tfce/sig_clusters

#mkdir -p IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6preproc_10ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters
#mkdir -p IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6preproc_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters
#mkdir -p IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6_10ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters
#mkdir -p IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters
mkdir -p IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/NOR_only/ds3_bi_nosmooth_10ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters
mkdir -p IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/NOR_only/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters

cp -r rsFC_Randomise_n80/NOR_only/ds3_bi_nosmooth_10ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/* IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/NOR_only/ds3_bi_nosmooth_10ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/
cp -r rsFC_Randomise_n80/NOR_only/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/* IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/NOR_only/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/
#cp -r rsFC_Randomise_n80/ds3_bi_fwhm6_10ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/* IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6_10ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/
#cp -r rsFC_Randomise_n80/ds3_bi_fwhm6_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/* IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/
#cp -r rsFC_Randomise_n80/ds3_bi_fwhm6preproc_10ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/* IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6preproc_10ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/
#cp -r rsFC_Randomise_n80/ds3_bi_fwhm6preproc_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/* IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6preproc_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/



#cp -r rsFC_Randomise_n80/ds3_bi_nosmooth_10ICs/two_step_randomise/1_sample_tfce/sig_clusters/* IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_nosmooth_10ICs/two_step_randomise/1_sample_tfce/sig_clusters/
#cp -r rsFC_Randomise_n80/ds3_bi_nosmooth_20ICs/two_step_randomise/1_sample_tfce/sig_clusters/* IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_nosmooth_20ICs/two_step_randomise/1_sample_tfce/sig_clusters/
#cp -r rsFC_Randomise_n80/ds3_bi_fwhm6_10ICs/two_step_randomise/1_sample_tfce/sig_clusters/* IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6_10ICs/two_step_randomise/1_sample_tfce/sig_clusters/
#cp -r rsFC_Randomise_n80/ds3_bi_fwhm6_20ICs/two_step_randomise/1_sample_tfce/sig_clusters/* IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6_20ICs/two_step_randomise/1_sample_tfce/sig_clusters/
#cp -r rsFC_Randomise_n80/ds3_bi_fwhm6preproc_10ICs/two_step_randomise/1_sample_tfce/sig_clusters/* IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6preproc_10ICs/two_step_randomise/1_sample_tfce/sig_clusters/
#cp -r rsFC_Randomise_n80/ds3_bi_fwhm6preproc_20ICs/two_step_randomise/1_sample_tfce/sig_clusters/* IC_fromNOR_rsFC_to_wmSC/rsFC_Randomise_n80/ds3_bi_fwhm6preproc_20ICs/two_step_randomise/1_sample_tfce/sig_clusters/
