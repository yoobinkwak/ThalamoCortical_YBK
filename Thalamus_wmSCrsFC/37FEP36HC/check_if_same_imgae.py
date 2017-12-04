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
            #print('checking ' + file1)
            f1 = nb.load(file1)
            f2 = nb.load(file2)
            data1 = f1.get_data()
            data2 = f2.get_data()
            
            diff = np.sum(data1!=data2)
            
            if diff != 0:
                print('error ' + file1)
                diffs.append((file1, file2, diff))
            #else:
                #print('no error ' + file1)

            file3 = '{subject}/37FEP36HC/{side}_ds{voxelsize}_mICA_dual_regression/{subject}_thresh_zstat00{ic}_stage2.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, ic=ic)
            file4 = 'tica_results/mICA_HCvsFEP_{side}_ds{voxelsize}/dim0/glm_out/{subject}_stage2_thresh_zstat00{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, subject=subject, ic=ic)
            #print('checking ' + file1)
            f3 = nb.load(file3)
            f4 = nb.load(file4)
            data3 = f3.get_data()
            data4 = f4.get_data()
            
            diff2 = np.sum(data3!=data4)
            
            if diff2 != 0:
                print('error ' + file3)
                diffs.append((file3, file4, diff2))
            #else:
                #print('no error ' + file3)

    
            z_file1 = '{subject}/37FEP36HC/{side}_ds{voxelsize}_thalamusICs_rsFC/Regressed/split_znorm_{subject}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, ic=ic)
            z_file2 = '{subject}/37FEP36HC/OM2015/Regress/split_regressed_{side}_{voxelsize}mm_4fwhm_IC{ic}_ts0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, ic=ic)
            z_f1 = nb.load(z_file1)
            z_f2 = nb.load(z_file2)
            z_data1 = z_f1.get_data()
            z_data2 = z_f2.get_data()

            z_diff = np.sum(z_data1!=z_data2)

            if z_diff != 0:
                print('error ' + z_file1)
                diffs.append((z_file1, z_file2, z_diff))
            #else:
                #print('no error ' + file1)


            z_file3 = '{subject}/37FEP36HC/{side}_ds{voxelsize}_mICA_dual_regression/znorm_{subject}_thresh_zstat00{ic}_stage2.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, ic=ic)
            z_file4 = 'tica_results/mICA_HCvsFEP_{side}_ds{voxelsize}/dim0/glm_out/znorm_{subject}_stage2_thresh_zstat00{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, subject=subject, ic=ic)
            #print('checking ' + z_file3)
            z_f3 = nb.load(z_file3)
            z_f4 = nb.load(z_file4)
            z_data3 = z_f3.get_data()
            z_data4 = z_f4.get_data()
            
            z_diff2 = np.sum(z_data3!=z_data4)
            
            if z_diff2 != 0:
                print('error ' + z_file3)
                diffs.append((z_file3, z_file4, z_diff2))
            #else:
                #print('no error ' + z_file3)

    
    df = pd.DataFrame(diffs)
    df.to_csv('check_errors_img.txt')

            
def nosmoothCheckSame (side, voxelsize):

    n_melodic_img = 'tica_results/mICA_HCvsFEP_{side}_ds{voxelsize}_nosmooth/dim0/melodic_IC.nii.gz'.format(side=side, voxelsize=voxelsize)
    n_melodicIC_map = nb.load(n_melodic_img)
    n_componentNum = n_melodicIC_map.shape[3]
    n_ICs=["%02d" % x for x in range(1,n_componentNum+1)]
    
    log = 'subject_list_rsFC.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()

    diffs = []
    for subject in subjects:
        for n_ic in n_ICs:
            file1 = '{subject}/37FEP36HC/{side}_ds{voxelsize}_nosmooth_thalamusICs_rsFC/Regressed/split_{subject}_thresh_zstat00{n_ic}_ts_regressed0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, n_ic=n_ic)
            file2 = '{subject}/37FEP36HC/OM2015/noZnorm/Regress/split_regressed_{side}_{voxelsize}mm_nosmooth_IC{n_ic}_ts0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, n_ic=n_ic)
            #print('checking ' + file1)
            f1 = nb.load(file1)
            f2 = nb.load(file2)
            data1 = f1.get_data()
            data2 = f2.get_data()
            
            diff = np.sum(data1!=data2)
            
            if diff != 0:
                print('error ' + file1)
                diffs.append((file1, file2, diff))

            file3 = '{subject}/37FEP36HC/{side}_ds{voxelsize}_nosmooth_mICA_dual_regression/{subject}_thresh_zstat00{n_ic}_stage2.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, n_ic=n_ic)
            file4 = 'tica_results/mICA_HCvsFEP_{side}_ds{voxelsize}_nosmooth/dim0/glm_out/{subject}_stage2_thresh_zstat00{n_ic}.nii.gz'.format(side=side, voxelsize=voxelsize, subject=subject, n_ic=n_ic)
            #print('checking ' + file1)
            f3 = nb.load(file3)
            f4 = nb.load(file4)
            data3 = f3.get_data()
            data4 = f4.get_data()
            
            diff = np.sum(data3!=data4)
            
            if diff != 0:
                print('error ' + file3)
                diffs.append((file3, file4, diff))
            #else:
                #print('no error ' + file3)

    
            z_file1 = '{subject}/37FEP36HC/{side}_ds{voxelsize}_nosmooth_thalamusICs_rsFC/Regressed/split_znorm_{subject}_thresh_zstat00{n_ic}_ts_regressed0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, n_ic=n_ic)
            z_file2 = '{subject}/37FEP36HC/OM2015/Regress/split_regressed_{side}_{voxelsize}mm_nosmooth_IC{n_ic}_ts0000.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, n_ic=n_ic)
            z_f1 = nb.load(z_file1)
            z_f2 = nb.load(z_file2)
            z_data1 = z_f1.get_data()
            z_data2 = z_f2.get_data()

            z_diff = np.sum(z_data1!=z_data2)

            if z_diff != 0:
                print('error ' + z_file1)
                diffs.append((z_file1, z_file2, z_diff))
    
            z_file3 = '{subject}/37FEP36HC/{side}_ds{voxelsize}_nosmooth_mICA_dual_regression/znorm_{subject}_thresh_zstat00{n_ic}_stage2.nii.gz'.format(subject=subject, side=side, voxelsize=voxelsize, n_ic=n_ic)
            z_file4 = 'tica_results/mICA_HCvsFEP_{side}_ds{voxelsize}_nosmooth/dim0/glm_out/znorm_{subject}_stage2_thresh_zstat00{n_ic}.nii.gz'.format(side=side, voxelsize=voxelsize, subject=subject, n_ic=n_ic)
            #print('checking ' + z_file3)
            z_f3 = nb.load(z_file3)
            z_f4 = nb.load(z_file4)
            z_data3 = z_f3.get_data()
            z_data4 = z_f4.get_data()
            
            z_diff2 = np.sum(z_data3!=z_data4)
            
            if z_diff2 != 0:
                print('error ' + z_file3)
                diffs.append((z_file3, z_file4, z_diff2))
            #else:
                #print('no error ' + z_file3)
    df = pd.DataFrame(diffs)
    df.to_csv('check_errors_nosmoothimg.txt')

            

if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., 3', type=str)
	args = parser.parse_args()

        checkSame(args.side[0], args.voxelsize[0])
        nosmoothCheckSame(args.side[0], args.voxelsize[0])
