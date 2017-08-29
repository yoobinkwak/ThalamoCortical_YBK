for i in [CNF]*
do
    for ds in 1 2 3 4 5 6 7
    do
        paste ${i}/dual_regression/thalamic_ts_IC${ds}.txt ${i}/motion/demeaned_mn.txt ${i}/nuisance/demeaned_CSF_noise.txt ${i}/nuisance/demeaned_WM_noise.txt > ${i}/dual_regression/IC${ds}_design.txt

        Text2Vest ${i}/dual_regression/IC${ds}_design.txt ${i}/dual_regression/IC${ds}_design.mat 

        fsl_glm -i ${i}/post_feat/temporal_filtered.nii.gz -d ${i}/dual_regression/IC${ds}_design.mat -o ${i}/dual_regression/IC${ds}_FC_map
    done
done







