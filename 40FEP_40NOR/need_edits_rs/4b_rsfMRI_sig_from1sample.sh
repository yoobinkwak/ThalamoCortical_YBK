rand_dir=rsFC_Randomise_n80

for sub_dir in ${rand_dir}/*ICs
do

    two_step_randomise_dir=${sub_dir}/two_step_randomise
    if [ ! -d ${two_step_randomise_dir} ] ; then
        mkdir ${two_step_randomise_dir}
    fi

    step2_input_dir=${two_step_randomise_dir}/inputs
    if [ ! -d ${step2_input_dir} ] ; then
        mkdir ${step2_input_dir}
    fi

    step1_output_cov=${sub_dir}/1_sample_tfce/cluster_t0.95_corrp
    step1_output_nocov=${sub_dir}/nocov_1_sample_tfce/cluster_t0.95_corrp


   
    for cluster_dir in ${step1_output_cov} ${step1_output_nocov}
    do
        for img in ${cluster_dir}/*gz
        do
            vox="$(fslstats ${img} -V | awk '{print $1}')"
            #if [ ${vox}? != 0 ] ; then
            if [ ${vox} != 0 ] ; then
                #echo ${step2_input_dir}
                #echo ${img}
                #echo ${vox}
                cp -r ${img} ${step2_input_dir}
            fi
        done
    done
done










       #for img in *.gz
       #do
           #if [[ ${img} != *"demeaned"* ]] ; then









#var="$(fslstats ${i} -V | awk '{print $1}')"
#if [ ${var}? != 0 ] ; then

