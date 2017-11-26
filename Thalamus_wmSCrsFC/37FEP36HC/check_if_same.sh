subj=${1}
side=${2}
voxel_size=${3} 


melodic_img=tica_results/mICA_HCvsFEP_${side}_ds${voxel_size}/dim0/melodic_IC.nii.gz
NumICs=`fslval ${melodic_img} dim 4`
for ic in $(seq -w 01 ${NumICs})
do
    file1=${subj}/37FEP36HC/${side}_ds${voxel_size}_mICA_dual_regression/${subj}_thresh_zstat00${ic}_stage1
    file2=tica_results/mICA_HCvsFEP_${side}_ds${voxel_size}/dim0/glm_out/${subj}_stage1_thresh_zstat00${ic}
    if cmp -s ${file1} ${file2}
    then
        echo "same"
    else
        echo ${file1} >> check_errors.txt
    fi

    z_file1=${subj}/37FEP36HC/${side}_ds${voxel_size}_mICA_dual_regression/znorm_${subj}_thresh_zstat00${ic}_stage1
    z_file2=tica_results/mICA_HCvsFEP_${side}_ds${voxel_size}/dim0/glm_out/znorm_${subj}_stage1_thresh_zstat00${ic}
    if cmp -s ${z_file1} ${z_file2}
    then
        echo "same"
    else
        echo ${z_file1} >> check_errors.txt
    fi
done

nosmooth_melodic_img=tica_results/mICA_HCvsFEP_${side}_ds${voxel_size}_nosmooth/dim0/melodic_IC.nii.gz
numICs=`fslval ${nosmooth_melodic_img} dim 4`
for IC in $(seq -w 01 ${numICs})
do
    FILE1=${subj}/37FEP36HC/${side}_ds${voxel_size}_nosmooth_mICA_dual_regression/${subj}_thresh_zstat00${IC}_stage1
    FILE2=tica_results/mICA_HCvsFEP_${side}_ds${voxel_size}_nosmooth/dim0/glm_out/${subj}_stage1_thresh_zstat00${IC}
    if cmp -s ${FILE1} ${FILE2}
    then
        echo "same"
    else
        echo ${FILE1} >> check_errors.txt
    fi

    z_FILE1=${subj}/37FEP36HC/${side}_ds${voxel_size}_nosmooth_mICA_dual_regression/znorm_${subj}_thresh_zstat00${IC}_stage1
    z_FILE2=tica_results/mICA_HCvsFEP_${side}_ds${voxel_size}_nosmooth/dim0/glm_out/znorm_${subj}_stage1_thresh_zstat00${IC}
    if cmp -s ${z_FILE1} ${z_FILE2}
    then
        echo "same"
    else
        echo ${z_FILE1} >> check_errors.txt
    fi
done







