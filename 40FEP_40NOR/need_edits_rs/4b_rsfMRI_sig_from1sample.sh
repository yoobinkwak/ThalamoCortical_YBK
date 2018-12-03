rand_dir=rsFC_Randomise_n80

#for sub_dir in ${rand_dir}/*ICs
#do
#
#    step1_output_cov=${sub_dir}/1_sample_tfce/cluster_t0.95_corrp
#    step1_output_nocov=${sub_dir}/nocov_1_sample_tfce/cluster_t0.95_corrp
#
#    two_step_randomise_dir=${sub_dir}/two_step_randomise
#    if [ ! -d ${two_step_randomise_dir} ] ; then
#        mkdir ${two_step_randomise_dir}
#    fi
#
#    step2_cov=${two_step_randomise_dir}/1_sample_tfce
#    if [ ! -d ${step2_cov} ] ; then
#        mkdir -p ${step2_cov}/sig_clusters
#    fi
#    step2_nocov=${two_step_randomise_dir}/nocov_1_sample_tfce
#    if [ ! -d ${step2_nocov} ] ; then
#        mkdir -p ${step2_nocov}/sig_clusters
#    fi
#    
#    for img in ${step1_output_cov}/*gz
#    do
#        vox="$(fslstats ${img} -V | awk '{print $1}')"
#        #if [ ${vox}? != 0 ] ; then
#        if [ ${vox} != 0 ] ; then
#            cp -r ${img} ${step2_cov}/sig_clusters
#        fi
#    done
#
#    for img2 in ${step1_output_nocov}/*gz
#    do
#        vox="$(fslstats ${img2} -V | awk '{print $1}')"
#        #if [ ${vox}? != 0 ] ; then
#        if [ ${vox} != 0 ] ; then
#            cp -r ${img2} ${step2_nocov}/sig_clusters
#        fi
#    done
#done




#for i in [FN]*
for i in NOR99*
#for i in FEP01*
#for i in $@
do
    subj_dir=${i}/rsFC_ICA_1sample
    if [ ! -d ${subj_dir} ] ; then
        mkdir -p ${subj_dir}/1_sample_tfce/
        mkdir -p ${subj_dir}/nocov_1_sample_tfce/
    fi
    subj_map=${i}/REST/Preprocess/bp2mni_ds3.nii.gz

    for sub_dir in ${rand_dir}/*ICs
    do
        sub_dir_name=$(echo ${sub_dir} | rev | cut -d"/" -f1 | rev)

        if [ ! -d ${subj_dir}/${sub_dir_name} ] ; then
            mkdir -p ${subj_dir}/1_sample_tfce/${sub_dir_name}/timeseries
            mkdir -p ${subj_dir}/nocov_1_sample_tfce/${sub_dir_name}/timeseries
        fi

        two_step_randomise_dir=${sub_dir}/two_step_randomise
        step2_cov=${two_step_randomise_dir}/1_sample_tfce/sig_clusters
        step2_nocov=${two_step_randomise_dir}/nocov_1_sample_tfce/sig_clusters
        
        
        for clusters in ${step2_cov}/*gz
        do
            clusters_file=$(echo ${clusters} | rev | cut -d"/" -f1 | rev)
            clusters_name=$(basename ${clusters_file} .nii.gz)
            echo ${clusters_name}
            if [ ! -d ${subj_dir}/1_sample_tfce/${sub_dir_name}/dual_regression/${clusters_name} ] ; then
                mkdir -p ${subj_dir}/1_sample_tfce/${sub_dir_name}/dual_regression/${clusters_name} 
            fi
            #fslmaths ${subj_map} -mas ${clusters} ${subj_dir}/1_sample_tfce/${sub_dir_name}/${clusters_name}
            fslmeants -i ${subj_map} -m ${clusters} -o ${subj_dir}/1_sample_tfce/${sub_dir_name}/timeseries/${clusters_name}
            dual_regression ${clusters} 0 -1 0 ${subj_dir}/1_sample_tfce/${sub_dir_name}/dual_regression/${clusters_name} ${subj_map}  
        done

        for clusters2 in ${step2_nocov}/*gz
        do
            clusters2_file=$(echo ${clusters2} | rev | cut -d"/" -f1 | rev)
            clusters2_name=$(basename ${clusters2_file} .nii.gz)
            echo ${clusters2_name}
            if [ ! -d ${subj_dir}/nocov_1_sample_tfce/${sub_dir_name}/dual_regression/${clusters2_name} ] ; then
                mkdir -p ${subj_dir}/nocov_1_sample_tfce/${sub_dir_name}/dual_regression/${clusters2_name} 
            fi
            #fslmaths ${subj_map} -mas ${clusters2} ${subj_dir}/nocov_1_sample_tfce/${sub_dir_name}/${clusters2_name}
            fslmeants -i ${subj_map} -m ${clusters2} -o ${subj_dir}/nocov_1_sample_tfce/${sub_dir_name}/timeseries/${clusters2_name}
            dual_regression ${clusters2} 0 -1 0 ${subj_dir}/nocov_1_sample_tfce/${sub_dir_name}/dual_regression/${clusters2_name} ${subj_map}  
        done


    done
done



























       #for img in *.gz
       #do
           #if [[ ${img} != *"demeaned"* ]] ; then









#var="$(fslstats ${i} -V | awk '{print $1}')"
#if [ ${var}? != 0 ] ; then

