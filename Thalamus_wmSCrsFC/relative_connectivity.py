import os 
import re
import sys
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import pandas as pd



def extractRelConn(mICA, side, voxelsize, smoothing):
    
    glm_dir = 'tica_results/{mICA}/dim0/glm_out'.format(mICA=mICA)

    melodicIC_loc = 'tica_results/{mICA}/dim0/melodic_IC.nii.gz'.format(mICA=mICA)
    melodicIC_map = nb.load(melodicIC_loc)
    componentNum = melodicIC_map.shape[3]
    
    IC_connectivity = 'WMconnectivity_{side}_{voxelsize}_{smoothing}.csv'.format(side=side, voxelsize=voxelsize, smoothing=smoothing)
    if not os.path.isfile(IC_connectivity):
        allData = []
        log = 'subject_list_37FEP36HC.txt'
        with open(log, 'r') as f:
            lines = f.read().split()
        imgInputs = []
        for line in lines:
            dataLoc = join (glm_dir, line)
            ICs=["%02d" % x for x in range(1,componentNum+1)]
            for ic in ICs:
                dataFile = '_stage2_thresh_zstat00{ic}.nii.gz'.format(ic=ic)
                imgInputs.append(dataLoc+dataFile)

        for line in lines:
            for ic in ICs:
                imgs = [x for x in imgInputs if '{line}_stage2_thresh_zstat00{ic}.nii.gz'.format(line=line, ic=ic) in x]
                for img in imgs:
                    im = nb.load(img).get_data()
                    ic_connectivity = sum(im[im != 0])
                    allData.append((line, ic, ic_connectivity))

        df = pd.DataFrame(allData)
        df.columns = ['subject', 'IC_number.', 'IC_connectivity']

        df.to_csv(IC_connectivity)

    df = pd.read_csv(IC_connectivity, index_col=0)
    df['side'] = '{side}'.format(side=side)
    df['voxel_size'] = '{voxelsize}'.format(voxelsize=voxelsize)
    df['spatial_smoothing'] = '{smoothing}'.format(smoothing=smoothing)
    total_connectivity_sum = df.groupby(['subject']).sum().reset_index()
    total_connectivity_sum.columns = ['subject', 'added_IC_numbers', 'Total_connectivity']
    new_df = pd.merge(df, total_connectivity_sum, on=['subject'], how='inner')
    new_df['Relative_connectivity'] = new_df.IC_connectivity / new_df.Total_connectivity


    demo = pd.read_csv('37FEP_36HC_demo.csv')
    demo.columns = ['subject', 'sex', 'age']
    for_stats = pd.merge(new_df, demo, on=['subject'], how='inner')
    
    for_stats.to_csv(IC_connectivity)






if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--mICA', '-mICA', nargs=1, help = 'mICA output directory', type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., 3mm', type=str)
	parser.add_argument('--smoothing', '-FWHM', nargs=1, help = 'e.g., 4fwhm', type=str)
	args = parser.parse_args()

        extractRelConn(args.mICA[0], args.side[0], args.voxelsize[0], args.smoothing[0])

    

