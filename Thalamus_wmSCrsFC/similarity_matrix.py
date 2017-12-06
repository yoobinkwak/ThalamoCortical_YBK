import os
from os.path import join, basename, isfile, isdir
import sys
import re
import argparse
import nibabel as nb
import numpy as np

#a = nb.load('all_ave_left_ds3_IC01.nii.gz')
#b = a.get_data()
#c = nb.load('all_ave_left_ds3_IC02.nii.gz')
#d = c.get_data()
#x = b.flatten()
#y = d.flatten()
#corr = np.corrcoef(x,y)



wm_dir = '37FEP36HC_averaged_wmSC'
sim_dir = join(wm_dir, 'similarity_matrix')
if not os.path.exists(sim_dir):
        os.mkdir(sim_dir)

imgInputs = []
l_dir = join(wm_dir, 'left_ds3')
l_inputs = os.listdir(l_dir)
l_componentNum = len([x for x in l_inputs if x.startswith('all')])
l_ICs = ["%02d" % x for x in range(1,l_componentNum+1)] 
for l_ic in l_ICs:
    for l_input in l_inputs:
        if l_input.startswith('all') and l_input.endswith('IC{l_ic}.nii.gz'.format(l_ic=l_ic)):
            imgInputs.append(l_dir+'/'+l_input)

r_dir = join(wm_dir, 'right_ds3')
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
    #print(flat)

corrInputs = []
for l_ic in l_ICs:
    l_X = [i for i in os.listdir(sim_dir) if i.startswith('flat') and i.endswith('left_ds3_IC{l_ic}'.format(l_ic=l_ic))]
    for lx_entry in l_X:
        corrInputs.append(sim_dir+'/'+lx_entry)
for r_ic in r_ICs:
    r_X = [i for i in os.listdir(sim_dir) if i.startswith('flat') and i.endswith('right_ds3_IC{r_ic}'.format(r_ic=r_ic))]
    for rx_entry in r_X:
        corrInputs.append(sim_dir+'/'+rx_entry)
#print(corrInputs)

for x in corrInputs:
    base = os.path.basename(x)
    corr_xY = join (sim_dir, 're_mat_{base}'.format(base=base))
    if not os.path.isfile(corr_xY):
        X = np.loadtxt(x)
        print(base)
        init = np.zeros((2,2))
        for y in corrInputs:
            Y= np.loadtxt(y)
            print(y)
            corr = np.corrcoef(X,Y)
            print(corr)
            init = np.append(init, corr, axis=1)
            print(init)
            print(init.shape)
            np.savetxt(corr_xY, init)

corr_XY = join(sim_dir, 'similarity_matrix')
if not os.path.isfile(corr_XY):
    to_append = []
    l_xs = [i for i in os.listdir(sim_dir) if 're_mat_flat_all_ave_left' in i]
    l_componentNum = len(l_xs)
    l_ICs = ["%02d" % x for x in range(1,l_componentNum+1)] 
    for l_ic in l_ICs:
        for l_x in l_xs:
            if 'IC{l_ic}'.format(l_ic=l_ic) in l_x:
                to_append.append(sim_dir+'/'+l_x)
    r_xs = [i for i in os.listdir(sim_dir) if 're_mat_flat_all_ave_right' in i]
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
        #print(arr.shape)
        array_append.append(arr)
    #print(array_append)
    XY = np.concatenate(array_append)
    #print(XY.shape)
    drop_init1 = np.delete(XY, 0, 1)
    drop_init2 = np.delete(drop_init1, 0, 1)
    #print(drop_init2.shape)
    np.savetxt(corr_XY, drop_init2)

















