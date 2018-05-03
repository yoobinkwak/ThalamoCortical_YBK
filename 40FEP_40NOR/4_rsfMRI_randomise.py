import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image

def nosmoothMergePerIC(voxelsize, side, IC):
    
    Randomise_dir = 'rsFC_Randomise_n80'
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
           #print(perSubj_perIC_demean)
           acrossSubjs_perIC_demean = nilearn.image.concat_imgs(perSubj_perIC_demean)
           acrossSubjs_perIC_demean.to_filename(merged_subjs_perIC_demean)


def nosmoothRandomise(voxelsize, side, IC):
    
    
    Randomise_dir = 'rsFC_Randomise_n80'
    randomise_dir = join(Randomise_dir, '{voxelsize}_{side}_nosmooth_{IC}ICs'.format(voxelsize=voxelsize, side=side, IC=IC))
    randomise_input_dir = join (randomise_dir, 'inputs')
    
    one_sample_tfce_out_dir = join(randomise_dir, '1_sample_tfce')
    if not os.path.exists(one_sample_tfce_out_dir):
        os.mkdir(one_sample_tfce_out_dir)

    two_group_tfce_out_dir = join(randomise_dir, '2_group_tfce')
    if not os.path.exists(two_group_tfce_out_dir):
        os.mkdir(two_group_tfce_out_dir)
    
    inputs = os.listdir(randomise_input_dir)
    
    for rand_input in inputs:
        rand_inputs = join(randomise_input_dir, rand_input)
        #print(rand_inputs)
        command = 'fslval {rand_inputs} dim4'.format(rand_inputs=rand_inputs)
        val = os.popen(command)
        a = val.read()
        b = a.strip()
        correct = '80'
        if b==correct:
            output_name = rand_inputs.split('/')[-1].split('.')[0]
            #print(output_name)
            one_sample_tfce_output_name = join(one_sample_tfce_out_dir, '{output_name}'.format(output_name=output_name))
            one_sample_tfce_output = join(one_sample_tfce_out_dir, '{output_name}_tfce_corrp_tstat1.nii.gz'.format(output_name=output_name))
            if not os.path.isfile(one_sample_tfce_output):
                command = 'randomise -i {rand_inputs} -o {one_sample_tfce_output_name} -1 -T --uncorrp'.format(rand_inputs=rand_inputs, one_sample_tfce_output_name=one_sample_tfce_output_name)
                os.popen(command).read

            two_group_tfce_output_name = join(two_group_tfce_out_dir, '{output_name}'.format(output_name=output_name))
            two_group_tfce_output = join(two_group_tfce_out_dir, '{output_name}_tfce_corrp_tstat1.nii.gz'.format(output_name=output_name))
            if not os.path.isfile(two_group_tfce_output):
                mat = 'designs/2group_80n_design.mat'
                con = 'designs/2group_design.con'
                command = 'randomise -i {rand_inputs} -o {two_group_tfce_output_name} -d {mat} -t {con} -T --uncorrp'.format(rand_inputs=rand_inputs, two_group_tfce_output_name=two_group_tfce_output_name, mat=mat, con=con)
                os.popen(command).read


