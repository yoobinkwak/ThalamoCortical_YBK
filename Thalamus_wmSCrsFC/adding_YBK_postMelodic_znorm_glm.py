import re
import sys
import os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
from scipy import stats


def zStats (side, hemi,  downsample, subject):

    melodicDir='tica_results/mICA_HCvsFEP_{side}{downsample}/dim0'.format(side=side, downsample=downsample)
    mmthreshDir = join(melodicDir, 'stats')
    mmthreshImgss = [join(mmthreshDir, x) for x in os.listdir(mmthreshDir) if x.startswith('thresh_zstat')]
    for mmthreshImgLoc in mmthreshImgss:
        mmthreshImgs = basename(mmthreshImgLoc)
        mmthreshImg = mmthreshImgs.split('.')[0]

        glm_dir = join(melodicDir, 'glm_out')
	stage_1_output = join(glm_dir, 'znorm_{subject}_stage1_{mmthreshImg}').format(subject=subject, mmthreshImg=mmthreshImg)
        if not os.path.isfile(stage_1_output):
            print('\tz-normalizing mmthrehsolded individual IC stage 1 output')
            fsl_reg_out = join(glm_dir, '{subject}_stage1_{mmthreshImg}'.format(subject=subject, mmthreshImg=mmthreshImg))
	    fsl_glm_mat = np.loadtxt(fsl_reg_out)
	    fsl_glm_mat_z = stats.zscore(fsl_glm_mat)
	    np.savetxt(stage_1_output, fsl_glm_mat_z)
        else:
            print('\tz-normalized mmthresholded individual IC stage 1 output')

        melodicIC_on_thal = join(glm_dir, '{subject}_stage1').format(subject=subject)
        znorm_melodicIC_on_thal = join(glm_dir, 'znorm_{subject}_stage1').format(subject=subject)
        if not os.path.isfile(znorm_melodicIC_on_thal):
            print('\tz-normalizing melodic_IC stage 1 output')
            glm_mat = np.loadtxt(melodicIC_on_thal)
            glm_mat_z = stats.zscore(glm_mat)
            np.savetxt(znorm_melodicIC_on_thal, glm_mat_z)
        else:
            print('\tz-normalized melodic_IC stage 1 output')

        stage_2_out = join(glm_dir, 'znorm_{subject}_stage2_{mmthreshImg}.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.isfile(stage_2_out):
            print('\trunning stage 2 with  z-normalized mmthresholded individual IC')
            subject_map = '{subject}/YB*/{side}/fdt_matrix2_reconstructed{downsample}.nii.gz'.format(side=side, subject=subject, downsample=downsample)
            stage_1_maps = [join(glm_dir, x) for x in os.listdir(glm_dir) if x.startswith('znorm_{subject}_stage1'.format(subject = subject))]
            for stage_1_map in stage_1_maps:
                command = 'fsl_glm -i {subject_map} -d {stage_1_map} -m /Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/{hemi}_thalamus_HOSC_60{downsample}.nii.gz -o {stage_2_out}'.format(subject_map = subject_map, stage_1_map = stage_1_map, hemi = hemi, downsample = downsample, stage_2_out = stage_2_out)
                os.popen(command).read()
        else:
            print('\tcompleted stage 2 with z-normalized mmthresholded individual IC')

        stage_2_znorm_melodicIC = join(glm_dir, 'znorm_{subject}_stage2.nii.gz'.format(subject=subject))
        if not os.path.isfile(stage_2_znorm_melodicIC):
            print('\trunning stage 2 with z-normalized melodic_IC')
            subject_map = '{subject}/YB*/{side}/fdt_matrix2_reconstructed{downsample}.nii.gz'.format(side=side, subject=subject, downsample=downsample)
            stage2_mat = join(glm_dir, 'znorm_{subject}_stage1').format(subject=subject)
            command = 'fsl_glm -i {subject_map} -d {stage2_mat} -m /Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/{hemi}_thalamus_HOSC_60{downsample}.nii.gz -o {stage_2_znorm_melodicIC}'.format(subject_map = subject_map, stage2_mat=stage2_mat, stage_2_znorm_melodicIC = stage_2_znorm_melodicIC,  hemi = hemi, downsample = downsample)
            os.popen(command).read()
        else:
            print('\tcompleted stage 2 with z-normalized melodic_IC')


if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--downsample', '-ds', nargs=1,  help = 'e.g., _ds3; none if no downsampling', type=str)
	parser.add_argument('--subject', '-subj', nargs=1, type=str)
	args = parser.parse_args()

        #if args.side == 'left':
        #    hemi = 'lh'
        #elif args.side == 'right':
        #    hemi = 'rh'
        get_hemi = lambda x: 'lh' if x == 'left' else 'rh' 
        hemi = get_hemi(args.side)

        if args.downsample == 'none':
            downsample = lambda : ''.join(' ' for _ in xrange(1))
            
        zStats(args.side[0], hemi, args.downsample[0], args.subject[0])
