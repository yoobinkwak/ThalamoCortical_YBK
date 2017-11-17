import re
import sys
import os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image

def mergePerSubject (mICA, subject):
    glm_dir = join (mICA, 'dim0/glm_out')
    check_dir = join(glm_dir, 'check_output')
    if not os.path.exists(check_dir):
        os.mkdir(check_dir)

    merged_noZnorm = join(check_dir, 'merged_noZnorm_{subject}.nii.gz').format(subject=subject)
    if not os.path.isfile(merged_noZnorm):
        noZnorm_maps = [join(glm_dir, x) for x in os.listdir(glm_dir) if x.startswith('{subject}_stage2_thresh_zstat'.format(subject = subject))]
        merge_noZnorm = nilearn.image.concat_imgs(noZnorm_maps)
        merge_noZnorm.to_filename(merged_noZnorm)

    merged_Znorm = join(check_dir, 'merged_Znorm_{subject}.nii.gz').format(subject=subject)
    if not os.path.isfile(merged_Znorm):
        Znorm_maps = [join(glm_dir, x) for x in os.listdir(glm_dir) if x.startswith('znorm_{subject}_stage2_thresh_zstat'.format(subject = subject))]
        merge_Znorm = nilearn.image.concat_imgs(Znorm_maps)
        merge_Znorm.to_filename(merged_Znorm)


if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--mICA', '-mICA', nargs=1, help = 'mICA output directory', type=str)
	parser.add_argument('--subject', '-subj', nargs=1, type=str)
	args = parser.parse_args()

	mergePerSubject(args.mICA[0], args.subject[0])