def threshold_95(voxelsize, side, IC):

    Randomise_dir = 'rsFC_Randomise_n80'
    randomise_dir = join(Randomise_dir, '{voxelsize}_{side}_nosmooth_{IC}ICs'.format(voxelsize=voxelsize, side=side, IC=IC))

    one_sample_tfce_out_dir = join(randomise_dir, '1_sample_tfce')
    two_group_tfce_out_dir = join(randomise_dir, '2_group_tfce')
    
    one_inputs = os.listdir(one_sample_tfce_out_dir)

    one_corrps = [x for x in one_inputs if '_corrp_' in x]
    #print(one_corrps)

    thr_corrp_one_sample_tfce_dir = join(one_sample_tfce_out_dir, 'cluster_t0.95_corrp')
    if not os.path.exists(thr_corrp_one_sample_tfce_dir):
        os.mkdir(thr_corrp_one_sample_tfce_dir)

    for one_corrp in one_corrps:
        one_corrp_data = join(one_sample_tfce_out_dir, one_corrp)
        thr_corrp_one_sample_tfce_output = join(thr_corrp_one_sample_tfce_dir, 't0.95_{one_corrp}'.format(one_corrp=one_corrp))
        if not os.path.isfile(thr_corrp_one_sample_tfce_output):
            command = 'cluster -i {one_corrp_data} -t 0.95 --othresh={thr_corrp_one_sample_tfce_output}'.format(one_corrp_data=one_corrp_data, thr_corrp_one_sample_tfce_output= thr_corrp_one_sample_tfce_output) 
            os.popen(command).read

    one_uncorrps = [x for x in one_inputs if '_p_' in x]
    #print(one_uncorrps)

    thr_uncorrp_one_sample_tfce_dir = join(one_sample_tfce_out_dir, 'cluster_t0.95_uncorrp')
    if not os.path.exists(thr_uncorrp_one_sample_tfce_dir):
        os.mkdir(thr_uncorrp_one_sample_tfce_dir)

    for one_uncorrp in one_uncorrps:
        one_uncorrp_data = join(one_sample_tfce_out_dir, one_uncorrp)
        thr_uncorrp_one_sample_tfce_output = join(thr_uncorrp_one_sample_tfce_dir, 't0.95_{one_uncorrp}'.format(one_uncorrp=one_uncorrp))
        if not os.path.isfile(thr_uncorrp_one_sample_tfce_output):
            command = 'cluster -i {one_uncorrp_data} -t 0.95 --othresh={thr_uncorrp_one_sample_tfce_output}'.format(one_uncorrp_data=one_uncorrp_data, thr_uncorrp_one_sample_tfce_output= thr_uncorrp_one_sample_tfce_output) 
            os.popen(command).read



    two_inputs = os.listdir(two_group_tfce_out_dir)

    two_corrps = [x for x in two_inputs if '_corrp_' in x]
    #print(two_corrps)

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
    #print(two_uncorrps)

    thr_uncorrp_two_group_tfce_dir = join(two_group_tfce_out_dir, 'cluster_t0.95_uncorrp')
    if not os.path.exists(thr_uncorrp_two_group_tfce_dir):
        os.mkdir(thr_uncorrp_two_group_tfce_dir)

    for two_uncorrp in two_uncorrps:
        two_uncorrp_data = join(two_group_tfce_out_dir, two_uncorrp)
        thr_uncorrp_two_group_tfce_output = join(thr_uncorrp_two_group_tfce_dir, 't0.95_{two_uncorrp}'.format(two_uncorrp=two_uncorrp))
        if not os.path.isfile(thr_uncorrp_two_group_tfce_output):
            command = 'cluster -i {two_uncorrp_data} -t 0.95 --othresh={thr_uncorrp_two_group_tfce_output}'.format(two_uncorrp_data=two_uncorrp_data, thr_uncorrp_two_group_tfce_output= thr_uncorrp_two_group_tfce_output) 
            os.popen(command).read


