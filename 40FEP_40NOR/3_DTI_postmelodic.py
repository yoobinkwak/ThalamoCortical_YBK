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
    
    
    out_dir = join(subject, 'Dual_Regression')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    subject_dir = join(out_dir, 'TensorICA')
    if not os.path.exists(subject_dir):
        os.mkdir(subject_dir)

    specific_dir = join(subject_dir, '{downsample}_{side}_{spatialsmooth}'.format(downsample=downsample, side=side, spatialsmooth=spatialsmooth))
    if not os.path.exists(specific_dir):
        os.mkdir(specific_dir)

    spatial_dir = join(specific_dir, 'SpatialRegression_Stage1')
    if not os.path.exists(spatial_dir):
        os.mkdir(spatial_dir)
    
    pattern_dir = join(specific_dir, 'wmSC_pattern')
    if not os.path.exists(pattern_dir):
        os.mkdir(pattern_dir)
    
    temporal_dir = join(specific_dir, 'TemporalRegression_Stage2')
    if not os.path.exists(temporal_dir):
        os.mkdir(temporal_dir)
   
    
    subject_map_dir = '/home/yoobinkwak/mICA_masked_inputs/40FEP_40NOR/{downsample}_{side}_{spatialsmooth}/masked_input'.format(downsample=downsample, side=side, spatialsmooth=spatialsmooth)

    log = 'subjects.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()
    line_no = subjects.index(subject)
    #print(line_no)
    ##subject_map = join(subject_map_dir,'input_{line_no}_masked_s2.0.nii.gz'.format(line_no=line_no)) ## for fwhm4
    subject_map = join(subject_map_dir,'input_{line_no}_masked_s3.0.nii.gz'.format(line_no=line_no))
    
    
    melodicDir='wmSC_ICA_mICA/{downsample}_{side}_{spatialsmooth}/dim0'.format(downsample=downsample, side=side, spatialsmooth=spatialsmooth)
    mmthreshDir = join(melodicDir, 'stats')

    mmthreshImgLoc = [join(mmthreshDir, x) for x in os.listdir(mmthreshDir) if x.startswith('thresh_zstat')]
    for mmthreshImgss in mmthreshImgLoc:
        mmthreshImgs = basename(mmthreshImgss)
        mmthreshImg = mmthreshImgs.split('.')[0]
            
        stage_1_demean = join(spatial_dir, '{subject}_{mmthreshImg}_stage1.txt'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(stage_1_demean):
            print(subject + 'running dual regression stage 1 for ' + mmthreshImg)
            command = 'fsl_glm -i {subject_map} -d {mmthreshImgss} -m {thal} -o {stage_1_demean} --demean'.format(subject_map=subject_map, mmthreshImgss=mmthreshImgss, thal=thal, stage_1_demean=stage_1_demean)
            os.popen(command).read()
       
        stage_2_demean = join(temporal_dir, '{subject}_{mmthreshImg}_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        z_stage_2_demean = join(temporal_dir, 'z_{subject}_{mmthreshImg}_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(z_stage_2_demean):
            print(subject + 'running dual regression stage 2 for ' + mmthreshImg)
            input_d = stage_1_demean
            command = 'fsl_glm -i {subject_map} -d {input_d} -m {thal} -o {stage_2_demean} --out_z={z_stage_2_demean} --demean'.format(subject_map=subject_map, input_d=input_d, thal=thal, stage_2_demean=stage_2_demean, z_stage_2_demean=z_stage_2_demean)
            os.popen(command).read()

        stage_2_desnorm = join(temporal_dir, '{subject}_{mmthreshImg}_stage2_desnorm.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        z_stage_2_desnorm = join(temporal_dir, 'z_{subject}_{mmthreshImg}_stage2_desnorm.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(z_stage_2_desnorm):
            print(subject + 'running dual regression stage 2 des_norm for ' + mmthreshImg)
            input_d = stage_1_demean
            command = 'fsl_glm -i {subject_map} -d {input_d} -m {thal} -o {stage_2_desnorm} --out_z={z_stage_2_desnorm} --demean --des_norm'.format(subject_map=subject_map, input_d=input_d, thal=thal, stage_2_desnorm=stage_2_desnorm, z_stage_2_desnorm=z_stage_2_desnorm)
            os.popen(command).read()

        thresholded_output = join(temporal_dir, 'z2.3_{subject}_{mmthreshImg}_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(thresholded_output):
            print(subject + 'thresholding dual regression output for ' + mmthreshImg)
            command = 'fslmaths {z_stage_2_demean} -thr 2.3 {thresholded_output}'.format(z_stage_2_demean=z_stage_2_demean, thresholded_output=thresholded_output)
            os.popen(command).read()

        thresholded_desnorm_output = join(temporal_dir, 'z2.3_{subject}_{mmthreshImg}_stage2_desnorm.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(thresholded_desnorm_output):
            print(subject + 'thresholding dual regression des_norm output for ' + mmthreshImg)
            command = 'fslmaths {z_stage_2_desnorm} -thr 2.3 {thresholded_desnorm_output}'.format(z_stage_2_desnorm=z_stage_2_desnorm, thresholded_desnorm_output=thresholded_desnorm_output)
            os.popen(command).read()

        
#        pattern_stage_1_demean = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage1.txt'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(pattern_stage_1_demean):
#            print(subject + 'running dual regression stage 1 for wmSC pattern for ' + mmthreshImg)
#            command = 'fsl_glm -i {subject_map} -d {mmthreshImgss} -o {pattern_stage_1_demean} --demean'.format(subject_map=subject_map, mmthreshImgss=mmthreshImgss, thal=thal, pattern_stage_1_demean=pattern_stage_1_demean)
#            os.popen(command).read()
#        
#        pattern_stage_2_demean = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        z_pattern_stage_2_demean = join(pattern_dir, 'z_{subject}_{mmthreshImg}_pattern_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(z_pattern_stage_2_demean):
#            print(subject + 'running dual regression stage 2 for wmSC pattern for ' + mmthreshImg)
#            input_d = pattern_stage_1_demean
#            command = 'fsl_glm -i {subject_map} -d {input_d} -o {pattern_stage_2_demean} --out_z={z_pattern_stage_2_demean} --demean'.format(subject_map=subject_map, input_d=input_d, thal=thal, pattern_stage_2_demean=pattern_stage_2_demean, z_pattern_stage_2_demean=z_pattern_stage_2_demean)
#            os.popen(command).read()
#
#        pattern_stage_2_desnorm = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        z_pattern_stage_2_desnorm = join(pattern_dir, 'z_{subject}_{mmthreshImg}_pattern_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(z_pattern_stage_2_desnorm):
#            print(subject + 'running dual regression stage 2 for wmSC pattern des_norm for ' + mmthreshImg)
#            input_d = pattern_stage_1_demean
#            command = 'fsl_glm -i {subject_map} -d {input_d} -o {pattern_stage_2_desnorm} --out_z={z_pattern_stage_2_desnorm} --demean --des_norm'.format(subject_map=subject_map, input_d=input_d, thal=thal, pattern_stage_2_desnorm=pattern_stage_2_desnorm, z_pattern_stage_2_desnorm=z_pattern_stage_2_desnorm)
#            os.popen(command).read()




def nosmoothPostMelodicGLM (subject, side, hemi, downsample):

    mni = 'mni_brain_${downsample}.nii.gz'.format(downsample=downsample)
    thal = 'masks/{hemi}_thalamus_HOSC_60_{downsample}.nii.gz'.format(hemi=hemi, downsample=downsample)  
   
    out_dir = join(subject, 'Dual_Regression')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    subject_dir = join(out_dir, 'TensorICA')
    if not os.path.exists(subject_dir):
        os.mkdir(subject_dir)

    specific_dir = join(subject_dir, '{downsample}_{side}_nosmooth'.format(downsample=downsample, side=side))
    if not os.path.exists(specific_dir):
        os.mkdir(specific_dir)

    spatial_dir = join(specific_dir, 'SpatialRegression_Stage1')
    if not os.path.exists(spatial_dir):
        os.mkdir(spatial_dir)
    
    pattern_dir = join(specific_dir, 'wmSC_pattern')
    if not os.path.exists(pattern_dir):
        os.mkdir(pattern_dir)
    
    temporal_dir = join(specific_dir, 'TemporalRegression_Stage2')
    if not os.path.exists(temporal_dir):
        os.mkdir(temporal_dir)

    
    subject_map = join(subject, 'Tractography/{side}/fdt_matrix2_reconstructed_{downsample}.nii.gz'.format(side=side, downsample=downsample))
    
    melodicDir='wmSC_ICA_mICA/{downsample}_{side}/dim0'.format(downsample=downsample, side=side)
    mmthreshDir = join(melodicDir, 'stats')

    mmthreshImgLoc = [join(mmthreshDir, x) for x in os.listdir(mmthreshDir) if x.startswith('thresh_zstat')]
    for mmthreshImgss in mmthreshImgLoc:
        mmthreshImgs = basename(mmthreshImgss)
        mmthreshImg = mmthreshImgs.split('.')[0]
          


        stage_1_demean = join(spatial_dir, '{subject}_{mmthreshImg}_stage1.txt'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(stage_1_demean):
            print(subject + 'running dual regression stage 1 for ' + mmthreshImg + 'nosmooth')
            command = 'fsl_glm -i {subject_map} -d {mmthreshImgss} -m {thal} -o {stage_1_demean} --demean'.format(subject_map=subject_map, mmthreshImgss=mmthreshImgss, thal=thal, stage_1_demean=stage_1_demean)
            os.popen(command).read()
       
        stage_2_demean = join(temporal_dir, '{subject}_{mmthreshImg}_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        z_stage_2_demean = join(temporal_dir, 'z_{subject}_{mmthreshImg}_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(z_stage_2_demean):
            print(subject + 'running dual regression stage 2 for ' + mmthreshImg + 'nosmooth')
            input_d = stage_1_demean
            command = 'fsl_glm -i {subject_map} -d {input_d} -m {thal} -o {stage_2_demean} --out_z={z_stage_2_demean} --demean'.format(subject_map=subject_map, input_d=input_d, thal=thal, stage_2_demean=stage_2_demean, z_stage_2_demean=z_stage_2_demean)
            os.popen(command).read()

        stage_2_desnorm = join(temporal_dir, '{subject}_{mmthreshImg}_stage2_desnorm.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        z_stage_2_desnorm = join(temporal_dir, 'z_{subject}_{mmthreshImg}_stage2_desnorm.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(z_stage_2_desnorm):
            print(subject + 'running dual regression stage 2 des_norm for ' + mmthreshImg + 'nosmooth')
            input_d = stage_1_demean
            command = 'fsl_glm -i {subject_map} -d {input_d} -m {thal} -o {stage_2_desnorm} --out_z={z_stage_2_desnorm} --demean --des_norm'.format(subject_map=subject_map, input_d=input_d, thal=thal, stage_2_desnorm=stage_2_desnorm, z_stage_2_desnorm=z_stage_2_desnorm)
            os.popen(command).read()

        thresholded_output = join(temporal_dir, 'z2.3_{subject}_{mmthreshImg}_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(thresholded_output):
            print(subject + 'thresholding dual regression output for ' + mmthreshImg + 'nosmooth')
            command = 'fslmaths {z_stage_2_demean} -thr 2.3 {thresholded_output}'.format(z_stage_2_demean=z_stage_2_demean, thresholded_output=thresholded_output)
            os.popen(command).read()

        thresholded_desnorm_output = join(temporal_dir, 'z2.3_{subject}_{mmthreshImg}_stage2_desnorm.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
        if not os.path.exists(thresholded_desnorm_output):
            print(subject + 'thresholding dual regression des_norm output for ' + mmthreshImg + 'nosmooth')
            command = 'fslmaths {z_stage_2_desnorm} -thr 2.3 {thresholded_desnorm_output}'.format(z_stage_2_desnorm=z_stage_2_desnorm, thresholded_desnorm_output=thresholded_desnorm_output)
            os.popen(command).read()

        
#        pattern_stage_1_demean = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage1.txt'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(pattern_stage_1_demean):
#            print(subject + 'running dual regression stage 1 for wmSC pattern for ' + mmthreshImg + 'nosmooth')
#            command = 'fsl_glm -i {subject_map} -d {mmthreshImgss} -o {pattern_stage_1_demean} --demean'.format(subject_map=subject_map, mmthreshImgss=mmthreshImgss, thal=thal, pattern_stage_1_demean=pattern_stage_1_demean)
#            os.popen(command).read()
#        
#        pattern_stage_2_demean = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        z_pattern_stage_2_demean = join(pattern_dir, 'z_{subject}_{mmthreshImg}_pattern_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(z_pattern_stage_2_demean):
#            print(subject + 'running dual regression stage 2 for wmSC pattern for ' + mmthreshImg + 'nosmooth')
#            input_d = pattern_stage_1_demean
#            command = 'fsl_glm -i {subject_map} -d {input_d} -o {pattern_stage_2_demean} --out_z={z_pattern_stage_2_demean} --demean'.format(subject_map=subject_map, input_d=input_d, thal=thal, pattern_stage_2_demean=pattern_stage_2_demean, z_pattern_stage_2_demean=z_pattern_stage_2_demean)
#            os.popen(command).read()
#
#        pattern_stage_2_desnorm = join(pattern_dir, '{subject}_{mmthreshImg}_pattern_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        z_pattern_stage_2_desnorm = join(pattern_dir, 'z_{subject}_{mmthreshImg}_pattern_stage2.nii.gz'.format(subject=subject, mmthreshImg=mmthreshImg))
#        if not os.path.exists(z_pattern_stage_2_desnorm):
#            print(subject + 'running dual regression stage 2 for wmSC pattern des_norm for ' + mmthreshImg + 'nosmooth')
#            input_d = pattern_stage_1_demean
#            command = 'fsl_glm -i {subject_map} -d {input_d} -o {pattern_stage_2_desnorm} --out_z={z_pattern_stage_2_desnorm} --demean --des_norm'.format(subject_map=subject_map, input_d=input_d, thal=thal, pattern_stage_2_desnorm=pattern_stage_2_desnorm, z_pattern_stage_2_desnorm=z_pattern_stage_2_desnorm)
#            os.popen(command).read()







if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--subject', '-subj', nargs=1, type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--hemi', '-hemi', nargs=1, help = 'lh or rh', type=str)
	parser.add_argument('--downsample', '-ds', nargs=1,  help = 'e.g., ds3; none if no downsampling', type=str)
	parser.add_argument('--spatialsmooth', '-fwhm', nargs=1,  help = 'e.g., fwhm4; none if no downsampling', type=str)
	args = parser.parse_args()

        postMelodicGLM(args.subject[0], args.side[0], args.hemi[0], args.downsample[0], args.spatialsmooth[0])
        nosmoothPostMelodicGLM(args.subject[0], args.side[0], args.hemi[0], args.downsample[0])

