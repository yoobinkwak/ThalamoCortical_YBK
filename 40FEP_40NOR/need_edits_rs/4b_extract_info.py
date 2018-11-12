import sys, os
from os.path import join, basename, isfile, isdir
import argparse
#from subprocess import Popen, PIPE
import subprocess

def clusterInfo(voxelsize, side, IC, compare):
    
    #working_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_nosmooth_{IC}ICs/{compare}_tfce'.format(voxelsize=voxelsize, side=side, IC=IC, compare=compare)
    #working_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_fwhm6_{IC}ICs/{compare}_tfce'.format(voxelsize=voxelsize, side=side, IC=IC, compare=compare)
    working_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_fwhm6preproc_{IC}ICs/{compare}_tfce'.format(voxelsize=voxelsize, side=side, IC=IC, compare=compare)
    imgs = [ x for x in os.listdir(working_dir) if 'nii.gz' in x]

    demeaned = [ x for x in imgs if 'demeaned' in x ] 
    demeaned_corrps = [ x for x in demeaned if 'tfce_corrp' in x ]
    demeaned_uncorrps = [ x for x in demeaned if 'tfce_p' in x ]
    demeaned_rawtests = [ x for x in demeaned if 'tfce' not in x ]
    
    undemeaned = [ x for x in imgs if 'demeaned' not in x ] 
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
    #if not(x.endswith('tstat2.nii.gz') for x in os.listdir(working_dir)):
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

    




def fslstatsV(voxelsize, side, IC, compare):
    
    #working_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_nosmooth_{IC}ICs/{compare}_tfce/cluster_t0.95_corrp'.format(voxelsize=voxelsize, side=side, IC=IC, compare=compare)
    #working_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_fwhm6_{IC}ICs/{compare}_tfce/cluster_t0.95_corrp'.format(voxelsize=voxelsize, side=side, IC=IC, compare=compare)
    working_dir = 'rsFC_Randomise_n80/{voxelsize}_{side}_fwhm6preproc_{IC}ICs/{compare}_tfce/cluster_t0.95_corrp'.format(voxelsize=voxelsize, side=side, IC=IC, compare=compare)
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
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., ds3', type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'bi, left or right', type=str)
	parser.add_argument('--IC', '-IC', nargs=1, help = 'e.g., 10 or 20', type=str)
	parser.add_argument('--compare', '-compare', nargs=1, help = '1_sample or 2_group or nocov_1_sample or nocov_2_group', type=str)
        args = parser.parse_args()
            
        clusterInfo(args.voxelsize[0], args.side[0], args.IC[0], args.compare[0])
        fslstatsV(args.voxelsize[0], args.side[0], args.IC[0], args.compare[0])

