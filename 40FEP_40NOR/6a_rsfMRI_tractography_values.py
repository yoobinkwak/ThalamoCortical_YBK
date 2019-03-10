import os 
import re
import sys
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import pandas as pd


def fdt_normalize(voxelsize, side, smoothing, IC):
    
    log = 'subjects.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()

    for subject in subjects:
        dataLoc = '{subject}/rsFC_seed_tractography/{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(subject=subject, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
        dataDirs = [ x for x in os.listdir(dataLoc) if '_demeaned_' in x]
        for dataDir in dataDirs:
            dataFile = '{dataLoc}/{dataDir}/fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            waytotal = '{dataLoc}/{dataDir}/waytotal'.format(dataLoc=dataLoc, dataDir=dataDir)

            if not os.path.isfile('{dataLoc}/{dataDir}/thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)):
                val = int(open('{}'.format(waytotal), 'r').read().replace('/n', '').replace(' ', ''))
                command = 'fslmaths {0} {1} {2} {3}'.format(dataFile, '-div', val, '{dataLoc}/{dataDir}/norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir))
                command_mask = 'fslmaths {0} {1} {2} {3}'.format(dataFile, '-div', val, '-bin {dataLoc}/{dataDir}/norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir))
                os.popen(command).read
                os.popen(command_mask).read

                ##### adding "-thrp 3" seems to render same results as not adding the option for some files...?
                command_thr = 'fslmaths {0} {1} {2} {3}'.format(dataFile, '-div', val, '-thrp 3 {dataLoc}/{dataDir}/thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir))
                command_thr_mask = 'fslmaths {0} {1} {2} {3}'.format(dataFile, '-div', val, '-thrp 3 -bin {dataLoc}/{dataDir}/thr_norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir))
                os.popen(command_thr).read
                os.popen(command_thr_mask).read
                

def registration(voxelsize, side, smoothing, IC):
    
    log = 'subjects.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()

    for subject in subjects:
        dataLoc = '{subject}/rsFC_seed_tractography/{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(subject=subject, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
        dataDirs = [ x for x in os.listdir(dataLoc) if '_demeaned_' in x]
        for dataDir in dataDirs:
           
            reg_normFA = '{dataLoc}/{dataDir}/reg_FA_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            reg_thrFA = '{dataLoc}/{dataDir}/reg_FA_thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            reg_normMD = '{dataLoc}/{dataDir}/reg_MD_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            reg_thrMD = '{dataLoc}/{dataDir}/reg_MD_thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            
            if not os.path.isfile(reg_normFA):
                norm_mask = '{dataLoc}/{dataDir}/norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                thr_mask = '{dataLoc}/{dataDir}/thr_norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                FA ='{subject}/DTI/dti_FA.nii.gz'.format(subject=subject)
                MD ='{subject}/DTI/dti_MD.nii.gz'.format(subject=subject)
                warp='{subject}/DTI/Registration/mni2reorient_t1w2nodif_coeff.nii.gz'.format(subject=subject)

                command_normFA = 'applywarp -i {0} -r {1} -w {2} -o {3}'.format(norm_mask, FA, warp, reg_normFA)
                command_thrFA = 'applywarp -i {0} -r {1} -w {2} -o {3}'.format(thr_mask, FA, warp, reg_thrFA)
                command_normMD = 'applywarp -i {0} -r {1} -w {2} -o {3}'.format(norm_mask, MD, warp, reg_normMD)
                command_thrMD = 'applywarp -i {0} -r {1} -w {2} -o {3}'.format(thr_mask, MD, warp, reg_thrMD)

                os.popen(command_normFA).read
                os.popen(command_thrFA).read
                os.popen(command_normMD).read
                os.popen(command_thrMD).read



def extract_tract(voxelsize, side, smoothing, IC):

    log = 'subjects.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()

    for subject in subjects:
        FA ='{subject}/DTI/dti_FA.nii.gz'.format(subject=subject)
        MD ='{subject}/DTI/dti_MD.nii.gz'.format(subject=subject)
        
        dataLoc = '{subject}/rsFC_seed_tractography/{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(subject=subject, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
        dataDirs = [ x for x in os.listdir(dataLoc) if '_demeaned_' in x]
        for dataDir in dataDirs:
            ic = '{dataDir}'.format(dataDir=dataDir).split('_')[1]
            
            seedDir = 'rsFC_Randomise_n80/{voxelsize}_{side}_{smoothing}_{IC}ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
            seedFile_name = ''.join([ x for x in os.listdir(seedDir) if '{ic}_demeaned_'.format(ic=ic) in x])
            seedFile = join(seedDir, seedFile_name)

            tract_norm = '{dataLoc}/{dataDir}/tract_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            tract_norm_mask = '{dataLoc}/{dataDir}/tract_norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            tract_thr_norm = '{dataLoc}/{dataDir}/tract_thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            tract_thr_norm_mask = '{dataLoc}/{dataDir}/tract_thr_norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)

            if not os.path.isfile(tract_norm):
                norm = '{dataLoc}/{dataDir}/norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                norm_mask = '{dataLoc}/{dataDir}/norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                thr = '{dataLoc}/{dataDir}/thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                thr_mask = '{dataLoc}/{dataDir}/thr_norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)

                command_tract_norm = 'fslmaths {0} -sub {1} -bin {2}'.format(norm, seedFile, tract_norm)
                command_tract_norm_mask = 'fslmaths {0} -sub {1} -bin {2}'.format(norm_mask, seedFile, tract_norm_mask)
                command_tract_thr_norm = 'fslmaths {0} -sub {1} -bin {2}'.format(thr, seedFile, tract_thr_norm)
                command_tract_thr_norm_mask = 'fslmaths {0} -sub {1} -bin {2}'.format(thr_mask, seedFile, tract_thr_norm_mask)

                os.popen(command_tract_norm).read
                os.popen(command_tract_norm_mask).read
                os.popen(command_tract_thr_norm).read
                os.popen(command_tract_thr_norm_mask).read



def extract_values(voxelsize, side, smoothing, IC):
    
    output_dir = 'Tractography_Values'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    outDir = join(output_dir, '{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC))
    if not os.path.exists(outDir):
        os.mkdir(outDir)

    out_txt = join(output_dir, 'values_{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC))
    if not os.path.isfile(out_txt):
        log = 'subjects.txt'
        with open(log, 'r') as f:
            subjects = f.read().split()
         
        for subject in subjects:
            ics =[]
            reg_normFA_imgs = []
            reg_thr_normFA_imgs = []
            reg_normMD_imgs = []
            reg_thr_normMD_imgs = []
            tract_norm_imgs =[]
            tract_norm_mask_imgs =[]
            tract_thr_norm_imgs =[]
            tract_thr_norm_mask_imgs =[]
            
            FA ='{subject}/DTI/dti_FA.nii.gz'.format(subject=subject)
            MD ='{subject}/DTI/dti_MD.nii.gz'.format(subject=subject)
            
            dataLoc = '{subject}/rsFC_seed_tractography/{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(subject=subject, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
            dataDirs = [ x for x in os.listdir(dataLoc) if '_demeaned_' in x]
            for dataDir in dataDirs:

                reg_normFA = '{dataLoc}/{dataDir}/reg_FA_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                reg_normFA_imgs.append(reg_normFA)
                reg_thrFA = '{dataLoc}/{dataDir}/reg_FA_thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                reg_thr_normFA_imgs.append(reg_thrFA)
                reg_normMD = '{dataLoc}/{dataDir}/reg_MD_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                reg_normMD_imgs.append(reg_normMD)
                reg_thrMD = '{dataLoc}/{dataDir}/reg_MD_thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                reg_thr_normMD_imgs.append(reg_thrMD)

                tract_norm = '{dataLoc}/{dataDir}/tract_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                tract_norm_imgs.append(tract_norm)
                tract_norm_mask = '{dataLoc}/{dataDir}/tract_norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                tract_norm_mask_imgs.append(tract_norm_mask)
                tract_thr_norm = '{dataLoc}/{dataDir}/tract_thr_norm_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                tract_thr_norm_imgs.append(tract_thr_norm)
                tract_thr_norm_mask = '{dataLoc}/{dataDir}/tract_thr_norm_fdt_paths_mask.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                tract_thr_norm_mask_imgs.append(tract_thr_norm_mask)
            
                ic = '{dataDir}'.format(dataDir=dataDir).split('_')[1]
                ics.append(ic)

            norm_tract_txt = join(outDir, 'tract_normalized.txt')
            for i, (ic, img) in enumerate(zip(ics, tract_norm_imgs)):
                norm_tract_output = open(norm_tract_txt, 'a')
                norm_tract_command = 'fslstats {0} -V'.format(img)
                norm_tract_out = os.popen(norm_tract_command)
                norm_tract_result = norm_tract_out.read()
                norm_tract_output.write(subject + "\t" + ic + "\t" + norm_tract_result)

            mask_norm_tract_txt = join(outDir, 'tract_normalized_masked.txt')
            for i, (ic, img) in enumerate(zip(ics, tract_norm_mask_imgs)):
                mask_norm_tract_output = open(mask_norm_tract_txt, 'a')
                mask_norm_tract_command = 'fslstats {0} -V'.format(img)
                mask_norm_tract_out = os.popen(mask_norm_tract_command)
                mask_norm_tract_result = mask_norm_tract_out.read()
                mask_norm_tract_output.write(subject + "\t" + ic + "\t" + mask_norm_tract_result)

            thr_norm_tract_txt = join(outDir, 'tract_normalized_thr.txt')
            for i, (ic, img) in enumerate(zip(ics, tract_thr_norm_imgs)):
                thr_norm_tract_output = open(thr_norm_tract_txt, 'a')
                thr_norm_tract_command = 'fslstats {0} -V'.format(img)
                thr_norm_tract_out = os.popen(thr_norm_tract_command)
                thr_norm_tract_result = thr_norm_tract_out.read()
                thr_norm_tract_output.write(subject + "\t" + ic + "\t" + thr_norm_tract_result)

            mask_thr_norm_tract_txt = join(outDir, 'tract_normalized_thr_masked.txt')
            for i, (ic, img) in enumerate(zip(ics, tract_thr_norm_mask_imgs)):
                mask_thr_norm_tract_output = open(mask_thr_norm_tract_txt, 'a')
                mask_thr_norm_tract_command = 'fslstats {0} -V'.format(img)
                mask_thr_norm_tract_out = os.popen(mask_thr_norm_tract_command)
                mask_thr_norm_tract_result = mask_thr_norm_tract_out.read()
                mask_thr_norm_tract_output.write(subject + "\t" + ic + "\t" + mask_thr_norm_tract_result)

                

            norm_FA_txt = join(outDir, 'FA_normalized.txt')
            for i, (ic, img) in enumerate(zip(ics, reg_normFA_imgs)):
                norm_FA_output = open(norm_FA_txt, 'a')
                norm_FA_command = ' fslstats {0} -k {1} -M'.format(FA, img)
                norm_FA_out = os.popen(norm_FA_command)
                norm_FA_result = norm_FA_out.read()
                norm_FA_output.write(subject + "\t" + ic + "\t" + norm_FA_result)

            thr_norm_FA_txt = join(outDir, 'FA_normalized_thr.txt')
            for i, (ic, img) in enumerate(zip(ics, reg_thr_normFA_imgs)):
                thr_norm_FA_output = open(thr_norm_FA_txt, 'a')
                thr_norm_FA_command = ' fslstats {0} -k {1} -M'.format(FA, img)
                thr_norm_FA_out = os.popen(thr_norm_FA_command)
                thr_norm_FA_result = thr_norm_FA_out.read()
                thr_norm_FA_output.write(subject + "\t" + ic + "\t" + thr_norm_FA_result)

                
            norm_MD_txt = join(outDir, 'MD_normalized.txt')
            for i, (ic, img) in enumerate(zip(ics, reg_normMD_imgs)):
                norm_MD_output = open(norm_MD_txt, 'a')
                norm_MD_command = ' fslstats {0} -k {1} -M'.format(MD, img)
                norm_MD_out = os.popen(norm_MD_command)
                norm_MD_result = norm_MD_out.read()
                norm_MD_output.write(subject + "\t" + ic + "\t" + norm_MD_result)

            thr_norm_MD_txt = join(outDir, 'MD_normalized_thr.txt')
            for i, (ic, img) in enumerate(zip(ics, reg_thr_normMD_imgs)):
                thr_norm_MD_output = open(thr_norm_MD_txt, 'a')
                thr_norm_MD_command = ' fslstats {0} -k {1} -M'.format(MD, img)
                thr_norm_MD_out = os.popen(thr_norm_MD_command)
                thr_norm_MD_result = thr_norm_MD_out.read()
                thr_norm_MD_output.write(subject + "\t" + ic + "\t" + thr_norm_MD_result)

        

                


                
            seedDir = 'rsFC_Randomise_n80/{voxelsize}_{side}_{smoothing}_{IC}ICs/two_step_randomise/nocov_1_sample_tfce/sig_clusters'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
            for ic in ics:
                seedFile_name = ''.join([ x for x in os.listdir(seedDir) if '{ic}_demeaned_'.format(ic=ic) in x])
                seedFile = join(seedDir, seedFile_name)
 


                

                








                



















            





            









if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--voxelsize', '-vox', nargs=1, type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--smoothing', '-smooth', nargs=1,  help = 'e.g., nosmooth, fwhm6, fwhm6preproc', type=str)
	parser.add_argument('--IC', '-IC', nargs=1, help = 'e.g., 10 or 20', type=str)
	args = parser.parse_args()

	fdt_normalize(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
	registration(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
	extract_tract(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
	extract_values(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
