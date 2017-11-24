import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image


def AvePerIC(mICA, side, voxelsize, smoothing):

    ave_dir = 'Averaged_eachIC_onThal'
    if not os.path.exists(ave_dir):
        os.mkdir(ave_dir)

    glm_dir = 'tica_results/{mICA}/dim0/glm_out'.format(mICA=mICA)

    melodicIC_loc = 'tica_results/{mICA}/dim0/melodic_IC.nii.gz'.format(mICA=mICA)
    melodicIC_map = nb.load(melodicIC_loc)
    componentNum = melodicIC_map.shape[3]

    log = 'subject_list_37FEP36HC.txt'
    with open(log, 'r') as f:
        lines = f.read().split()
    imgInputs = []
    for line in lines:
        dataLoc = join (glm_dir, 'znorm_'+line)
        ICs=["%02d" % x for x in range(1,componentNum+1)]
        for ic in ICs:
            dataFile = '_stage2_thresh_zstat00{ic}.nii.gz'.format(ic=ic)
            imgInputs.append(dataLoc+dataFile)
    for ic in ICs:
       averaged_perIC = join(ave_dir, '{side}_{voxelsize}_{smoothing}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, smoothing=smoothing, ic=ic))
       if not os.path.isfile(averaged_perIC):
           perSubj_perIC = [x for x in imgInputs if '_stage2_thresh_zstat00{ic}.nii.gz'.format(ic=ic) in x]
           ave_perIC = nilearn.image.mean_img(perSubj_perIC)
           ave_perIC.to_filename(averaged_perIC)

def noZnormAvePerIC(mICA, side, voxelsize, smoothing):

    ave_dir = 'Averaged_eachIC_onThal'
    noZnorm_ave_dir = join (ave_dir, 'noZnorm')
    if not os.path.exists(noZnorm_ave_dir):
        os.mkdir(noZnorm_ave_dir)

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
       averaged_perIC = join(noZnorm_ave_dir, '{side}_{voxelsize}_{smoothing}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, smoothing=smoothing, ic=ic))
       if not os.path.isfile(averaged_perIC):
           perSubj_perIC = [x for x in imgInputs if '_stage2_thresh_zstat00{ic}.nii.gz'.format(ic=ic) in x]
           ave_perIC = nilearn.image.mean_img(perSubj_perIC)
           ave_perIC.to_filename(averaged_perIC)






if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--mICA', '-mICA', nargs=1, help = 'mICA output directory', type=str) 
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., 3mm', type=str)
	parser.add_argument('--smoothing', '-FWHM', nargs=1, help = 'e.g., 4fwhm', type=str)
	args = parser.parse_args()

        AvePerIC(args.mICA[0], args.side[0], args.voxelsize[0], args.smoothing[0])
        noZnormAvePerIC(args.mICA[0], args.side[0], args.voxelsize[0], args.smoothing[0])

