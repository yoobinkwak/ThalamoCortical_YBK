import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image


### merged randmoise inputs manually copied from "inputs" to "selected_ICs/selected_inputs"


def randomise(voxelsize, side, smoothing, IC):

    randomise_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_{smoothing}_{IC}ICs/selected_ICs'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)

    randomise_input_dir = join(randomise_dir, 'selected_inputs')

    two_group_tfce_out_dir = join(randomise_dir, '2_group_tfce')
    if not os.path.exists(two_group_tfce_out_dir):
        os.mkdir(two_group_tfce_out_dir)

    nocov_one_sample_tfce_out_dir = join(randomise_dir, 'nocov_1_sample_tfce')
    if not os.path.exists(nocov_one_sample_tfce_out_dir):
        os.mkdir(nocov_one_sample_tfce_out_dir)

    one_sample_tfce_out_dir = join(randomise_dir, '1_sample_tfce')
    if not os.path.exists(one_sample_tfce_out_dir):
        os.mkdir(one_sample_tfce_out_dir)

    nocov_two_group_tfce_out_dir = join(randomise_dir, 'nocov_2_group_tfce')
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

        nocov_one_sample_tfce_output_name = join(nocov_one_sample_tfce_out_dir, '{output_name}'.format(output_name=output_name))
        nocov_one_sample_tfce_output = join(nocov_one_sample_tfce_out_dir, '{output_name}_tfce_corrp_tstat1.nii.gz'.format(output_name=output_name))
        if not os.path.isfile(nocov_one_sample_tfce_output):
            command = 'randomise -i {rand_inputs} -o {nocov_one_sample_tfce_output_name} -1 -T --uncorrp'.format(rand_inputs=rand_inputs, nocov_one_sample_tfce_output_name=nocov_one_sample_tfce_output_name)
            os.popen(command).read

        one_sample_tfce_output_name = join(one_sample_tfce_out_dir, '{output_name}'.format(output_name=output_name))
        one_sample_tfce_output = join(one_sample_tfce_out_dir, '{output_name}_tfce_corrp_tstat1.nii.gz'.format(output_name=output_name))
        if not os.path.isfile(one_sample_tfce_output):
            mat = 'designs/1group_80n_design.mat'
            con = 'designs/1group_nocov_design.con'
            command = 'randomise -i {rand_inputs} -o {one_sample_tfce_output_name} -d {mat} -t {con} -T --uncorrp'.format(rand_inputs=rand_inputs, one_sample_tfce_output_name=one_sample_tfce_output_name, mat=mat, con=con)
            os.popen(command).read
        
        nocov_two_group_tfce_output_name = join(nocov_two_group_tfce_out_dir, '{output_name}'.format(output_name=output_name))
        nocov_two_group_tfce_output = join(nocov_two_group_tfce_out_dir, '{output_name}_tfce_corrp_tstat1.nii.gz'.format(output_name=output_name))
        if not os.path.isfile(nocov_two_group_tfce_output):
            mat = 'designs/2group_80n_nocov_design.mat'
            con = 'designs/2group_nocov_design.con'
            command = 'randomise -i {rand_inputs} -o {nocov_two_group_tfce_output_name} -d {mat} -t {con} -T --uncorrp'.format(rand_inputs=rand_inputs, nocov_two_group_tfce_output_name=nocov_two_group_tfce_output_name, mat=mat, con=con)
            os.popen(command).read




def threshold(voxelsize, side, smoothing, IC):

    randomise_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_{smoothing}_{IC}ICs/selected_ICs'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)

    #two_group_tfce_out_dir = join(randomise_dir, '2_group_tfce')
    #two_group_tfce_out_dir = join(randomise_dir, 'nocov_1_sample_tfce')
    two_group_tfce_out_dir = join(randomise_dir, '1_sample_tfce')

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





def clusterInfo(voxelsize, side, smoothing, IC):

    #working_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_{smoothing}_{IC}ICs/selected_ICs/2_group_tfce'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
    #working_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_{smoothing}_{IC}ICs/selected_ICs/nocov_1_sample_tfce'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
    working_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_{smoothing}_{IC}ICs/selected_ICs/1_sample_tfce'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)

    imgs = [ x for x in os.listdir(working_dir) if 'nii.gz' in x]

    demeaned = [ x for x in imgs if '_demeaned_' in x ]
    demeaned_corrps = [ x for x in demeaned if 'tfce_corrp' in x ]
    demeaned_uncorrps = [ x for x in demeaned if 'tfce_p' in x ]
    demeaned_rawtests = [ x for x in demeaned if 'tfce' not in x ]

    undemeaned = [ x for x in imgs if '_undemeaned_' in x ]
    undemeaned_corrps = [ x for x in undemeaned if 'tfce_corrp' in x ]
    undemeaned_uncorrps = [ x for x in undemeaned if 'tfce_p' in x ]
    undemeaned_rawtests = [ x for x in undemeaned if 'tfce' not in x ]


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

    #working_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_{smoothing}_{IC}ICs/selected_ICs/2_group_tfce/cluster_t0.95_corrp'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
    #working_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_{smoothing}_{IC}ICs/selected_ICs/nocov_1_sample_tfce/cluster_t0.95_corrp'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
    working_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_{smoothing}_{IC}ICs/selected_ICs/1_sample_tfce/cluster_t0.95_corrp'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
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

	randomise(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
	threshold(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
	clusterInfo(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
	fslstatsV(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
