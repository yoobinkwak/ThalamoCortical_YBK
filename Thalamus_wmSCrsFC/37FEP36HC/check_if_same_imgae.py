import os
import sys
import re
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import pandas as pd



def checkSame (side, voxelsize):

    melodic_img = 'tica_results/mICA_HCvsFEP_{side}_ds{voxelsize}/dim0/melodic_IC.nii.gz'.format(side=side, voxelsize=voxelsize)
    melodicIC_map = nb.load(melodic_img)
    componentNum = melodicIC_map.shape[3]
    ICs=["%02d" % x for x in range(1,componentNum+1)]
    
    log = 'subject_list_rsFC.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()

    diffs = []
    for subject in subjects:
        for ic in ICs:
            file1 = '{subject}/37FEP36HC/{side}_ds{voxelsize}_thalamusICs_rsFC/Regressed/split_{subject}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, ic=ic)
            file2 = '{subject}/37FEP36HC/OM2015/noZnorm/Regress/split_regressed_{side}_{voxelsize}mm_4fwhm_IC{ic}_ts0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, ic=ic)
            f1 = nb.load(file1)
            f2 = nb.load(file2)
            data1 = f1.get_data()
            data2 = f2.get_data()
            
            diff = np.sum(data1!=data2)
            
            if diff != 0:
                diffs.append((file1, file2, diff))
    
            z_file1 = '{subject}/37FEP36HC/{side}_ds{voxelsize}_thalamusICs_rsFC/Regressed/split_znorm_{subject}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, ic=ic)
            z_file2 = '{subject}/37FEP36HC/OM2015/Regress/split_regressed_{side}_{voxelsiz}mm_4fwhm_IC{ic}_ts0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, ic=ic)
            z_f1 = nb.load(z_file1)
            z_f2 = nb.load(z_file2)
            z_data1 = z_f1.get_data()
            z_data2 = z_f2.get_data()

            z_diff = np.sum(z_data1!=z_data2)

            if z_diff != 0:
                diffs.append((z_file1, z_file2, z_diff))
    
    df = pd.DataFrame(diffs)
    df.to_csv('check_errors_img.txt')

            
def nosmoothCheckSame (side, voxelsize):

    melodic_img = 'tica_results/mICA_HCvsFEP_{side}_ds{voxelsize}_nosmooth/dim0/melodic_IC.nii.gz'.format(side=side, voxelsize=voxelsize)
    melodicIC_map = nb.load(melodic_img)
    componentNum = melodicIC_map.shape[3]
    ICs=["%02d" % x for x in range(1,componentNum+1)]
    
    log = 'subject_list_rsFC.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()

    diffs = []
    for subject in subjects:
        for ic in ICs:
            file1 = '{subject}/37FEP36HC/{side}_ds{voxelsize}_nosmooth_thalamusICs_rsFC/Regressed/split_{subject}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, ic=ic)
            file2 = '{subject}/37FEP36HC/OM2015/noZnorm/Regress/split_regressed_{side}_{voxelsize}mm_nosmooth_IC{ic}_ts0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, ic=ic)
            f1 = nb.load(file1)
            f2 = nb.load(file2)
            data1 = f1.get_data()
            data2 = f2.get_data()
            
            diff = np.sum(data1!=data2)
            
            if diff != 0:
                diffs.append((file1, file2, diff))
    
            z_file1 = '{subject}/37FEP36HC/{side}_ds{voxelsize}_nosmooth_thalamusICs_rsFC/Regressed/split_znorm_{subject}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, ic=ic)
            z_file2 = '{subject}/37FEP36HC/OM2015/Regress/split_regressed_{side}_{voxelsiz}mm_nosmooth_IC{ic}_ts0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, ic=ic)
            z_f1 = nb.load(z_file1)
            z_f2 = nb.load(z_file2)
            z_data1 = z_f1.get_data()
            z_data2 = z_f2.get_data()

            z_diff = np.sum(z_data1!=z_data2)

            if z_diff != 0:
                diffs.append((z_file1, z_file2, z_diff))
    
    df = pd.DataFrame(diffs)
    df.to_csv('check_errors_img.txt')

            

            





if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., 3', type=str)
	args = parser.parse_args()

        checkSame(args.side[0], args.voxelsize[0])
        nosmoothCheckSame(args.side[0], args.voxelsize[0])

