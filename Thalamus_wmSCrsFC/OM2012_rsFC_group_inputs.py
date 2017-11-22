import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image

def mergeOM12rsFC(side, voxelsize, smoothing, IC):

    randomise_dir = 'OM2012_rsFC_stats'
    if not os.path.exists(randomise_dir):
        os.mkdir(randomise_dir)
    randomise_input_dir = join (randomise_dir, 'input')
    if not os.path.exists(randomise_input_dir):
        os.mkdir(randomise_input_dir)

    log = 'subject_list_rsFC.txt'
    with open(log, 'r') as f:
        lines = f.read().split()
    imgInputs = []
    for line in lines:
        dataLoc = line+'/OM2012/'
        dataFile = 'split_{side}_{voxelsize}_{smoothing}_IC{IC}_regressed0000.nii.gz'.format(side=side, voxelsize=voxelsize, smoothing=smoothing, IC=IC)
        imgInputs.append(dataLoc+dataFile)
    
    FEP_list = []
    for line in lines:
        if line.startswith('FEP'):
            subj = line+'/OM2012/'
            img = 'split_{side}_{voxelsize}_{smoothing}_IC{IC}_regressed0000.nii.gz'.format(side=side, voxelsize=voxelsize, smoothing=smoothing, IC=IC)
            FEP_list.append(subj+img)
    
    NOR_list = []
    for line in lines:
        if line.startswith('NOR'):
            subj = line+'/OM2012/'
            img = 'split_{side}_{voxelsize}_{smoothing}_IC{IC}_regressed0000.nii.gz'.format(side=side, voxelsize=voxelsize, smoothing=smoothing, IC=IC)
            NOR_list.append(subj+img)
   
    merged_subjs = join(randomise_input_dir, '{side}_{voxelsize}_{smoothing}_IC{IC}.nii.gz'.format(side=side, voxelsize=voxelsize, smoothing=smoothing, IC=IC))
    if not os.path.isfile(merged_subjs):
        perSubj = [x for x in imgInputs if 'split_{side}_{voxelsize}_{smoothing}_IC{IC}_regressed0000.nii.gz'.format(side=side, voxelsize=voxelsize, smoothing=smoothing, IC=IC) in x]
        acrossSubjs = nilearn.image.concat_imgs(perSubj)
        acrossSubjs.to_filename(merged_subjs)

    merged_FEP = join(randomise_input_dir, 'FEP_{side}_{voxelsize}_{smoothing}_IC{IC}.nii.gz'.format(side=side, voxelsize=voxelsize, smoothing=smoothing, IC=IC))
    if not os.path.isfile(merged_FEP):
        FEP = [x for x in FEP_list if 'split_{side}_{voxelsize}_{smoothing}_IC{IC}_regressed0000.nii.gz'.format(side=side, voxelsize=voxelsize, smoothing=smoothing, IC=IC) in x]
        print(FEP)
        acrossFEP = nilearn.image.concat_imgs(FEP)
        acrossFEP.to_filename(merged_FEP)

    merged_NOR = join(randomise_input_dir, 'NOR_{side}_{voxelsize}_{smoothing}_IC{IC}.nii.gz'.format(side=side, voxelsize=voxelsize, smoothing=smoothing, IC=IC))
    if not os.path.isfile(merged_NOR):
        NOR = [x for x in NOR_list if 'split_{side}_{voxelsize}_{smoothing}_IC{IC}_regressed0000.nii.gz'.format(side=side, voxelsize=voxelsize, smoothing=smoothing, IC=IC) in x]
        print(NOR)
        acrossNOR = nilearn.image.concat_imgs(NOR)
        acrossNOR.to_filename(merged_NOR)



if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., 3mm', type=str)
	parser.add_argument('--smoothing', '-FWHM', nargs=1, help = 'e.g., 4fwhm', type=str)
	parser.add_argument('--IC', '-IC', nargs=1, help = 'IC number', type=str)
	args = parser.parse_args()

        mergeOM12rsFC(args.side[0], args.voxelsize[0], args.smoothing[0], args.IC[0])
