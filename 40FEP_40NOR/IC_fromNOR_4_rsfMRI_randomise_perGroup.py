import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image



def mergePerIC(voxelsize, side, smoothing, IC):
    
    randomise_NOR_only='rsFC_Randomise_n80/NOR_only'
    if not os.path.exists(randomise_NOR_only):
        os.mkdir(randomise_NOR_only)
    
    randomise_dir = join(randomise_NOR_only, '{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC))
    if not os.path.exists(randomise_dir):
        os.mkdir(randomise_dir)

    #randomise_input_dir = join(randomise_dir, 'NOR_inputs')
    randomise_input_dir = join(randomise_dir, 'FEP_inputs')
    if not os.path.exists(randomise_input_dir):
        os.mkdir(randomise_input_dir)


    #log = 'subjects_NOR.txt'
    log = 'subjects_FEP.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()

    imgInputs_demean = []
    imgInputs_undemean = []

    for subj in subjects:
        dataLoc = subj+'/Dual_Regression/fromNOR_ConcatICA/{voxelsize}_{side}_{smoothing}_{IC}ICs//TemporalRegression_Stage2'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
    
        componentNum = int('{IC}'.format(IC=IC))
        ICs=["%02d" % x for x in range(0,componentNum)]
        for ic in ICs:
            
            dataFile_demean = join(dataLoc, '{subj}_stage2_demeaned_00{ic}.nii.gz'.format(subj=subj, ic=ic))
            if not os.path.isfile(dataFile_demean):
                print('splitting stage2_demeaned')
                presplit_dataFile_demean = join(dataLoc, '{subj}_stage2_demeaned.nii.gz'.format(subj=subj))
                split_dataFile_demean = join(dataLoc, '{subj}_stage2_demeaned_'.format(subj=subj))
                command_demean = 'fslsplit {presplit_dataFile_demean} {split_dataFile_demean}'.format(presplit_dataFile_demean=presplit_dataFile_demean, split_dataFile_demean=split_dataFile_demean)
                os.popen(command_demean).read
            else:
                imgInputs_demean.append(dataFile_demean)


            dataFile_undemean = join(dataLoc, '{subj}_stage2_00{ic}.nii.gz'.format(subj=subj, ic=ic))
            if not os.path.isfile(dataFile_undemean):
                print('splitting stage2_undemeaned')
                presplit_dataFile = join(dataLoc, '{subj}_stage2.nii.gz'.format(subj=subj))
                split_dataFile = join(dataLoc, '{subj}_stage2_'.format(subj=subj))
                command = 'fslsplit {presplit_dataFile} {split_dataFile}'.format(presplit_dataFile=presplit_dataFile, split_dataFile=split_dataFile)
                os.popen(command).read
            else:
                imgInputs_undemean.append(dataFile_undemean)



    for ic in ICs:
        merged_subjs_perIC_demean = join(randomise_input_dir, 'concatenated_{voxelsize}_{side}_{smoothing}_IC{ic}_demeaned.nii.gz'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, ic=ic))
        if not os.path.isfile(merged_subjs_perIC_demean):
           perSubj_perIC_demean = [x for x in imgInputs_demean if '00{ic}'.format(ic=ic) in x]
           acrossSubjs_perIC_demean = nilearn.image.concat_imgs(perSubj_perIC_demean)
           acrossSubjs_perIC_demean.to_filename(merged_subjs_perIC_demean)

        merged_subjs_perIC_undemean = join(randomise_input_dir, 'concatenated_{voxelsize}_{side}_{smoothing}_IC{ic}.nii.gz'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, ic=ic))
        if not os.path.isfile(merged_subjs_perIC_undemean):
           perSubj_perIC_undemean = [x for x in imgInputs_undemean if '00{ic}'.format(ic=ic) in x]
           acrossSubjs_perIC_undemean = nilearn.image.concat_imgs(perSubj_perIC_undemean)
           acrossSubjs_perIC_undemean.to_filename(merged_subjs_perIC_undemean)



