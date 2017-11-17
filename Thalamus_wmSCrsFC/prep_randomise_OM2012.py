import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image



def mergePerIC(mICA, side, voxelsize, smoothing):

    glm_dir = 'tica_results/{mICA}/dim0/glm_out'.format(mICA=mICA)
    randomise_dir = 'OM2012_tensor_stats'
    if not os.path.exists(randomise_dir):
        os.mkdir(randomise_dir)

    melodicIC_loc = 'tica_results/{mICA}/dim0/melodic_IC.nii.gz'.format(mICA=mICA)
    melodicIC_map = nb.load(melodicIC_loc)
    componentNum = melodicIC_map.shape[3]

    ICs=["%02d" % x for x in range(1,componentNum+1)]
    for ic in ICs:
        merged_subjs_perIC = join(randomise_dir, '{side}_IC{ic}_{voxelsize}_{smoothing}.nii.gz'.format(ic=ic, side=side, voxelsize=voxelsize, smoothing=smoothing))
        if not os.path.isfile(merged_subjs_perIC):
            perSubj_perIC = [join(glm_dir, x) for x in os.listdir(glm_dir) if x.startswith('znorm') and x.endswith('stage2_thresh_zstat00{ic}.nii.gz'.format(ic=ic))]
            acrossSubjs_perIC = nilearn.image.concat_imgs(perSubj_perIC)
            acrossSubjs_perIC.to_filename(merged_subjs_perIC)


if __name__== "__main__":
	parser = argparse.ArgumentParser()
        parser.add_argument('--mICA', '-mICA', nargs=1, help = 'mICA output directory', type=str)   
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., 2,3', type=str)
	parser.add_argument('--smoothing', '-FWHM', nargs=1, help = 'e.g., 4fwhm', type=str)
	args = parser.parse_args()

        mergePerIC(args.mICA[0], args.side[0], args.voxelsize[0], args.smoothing[0])
