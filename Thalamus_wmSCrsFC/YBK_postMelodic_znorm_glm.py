import re
import sys
import os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
from scipy import stats





def zStats (side, hemi, downsample, subject):
    
    melodicDir='tica_results/mICA_HCvsFEP_{side}{downsample}/dim0'.format(side=side, downsample=downsample)
    mmthreshDir = join(melodicDir, 'stats')
    mmthreshImgss = [join(mmthreshDir, x) for x in os.listdir(mmthreshDir) if x.startswith('thresh_zstat')]
    for mmthreshImgLoc in mmthreshImgss:
        mmthreshImgs = basename(mmthreshImgLoc)
        mmthreshImg = mmthreshImgs.split('.')[0]

        glm_dir = join(melodicDir, 'glm_out')
	stage_1_output = join(glm_dir, 'znorm_{subject}_stage1_{mmthreshImg}').format(subject=subject, mmthreshImg=mmthreshImg)
        if not os.path.isfile(stage_1_output):
            print('\tz-normalizing stage 1 output')
            fsl_reg_out = join(glm_dir, '{subject}_stage1_{mmthreshImg}'.format(subject=subject, mmthreshImg=mmthreshImg))
	    fsl_glm_mat = np.loadtxt(fsl_reg_out)
	    fsl_glm_mat_z = stats.zscore(fsl_glm_mat)
	    np.savetxt(stage_1_output, fsl_glm_mat_z)
        else:
            print('\tz-normalized stage 1 output')

        stage_2_out = join(glm_dir, 'znorm_{subject}_stage2_{mmthreshImg}.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.isfile(stage_2_out):
            print('\trunning stage 2')
            subject_map = '{subject}/YB*/{side}/fdt_matrix2_reconstructed{downsample}.nii.gz'.format(side=side, subject=subject, downsample=downsample)
            stage_1_maps = [join(glm_dir, x) for x in os.listdir(glm_dir) if x.startswith('znorm_{subject}_stage1'.format(subject = subject))]
            for stage_1_map in stage_1_maps:
                command = 'fsl_glm -i {subject_map} -d {stage_1_map} -m /Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/{hemi}_thalamus_HOSC_60{downsample}.nii.gz -o {stage_2_out}'.format(subject_map = subject_map, stage_1_map = stage_1_map, hemi = hemi, downsample = downsample, stage_2_out = stage_2_out)
                os.popen(command).read()
        else:
            print('\tcompleted stage 2')


if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--hemi', '-hemi', help = 'lh or rh', nargs=1, type=str)
	parser.add_argument('--downsample', '-ds', nargs=1, help = 'e.g., _ds3', type=str)
	parser.add_argument('--subject', '-sub', nargs=1, type=str)
	args = parser.parse_args()

	zStats(args.side[0], args.hemi[0], args.downsample[0], args.subject[0])
