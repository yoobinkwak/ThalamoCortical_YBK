import os 
import re
import sys
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import pandas as pd


def fdt_normalize(voxelsize, side, smoothing, IC):
    
    log = 'subjects.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()

    for subject in subjects:
        dataLoc = '{subject}/rsFC_seed_tractography/{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(subject=subject, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
        dataDirs = [ x for x in os.listdir(dataLoc) if '_demeaned_' in x]
        for dataDir in dataDirs:
            dataFile = '{dataLoc}/{dataDir}/fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            waytotal = '{dataLoc}/{dataDir}/waytotal'.format(dataLoc=dataLoc, dataDir=dataDir)

            if not os.path.isfile('{dataLoc}/{dataDir}/thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)):
                val = int(open('{}'.format(waytotal), 'r').read().replace('/n', '').replace(' ', ''))
                command = 'fslmaths {0} {1} {2} {3}'.format(dataFile, '-div', val, '{dataLoc}/{dataDir}/norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir))
                command_mask = 'fslmaths {0} {1} {2} {3}'.format(dataFile, '-div', val, '-bin {dataLoc}/{dataDir}/norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir))
                os.popen(command).read
                os.popen(command_mask).read

                ##### adding "-thrp 3" seems to render same results as not adding the option for some files...?
                command_thr = 'fslmaths {0} {1} {2} {3}'.format(dataFile, '-div', val, '-thrp 3 {dataLoc}/{dataDir}/thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir))
                command_thr_mask = 'fslmaths {0} {1} {2} {3}'.format(dataFile, '-div', val, '-thrp 3 -bin {dataLoc}/{dataDir}/thr_norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir))
                os.popen(command_thr).read
                os.popen(command_thr_mask).read




def registration(voxelsize, side, smoothing, IC):
    
    log = 'subjects.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()

    for subject in subjects:
        dataLoc = '{subject}/rsFC_seed_tractography/{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(subject=subject, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
        dataDirs = [ x for x in os.listdir(dataLoc) if '_demeaned_' in x]
        for dataDir in dataDirs:
           
            reg_normFA = '{dataLoc}/{dataDir}/reg_FA_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            reg_thrFA = '{dataLoc}/{dataDir}/reg_FA_thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            reg_normMD = '{dataLoc}/{dataDir}/reg_MD_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            reg_thrMD = '{dataLoc}/{dataDir}/reg_MD_thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            
            if not os.path.isfile(reg_normFA):
                norm_mask = '{dataLoc}/{dataDir}/norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                thr_mask = '{dataLoc}/{dataDir}/thr_norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                FA ='{subject}/DTI/dti_FA.nii.gz'.format(subject=subject)
                MD ='{subject}/DTI/dti_MD.nii.gz'.format(subject=subject)
                warp='{subject}/DTI/Registration/mni2reorient_t1w2nodif_coeff.nii.gz'.format(subject=subject)

                command_normFA = 'applywarp -i {0} -r {1} -w {2} -o {3}'.format(norm_mask, FA, warp, reg_normFA)
                command_thrFA = 'applywarp -i {0} -r {1} -w {2} -o {3}'.format(thr_mask, FA, warp, reg_thrFA)
                command_normMD = 'applywarp -i {0} -r {1} -w {2} -o {3}'.format(norm_mask, MD, warp, reg_normMD)
                command_thrMD = 'applywarp -i {0} -r {1} -w {2} -o {3}'.format(thr_mask, MD, warp, reg_thrMD)

                os.popen(command_normFA).read
                os.popen(command_thrFA).read
                os.popen(command_normMD).read
                os.popen(command_thrMD).read








if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--voxelsize', '-vox', nargs=1, type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--smoothing', '-smooth', nargs=1,  help = 'e.g., nosmooth, fwhm6, fwhm6preproc', type=str)
	parser.add_argument('--IC', '-IC', nargs=1, help = 'e.g., 10 or 20', type=str)
	args = parser.parse_args()

	fdt_normalize(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
	registration(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
