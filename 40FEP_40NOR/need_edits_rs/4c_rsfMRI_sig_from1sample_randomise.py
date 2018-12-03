import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image



#rsFC_Randomise_n80/ds3_bi_nosmooth_10ICs/two_step_randomise/1_sample_tfce

#rsFC_Randomise_n80/ds3_bi_nosmooth_10ICs/two_step_randomise/1_sample_tfce/step2_inputs

#NOR99_KS/rsFC_ICA_1sample/1_sample_tfce/ds3_bi_nosmooth_10ICs/dual_regression/t0.95_concatenated_ds3_bi_nosmooth_IC00_demeaned_tfce_corrp_tstat1/dr_stage2_subject00000.nii.gz


def mergePerIC(voxelsize, side, smoothing, IC, stats):
    
    randomise_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_{smoothing}_{IC}ICs/two_step_randomise/{stats}_tfce'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC, stats=stats)

    randomise_input_dir = join(randomise_dir, 'step2_inputs')
    if not os.path.exists(randomise_input_dir):
        os.mkdir(randomise_input_dir)

    sig_cluster_dir = join(randomise_dir, 'sig_clusters')
    #demeaned_component_num = len([x for x in os.listdir(sig_cluster_dir) if 'demeaned' in x])
    #undemeaned_component_num = len([x for x in os.listdir(sig_cluster_dir) if 'demeaned' not in x])

    log = 'subjects.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()

    imgInputs_demean = []
    imgInputs_undemean = []

    componentNum = int('{IC}'.format(IC=IC))
    
    ICs=["%02d" % x for x in range(0,componentNum)]
    for ic in ICs:
        for subj in subjects:
            demeaned_dataFile = subj+'/rsFC_ICA_1sample/{stats}_tfce/{voxelsize}_{side}_{smoothing}_{IC}ICs/dual_regression/t0.95_concatenated_{voxelsize}_{side}_{smoothing}_IC{ic}_demeaned_tfce_corrp_tstat1/dr_stage2_subject00000.nii.gz'.format(stats=stats, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC, ic=ic)
            undemeaned_dataFile = subj+'/rsFC_ICA_1sample/{stats}_tfce/{voxelsize}_{side}_{smoothing}_{IC}ICs/dual_regression/t0.95_concatenated_{voxelsize}_{side}_{smoothing}_IC{ic}_tfce_corrp_tstat1/dr_stage2_subject00000.nii.gz'.format(stats=stats, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC, ic=ic)

            if os.path.isfile(demeaned_dataFile):
                imgInputs_demean.append(demeaned_dataFile)

            if os.path.isfile(undemeaned_dataFile):
                imgInputs_undemean.append(undemeaned_dataFile)


    for ic in ICs:
        sig_cluster_demeaned = join(sig_cluster_dir, 't0.95_concatenated_{voxelsize}_{side}_{smoothing}_IC{ic}_demeaned_tfce_corrp_tstat1.nii.gz'.format(voxelsize=voxelsize, side=side,smoothing=smoothing, ic=ic))
        if os.path.isfile(sig_cluster_demeaned):
            merged_subjs_perIC_demean = join(randomise_input_dir, 'concatenated_{voxelsize}_{side}_{smoothing}_IC{ic}_demeaned.nii.gz'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, ic=ic))
            if not os.path.isfile(merged_subjs_perIC_demean):
                perSubj_perIC_demean = [x for x in imgInputs_demean if 'IC{ic}'.format(ic=ic) in x]
                acrossSubjs_perIC_demean = nilearn.image.concat_imgs(perSubj_perIC_demean)
                acrossSubjs_perIC_demean.to_filename(merged_subjs_perIC_demean)


        sig_cluster_undemeaned = join(sig_cluster_dir, 't0.95_concatenated_{voxelsize}_{side}_{smoothing}_IC{ic}_tfce_corrp_tstat1.nii.gz'.format(voxelsize=voxelsize, side=side,smoothing=smoothing, ic=ic))
        if os.path.isfile(sig_cluster_undemeaned):
            merged_subjs_perIC_undemean = join(randomise_input_dir, 'concatenated_{voxelsize}_{side}_{smoothing}_IC{ic}_undemeaned.nii.gz'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, ic=ic))
            if not os.path.isfile(merged_subjs_perIC_undemean):
                perSubj_perIC_undemean = [x for x in imgInputs_undemean if 'IC{ic}'.format(ic=ic) in x]
                acrossSubjs_perIC_undemean = nilearn.image.concat_imgs(perSubj_perIC_undemean)
                acrossSubjs_perIC_undemean.to_filename(merged_subjs_perIC_undemean)





















if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--voxelsize', '-vox', nargs=1, type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--smoothing', '-smooth', nargs=1,  help = 'e.g., nosmooth, fwhm6, fwhm6preproc', type=str)
	parser.add_argument('--IC', '-IC', nargs=1, help = 'e.g., 10 or 20', type=str)
	parser.add_argument('--stats', '-stats', nargs=1, help = 'e.g., 1_sample or nocov_1_sample', type=str)

	args = parser.parse_args()

	mergePerIC(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0], args.stats[0])