def randomise(voxelsize, side, smoothing, IC):

    randomise_dir = 'rsFC_Randomise_n80/NOR_only/{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)

    #randomise_input_dir = join(randomise_dir, 'NOR_inputs')
    randomise_input_dir = join(randomise_dir, 'FEP_inputs')

    #nocov_one_sample_tfce_out_dir = join(randomise_dir, 'NOR_nocov_1_sample_tfce')
    nocov_one_sample_tfce_out_dir = join(randomise_dir, 'FEP_nocov_1_sample_tfce')
    if not os.path.exists(nocov_one_sample_tfce_out_dir):
        os.mkdir(nocov_one_sample_tfce_out_dir)
    
    #nocov_one_sample_cluster_out_dir = join(randomise_dir, 'NOR_nocov_1_sample_cluster')
    nocov_one_sample_cluster_out_dir = join(randomise_dir, 'FEP_nocov_1_sample_cluster')
    if not os.path.exists(nocov_one_sample_cluster_out_dir):
        os.mkdir(nocov_one_sample_cluster_out_dir)
    
    #nocov_one_sample_voxel_out_dir = join(randomise_dir, 'NOR_nocov_1_sample_voxel')
    nocov_one_sample_voxel_out_dir = join(randomise_dir, 'FEP_nocov_1_sample_voxel')
    if not os.path.exists(nocov_one_sample_voxel_out_dir):
        os.mkdir(nocov_one_sample_voxel_out_dir)
    

    inputs = os.listdir(randomise_input_dir)

    for rand_input in inputs:
        rand_inputs = join(randomise_input_dir, rand_input)
        command = 'fslval {rand_inputs} dim4'.format(rand_inputs=rand_inputs)
        val = os.popen(command)
        a = val.read()
        b = a.strip()
        correct = '40'
        if b==correct:
            output_name = rand_inputs.split('/')[-1].split('.')[0]

        nocov_one_sample_tfce_output_name = join(nocov_one_sample_tfce_out_dir, '{output_name}'.format(output_name=output_name))
        nocov_one_sample_tfce_output = join(nocov_one_sample_tfce_out_dir, '{output_name}_tfce_corrp_tstat1.nii.gz'.format(output_name=output_name))
        if not os.path.isfile(nocov_one_sample_tfce_output):
            command = 'randomise -i {rand_inputs} -o {nocov_one_sample_tfce_output_name} -1 -T --uncorrp'.format(rand_inputs=rand_inputs, nocov_one_sample_tfce_output_name=nocov_one_sample_tfce_output_name)
            os.popen(command).read

        nocov_one_sample_cluster_output_name = join(nocov_one_sample_cluster_out_dir, '{output_name}'.format(output_name=output_name))
        nocov_one_sample_cluster_output = join(nocov_one_sample_cluster_out_dir, '{output_name}_clustere_corrp_tstat1.nii.gz'.format(output_name=output_name))
        if not os.path.isfile(nocov_one_sample_cluster_output):
            command = 'randomise -i {rand_inputs} -o {nocov_one_sample_cluster_output_name} -1 -c 2 --uncorrp'.format(rand_inputs=rand_inputs, nocov_one_sample_cluster_output_name=nocov_one_sample_cluster_output_name)
            os.popen(command).read

        nocov_one_sample_voxel_output_name = join(nocov_one_sample_voxel_out_dir, '{output_name}'.format(output_name=output_name))
        nocov_one_sample_voxel_output = join(nocov_one_sample_voxel_out_dir, '{output_name}_vox_corrp_tstat1.nii.gz'.format(output_name=output_name))
        if not os.path.isfile(nocov_one_sample_voxel_output):
            command = 'randomise -i {rand_inputs} -o {nocov_one_sample_voxel_output_name} -1 -x --uncorrp'.format(rand_inputs=rand_inputs, nocov_one_sample_voxel_output_name=nocov_one_sample_voxel_output_name)
            os.popen(command).read




