#flirt -in masks/masks/mni_brain_ds3.nii.gz -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -out masks/mni_brain_3to2 -omat masks/mni_brain_3to2.mat
#flirt -in masks/mni_ds3.nii.gz -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm.nii.gz -out masks/mni_3to2 -omat masks/mni_3to2.mat
#mkdir 2mm_sig_clusters

#DIR=rsFC_Randomise_n80/NOR_only/ds3_bi_nosmooth_20ICs/two_step_randomise/NOR_nocov_1_sample_tfce/sig_clusters
#DIR=rsFC_Randomise_n80/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters
DIR=rsFC_Randomise_n80/NOR_only/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters

cd ${DIR}
for i in *
do
    #flirt -in ${i} -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -applyxfm -init /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/masks/mni_brain_3to2.mat -out /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/2mm_sig_clusters/NOR_only/ds3_bi_nosmooth_20ICs/two_step_randomise/NOR_nocov_1_sample_tfce/sig_clusters/2mm_brain_${i}
    #fslmaths /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/2mm_sig_clusters/NOR_only/ds3_bi_nosmooth_20ICs/two_step_randomise/NOR_nocov_1_sample_tfce/sig_clusters/2mm_brain_${i} -thrP 10 /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/2mm_sig_clusters/NOR_only/ds3_bi_nosmooth_20ICs/two_step_randomise/NOR_nocov_1_sample_tfce/sig_clusters/10thrP_2mm_brain_${i}


    #flirt -in ${i} -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -applyxfm -init /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/masks/mni_brain_3to2.mat -out /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/2mm_sig_clusters/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/2mm_brain_${i}
    #fslmaths /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/2mm_sig_clusters/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/2mm_brain_${i} -thrP 10 /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/2mm_sig_clusters/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/10thrP_2mm_brain_${i}


    flirt -in ${i} -ref /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz -applyxfm -init /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/masks/mni_brain_3to2.mat -out /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/2mm_sig_clusters/NOR_only/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/2mm_brain_${i}
    fslmaths /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/2mm_sig_clusters/NOR_only/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/2mm_brain_${i} -thrP 10 /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/2mm_sig_clusters/NOR_only/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters/10thrP_2mm_brain_${i}

done




#flirt -in <cluster> -ref <MNI2mm> -applyxfm -init <3_2.mat> -out <2mm_cluster>
#fslmaths <2mm_cluster> -thrP 10 <10thrP_2mm_cluster>
