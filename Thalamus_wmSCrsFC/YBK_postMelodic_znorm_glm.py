import re
import sys
import os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
from scipy import stats





def zStats (melodicDir, subject):
    mmthreshDir = join(melodicDir, 'stats')
    mmthreshImgss = [join(mmthreshDir, x) for x in os.listdir(mmthreshDir) if x.startswith('thresh_zstat')]
    for mmthreshImgLoc in mmthreshImgss:
        mmthreshImgs = basename(mmthreshImgLoc)
        mmthreshImg = mmthreshImgs.split('.')[0]
         
        fsl_reg_out = join(melodicDir, 'glm_out', '{subject}_stage1_{mmthreshImg}'.format(subject=subject, mmthreshImg=mmthreshImg))
	fsl_glm_mat = np.loadtxt(fsl_reg_out)
	fsl_glm_mat_z = stats.zscore(fsl_glm_mat)
	np.savetxt(os.path.join(melodicDir, 'glm_out', 'znorm_{subject}_stage1_{mmthreshImg}').format(subject=subject, mmthreshImg=mmthreshImg), fsl_glm_mat_z)

        subject_map = '{subject}/YB*/left/fdt_matrix2_reconstructed_ds3.nii.gz'.format(subject=subject)
        stage_1_dir = join(melodicDir, 'glm_out')
        stage_1_maps = [join(stage_1_dir, x) for x in os.listdir(stage_1_dir) if x.startswith('znorm_{subject}_stage1'.format(subject = subject))]
        for stage_1_map in stage_1_maps:
            stage_2_out = join(melodicDir, 'glm_out', 'znorm_{subject}_stage2_{mmthreshImg}'.format(subject=subject, mmthreshImg=mmthreshImg))
            command = 'fsl_glm -i {subject_map} -d {stage_1_map} -o {stage_2_out}'.format(subject_map = subject_map, stage_1_map = stage_1_map, stage_2_out = stage_2_out)
            os.popen(command).read()


if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--melodicdir', '-md', nargs=1, type=str)
	parser.add_argument('--subject', '-s', nargs=1, type=str)
	args = parser.parse_args()

	zStats(args.melodicdir[0], args.subject[0])

	
