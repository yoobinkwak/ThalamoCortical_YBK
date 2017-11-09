import re
import sys
import os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
from scipy import stats



def zStats (melodicDir, subject):
	fsl_reg_out = join(melodicDir, 'glm_out_dir', 'fsl_glm_output_${subject}'.format(subject=subject)
	fsl_glm_mat = np.loadtxt(fsl_reg_out)
	fsl_glm_mat_z = stats.zscore(fsl_glm_mat)
	return fsl_glm_mat_z

def construct (melodicDir, subject):
	mniLoc = '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm.nii.gz'
	thalamusLoc = '/Volume/CCNC_W1_2T/Thalamus_SCrsFC_20171026/rh_thalamus_HOSC_60.nii.gz'
	
	icMap_loc = join(melodicDir, 'melodic_IC.nii.gz')
	icMap_nb = nb.load(icMap_loc)
	componentNum = icMap_nb.shape[3]
	voxSize = icMap_nb.header.get_zooms()[0]

	thalamus = nb.load(thalamusLoc)
	thalData = thalamus.get_data()
	thalNZ = np.nonzero(thalData)
	thalVoxelNum = len(thalNZ[0])
	thalInd = np.ravel_multi_index((thalNZ[0],thalNZ[1],thalNZ[2]), dims=thalData.shape, order='F')


	subject_list = join(melodicDir, 'subjects.txt')
	if not isfile(subject_list):
		subjectlist = []
		path=
		dirList=os.listdir(path)
		with open(subjects.txt, "w") as f:
			for filename in dirList:
				if filename.startswith(('C','F','N')):
					f.write(filename + '\n')
	
	subjectNum = sum(1 for line in open(subject_list))
	
	fsl_glm_mat_sub = np.zeros(thalVoxelNum * componentNum * subjectNum)
	fsl_glm_mat_sub = fsl_glm_mat_sub.reshape(thalVoxelNum, componentNum, subjectNum)
	
	fsl_glm_mat_loc = join(melodicDir, 'fsl_glm_mat_sub.npy')
	if not isfile(fsl_glm_mat_loc): 
		fsl_glm_mat_z = zStats(melodicDir, subject)
		print(fsl_glm_mat_z.shape)
		print(fsl_glm_mat_sub.shape)
	
		phrase = subject
		with open(subject_list) as f:
			for i, line in enumerate(f, 1):
				if phrase in line:
					num = i
					fsl_glm_mat_sub[:,:, num] = fsl_glm_mat_z
					np.save(join(melodicDir, 'fsl_glm_mat_sub'), fsl_glm_mat_sub)

	mask_ravel_rep = np.tile(np.zeros_like(thalData).ravel()[:, np.newaxis], componentNum)
	mask_ravel_rep_sub = np.tile(mask_ravel_rep[:,:, np.newaxis], subjectNum)
	mask_ravel_rep_sub[thalInd, :,:] = fsl_glm_mat_sub
	mask5D = mask_ravel_rep_sub.reshape([thalData.shape[0], thalData.shape[1], thalData.shape[2], componentNum, subjectNum], order='F')











if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--subject', '-s', nargs=1, type=str)
	parser.add_argument('--melodicdir', '-md', nargs=1, type=str)
	args = parser.parse_args()

	zStats(args.subject[0], args.melodicdir[0])
	construct(args.subject[0], args.melodicdir[0])

	
