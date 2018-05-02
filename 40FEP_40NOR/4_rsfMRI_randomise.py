import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image

def nosmoothMergePerIC(voxelsize, side, IC):
    
    Randomise_dir = 'rsFC_Randomise'
    if not os.path.exists(Randomise_dir):
        os.mkdir(Randomise_dir)

    randomise_dir = join(Randomise_dir, '{voxelsize}_{side}_nosmooth_{IC}ICs'.format(voxelsize=voxelsize, side=side, IC=IC))
    if not os.path.exists(randomise_dir):
        os.mkdir(randomise_dir)

    randomise_input_dir = join (randomise_dir, 'inputs')
    if not os.path.exists(randomise_input_dir):
        os.mkdir(randomise_input_dir)


    melodicIC_map = nb.load('rsFC_ICA_cmd/{voxelsize}_{side}_{IC}ICs_masked/melodic_IC.nii.gz'.format(voxelsize=voxelsize, side=side, IC=IC))
    componentNum = melodicIC_map.shape[3]

    log = 'subjects.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()
    
    imgInputs = []
    imgInputs_demean = []

    for subj in subjects:
        dataLoc = subj+'/DualRegression_TemporalICA/TemporalRegression_Stage2/{voxelsize}_{side}_nosmooth_{IC}ICs_bp2mni'.format(voxelsize=voxelsize, side=side, IC=IC)

        ICs=["%02d" % x for x in range(0,componentNum)]
        for ic in ICs:
            dataFile = join(dataLoc, '{subj}_stage2_00{ic}.nii.gz'.format(subj=subj, ic=ic))
            if not os.path.isfile(dataFile):
                print('splitting stage2')
                presplit_dataFile = join(dataLoc, '{subj}_stage2.nii.gz'.format(subj=subj))
                split_dataFile = join(dataLoc, '{subj}_stage2_'.format(subj=subj))
                command = 'fslsplit {presplit_dataFile} {split_dataFile}'.format(presplit_dataFile=presplit_dataFile, split_dataFile=split_dataFile)
                os.popen(command).read
            else:
                imgInputs.append(dataFile)
                #print(imgInputs)

            dataFile_demean = join(dataLoc, '{subj}_stage2_demeaned_00{ic}.nii.gz'.format(subj=subj, ic=ic))
            if not os.path.isfile(dataFile_demean):
                print('splitting stage2_demeaned')
                presplit_dataFile_demean = join(dataLoc, '{subj}_stage2_demeaned.nii.gz'.format(subj=subj))
                split_dataFile_demean = join(dataLoc, '{subj}_stage2_demeaned_'.format(subj=subj))
                command_demean = 'fslsplit {presplit_dataFile_demean} {split_dataFile_demean}'.format(presplit_dataFile_demean=presplit_dataFile_demean, split_dataFile_demean=split_dataFile_demean)
                os.popen(command_demean).read
            else:
                imgInputs_demean.append(dataFile_demean)
                #print(imgInputs_demean)

    for ic in ICs:
        merged_subjs_perIC = join(randomise_input_dir, 'concatenated_{voxelsize}_{side}_nosmooth_IC{ic}.nii.gz'.format(voxelsize=voxelsize, side=side, ic=ic))
        if not os.path.isfile(merged_subjs_perIC):
           perSubj_perIC = [x for x in imgInputs if '00{ic}'.format(ic=ic) in x]
           #print(perSubj_perIC)
           acrossSubjs_perIC = nilearn.image.concat_imgs(perSubj_perIC)
           acrossSubjs_perIC.to_filename(merged_subjs_perIC)

        merged_subjs_perIC_demean = join(randomise_input_dir, 'concatenated_{voxelsize}_{side}_nosmooth_IC{ic}_demeaned.nii.gz'.format(voxelsize=voxelsize, side=side, ic=ic))
        if not os.path.isfile(merged_subjs_perIC_demean):
           perSubj_perIC_demean = [x for x in imgInputs_demean if '00{ic}'.format(ic=ic) in x]
           print(perSubj_perIC_demean)
           acrossSubjs_perIC_demean = nilearn.image.concat_imgs(perSubj_perIC_demean)
           acrossSubjs_perIC_demean.to_filename(merged_subjs_perIC_demean)








                









if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., ds3', type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'bi, left or right', type=str)
	parser.add_argument('--IC', '-IC', nargs=1, help = 'e.g., 10 or 20', type=str)
	args = parser.parse_args()

        nosmoothMergePerIC(args.voxelsize[0], args.side[0], args.IC[0])






