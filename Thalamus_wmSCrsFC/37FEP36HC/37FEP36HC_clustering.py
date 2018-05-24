import os
from os.path import join, basename, isfile, isdir
import sys
import re
import argparse
import nibabel as nb
import numpy as np
from scipy import stats
from sklearn.cluster import AffinityPropagation


def similarity(mode):

    ave_dir = '37FEP36HC_averaged_{mode}'.format(mode=mode)
    sim_dir = join(ave_dir, 'similarity')
    if not os.path.exists(sim_dir):
        os.mkdir(sim_dir)

    imgInputs = []
    l_dir = join(ave_dir, 'left_ds3')
    l_inputs = os.listdir(l_dir)
    l_componentNum = len([x for x in l_inputs if x.startswith('all')])
    l_ICs = ["%02d" % x for x in range(1,l_componentNum+1)]
    for l_ic in l_ICs:
        for l_input in l_inputs:
            if l_input.startswith('all') and l_input.endswith('IC{l_ic}.nii.gz'.format(l_ic=l_ic)):
                imgInputs.append(l_dir+'/'+l_input)

    r_dir = join(ave_dir, 'right_ds3')
    r_inputs = os.listdir(r_dir)
    r_componentNum = len([x for x in r_inputs if x.startswith('all')])
    r_ICs = ["%02d" % x for x in range(1,r_componentNum+1)]
    for r_ic in r_ICs:
        for r_input in r_inputs:
            if r_input.startswith('all') and r_input.endswith('IC{r_ic}.nii.gz'.format(r_ic=r_ic)):
                imgInputs.append(r_dir+'/'+r_input)


    for x in imgInputs:
        base = os.path.basename(x)
        name = base.split('.')[0]
        flat = join(sim_dir, 'flat_{name}'.format(name=name))
        if not os.path.isfile(flat):
            a = nb.load(x)
            b = a.get_data()
            c = b.flatten()
            np.savetxt(flat, c)


    corrInputs = []
    for l_ic in l_ICs:
        l_X = [i for i in os.listdir(sim_dir) if i.startswith('flat') and i.endswith('left_ds3_IC{l_ic}'.format(l_ic=l_ic))]
        for lx_entry in l_X:
            corrInputs.append(sim_dir+'/'+lx_entry)
    for r_ic in r_ICs:
        r_X = [i for i in os.listdir(sim_dir) if i.startswith('flat') and i.endswith('right_ds3_IC{r_ic}'.format(r_ic=r_ic))]
        for rx_entry in r_X:
            corrInputs.append(sim_dir+'/'+rx_entry)


    for x in corrInputs:
        base = os.path.basename(x)
        CORRxy = join (sim_dir, 'correlate_mat_{base}'.format(base=base))
        if not os.path.isfile(CORRxy):
            X = np.loadtxt(x)
            print(base)
            initial = np.zeros((1,))
            for y in corrInputs:
                Y= np.loadtxt(y)
                pearson_corr = stats.pearsonr(X,Y)
                corr = pearson_corr[0:1]
                corr = np.array(corr)
                initial = np.append(initial, corr)
                np.savetxt(CORRxy, initial)


    CORRXY = join(sim_dir, 'correlate_similarity_matrix')
    if not os.path.isfile(CORRXY):
        to_append = []
        l_xs = [i for i in os.listdir(sim_dir) if 'correlate_mat_flat_all_ave_left' in i]
        l_componentNum = len(l_xs)
        l_ICs = ["%02d" % x for x in range(1,l_componentNum+1)] 
        for l_ic in l_ICs:
            for l_x in l_xs:
                if 'IC{l_ic}'.format(l_ic=l_ic) in l_x:
                    to_append.append(sim_dir+'/'+l_x)
        r_xs = [i for i in os.listdir(sim_dir) if 'correlate_mat_flat_all_ave_right' in i]
        r_componentNum = len(r_xs)
        r_ICs = ["%02d" % x for x in range(1,r_componentNum+1)] 
        for r_ic in r_ICs:
            for r_x in r_xs:
                if 'IC{r_ic}'.format(r_ic=r_ic) in r_x:
                    to_append.append(sim_dir+'/'+r_x)
    #print(to_append)
        array_append = []
        for x in to_append:
            arr = np.loadtxt(x)
            arr = np.delete(arr, 0)
            #print(arr.shape)
            array_append.append(arr)
        #print(array_append)
        XY = np.concatenate(array_append)
        print(XY.shape)
        result = XY.reshape((60, 60))
        print(result) 
        np.savetxt(CORRXY, result)
















if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--mode', '-mode', nargs=1, help = 'wmSC or rsFC', type=str)
	args = parser.parse_args()

        similarity(args.mode[0])

