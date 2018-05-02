import re
import sys
import os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
from scipy import stats

def postMelodicGLM (subject, side, hemi, downsample, spatialsmooth):
    
    mni = 'mni_brain_${downsample}.nii.gz'.format(downsample=downsample)
    thal = 'masks/{hemi}_thalamus_HOSC_60_{downsample}.nii.gz'.format(hemi=hemi, downsample=downsample)  
    
    melodicDir='wmSC_ICA_mICA/{downsample}_{side}_{spatialsmooth}/dim0'.format(downsample=downsample, side=side, spatialsmooth=spatialsmooth)
    mmthreshDir = join(melodicDir, 'stats')
    
    subject_dir = join(subject, 'DualRegression_TensorICA')
    if not os.path.exists(subject_dir):
        print('\ creating subject_dir for ' + subject)
        os.mkdir(subject_dir)

    spatial = join(subject_dir, 'SpatialRegression_Stage1')
    if not os.path.exists(spatial):
        os.mkdir(spatial)
    
    pattern = join(subject_dir, 'wmSC_pattern')
    if not os.path.exists(pattern):
        os.mkdir(pattern)
    
    temporal = join(subject_dir, 'TemporalRegression_Stage2')
    if not os.path.exists(temporal):
        os.mkdir(temporal)
    
    subject_map_dir ='wmSC_ICA_mICA/{downsample}_{side}_{spatialsmooth}/masked_input'.format(downsample=downsample, side=side, spatialsmooth=spatialsmooth)
    log = 'subjects.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()
    line_no = subjects.index(subject)
    print(line_no)
    subject_map = join(subject_map_dir,'input_{line_no}_masked_s2.0.nii.gz'.format(line_no=line_no))
    #subject_map = join(subject_map_dir,'input_{line_no}_masked_s3.0.nii.gz'.format(line_no=line_no)) ## in "edit2_3_DTI_postmelodic.py" (script deleted)
    
    spatial_dir = join(spatial, '{downsample}_{side}_{spatialsmooth}'.format(downsample=downsample, side=side, spatialsmooth=spatialsmooth))
    if not os.path.exists(spatial_dir):
        print('\ creating spatial regression directory for ' + subject)
        os.mkdir(spatial_dir)

    pattern_dir = join(pattern, '{downsample}_{side}_{spatialsmooth}'.format(downsample=downsample, side=side, spatialsmooth=spatialsmooth))
    if not os.path.exists(pattern_dir):
        print('\ creating wmSC pattern directory for ' + subject)
        os.mkdir(pattern_dir)
    
    temporal_dir = join(temporal, '{downsample}_{side}_{spatialsmooth}'.format(downsample=downsample, side=side, spatialsmooth=spatialsmooth))
    if not os.path.exists(temporal_dir):
        print('\ creating temporal directory for ' + subject)
        os.mkdir(temporal_dir)

    mmthreshImgLoc = [join(mmthreshDir, x) for x in os.listdir(mmthreshDir) if x.startswith('thresh_zstat')]
    for mmthreshImgss in mmthreshImgLoc:
        mmthreshImgs = basename(mmthreshImgss)
        mmthreshImg = mmthreshImgs.split('.')[0]
            
#        stage_1 = join(spatial_dir, '{subject}_{mmthreshImg}_stage1'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(stage_1):
#            print(subject + 'running dual regression stage 1 for ' + mmthreshImg)
#            command = 'fsl_glm -i {subject_map} -d {mmthreshImgss} -m {thal} -o {stage_1}'.format(subject_map=subject_map, mmthreshImgss=mmthreshImgss, thal=thal, stage_1=stage_1)
#            os.popen(command).read()

