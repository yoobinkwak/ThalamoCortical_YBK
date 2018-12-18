import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image



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



def randomise(voxelsize, side, smoothing, IC, stats):

    randomise_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_{smoothing}_{IC}ICs/two_step_randomise/{stats}_tfce'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC, stats=stats)

    randomise_input_dir = join(randomise_dir, 'step2_inputs')

    two_group_tfce_out_dir = join(randomise_dir, 'step2_2group_tfce')
    if not os.path.exists(two_group_tfce_out_dir):
        os.mkdir(two_group_tfce_out_dir)

    nocov_two_group_tfce_out_dir = join(randomise_dir, 'step2_nocov_2group_tfce')
    if not os.path.exists(nocov_two_group_tfce_out_dir):
        os.mkdir(nocov_two_group_tfce_out_dir)

    inputs = os.listdir(randomise_input_dir)

    for rand_input in inputs:
        rand_inputs = join(randomise_input_dir, rand_input)
        command = 'fslval {rand_inputs} dim4'.format(rand_inputs=rand_inputs)
        val = os.popen(command)
        a = val.read()
        b = a.strip()
        correct = '80'
        if b==correct:
            output_name = rand_inputs.split('/')[-1].split('.')[0]


        two_group_tfce_output_name = join(two_group_tfce_out_dir, '{output_name}'.format(output_name=output_name))
        two_group_tfce_output = join(two_group_tfce_out_dir, '{output_name}_tfce_corrp_tstat1.nii.gz'.format(output_name=output_name))
        if not os.path.isfile(two_group_tfce_output):
            mat = 'designs/2group_80n_design.mat'
            con = 'designs/2group_design.con'
            command = 'randomise -i {rand_inputs} -o {two_group_tfce_output_name} -d {mat} -t {con} -T --uncorrp'.format(rand_inputs=rand_inputs, two_group_tfce_output_name=two_group_tfce_output_name, mat=mat, con=con)
            os.popen(command).read


        nocov_two_group_tfce_output_name = join(nocov_two_group_tfce_out_dir, '{output_name}'.format(output_name=output_name))
        nocov_two_group_tfce_output = join(nocov_two_group_tfce_out_dir, '{output_name}_tfce_corrp_tstat1.nii.gz'.format(output_name=output_name))
        if not os.path.isfile(nocov_two_group_tfce_output):
            mat = 'designs/2group_80n_nocov_design.mat'
            con = 'designs/2group_nocov_design.con'
            command = 'randomise -i {rand_inputs} -o {nocov_two_group_tfce_output_name} -d {mat} -t {con} -T --uncorrp'.format(rand_inputs=rand_inputs, nocov_two_group_tfce_output_name=nocov_two_group_tfce_output_name, mat=mat, con=con)
            os.popen(command).read




def threshold(voxelsize, side, smoothing, IC, stats):


    randomise_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_{smoothing}_{IC}ICs/two_step_randomise/{stats}_tfce'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC, stats=stats)

    two_group_tfce_out_dir = join(randomise_dir, 'step2_2group_tfce')

    two_inputs = os.listdir(two_group_tfce_out_dir)

    two_corrps = [x for x in two_inputs if '_corrp_' in x]

    thr_corrp_two_group_tfce_dir = join(two_group_tfce_out_dir, 'cluster_t0.95_corrp')
    if not os.path.exists(thr_corrp_two_group_tfce_dir):
        os.mkdir(thr_corrp_two_group_tfce_dir)

    for two_corrp in two_corrps:
        two_corrp_data = join(two_group_tfce_out_dir, two_corrp)
        thr_corrp_two_group_tfce_output = join(thr_corrp_two_group_tfce_dir, 't0.95_{two_corrp}'.format(two_corrp=two_corrp))
        if not os.path.isfile(thr_corrp_two_group_tfce_output):
            command = 'cluster -i {two_corrp_data} -t 0.95 --othresh={thr_corrp_two_group_tfce_output}'.format(two_corrp_data=two_corrp_data, thr_corrp_two_group_tfce_output= thr_corrp_two_group_tfce_output)
            os.popen(command).read


    two_uncorrps = [x for x in two_inputs if '_p_' in x]

    thr_uncorrp_two_group_tfce_dir = join(two_group_tfce_out_dir, 'cluster_t0.95_uncorrp')
    if not os.path.exists(thr_uncorrp_two_group_tfce_dir):
        os.mkdir(thr_uncorrp_two_group_tfce_dir)

    for two_uncorrp in two_uncorrps:
        two_uncorrp_data = join(two_group_tfce_out_dir, two_uncorrp)
        thr_uncorrp_two_group_tfce_output = join(thr_uncorrp_two_group_tfce_dir, 't0.95_{two_uncorrp}'.format(two_uncorrp=two_uncorrp))
        if not os.path.isfile(thr_uncorrp_two_group_tfce_output):
            command = 'cluster -i {two_uncorrp_data} -t 0.95 --othresh={thr_uncorrp_two_group_tfce_output}'.format(two_uncorrp_data=two_uncorrp_data, thr_uncorrp_two_group_tfce_output= thr_uncorrp_two_group_tfce_output)
            os.popen(command).read










if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--voxelsize', '-vox', nargs=1, type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--smoothing', '-smooth', nargs=1,  help = 'e.g., nosmooth, fwhm6, fwhm6preproc', type=str)
	parser.add_argument('--IC', '-IC', nargs=1, help = 'e.g., 10 or 20', type=str)
	parser.add_argument('--stats', '-stats', nargs=1, help = 'e.g., 1_sample or nocov_1_sample', type=str)

	args = parser.parse_args()

	mergePerIC(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0], args.stats[0])
	randomise(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0], args.stats[0])
	threshold(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0], args.stats[0])
