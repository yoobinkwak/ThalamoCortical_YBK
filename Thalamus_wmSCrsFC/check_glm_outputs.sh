mICA=${1}
subj=${2}

glm_dir=${mICA}/dim0/glm_out

for i in ${glm_dir}/znorm_${subj}_stage2_thresh*nii.gz
do
    dim4=`fslval ${i} dim4`
    correct=1
    if [ ! ${dim4} == ${correct} ] ; then
        echo ${i} >> error_glm_output.txt
    fi
done


