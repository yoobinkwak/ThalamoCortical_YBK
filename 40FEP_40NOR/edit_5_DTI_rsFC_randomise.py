import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image


def mergePerIC(voxelsize, side, spatialsmooth):

    randomise = 'Randomise_TensorICA2RSFC'
    if not os.path.exists(randomise):
        os.mkdir(randomise)
    randomise_dir = join(randomise, '{voxelsize}_{side}_{spatialsmooth}'.format(voxelsize=voxelsize, side=side, spatialsmooth=spatialsmooth)
    if not os.path.exists(randomise_dir):
        os.mkdir(randomise_dir)
    randomise_input_dir = join (randomise_dir, 'input')
    if not os.path.exists(randomise_input_dir):
        os.mkdir(randomise_input_dir)

    melodicIC_map = nb.load('wmSC_ICA_mICA/{voxelsize}_{side}_{spatialsmooth}/dim0/melodic_IC.nii.gz'.format(voxelsize=voxelsize, side=side, spatialsmooth=spatialsmooth))
    componentNum = melodicIC_map.shape[3]

    log = 'subject_list_rsFC.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()
    imgInputs = []
    for subj in subjects:
        dataLoc = subj+'/TensorIC_RSFC/${voxel_size}_${side}_${spatialsmooth}/SpatialMap/'.format(voxelsize=voxelsize, side=side, spatialsmooth=spatialsmooth)
        ICs=["%02d" % x for x in range(1,componentNum+1)]
        for ic in ICs:
            dataFile='{subj}_IC{ic}_map0000.nii.gz'.format(subj=subj, ic=ic)
            imgInputs.append(dataLoc+dataFile)


    for ic in ICs:
        merged_subjs_perIC = join(randomise_input_dir, 'concatenated_{voxelsize}_{side}_{spatialsmooth}_IC{ic}.nii.gz'.format(voxelsize=voxelsize, side=side, spatialsmooth=spatialsmooth, ic=ic))
        if not os.path.isfile(merged_subjs_perIC):
            perSubj_perIC = [x for x in imgInputs if '00{ic}'.format(ic=ic) in x]
            print(perSubj_perIC)
            acrossSubjs_perIC = nilearn.image.concat_imgs(perSubj_perIC)
            acrossSubjs_perIC.to_filename(merged_subjs_perIC)







def nosmoothMergePerIC(voxelsize, side):

    randomise = 'Randomise_TensorICA2RSFC'
    if not os.path.exists(randomise):
        os.mkdir(randomise)
    randomise_dir = join(randomise, '{voxelsize}_{side}_nosmooth'.format(voxelsize=voxelsize, side=side))
    if not os.path.exists(randomise_dir):
        os.mkdir(randomise_dir)
    randomise_input_dir = join (randomise_dir, 'input')
    if not os.path.exists(randomise_input_dir):
        os.mkdir(randomise_input_dir)

    melodicIC_map = nb.load('wmSC_ICA_mICA/{voxelsize}_{side}/dim0/melodic_IC.nii.gz'.format(voxelsize=voxelsize, side=side))
    componentNum = melodicIC_map.shape[3]

    log = 'subject_list_rsFC.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()
    imgInputs = []
    for subj in subjects:
        dataLoc = subj+'/TensorIC_RSFC/${voxel_size}_${side}_nosmooth/SpatialMap/'.format(voxelsize=voxelsize, side=side)
        ICs=["%02d" % x for x in range(1,componentNum+1)]
        for ic in ICs:
            dataFile='{subj}_IC{ic}_map0000.nii.gz'.format(subj=subj, ic=ic)
            imgInputs.append(dataLoc+dataFile)


    for ic in ICs:
        merged_subjs_perIC = join(randomise_input_dir, 'concatenated_{voxelsize}_{side}_nosmooth_IC{ic}.nii.gz'.format(voxelsize=voxelsize, side=side, ic=ic))
        if not os.path.isfile(merged_subjs_perIC):
            perSubj_perIC = [x for x in imgInputs if '00{ic}'.format(ic=ic) in x]
            print(perSubj_perIC)
            acrossSubjs_perIC = nilearn.image.concat_imgs(perSubj_perIC)
            acrossSubjs_perIC.to_filename(merged_subjs_perIC)







if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., ds3 or 2mm', type=str)
        parser.add_argument('--spatialsmooth', '-fwhm', nargs=1,  help = 'e.g., fwhm4', type=str)
	args = parser.parse_args()

        mergePerIC(args.side[0], args.voxelsize[0], args.spatialsmooth[0])

