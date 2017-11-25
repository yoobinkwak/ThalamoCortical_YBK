import re
import sys
import os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
from scipy import stats

def postMelodicGLM (subject, side, hemi, downsample):
    
    mni = 'mni${downsample}.nii.gz'.format(downsample=downsample)
    thal = '{hemi}_thalamus_HOSC_60{downsample}.nii.gz'.format(hemi=hemi, downsample=downsample)  
    
    melodicDir='tica_results/mICA_FEPvsCHRvsHC_{side}{downsample}/dim0'.format(side=side, downsample=downsample)
    mmthreshDir = join(melodicDir, 'stats')
    
    subject_dir = join(subject, '34FEP68CHR69HC')
    if not os.path.exists(subject_dir):
        print('\ creating subject_dir for ' + subject)
        os.mkdir(subject_dir)
        
    subject_map = join(subject, 'YB_wb_thalamus_tractography/{side}/fdt_matrix2_reconstructed{downsample}.nii.gz'.format(side=side, downsample=downsample))
    
    mICA_dr = join(subject_dir, '{side}{downsample}_mICA_dual_regression'.format(side=side, downsample=downsample))
    if not os.path.exists(mICA_dr):
        print('\ creating mICA_dual_regression for ' + subject)
        os.mkdir(mICA_dr)

    mmthreshImgLoc = [join(mmthreshDir, x) for x in os.listdir(mmthreshDir) if x.startswith('thresh_zstat')]
    for mmthreshImgss in mmthreshImgLoc:
        mmthreshImgs = basename(mmthreshImgss)
        mmthreshImg = mmthreshImgs.split('.')[0]
            
        stage_1 = join(mICA_dr, '{subject}_{mmthreshImg}_stage1'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(stage_1):
            print(subject + 'running glm stage 1 for ' + mmthreshImg)
            print(subject_map)
            print(mmthreshImgss)
            print(thal)
            print(stage_1)
            command = 'fsl_glm -i {subject_map} -d {mmthreshImgss} -m {thal} -o {stage_1}'.format(subject_map=subject_map, mmthreshImgss=mmthreshImgss, thal=thal, stage_1=stage_1)
            os.popen(command).read()

        znorm_stage_1 = join(mICA_dr, 'znorm_{subject}_{mmthreshImg}_stage1'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(znorm_stage_1):
            print(subject + 'running z normalization on stage 1 output for ' + mmthreshImg)
            fsl_reg_out = stage_1
            fsl_glm_mat = np.loadtxt(fsl_reg_out)
            fsl_glm_mat_z = stats.zscore(fsl_glm_mat)
            np.savetxt(znorm_stage_1, fsl_glm_mat_z)
        
        stage_2 = join(mICA_dr, '{subject}_{mmthreshImg}_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(stage_2):
            print(subject + 'running glm stage 2 for ' + mmthreshImg)
            input_d = stage_1
            command = 'fsl_glm -i {subject_map} -d {input_d} -m {thal} -o {stage_2}'.format(subject_map=subject_map, input_d=input_d, thal=thal, stage_2=stage_2)
            os.popen(command).read()
            
        znorm_stage_2 = join(mICA_dr, 'znorm_{subject}_{mmthreshImg}_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(znorm_stage_2):
            print(subject + 'running glm stage 2 for z normalized' + mmthreshImg)
            znorm_input_d = znorm_stage_1
            command = 'fsl_glm -i {subject_map} -d {znorm_input_d} -m {thal} -o {znorm_stage_2}'.format(subject_map=subject_map, znorm_input_d=znorm_input_d, thal=thal, znorm_stage_2=znorm_stage_2)
            os.popen(command).read()






if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--subject', '-subj', nargs=1, type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--hemi', '-hemi', nargs=1, help = 'lh or rh', type=str)
	parser.add_argument('--downsample', '-ds', nargs=1,  help = 'e.g., _ds3; none if no downsampling', type=str)
	args = parser.parse_args()

        postMelodicGLM(args.subject[0], args.side[0], args.hemi[0], args.downsample[0])

