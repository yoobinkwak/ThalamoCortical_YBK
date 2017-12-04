import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image


def mergePerIC(side, voxelsize):

    randomise_dir = '37FEP36HC_randomise_wmSC'
    if not os.path.exists(randomise_dir):
        os.mkdir(randomise_dir)
    randomise_input_dir = join (randomise_dir, 'inputs')
    if not os.path.exists(randomise_input_dir):
        os.mkdir(randomise_input_dir)

    melodicIC_map = nb.load('tica_results/mICA_HCvsFEP_{side}_ds{voxelsize}/dim0/melodic_IC.nii.gz'.format(side=side, voxelsize=voxelsize))
    componentNum = melodicIC_map.shape[3]


    log = 'subject_list_37FEP36HC.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()
    imgInputs = []
    for subj in subjects:
        dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_mICA_dual_regression/'.format(side=side, voxelsize=voxelsize)
        ICs=["%02d" % x for x in range(1,componentNum+1)]
        for ic in ICs:
            dataFile = '{subj}_thresh_zstat00{ic}_stage2.nii.gz'.format(subj=subj, ic=ic)
            imgInputs.append(dataLoc+dataFile)

    for ic in ICs:
       merged_subjs_perIC = join(randomise_input_dir, 'concatenated_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
       if not os.path.isfile(merged_subjs_perIC):
           perSubj_perIC = [x for x in imgInputs if '00{ic}'.format(ic=ic) in x]
           print(perSubj_perIC)
           acrossSubjs_perIC = nilearn.image.concat_imgs(perSubj_perIC)
           acrossSubjs_perIC.to_filename(merged_subjs_perIC)




def ZnormMergePerIC(side, voxelsize):

    randomise_dir = '37FEP36HC_randomise_wmSC'
    if not os.path.exists(randomise_dir):
        os.mkdir(randomise_dir)
    randomise_input_dir = join (randomise_dir, 'znorm_inputs')
    if not os.path.exists(randomise_input_dir):
        os.mkdir(randomise_input_dir)

    melodicIC_map = nb.load('tica_results/mICA_HCvsFEP_{side}_ds{voxelsize}/dim0/melodic_IC.nii.gz'.format(side=side, voxelsize=voxelsize))
    componentNum = melodicIC_map.shape[3]


    log = 'subject_list_37FEP36HC.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()
    imgInputs = []
    for subj in subjects:
        dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_mICA_dual_regression/'.format(side=side, voxelsize=voxelsize)
        ICs=["%02d" % x for x in range(1,componentNum+1)]
        for ic in ICs:
            dataFile = 'znorm_{subj}_thresh_zstat00{ic}_stage2.nii.gz'.format(subj=subj, ic=ic)
            imgInputs.append(dataLoc+dataFile)

    for ic in ICs:
       merged_subjs_perIC = join(randomise_input_dir, 'concatenated_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
       if not os.path.isfile(merged_subjs_perIC):
           perSubj_perIC = [x for x in imgInputs if '00{ic}'.format(ic=ic) in x]
           print(perSubj_perIC)
           acrossSubjs_perIC = nilearn.image.concat_imgs(perSubj_perIC)
           acrossSubjs_perIC.to_filename(merged_subjs_perIC)
        




if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., 3mm', type=str)
	args = parser.parse_args()

        mergePerIC(args.side[0], args.voxelsize[0])
        ZnormMergePerIC(args.side[0], args.voxelsize[0])

