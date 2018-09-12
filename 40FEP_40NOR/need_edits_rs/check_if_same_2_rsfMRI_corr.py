import os
import sys
import re
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import pandas as pd


def checkSame (subject):
    
    general_dir='/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109'
    
    diffs = []

    
    #file1_name='{subject}/RSFC/Bi_ds3_fisherZ.nii.gz'.format(subject=subject)
    #file2_name='{subject}/test_RSFC/Bi_ds3_fisherZ.nii.gz'.format(subject=subject)
    file1_name='{subject}/test_RSFC/Bi_ds3_fisherZ.nii.gz'.format(subject=subject)
    file2_name='{subject}/pre_RSFC/Bi_ds3_fisherZ.nii.gz'.format(subject=subject)

    file1 = join(general_dir, file1_name)
    file2 = join(general_dir, file2_name)

    f1 = nb.load(file1)
    f2 = nb.load(file2)
    data1 = f1.get_data()
    data2 = f2.get_data()

    diff = np.sum(data1!=data2)
    if diff != 0:
        print('error ' + file1)
        diffs.append((file1_name, file2_name, diff))



    #file3_name='{subject}/RSFC/Bi_ds3_fisherZ_s3.nii.gz'.format(subject=subject)
    #file4_name='{subject}/test_RSFC/Bi_ds3_fisherZ_s3.nii.gz'.format(subject=subject)
    file3_name='{subject}/test_RSFC/Bi_ds3_fisherZ_s3.nii.gz'.format(subject=subject)
    file4_name='{subject}/pre_RSFC/Bi_ds3_fisherZ_s3.nii.gz'.format(subject=subject)

    file3 = join(general_dir, file3_name)
    file4 = join(general_dir, file4_name)

    f3 = nb.load(file3)
    f4 = nb.load(file4)
    data3 = f3.get_data()
    data4 = f4.get_data()

    diff = np.sum(data3!=data4)
    if diff != 0:
        print('error ' + file3)
        diffs.append((file3_name, file4_name, diff))



    #file5_name='{subject}/RSFC/with_spatial_smoothing/Bi_ds3_fisherZ.nii.gz'.format(subject=subject)
    #file6_name='{subject}/test_RSFC/with_spatial_smoothing/Bi_ds3_fisherZ.nii.gz'.format(subject=subject)
    file5_name='{subject}/test_RSFC/with_spatial_smoothing/Bi_ds3_fisherZ.nii.gz'.format(subject=subject)
    file6_name='{subject}/pre_RSFC/with_spatial_smoothing/Bi_ds3_fisherZ.nii.gz'.format(subject=subject)

    file5 = join(general_dir, file5_name)
    file6 = join(general_dir, file6_name)

    f5 = nb.load(file5)
    f6 = nb.load(file6)
    data5 = f5.get_data()
    data6 = f6.get_data()

    diff = np.sum(data5!=data6)
    if diff != 0:
        print('error ' + file5)
        diffs.append((file5_name, file6_name, diff))

    df = pd.DataFrame(diffs)
    df.to_csv('/Volume/CCNC_BI_3T_ext/thalamus_wmSCrsFC_20180109/need_edit_scripts/check_2_rsfMRI_corr.txt', mode='a', header=False)



if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--subject', '-subj', nargs=1, help = 'e.g., NOR99_KS', type=str)
	args = parser.parse_args()

        checkSame(args.subject[0])