def threshold(voxelsize, side, smoothing, IC):

    randomise_dir = 'rsFC_Randomise_n80/NOR_only/{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)

    #nocov_one_sample_tfce_out_dir = join(randomise_dir, 'NOR_nocov_1_sample_tfce')
    #nocov_one_sample_cluster_out_dir = join(randomise_dir, 'NOR_nocov_1_sample_cluster')
    #nocov_one_sample_voxel_out_dir = join(randomise_dir, 'NOR_nocov_1_sample_voxel')
    nocov_one_sample_tfce_out_dir = join(randomise_dir, 'FEP_nocov_1_sample_tfce')
    nocov_one_sample_cluster_out_dir = join(randomise_dir, 'FEP_nocov_1_sample_cluster')
    nocov_one_sample_voxel_out_dir = join(randomise_dir, 'FEP_nocov_1_sample_voxel')
    
    one_inputs = os.listdir(nocov_one_sample_tfce_out_dir)
    one_cluster_inputs = os.listdir(nocov_one_sample_cluster_out_dir)
    one_voxel_inputs = os.listdir(nocov_one_sample_voxel_out_dir)

    one_corrps = [x for x in one_inputs if '_corrp_' in x]
    one_cluster_corrps = [x for x in one_cluster_inputs if '_corrp_' in x]
    one_voxel_corrps = [x for x in one_voxel_inputs if '_corrp_' in x]


    thr_corrp_nocov_one_sample_tfce_dir = join(nocov_one_sample_tfce_out_dir, 'cluster_t0.95_corrp')
    if not os.path.exists(thr_corrp_nocov_one_sample_tfce_dir):
        os.mkdir(thr_corrp_nocov_one_sample_tfce_dir)

    for one_corrp in one_corrps:
        one_corrp_data = join(nocov_one_sample_tfce_out_dir, one_corrp)
        print(one_corrp_data)
        thr_corrp_nocov_one_sample_tfce_output = join(thr_corrp_nocov_one_sample_tfce_dir, 't0.95_{one_corrp}'.format(one_corrp=one_corrp))
        if not os.path.isfile(thr_corrp_nocov_one_sample_tfce_output):
            command = 'cluster -i {one_corrp_data} -t 0.95 --othresh={thr_corrp_nocov_one_sample_tfce_output}'.format(one_corrp_data=one_corrp_data, thr_corrp_nocov_one_sample_tfce_output= thr_corrp_nocov_one_sample_tfce_output)
            os.popen(command).read


    thr_corrp_nocov_one_sample_cluster_dir = join(nocov_one_sample_cluster_out_dir, 'cluster_t0.95_corrp')
    if not os.path.exists(thr_corrp_nocov_one_sample_cluster_dir):
        os.mkdir(thr_corrp_nocov_one_sample_cluster_dir)

    for one_cluster_corrp in one_cluster_corrps:
        one_cluster_corrp_data = join(nocov_one_sample_cluster_out_dir, one_cluster_corrp)
        print(one_cluster_corrp_data)
        thr_corrp_nocov_one_sample_cluster_output = join(thr_corrp_nocov_one_sample_cluster_dir, 't0.95_{one_cluster_corrp}'.format(one_cluster_corrp=one_cluster_corrp))
        if not os.path.isfile(thr_corrp_nocov_one_sample_cluster_output):
            command = 'cluster -i {one_cluster_corrp_data} -t 0.95 --othresh={thr_corrp_nocov_one_sample_cluster_output}'.format(one_cluster_corrp_data=one_cluster_corrp_data, thr_corrp_nocov_one_sample_cluster_output= thr_corrp_nocov_one_sample_cluster_output)
            os.popen(command).read


    thr_corrp_nocov_one_sample_voxel_dir = join(nocov_one_sample_voxel_out_dir, 'cluster_t0.95_corrp')
    if not os.path.exists(thr_corrp_nocov_one_sample_voxel_dir):
        os.mkdir(thr_corrp_nocov_one_sample_voxel_dir)

    for one_voxel_corrp in one_voxel_corrps:
        one_voxel_corrp_data = join(nocov_one_sample_voxel_out_dir, one_voxel_corrp)
        print(one_voxel_corrp_data)
        thr_corrp_nocov_one_sample_voxel_output = join(thr_corrp_nocov_one_sample_voxel_dir, 't0.95_{one_voxel_corrp}'.format(one_voxel_corrp=one_voxel_corrp))
        if not os.path.isfile(thr_corrp_nocov_one_sample_voxel_output):
            command = 'cluster -i {one_voxel_corrp_data} -t 0.95 --othresh={thr_corrp_nocov_one_sample_voxel_output}'.format(one_voxel_corrp_data=one_voxel_corrp_data, thr_corrp_nocov_one_sample_voxel_output= thr_corrp_nocov_one_sample_voxel_output)
            os.popen(command).read





