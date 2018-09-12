import os
import sys
import re
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import pandas as pd

def checkSame (subject, voxelsize, side):

    #melodic_img='/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/wmSC_ICA_mICA/{voxelsize}_{side}_fwhm6/dim0/melodic_IC.nii.gz'.format(voxelsize=voxelsize, side=side)
    melodic_img='/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/wmSC_ICA_mICA/{voxelsize}_{side}/dim0/melodic_IC.nii.gz'.format(voxelsize=voxelsize, side=side)
    melodicIC_map = nb.load(melodic_img)
    componentNum = melodicIC_map.shape[3]
    ICs=["%02d" % x for x in range(1,componentNum+1)]


    diffs = []
    for ic in ICs:
        file1='/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/{subject}/DualRegression_TensorICA/TemporalRegression_Stage2/{voxelsize}_{side}_nosmooth/{subject}_thresh_zstat00{ic}_stage2_demeaned.nii.gz'.format(subject=subject, voxelsize=voxelsize, side=side, ic=ic)  
        file2='/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/{subject}/Dual_Regression/TensorICA/{voxelsize}_{side}_nosmooth/TemporalRegression_Stage2/{subject}_thresh_zstat00{ic}_stage2_desnorm.nii.gz'.format(subject=subject, voxelsize=voxelsize, side=side, ic=ic)  
        f1 = nb.load(file1)
        f2 = nb.load(file2)
        data1 = f1.get_data()
        data2 = f2.get_data()

        diff = np.sum(data1!=data2)

        if diff != 0:
            print('error ' + file1)
            diffs.append((file1, file2, diff))

        file3='/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/{subject}/DualRegression_TensorICA/TemporalRegression_Stage2/{voxelsize}_{side}_nosmooth/z_{subject}_thresh_zstat00{ic}_stage2_demeaned.nii.gz'.format(subject=subject, voxelsize=voxelsize, side=side, ic=ic)  
        file4='/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/{subject}/Dual_Regression/TensorICA/{voxelsize}_{side}_nosmooth/TemporalRegression_Stage2/z_{subject}_thresh_zstat00{ic}_stage2_desnorm.nii.gz'.format(subject=subject, voxelsize=voxelsize, side=side, ic=ic)  
        f3 = nb.load(file3)
        f4 = nb.load(file4)
        data3 = f3.get_data()
        data4 = f4.get_data()

        z_diff = np.sum(data3!=data4)

        if z_diff != 0:
            print('error ' + file3)
            diffs.append((file3, file4, z_diff))


        file5='/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/{subject}/DualRegression_TensorICA/TemporalRegression_Stage2/{voxelsize}_{side}_nosmooth/z2.3_{subject}_thresh_zstat00{ic}_stage2_demeaned.nii.gz'.format(subject=subject, voxelsize=voxelsize, side=side, ic=ic)  
        file6='/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/{subject}/Dual_Regression/TensorICA/{voxelsize}_{side}_nosmooth/TemporalRegression_Stage2/z2.3_{subject}_thresh_zstat00{ic}_stage2_desnorm.nii.gz'.format(subject=subject, voxelsize=voxelsize, side=side, ic=ic)  
        f5 = nb.load(file5)
        f6 = nb.load(file6)
        data5 = f5.get_data()
        data6 = f6.get_data()

        z23_diff = np.sum(data5!=data6)

        if z23_diff != 0:
            print('error ' + file5)
            diffs.append((file5, file6, z23_diff))







    df = pd.DataFrame(diffs)
    df.to_csv('/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/need_edit_scripts/check_3_DTI_stage2.txt')






if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--subject', '-subj', nargs=1, help = 'e.g., NOR99_KS', type=str)
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., ds3', type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	args = parser.parse_args()

        checkSame(args.subject[0], args.voxelsize[0], args.side[0])