def check_slices(voxelsize, side, IC):

    Randomise_dir = 'rsFC_Randomise_n80'
    randomise_dir = join(Randomise_dir, '{voxelsize}_{side}_nosmooth_{IC}ICs'.format(voxelsize=voxelsize, side=side, IC=IC))
    
    one_sample_tfce_out_dir = join(randomise_dir, '1_sample_tfce')
    thr_corrp_one_sample_tfce_dir = join(one_sample_tfce_out_dir, 'cluster_t0.95_corrp')
    thr_corrp_one_sample_tfce_slices_dir = join(thr_corrp_one_sample_tfce_dir, 'slicer')
    if not os.path.exists(thr_corrp_one_sample_tfce_slices_dir):
        os.mkdir(thr_corrp_one_sample_tfce_slices_dir)
    one_corrp_inputs = [x for x in os.listdir(thr_corrp_one_sample_tfce_dir) if 'gz' in x]
    for one_corrp_input in one_corrp_inputs:
        one_corrp_slicer_name = one_corrp_input.split('/')[-1].split('.')[1]
        one_corrp_slicer_input = join(thr_corrp_one_sample_tfce_dir, one_corrp_input)
        print(one_corrp_slicer_input)
        one_corrp_slicer_output = join(thr_corrp_one_sample_tfce_slices_dir, 't0.{one_corrp_slicer_name}.png'.format(one_corrp_slicer_name=one_corrp_slicer_name))
        if not os.path.isfile(one_corrp_slicer_output):
            command = 'slicer {one_corrp_slicer_input} -L -A 600 {one_corrp_slicer_output}'.format(one_corrp_slicer_input=one_corrp_slicer_input, one_corrp_slicer_output=one_corrp_slicer_output) 
            os.popen(command).read

    thr_uncorrp_one_sample_tfce_dir = join(one_sample_tfce_out_dir, 'cluster_t0.95_uncorrp')
    thr_uncorrp_one_sample_tfce_slices_dir = join(thr_uncorrp_one_sample_tfce_dir, 'slicer')
    if not os.path.exists(thr_uncorrp_one_sample_tfce_slices_dir):
        os.mkdir(thr_uncorrp_one_sample_tfce_slices_dir)
    one_uncorrp_inputs = [x for x in os.listdir(thr_uncorrp_one_sample_tfce_dir) if 'gz' in x]
    for one_uncorrp_input in one_uncorrp_inputs:
        one_uncorrp_slicer_name = one_uncorrp_input.split('/')[-1].split('.')[1]
        one_uncorrp_slicer_input = join(thr_uncorrp_one_sample_tfce_dir, one_uncorrp_input)
        print(one_uncorrp_slicer_input)
        one_uncorrp_slicer_output = join(thr_uncorrp_one_sample_tfce_slices_dir, 't0.{one_uncorrp_slicer_name}.png'.format(one_uncorrp_slicer_name=one_uncorrp_slicer_name))
        if not os.path.isfile(one_uncorrp_slicer_output):
            command = 'slicer {one_uncorrp_slicer_input} -L -A 600 {one_uncorrp_slicer_output}'.format(one_uncorrp_slicer_input=one_uncorrp_slicer_input, one_uncorrp_slicer_output=one_uncorrp_slicer_output) 
            os.popen(command).read



    two_group_tfce_out_dir = join(randomise_dir, '2_group_tfce')
    thr_corrp_two_group_tfce_dir = join(two_group_tfce_out_dir, 'cluster_t0.95_corrp')
    thr_corrp_two_group_tfce_slices_dir = join(thr_corrp_two_group_tfce_dir, 'slicer')
    if not os.path.exists(thr_corrp_two_group_tfce_slices_dir):
        os.mkdir(thr_corrp_two_group_tfce_slices_dir)
    two_corrp_inputs = [x for x in os.listdir(thr_corrp_two_group_tfce_dir) if 'gz' in x]
    for two_corrp_input in two_corrp_inputs:
        two_corrp_slicer_name = two_corrp_input.split('/')[-1].split('.')[1]
        two_corrp_slicer_input = join(thr_corrp_two_group_tfce_dir, two_corrp_input)
        print(two_corrp_slicer_input)
        two_corrp_slicer_output = join(thr_corrp_two_group_tfce_slices_dir, 't0.{two_corrp_slicer_name}.png'.format(two_corrp_slicer_name=two_corrp_slicer_name))
        if not os.path.isfile(two_corrp_slicer_output):
            command = 'slicer {two_corrp_slicer_input} -L -A 600 {two_corrp_slicer_output}'.format(two_corrp_slicer_input=two_corrp_slicer_input, two_corrp_slicer_output=two_corrp_slicer_output) 
            os.popen(command).read

    thr_uncorrp_two_group_tfce_dir = join(two_group_tfce_out_dir, 'cluster_t0.95_uncorrp')
    thr_uncorrp_two_group_tfce_slices_dir = join(thr_uncorrp_two_group_tfce_dir, 'slicer')
    if not os.path.exists(thr_uncorrp_two_group_tfce_slices_dir):
        os.mkdir(thr_uncorrp_two_group_tfce_slices_dir)
    two_uncorrp_inputs = [x for x in os.listdir(thr_uncorrp_two_group_tfce_dir) if 'gz' in x]
    for two_uncorrp_input in two_uncorrp_inputs:
        two_uncorrp_slicer_name = two_uncorrp_input.split('/')[-1].split('.')[1]
        two_uncorrp_slicer_input = join(thr_uncorrp_two_group_tfce_dir, two_uncorrp_input)
        print(two_uncorrp_slicer_input)
        two_uncorrp_slicer_output = join(thr_uncorrp_two_group_tfce_slices_dir, 't0.{two_uncorrp_slicer_name}.png'.format(two_uncorrp_slicer_name=two_uncorrp_slicer_name))
        if not os.path.isfile(two_uncorrp_slicer_output):
            command = 'slicer {two_uncorrp_slicer_input} -L -A 600 {two_uncorrp_slicer_output}'.format(two_uncorrp_slicer_input=two_uncorrp_slicer_input, two_uncorrp_slicer_output=two_uncorrp_slicer_output) 
            os.popen(command).read













if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., ds3', type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'bi, left or right', type=str)
	parser.add_argument('--IC', '-IC', nargs=1, help = 'e.g., 10 or 20', type=str)
	args = parser.parse_args()

        nosmoothMergePerIC(args.voxelsize[0], args.side[0], args.IC[0])
        nosmoothRandomise(args.voxelsize[0], args.side[0], args.IC[0])
        threshold_95(args.voxelsize[0], args.side[0], args.IC[0])
        check_slices(args.voxelsize[0], args.side[0], args.IC[0])