def clusterInfo(voxelsize, side, smoothing, IC):

    #working_dir = 'rsFC_Randomise_n80/NOR_only/{voxelsize}_{side}_{smoothing}_{IC}ICs/NOR_nocov_1_sample_tfce'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
    working_dir = 'rsFC_Randomise_n80/NOR_only/{voxelsize}_{side}_{smoothing}_{IC}ICs/FEP_nocov_1_sample_tfce'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)

    imgs = [ x for x in os.listdir(working_dir) if 'nii.gz' in x]

    demeaned = [ x for x in imgs if '_demeaned_' in x ]
    demeaned_corrps = [ x for x in demeaned if 'tfce_corrp' in x ]
    demeaned_uncorrps = [ x for x in demeaned if 'tfce_p' in x ]
    demeaned_rawtests = [ x for x in demeaned if 'tfce' not in x ]
    #demeaned_corrps = [ x for x in demeaned if 'clustere_corrp' in x ]
    #demeaned_uncorrps = [ x for x in demeaned if 'clustere_p' in x ]
    #demeaned_rawtests = [ x for x in demeaned if 'clustere' not in x ]
    #demeaned_corrps = [ x for x in demeaned if 'vox_corrp' in x ]
    #demeaned_uncorrps = [ x for x in demeaned if 'vox_p' in x ]
    #demeaned_rawtests = [ x for x in demeaned if 'vox' not in x ]

    undemeaned = [ x for x in imgs if '_undemeaned_' in x ]
    undemeaned_corrps = [ x for x in undemeaned if 'tfce_corrp' in x ]
    undemeaned_uncorrps = [ x for x in undemeaned if 'tfce_p' in x ]
    undemeaned_rawtests = [ x for x in undemeaned if 'tfce' not in x ]
    #undemeaned_corrps = [ x for x in undemeaned if 'clustere_corrp' in x ]
    #undemeaned_uncorrps = [ x for x in undemeaned if 'clustere_p' in x ]
    #undemeaned_rawtests = [ x for x in undemeaned if 'clustere' not in x ]
    #undemeaned_corrps = [ x for x in undemeaned if 'vox_corrp' in x ]
    #undemeaned_uncorrps = [ x for x in undemeaned if 'vox_p' in x ]
    #undemeaned_rawtests = [ x for x in undemeaned if 'vox' not in x ]


    if any(x.endswith('tstat2.nii.gz') for x in os.listdir(working_dir)):
        demeaned_corrps_t1 = [ x for x in demeaned_corrps if 'tstat1' in x ]
        demeaned_corrps_t2 = [ x for x in demeaned_corrps if 'tstat2' in x ]
        demeaned_uncorrps_t1 = [ x for x in demeaned_uncorrps if 'tstat1' in x ]
        demeaned_uncorrps_t2 = [ x for x in demeaned_uncorrps if 'tstat2' in x ]
        demeaned_rawtests_t1 = [ x for x in demeaned_rawtests if 'tstat1' in x ]
        demeaned_rawtests_t2 = [ x for x in demeaned_rawtests if 'tstat2' in x ]

        for i, (demeaned_corrp_t1, demeaned_rawtest_t1) in enumerate(zip(demeaned_corrps_t1, demeaned_rawtests_t1)):
        #for i, (demeaned_uncorrp_t1, demeaned_rawtest_t1) in enumerate(zip(demeaned_uncorrps_t1, demeaned_rawtests_t1)):
            ic = "{0:0=2d}".format(i)
            cluster_info_dir = join(working_dir, 'info_cluster_t0.95_corrp_t1')
            #cluster_info_dir = join(working_dir, 'info_cluster_t0.95_uncorrp_t1')
            if not os.path.exists(cluster_info_dir):
                os.mkdir(cluster_info_dir)
            cluster_info_output = join(cluster_info_dir, 't0.95_concatenated_{voxelsize}_{side}_nosmooth_IC{ic}_demeaned_t1.txt'.format(voxelsize=voxelsize, side=side, ic=ic))
            if not os.path.isfile(cluster_info_output):
                demeaned_corrp_t1_input = join(working_dir, demeaned_corrp_t1)
                #demeaned_uncorrp_t1_input = join(working_dir, demeaned_uncorrp_t1)
                demeaned_rawtest_t1_input = join(working_dir, demeaned_rawtest_t1)
                command = 'cluster -i {demeaned_corrp_t1_input} -t 0.95 -c {demeaned_rawtest_t1_input} --scalarname="1-p" > {cluster_info_output}'.format(demeaned_corrp_t1_input=demeaned_corrp_t1_input, demeaned_rawtest_t1_input=demeaned_rawtest_t1_input, cluster_info_output=cluster_info_output)
                #command = 'cluster -i {demeaned_uncorrp_t1_input} -t 0.95 -c {demeaned_rawtest_t1_input} --scalarname="1-p" > {cluster_info_output}'.format(demeaned_uncorrp_t1_input=demeaned_uncorrp_t1_input, demeaned_rawtest_t1_input=demeaned_rawtest_t1_input, cluster_info_output=cluster_info_output)
                os.popen(command).read

        for i, (demeaned_corrp_t2, demeaned_rawtest_t2) in enumerate(zip(demeaned_corrps_t2, demeaned_rawtests_t2)):
        #for i, (demeaned_uncorrp_t2, demeaned_rawtest_t2) in enumerate(zip(demeaned_uncorrps_t2, demeaned_rawtests_t2)):
            ic = "{0:0=2d}".format(i)
            cluster_info_dir = join(working_dir, 'info_cluster_t0.95_corrp_t2')
            #cluster_info_dir = join(working_dir, 'info_cluster_t0.95_uncorrp_t2')
            if not os.path.exists(cluster_info_dir):
                os.mkdir(cluster_info_dir)
            cluster_info_output = join(cluster_info_dir, 't0.95_concatenated_{voxelsize}_{side}_nosmooth_IC{ic}_demeaned_t2.txt'.format(voxelsize=voxelsize, side=side, ic=ic))
            if not os.path.isfile(cluster_info_output):
                demeaned_corrp_t2_input = join(working_dir, demeaned_corrp_t2)
                #demeaned_uncorrp_t2_input = join(working_dir, demeaned_uncorrp_t2)
                demeaned_rawtest_t2_input = join(working_dir, demeaned_rawtest_t2)
                command = 'cluster -i {demeaned_corrp_t2_input} -t 0.95 -c {demeaned_rawtest_t2_input} --scalarname="1-p" > {cluster_info_output}'.format(demeaned_corrp_t2_input=demeaned_corrp_t2_input, demeaned_rawtest_t2_input=demeaned_rawtest_t2_input, cluster_info_output=cluster_info_output)
                #command = 'cluster -i {demeaned_uncorrp_t2_input} -t 0.95 -c {demeaned_rawtest_t2_input} --scalarname="1-p" > {cluster_info_output}'.format(demeaned_uncorrp_t2_input=demeaned_uncorrp_t2_input, demeaned_rawtest_t2_input=demeaned_rawtest_t2_input, cluster_info_output=cluster_info_output)
                os.popen(command).read


        undemeaned_corrps_t1 = [ x for x in undemeaned_corrps if 'tstat1' in x ]
        undemeaned_corrps_t2 = [ x for x in undemeaned_corrps if 'tstat2' in x ]
        undemeaned_uncorrps_t1 = [ x for x in undemeaned_uncorrps if 'tstat1' in x ]
        undemeaned_uncorrps_t2 = [ x for x in undemeaned_uncorrps if 'tstat2' in x ]
        undemeaned_rawtests_t1 = [ x for x in undemeaned_rawtests if 'tstat1' in x ]
        undemeaned_rawtests_t2 = [ x for x in undemeaned_rawtests if 'tstat2' in x ]

        for i, (undemeaned_corrp_t1, undemeaned_rawtest_t1) in enumerate(zip(undemeaned_corrps_t1, undemeaned_rawtests_t1)):
        #for i, (undemeaned_uncorrp_t1, undemeaned_rawtest_t1) in enumerate(zip(undemeaned_uncorrps_t1, undemeaned_rawtests_t1)):
            ic = "{0:0=2d}".format(i)
            cluster_info_dir = join(working_dir, 'info_cluster_t0.95_corrp_t1')
            #cluster_info_dir = join(working_dir, 'info_cluster_t0.95_uncorrp_t1')
            if not os.path.exists(cluster_info_dir):
                os.mkdir(cluster_info_dir)
            cluster_info_output = join(cluster_info_dir, 't0.95_concatenated_{voxelsize}_{side}_nosmooth_IC{ic}_undemeaned_t1.txt'.format(voxelsize=voxelsize, side=side, ic=ic))
            if not os.path.isfile(cluster_info_output):
                undemeaned_corrp_t1_input = join(working_dir, undemeaned_corrp_t1)
                #undemeaned_uncorrp_t1_input = join(working_dir, undemeaned_uncorrp_t1)
                undemeaned_rawtest_t1_input = join(working_dir, undemeaned_rawtest_t1)
                command = 'cluster -i {undemeaned_corrp_t1_input} -t 0.95 -c {undemeaned_rawtest_t1_input} --scalarname="1-p" > {cluster_info_output}'.format(undemeaned_corrp_t1_input=undemeaned_corrp_t1_input, undemeaned_rawtest_t1_input=undemeaned_rawtest_t1_input, cluster_info_output=cluster_info_output)
                #command = 'cluster -i {undemeaned_uncorrp_t1_input} -t 0.95 -c {undemeaned_rawtest_t1_input} --scalarname="1-p" > {cluster_info_output}'.format(undemeaned_uncorrp_t1_input=undemeaned_uncorrp_t1_input, undemeaned_rawtest_t1_input=undemeaned_rawtest_t1_input, cluster_info_output=cluster_info_output)
                os.popen(command).read

        for i, (undemeaned_corrp_t2, undemeaned_rawtest_t2) in enumerate(zip(undemeaned_corrps_t2, undemeaned_rawtests_t2)):
        #for i, (undemeaned_uncorrp_t2, undemeaned_rawtest_t2) in enumerate(zip(undemeaned_uncorrps_t2, undemeaned_rawtests_t2)):
            ic = "{0:0=2d}".format(i)
            cluster_info_dir = join(working_dir, 'info_cluster_t0.95_corrp_t2')
            #cluster_info_dir = join(working_dir, 'info_cluster_t0.95_uncorrp_t2')
            if not os.path.exists(cluster_info_dir):
                os.mkdir(cluster_info_dir)
            cluster_info_output = join(cluster_info_dir, 't0.95_concatenated_{voxelsize}_{side}_nosmooth_IC{ic}_undemeaned_t2.txt'.format(voxelsize=voxelsize, side=side, ic=ic))
            if not os.path.isfile(cluster_info_output):
                undemeaned_corrp_t2_input = join(working_dir, undemeaned_corrp_t2)
                #undemeaned_uncorrp_t2_input = join(working_dir, undemeaned_uncorrp_t2)
                undemeaned_rawtest_t2_input = join(working_dir, undemeaned_rawtest_t2)
                command = 'cluster -i {undemeaned_corrp_t2_input} -t 0.95 -c {undemeaned_rawtest_t2_input} --scalarname="1-p" > {cluster_info_output}'.format(undemeaned_corrp_t2_input=undemeaned_corrp_t2_input, undemeaned_rawtest_t2_input=undemeaned_rawtest_t2_input, cluster_info_output=cluster_info_output)
                #command = 'cluster -i {undemeaned_uncorrp_t2_input} -t 0.95 -c {undemeaned_rawtest_t2_input} --scalarname="1-p" > {cluster_info_output}'.format(undemeaned_uncorrp_t2_input=undemeaned_uncorrp_t2_input, undemeaned_rawtest_t2_input=undemeaned_rawtest_t2_input, cluster_info_output=cluster_info_output)
                os.popen(command).read


    else:
        for i, (demeaned_corrp, demeaned_rawtest) in enumerate(zip(demeaned_corrps, demeaned_rawtests)):
        #for i, (demeaned_uncorrp, demeaned_rawtest) in enumerate(zip(demeaned_uncorrps, demeaned_rawtests)):
            ic = "{0:0=2d}".format(i)
            cluster_info_dir = join(working_dir, 'info_cluster_t0.95_corrp')
            #cluster_info_dir = join(working_dir, 'info_cluster_t0.95_uncorrp')
            if not os.path.exists(cluster_info_dir):
                os.mkdir(cluster_info_dir)
            cluster_info_output = join(cluster_info_dir, 't0.95_concatenated_{voxelsize}_{side}_nosmooth_IC{ic}_demeaned.txt'.format(voxelsize=voxelsize, side=side, ic=ic))
            if not os.path.isfile(cluster_info_output):
                demeaned_corrp_input = join(working_dir, demeaned_corrp)
                #demeaned_uncorrp_input = join(working_dir, demeaned_uncorrp)
                demeaned_rawtest_input = join(working_dir, demeaned_rawtest)
                command = 'cluster -i {demeaned_corrp_input} -t 0.95 -c {demeaned_rawtest_input} --scalarname="1-p" > {cluster_info_output}'.format(demeaned_corrp_input=demeaned_corrp_input, demeaned_rawtest_input=demeaned_rawtest_input, cluster_info_output=cluster_info_output)
                #command = 'cluster -i {demeaned_uncorrp_input} -t 0.95 -c {demeaned_rawtest_input} --scalarname="1-p" > {cluster_info_output}'.format(demeaned_uncorrp_input=demeaned_uncorrp_input, demeaned_rawtest_input=demeaned_rawtest_input, cluster_info_output=cluster_info_output)
                os.popen(command).read

        for i, (undemeaned_corrp, undemeaned_rawtest) in enumerate(zip(undemeaned_corrps, undemeaned_rawtests)):
        #for i, (undemeaned_uncorrp, undemeaned_rawtest) in enumerate(zip(undemeaned_uncorrps, undemeaned_rawtests)):
            ic = "{0:0=2d}".format(i)
            cluster_info_dir = join(working_dir, 'info_cluster_t0.95_corrp')
            #cluster_info_dir = join(working_dir, 'info_cluster_t0.95_uncorrp')
            if not os.path.exists(cluster_info_dir):
                os.mkdir(cluster_info_dir)
            cluster_info_output = join(cluster_info_dir, 't0.95_concatenated_{voxelsize}_{side}_nosmooth_IC{ic}_undemeaned.txt'.format(voxelsize=voxelsize, side=side, ic=ic))
            if not os.path.isfile(cluster_info_output):
                undemeaned_corrp_input = join(working_dir, undemeaned_corrp)
                #undemeaned_uncorrp_input = join(working_dir, undemeaned_uncorrp)
                undemeaned_rawtest_input = join(working_dir, undemeaned_rawtest)
                command = 'cluster -i {undemeaned_corrp_input} -t 0.95 -c {undemeaned_rawtest_input} --scalarname="1-p" > {cluster_info_output}'.format(undemeaned_corrp_input=undemeaned_corrp_input, undemeaned_rawtest_input=undemeaned_rawtest_input, cluster_info_output=cluster_info_output)
                #command = 'cluster -i {undemeaned_uncorrp_input} -t 0.95 -c {undemeaned_rawtest_input} --scalarname="1-p" > {cluster_info_output}'.format(undemeaned_uncorrp_input=undemeaned_uncorrp_input, undemeaned_rawtest_input=undemeaned_rawtest_input, cluster_info_output=cluster_info_output)
                os.popen(command).read