#        pattern_stage_1 = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage1'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(pattern_stage_1):
#            print(subject + 'running dual regression stage 1 for wmSC pattern')
#            command = 'fsl_glm -i {subject_map} -d {mmthreshImgss} -o {pattern_stage_1}'.format(subject_map=subject_map, mmthreshImgss=mmthreshImgss, thal=thal, pattern_stage_1=pattern_stage_1)
#            os.popen(command).read()

        stage_1_demean = join(spatial_dir, '{subject}_{mmthreshImg}_stage1_demeaned'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(stage_1_demean):
            print(subject + 'running dual regression stage 1 demean for ' + mmthreshImg)
            command = 'fsl_glm -i {subject_map} -d {mmthreshImgss} -m {thal} -o {stage_1_demean} --demean'.format(subject_map=subject_map, mmthreshImgss=mmthreshImgss, thal=thal, stage_1_demean=stage_1_demean)
            os.popen(command).read()
        
        pattern_stage_1_demean = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage1_demeaned'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(pattern_stage_1_demean):
            print(subject + 'running dual regression stage 1 demean for wmSC pattern for ' + mmthreshImg)
            command = 'fsl_glm -i {subject_map} -d {mmthreshImgss} -o {pattern_stage_1_demean} --demean'.format(subject_map=subject_map, mmthreshImgss=mmthreshImgss, thal=thal, pattern_stage_1_demean=pattern_stage_1_demean)
            os.popen(command).read()
        

#        stage_2 = join(temporal_dir, '{subject}_{mmthreshImg}_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        z_stage_2 = join(temporal_dir, 'z_{subject}_{mmthreshImg}_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(z_stage_2):
#            print(subject + 'running glm stage 2 for ' + mmthreshImg)
#            input_d = stage_1
#            command = 'fsl_glm -i {subject_map} -d {input_d} -m {thal} -o {stage_2} --out_z={z_stage_2}'.format(subject_map=subject_map, input_d=input_d, thal=thal, stage_2=stage_2, z_stage_2=z_stage_2)
#            os.popen(command).read()

#        pattern_stage_2 = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        z_pattern_stage_2 = join(pattern_dir, 'z_{subject}_{mmthreshImg}_pattern_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(z_pattern_stage_2):
#            print(subject + 'running glm stage 2 for wmSC pattern')
#            input_d = pattern_stage_1
#            command = 'fsl_glm -i {subject_map} -d {input_d} -o {pattern_stage_2} --out_z={z_pattern_stage_2}'.format(subject_map=subject_map, input_d=input_d, thal=thal, pattern_stage_2=pattern_stage_2, z_pattern_stage_2=z_pattern_stage_2)
#            os.popen(command).read()
            
        stage_2_demean = join(temporal_dir, '{subject}_{mmthreshImg}_stage2_demeaned.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        z_stage_2_demean = join(temporal_dir, 'z_{subject}_{mmthreshImg}_stage2_demeaned.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(z_stage_2_demean):
            print(subject + 'running glm stage 2 demean for ' + mmthreshImg)
            input_d = stage_1_demean
            command = 'fsl_glm -i {subject_map} -d {input_d} -m {thal} -o {stage_2_demean} --out_z={z_stage_2_demean} --demean --des_norm'.format(subject_map=subject_map, input_d=input_d, thal=thal, stage_2_demean=stage_2_demean, z_stage_2_demean=z_stage_2_demean)
            os.popen(command).read()

        thresholded_output = join(temporal_dir, 'z2.3_{subject}_{mmthreshImg}_stage2_demeaned.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(thresholded_output):
            print(subject + 'thresholding dual regression output for ' + mmthreshImg)
            command = 'fslmaths {z_stage_2_demean} -thr 2.3 {thresholded_output}'.format(z_stage_2_demean=z_stage_2_demean, thresholded_output=thresholded_output)
            os.popen(command).read()

        pattern_stage_2_demean = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage2_demeaned.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        z_pattern_stage_2_demean = join(pattern_dir, 'z_{subject}_{mmthreshImg}_pattern_stage2_demeaned.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(z_pattern_stage_2_demean):
            print(subject + 'running glm stage 2 demean for wmSC pattern for ' + mmthreshImg)
            input_d = pattern_stage_1_demean
            command = 'fsl_glm -i {subject_map} -d {input_d} -o {pattern_stage_2_demean} --out_z={z_pattern_stage_2_demean} --demean --des_norm'.format(subject_map=subject_map, input_d=input_d, thal=thal, pattern_stage_2_demean=pattern_stage_2_demean, z_pattern_stage_2_demean=z_pattern_stage_2_demean)
            os.popen(command).read()

        thresholded_pattern = join(pattern_dir, 'z2.3_{subject}_{mmthreshImg}_pattern_stage2_demeaned.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(thresholded_pattern):
            print(subject + 'thresholding wmSC pattern for ' + mmthreshImg)
            command = 'fslmaths {z_pattern_stage_2_demean} -thr 2.3 {thresholded_pattern}'.format(z_pattern_stage_2_demean=z_pattern_stage_2_demean, thresholded_pattern=thresholded_pattern)
            os.popen(command).read()


def nosmoothPostMelodicGLM (subject, side, hemi, downsample):

    mni = 'mni_brain_${downsample}.nii.gz'.format(downsample=downsample)
    thal = 'masks/{hemi}_thalamus_HOSC_60_{downsample}.nii.gz'.format(hemi=hemi, downsample=downsample)  
    
    melodicDir='wmSC_ICA_mICA/{downsample}_{side}/dim0'.format(downsample=downsample, side=side)
    mmthreshDir = join(melodicDir, 'stats')
    
    subject_dir = join(subject, 'DualRegression_TensorICA')
    if not os.path.exists(subject_dir):
        print('\ creating subject_dir for ' + subject)
        os.mkdir(subject_dir)
    
    spatial = join(subject_dir, 'SpatialRegression_Stage1')
    if not os.path.exists(spatial):
        os.mkdir(spatial)
    
    pattern = join(subject_dir, 'wmSC_pattern')
    if not os.path.exists(pattern):
        os.mkdir(pattern)
    
    temporal = join(subject_dir, 'TemporalRegression_Stage2')
    if not os.path.exists(temporal):
        os.mkdir(temporal)
    
    subject_map = join(subject, 'Tractography/{side}/fdt_matrix2_reconstructed_{downsample}.nii.gz'.format(side=side, downsample=downsample))
    
    spatial_dir = join(spatial, '{downsample}_{side}_nosmooth'.format(downsample=downsample, side=side))
    if not os.path.exists(spatial_dir):
        print('\ creating spatial regression directory for ' + subject)
        os.mkdir(spatial_dir)

    pattern_dir = join(pattern, '{downsample}_{side}_nosmooth'.format(downsample=downsample, side=side))
    if not os.path.exists(pattern_dir):
        print('\ creating wmSC pattern directory for ' + subject)
        os.mkdir(pattern_dir)
    
    temporal_dir = join(temporal, '{downsample}_{side}_nosmooth'.format(downsample=downsample, side=side))
    if not os.path.exists(temporal_dir):
        print('\ creating temporal directory for ' + subject)
        os.mkdir(temporal_dir)

    mmthreshImgLoc = [join(mmthreshDir, x) for x in os.listdir(mmthreshDir) if x.startswith('thresh_zstat')]
    for mmthreshImgss in mmthreshImgLoc:
        mmthreshImgs = basename(mmthreshImgss)
        mmthreshImg = mmthreshImgs.split('.')[0]
            
#        stage_1 = join(spatial_dir, '{subject}_{mmthreshImg}_stage1'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(stage_1):
#            print(subject + 'running dual regression stage 1 for ' + mmthreshImg)
#            command = 'fsl_glm -i {subject_map} -d {mmthreshImgss} -m {thal} -o {stage_1}'.format(subject_map=subject_map, mmthreshImgss=mmthreshImgss, thal=thal, stage_1=stage_1)
#            os.popen(command).read()

#        pattern_stage_1 = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage1'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(pattern_stage_1):
#            print(subject + 'running dual regression stage 1 for wmSC pattern')
#            command = 'fsl_glm -i {subject_map} -d {mmthreshImgss} -o {pattern_stage_1}'.format(subject_map=subject_map, mmthreshImgss=mmthreshImgss, thal=thal, pattern_stage_1=pattern_stage_1)
#            os.popen(command).read()

        stage_1_demean = join(spatial_dir, '{subject}_{mmthreshImg}_stage1_demeaned'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(stage_1_demean):
            print(subject + 'running dual regression stage 1 demean for ' + mmthreshImg)
            command = 'fsl_glm -i {subject_map} -d {mmthreshImgss} -m {thal} -o {stage_1_demean} --demean'.format(subject_map=subject_map, mmthreshImgss=mmthreshImgss, thal=thal, stage_1_demean=stage_1_demean)
            os.popen(command).read()
        
        pattern_stage_1_demean = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage1_demeaned'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(pattern_stage_1_demean):
            print(subject + 'running dual regression stage 1 demean for wmSC pattern for ' + mmthreshImg)
            command = 'fsl_glm -i {subject_map} -d {mmthreshImgss} -o {pattern_stage_1_demean} --demean'.format(subject_map=subject_map, mmthreshImgss=mmthreshImgss, thal=thal, pattern_stage_1_demean=pattern_stage_1_demean)
            os.popen(command).read()
        

#        stage_2 = join(temporal_dir, '{subject}_{mmthreshImg}_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        z_stage_2 = join(temporal_dir, 'z_{subject}_{mmthreshImg}_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(z_stage_2):
#            print(subject + 'running glm stage 2 for ' + mmthreshImg)
#            input_d = stage_1
#            command = 'fsl_glm -i {subject_map} -d {input_d} -m {thal} -o {stage_2} --out_z={z_stage_2}'.format(subject_map=subject_map, input_d=input_d, thal=thal, stage_2=stage_2, z_stage_2=z_stage_2)
#            os.popen(command).read()

#        pattern_stage_2 = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        z_pattern_stage_2 = join(pattern_dir, 'z_{subject}_{mmthreshImg}_pattern_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(z_pattern_stage_2):
#            print(subject + 'running glm stage 2 for wmSC pattern')
#            input_d = pattern_stage_1
#            command = 'fsl_glm -i {subject_map} -d {input_d} -o {pattern_stage_2} --out_z={z_pattern_stage_2}'.format(subject_map=subject_map, input_d=input_d, thal=thal, pattern_stage_2=pattern_stage_2, z_pattern_stage_2=z_pattern_stage_2)
#            os.popen(command).read()
            
        stage_2_demean = join(temporal_dir, '{subject}_{mmthreshImg}_stage2_demeaned.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        z_stage_2_demean = join(temporal_dir, 'z_{subject}_{mmthreshImg}_stage2_demeaned.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(z_stage_2_demean):
            print(subject + 'running glm stage 2 demean for ' + mmthreshImg)
            input_d = stage_1_demean
            command = 'fsl_glm -i {subject_map} -d {input_d} -m {thal} -o {stage_2_demean} --out_z={z_stage_2_demean} --demean --des_norm'.format(subject_map=subject_map, input_d=input_d, thal=thal, stage_2_demean=stage_2_demean, z_stage_2_demean=z_stage_2_demean)
            os.popen(command).read()

        thresholded_output = join(temporal_dir, 'z2.3_{subject}_{mmthreshImg}_stage2_demeaned.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(thresholded_output):
            print(subject + 'thresholding dual regression output for ' + mmthreshImg)
            command = 'fslmaths {z_stage_2_demean} -thr 2.3 {thresholded_output}'.format(z_stage_2_demean=z_stage_2_demean, thresholded_output=thresholded_output)
            os.popen(command).read()
        
        pattern_stage_2_demean = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage2_demeaned.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        z_pattern_stage_2_demean = join(pattern_dir, 'z_{subject}_{mmthreshImg}_pattern_stage2_demeaned.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(z_pattern_stage_2_demean):
            print(subject + 'running glm stage 2 demean for wmSC pattern for ' + mmthreshImg)
            input_d = pattern_stage_1_demean
            command = 'fsl_glm -i {subject_map} -d {input_d} -o {pattern_stage_2_demean} --out_z={z_pattern_stage_2_demean} --demean --des_norm'.format(subject_map=subject_map, input_d=input_d, thal=thal, pattern_stage_2_demean=pattern_stage_2_demean, z_pattern_stage_2_demean=z_pattern_stage_2_demean)
            os.popen(command).read()

        thresholded_pattern = join(pattern_dir, 'z2.3_{subject}_{mmthreshImg}_pattern_stage2_demeaned.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(thresholded_pattern):
            print(subject + 'thresholding wmSC pattern for ' + mmthreshImg)
            command = 'fslmaths {z_pattern_stage_2_demean} -thr 2.3 {thresholded_pattern}'.format(z_pattern_stage_2_demean=z_pattern_stage_2_demean, thresholded_pattern=thresholded_pattern)
            os.popen(command).read()



    



if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--subject', '-subj', nargs=1, type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--hemi', '-hemi', nargs=1, help = 'lh or rh', type=str)
	parser.add_argument('--downsample', '-ds', nargs=1,  help = 'e.g., ds3; none if no downsampling', type=str)
	parser.add_argument('--spatialsmooth', '-fwhm', nargs=1,  help = 'e.g., fwhm4; none if no downsampling', type=str)
	args = parser.parse_args()

        postMelodicGLM(args.subject[0], args.side[0], args.hemi[0], args.downsample[0], args.spatialsmooth[0])
        #nosmoothPostMelodicGLM(args.subject[0], args.side[0], args.hemi[0], args.downsample[0])

