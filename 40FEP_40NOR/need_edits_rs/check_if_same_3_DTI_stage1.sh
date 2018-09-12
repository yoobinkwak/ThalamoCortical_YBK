subj=${1}
side=${2}   #left or right
voxel_size=${3} #ds3

#melodic_img=/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/wmSC_ICA_mICA/${voxel_size}_${side}_fwhm6/dim0/melodic_IC.nii.gz
melodic_img=/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/wmSC_ICA_mICA/${voxel_size}_${side}/dim0/melodic_IC.nii.gz
NumICs=`fslval ${melodic_img} dim4`

for ic in $(seq -w 01 ${NumICs})
do
#    file1=/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/${subj}/DualRegression_TensorICA/SpatialRegression_Stage1/${voxel_size}_${side}_fwhm6/${subj}_thresh_zstat00${ic}_stage1_demeaned
#    file2=/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/${subj}/Dual_Regression/TensorICA/ds3_right_fwhm6/SpatialRegression_Stage1/${subj}_thresh_zstat00${ic}_stage1.txt
#    cmp ${file1} ${file2} >> /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/need_edit_scripts/check_3_DTI_stage1.txt
#    diff -q ${file1} ${file2} >> /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/need_edit_scripts/check_3_DTI_stage1.txt
#    diff -s ${file1} ${file2} >> /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/need_edit_scripts/check_3_DTI_stage1.txt


    file1=/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/${subj}/DualRegression_TensorICA/SpatialRegression_Stage1/${voxel_size}_${side}_nosmooth/${subj}_thresh_zstat00${ic}_stage1_demeaned
    file2=/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/${subj}/Dual_Regression/TensorICA/ds3_right_nosmooth/SpatialRegression_Stage1/${subj}_thresh_zstat00${ic}_stage1.txt
    cmp ${file1} ${file2} >> /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/need_edit_scripts/check_3_DTI_stage1.txt
    diff -q ${file1} ${file2} >> /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/need_edit_scripts/check_3_DTI_stage1.txt
    diff -s ${file1} ${file2} >> /Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/need_edit_scripts/check_3_DTI_stage1.txt






done