def fslstatsV(voxelsize, side, smoothing, IC):

    #working_dir = 'rsFC_Randomise_n80/NOR_only/{voxelsize}_{side}_{smoothing}_{IC}ICs/NOR_nocov_1_sample_tfce/cluster_t0.95_corrp'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC) 
    working_dir = 'rsFC_Randomise_n80/NOR_only/{voxelsize}_{side}_{smoothing}_{IC}ICs/FEP_nocov_1_sample_tfce/cluster_t0.95_corrp'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC) 

    imgs = [ x for x in os.listdir(working_dir) if 'nii.gz' in x]
    save_txt = join(working_dir, 'fslstatsV.txt')
    if not os.path.isfile(save_txt):
        for img in imgs:
            img_input = join(working_dir, img)
            output = open(save_txt, 'a')
            command = 'fslstats {img_input} -V'.format(img_input=img_input)
            out = os.popen(command)
            result = out.read()
            output.write(img + '\n' + result)









if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--voxelsize', '-vox', nargs=1, type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--smoothing', '-smooth', nargs=1,  help = 'e.g., nosmooth, fwhm6, fwhm6preproc', type=str)
	parser.add_argument('--IC', '-IC', nargs=1, help = 'e.g., 10 or 20', type=str)

	args = parser.parse_args()

	mergePerIC(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
	randomise(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
	threshold(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
	clusterInfo(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
	fslstatsV(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
