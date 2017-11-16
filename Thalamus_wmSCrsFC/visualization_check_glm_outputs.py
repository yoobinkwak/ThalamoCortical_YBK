import os
import sys
import re
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np


def overlay(mICA, hemi, subject):
    
    mniLoc = '/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/mni_ds3.nii.gz'
    mni = nb.load(mniLoc)
    mni_data = mni.get_data()
    thalamusLoc = '/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/{hemi}_thalamus_HOSC_60_ds3.nii.gz'.format(hemi=hemi)
    thalamus = nb.load(thalamusLoc)
    thalData = thalamus.get_data()

    glm_dir = join (mICA, 'dim0/glm_out')
    vis_dir = join(glm_dir, 'visualization')
    if not os.path.exists(vis_dir):
        os.makedirs(vis_dir)

    inputs_noZnorm = [join(glm_dir, x) for x in os.listdir(glm_dir) if x.startswith('{subject}_stage2_thresh_zstat'.format(subject = subject)) and x.endswith('.nii.gz')]
    for input_noZnorm in inputs_noZnorm:
        img_noZnorm = basename(input_noZnorm)
        name_noZnorm = img_noZnorm.split('.')[0]
        overlayOut = join(vis_dir, 'overlay_{name_noZnorm}.nii.gz').format(name_noZnorm=name_noZnorm)
        slicerOut = join(vis_dir, 'slicer_{name_noZnorm}.ppm').format(name_noZnorm=name_noZnorm)
        pngOut = join(vis_dir, 'sliced_{name_noZnorm}.png').format(name_noZnorm=name_noZnorm)
        if not isfile(pngOut):
            command = 'overlay 1 0 {thalamus} -A {input_noZnorm} 2.5 10 {overlayOut}'.format(thalamus=thalamus, input_noZnorm=input_noZnorm, overlayOut = overlayOut)
            os.popen(command).read()
            command = 'slicer {overlayOut} -A 1200 {slicerOut}'.format(overlayOut = overlayOut, slicerOut = slicerOut)
            os.popen(command).read()
            command = 'convert {slicerOut} {pngOut}'.format(slicerOut = slicerOut, pngOut = pngOut)
            os.popen(command).read()



    inputs_Znorm = [join(glm_dir, x) for x in os.listdir(glm_dir) if x.startswith('znorm_{subject}_stage2_thresh_zstat'.format(subject = subject)) and x.endswith('.nii.gz')]
    for input_Znorm in inputs_Znorm:
        img_Znorm = basename(input_Znorm)
        name_Znorm = img_Znorm.split('.')[0]
        overlay_out = join(vis_dir, 'overlay_{name_Znorm}.nii.gz').format(name_Znorm=name_Znorm)
        slicer_out = join(vis_dir, 'slicer_{name_Znorm}.ppm').format(name_Znorm=name_Znorm)
        png_out = join(vis_dir, 'sliced_{name_Znorm}.png').format(name_Znorm=name_Znorm)
        if not isfile(png_out):
            command = 'overlay 1 0 {thalamus} -A {input_Znorm} 2.5 10 {overlay_out}'.format(thalamus=thalamus, input_Znorm=input_Znorm, overlay_out = overlay_out)
            os.popen(command).read()
            command = 'slicer {overlay_out} -A 1200 {slicer_out}'.format(overlay_out = overlay_out, slicer_out = slicer_out)
            os.popen(command).read()
            command = 'convert {slicer_out} {png_out}'.format(slicer_out = slicer_out, png_out = png_out)
            os.popen(command).read()










if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--mICA', '-mica', nargs=1, help = 'mICA directory', type=str)
	parser.add_argument('--hemi', '-hemi', nargs=1, help = 'lh  or rh', type=str)
	parser.add_argument('--subject', '-subj', nargs=1, type=str)
	args = parser.parse_args()

	overlay(args.mICA[0], args.hemi[0],  args.subject[0])
