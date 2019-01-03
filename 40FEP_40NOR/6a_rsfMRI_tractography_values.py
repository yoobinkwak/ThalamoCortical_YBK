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
    #log = 'test_subj.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()

    for subject in subjects:
        dataLoc = '{subject}/rsFC_seed_tractography/{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(subject=subject, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)

        dataDirs = [ x for x in os.listdir(dataLoc) if '_demeaned_' in x]
        for dataDir in dataDirs:
            dataFile = '{dataLoc}/{dataDir}/fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            waytotal = '{dataLoc}/{dataDir}/waytotal'.format(dataLoc=dataLoc, dataDir=dataDir)

            #if not os.path.isfile('{dataLoc}/{dataDir}/norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)):
            if not os.path.isfile('{dataLoc}/{dataDir}/thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)):
                val = int(open('{}'.format(waytotal), 'r').read().replace('/n', '').replace(' ', ''))
                command = 'fslmaths {0} {1} {2} {3}'.format(dataFile, '-div', val, '{dataLoc}/{dataDir}/norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir))
                command_mask = 'fslmaths {0} {1} {2} {3}'.format(dataFile, '-div', val, '-bin {dataLoc}/{dataDir}/norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir))
                os.popen(command).read
                os.popen(command_mask).read

                ##### adding "-thrp 3" seems to render same results as not adding the option...?
                command_thr = 'fslmaths {0} {1} {2} {3}'.format(dataFile, '-div', val, '-thrp 3 {dataLoc}/{dataDir}/thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir))
                command_thr_mask = 'fslmaths {0} {1} {2} {3}'.format(dataFile, '-div', val, '-thrp 3 -bin {dataLoc}/{dataDir}/thr_norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir))
                os.popen(command_thr).read
                os.popen(command_thr_mask).read











if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--subject', '-subj', nargs=1, type=str)
	parser.add_argument('--voxelsize', '-vox', nargs=1, type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--smoothing', '-smooth', nargs=1,  help = 'e.g., nosmooth, fwhm6, fwhm6preproc', type=str)
	parser.add_argument('--IC', '-IC', nargs=1, help = 'e.g., 10 or 20', type=str)
	args = parser.parse_args()

	#fdt_normalize(args.subject[0], args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
	fdt_normalize(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
