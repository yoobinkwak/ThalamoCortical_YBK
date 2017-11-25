import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image


def mergePerIC(mICA, side, voxelsize, smoothing):

    randomise_dir = 're_OM2012_tensor_stats'
    if not os.path.exists(randomise_dir):
        os.mkdir(randomise_dir)
    randomise_input_dir = join (randomise_dir, 'noZnorm_inputs')
    if not os.path.exists(randomise_input_dir):
        os.mkdir(randomise_input_dir)

    glm_dir = 'tica_results/{mICA}/dim0/glm_out'.format(mICA=mICA)

    melodicIC_loc = 'tica_results/{mICA}/dim0/melodic_IC.nii.gz'.format(mICA=mICA)
    melodicIC_map = nb.load(melodicIC_loc)
    componentNum = melodicIC_map.shape[3]


    log = 'subject_list_37FEP36HC.txt'
    with open(log, 'r') as f:
        lines = f.read().split()
    imgInputs = []
    for line in lines:
        dataLoc = join (glm_dir, line)
        ICs=["%02d" % x for x in range(1,componentNum+1)]
        for ic in ICs:
            dataFile = '_stage2_thresh_zstat00{ic}.nii.gz'.format(ic=ic)
            imgInputs.append(dataLoc+dataFile)

    for ic in ICs:
       merged_subjs_perIC = join(randomise_input_dir, '{side}_{voxelsize}_{smoothing}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, smoothing=smoothing, ic=ic))
       if not os.path.isfile(merged_subjs_perIC):
           perSubj_perIC = [x for x in imgInputs if '_stage2_thresh_zstat00{ic}.nii.gz'.format(ic=ic) in x]
           print(perSubj_perIC)
           acrossSubjs_perIC = nilearn.image.concat_imgs(perSubj_perIC)
           acrossSubjs_perIC.to_filename(merged_subjs_perIC)

        




if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--mICA', '-mICA', nargs=1, help = 'mICA output directory', type=str) 
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., 3mm', type=str)
	parser.add_argument('--smoothing', '-FWHM', nargs=1, help = 'e.g., 4fwhm', type=str)
	args = parser.parse_args()

        mergePerIC(args.mICA[0], args.side[0], args.voxelsize[0], args.smoothing[0])

