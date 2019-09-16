import os
from os.path import join, basename, dirname, isfile, isdir
import re
import nibabel as nb
import numpy as np
import pandas as pd
# import pp
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
#get_ipython().magic(u'matplotlib inline')

# from __future__ import division
import pickle

import glob


def get_brain_figures(imgLoc_or_img_data, 
                      title='title', outputDir='', 
                      save=False, axial=True, 
                      thalamus_highlight=False):
    # Read nifty images
    try:
        img = nb.load(imgLoc_or_img_data)
        data = img.get_data()
    # if imgLoc_or_img_data is already a matrix
    except:
        data = imgLoc_or_img_data
    
    # figure height
    if axial:
        fig_height=5.5
    else:
        fig_height=4
    
    # make frame
    fig, axes = plt.subplots(ncols=4, # number of columns in the figure
                             nrows=2, # number of rows in the figure
                             figsize=(9, fig_height), 
                             dpi=100, # resolution
                             gridspec_kw={'wspace':0, 'hspace':0}, # space between axes
                             squeeze=True)
        
    # Lowest slice number to show
    # axial view
    if axial:
        if thalamus_highlight:
            slice_num=23
        else:
            slice_num=20
            
    # sagittal view
    else:
        #slice_num=15
        if thalamus_highlight:
            slice_num=30
        else:
            slice_num=15
    
    # loop through axes
    for num, ax in enumerate(np.ravel(axes)):       
        if axial:
            if thalamus_highlight:
                mni_2d_slice = np.flipud(mni_3mm_smoothed_data[15:45, 25:45, slice_num].T)
                thalamus_mask_data_masked = np.flipud(np.ma.masked_where(thalamus_mask_data < 1, 
                                                                         thalamus_mask_data)[15:45, 25:45, slice_num].T)
                #img_2d_slice = np.flipud(np.ma.masked_where(data < 2.3, data)[15:45, 25:45, slice_num].T)
                img_2d_slice = np.flipud(np.ma.masked_where(data == 0, data)[15:45, 25:45, slice_num].T)
               
                
            else:
                mni_2d_slice = np.flipud(mni_3mm_smoothed_data[:, :, slice_num].T)
                img_2d_slice = np.flipud(np.ma.masked_where(data < 2.3, data)[:, :, slice_num].T)
                #img_2d_slice = np.flipud(np.ma.masked_where(data == 0 , data)[:, :, slice_num].T)

                

                    # MNI background
        else:
            if thalamus_highlight:
                thalamus_mask_data_masked = np.flipud(np.ma.masked_where(thalamus_mask_data < 1, 
                                                                         #thalamus_mask_data)[slice_num, :, :].T)
                                                                         ##thalamus_mask_data)[slice_num, 25:45, 15:45].T)
                                                                         thalamus_mask_data)[slice_num, 25:45, 20:26].T)
                #mni_2d_slice = np.flipud(mni_3mm_smoothed_data[slice_num, :, :].T)
                ##mni_2d_slice = np.flipud(mni_3mm_smoothed_data[slice_num, 25:45, 15:45].T)
                mni_2d_slice = np.flipud(mni_3mm_smoothed_data[slice_num, 25:45, 20:26].T)
                #img_2d_slice = np.flipud(np.ma.masked_where(data < 2.3, data)[slice_num, :, :].T)
                ##img_2d_slice = np.flipud(np.ma.masked_where(data == 0, data)[slice_num, 25:45, 15:45].T)
                img_2d_slice = np.flipud(np.ma.masked_where(data == 0, data)[slice_num, 25:45, 20:26].T)

            else:
                mni_2d_slice = np.flipud(mni_3mm_smoothed_data[slice_num, :, :].T)
                #img_2d_slice = np.flipud(np.ma.masked_where(data < 2.3, data)[slice_num, :, :].T)
                img_2d_slice = np.flipud(np.ma.masked_where(data == 0 , data)[slice_num, :, :].T)



        ax.imshow(mni_2d_slice, cmap=plt.cm.gray)
        if thalamus_highlight:
            ax.imshow(thalamus_mask_data_masked, 
                      cmap='coolwarm', 
                      alpha=0.3)
            
        zthrmap = ax.imshow(img_2d_slice, cmap='autumn', 
                            vmin=2.3,
                             vmax=6)
        
#        zthrmap = ax.imshow(img_2d_slice, cmap='autumn',
#                            vmin=0,
#                            vmax=1)
                            
        # remove labels
        ax.set_xticklabels('')
        ax.set_yticklabels('')
        ax.set_xticks([])
        ax.set_yticks([])

        # Coordinate
        if axial:
            new_coord = mni_3mm_smoothed_img.affine[:3, :3].dot([0,0,slice_num]) + mni_3mm_smoothed_img.affine[:3,3]
            ax.set_xlabel(int(new_coord[-1]), fontsize=15)
            if thalamus_highlight:
                slice_num = slice_num + 1
            else:
                slice_num = slice_num + 3

        else:
            new_coord = mni_3mm_smoothed_img.affine[:3, :3].dot([slice_num, 0,0]) + mni_3mm_smoothed_img.affine[:3,3]
            ax.set_xlabel(int(new_coord[0]), fontsize=15)
            slice_num = slice_num + 4

        
    fig.suptitle(title, y=0.9)

    # Add axes for the colorbar at the right side of the figure
    fig.subplots_adjust(right=0.8)
    # [*left*, *bottom*, *width*,*height*]
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])

    cbar = fig.colorbar(zthrmap, 
                        cax=cbar_ax, 
                        format='%0.1f')
    cbar.set_label('Z values', fontsize=15)
    cbar.ax.tick_params(labelsize=15)
    cbar.ax.yaxis.set_label_position('left')
    
    if save==False:
        pass
    else:
        if not isdir(outputDir):
            os.mkdir(outputDir)
        fig.savefig('{}/{}.png'.format(outputDir, title))
        plt.close()



mni_3mm_smoothed_loc = 'masks/mni_brain_ds3.nii.gz'
mni_3mm_smoothed_img = nb.load(mni_3mm_smoothed_loc)
mni_3mm_smoothed_data = mni_3mm_smoothed_img.get_data()


thalamus_mask_loc = 'masks/bi_thalamus_HOSC_60_ds3.nii.gz'
thalamus_mask_img = nb.load(thalamus_mask_loc)
thalamus_mask_data = thalamus_mask_img.get_data()



#images = glob.glob('rsFC_ICA_cmd/NOR_only/NOR_ds3_bi_20ICs_masked/vol*') 

#df = pd.DataFrame({'location':images})
#df['number'] = df['location'].str.findall('00(\d{2})').str[0]



#for index, row in df.iterrows():
#    get_brain_figures(row['location'], 
#                      title='IC{}_axial'.format(row['number']),
#                      outputDir='figures_20190902/nosmooth_20/ICA/axial', 
#                      save=True)
    
#    get_brain_figures(row['location'], 
#                     title='IC{}_sagittal'.format(row['number']),
#                     outputDir='figures_20190902/nosmooth_20/ICA/sagittal', 
#                     save=True,
#                     axial=False)



source_images = glob.glob('rsFC_Randomise_n80/NOR_only/ds3_bi_nosmooth_20ICs/NOR_nocov_1_sample_tfce/cluster_t0.95_corrp/*_dem*') 

s_df = pd.DataFrame({'location':source_images})
s_df['number'] = s_df['location'].str.findall('IC(\d{2})').str[0]
s_df['stat'] = s_df['location'].str.findall('(tstat1|tstat2)').str[0]



for s_image in source_images:
    s_img = nb.load(s_image)
    s_data = s_img.get_data()
    check = np.nonzero(s_data)



for index, row in s_df.iterrows():
#    get_brain_figures(row['location'], 
#                      title='IC{}_{}_source_axial'.format(row['number'], row['stat']),
#                      outputDir='figures_20190902/nosmooth_20/IC_source_1sample_NOR/axial',
#                      thalamus_highlight=True,
#                      save=True)
    get_brain_figures(row['location'], 
                      title='IC{}_{}_source_sagittal'.format(row['number'], row['stat']),
                      outputDir='figures_20190724/nosmooth_20/IC_source_1sample_NOR/saggital', 
                      save=True,
                      thalamus_highlight=True,
                      axial=False)
#    get_brain_figures(row['location'], 
#                      title='IC{}_{}_source_sagittal'.format(row['number'], row['stat']),
#                      outputDir='figures_20190902/nosmooth_20/IC_source_1sample_NOR/brain_saggital', 
#                      save=True,
#                      axial=False)




#images = glob.glob('/Users/yoobinkwak/Desktop/wmSC_ave/ds3_bi_nosmooth_20ICs/*') 
#images = glob.glob('wmSC_ave/9*') 

#df = pd.DataFrame({'location':images})
##df['thr'] = df['location'].str.findall('(10thrP|20thrP|90thrP|95thrP)').str[0]
#df['thr'] = df['location'].str.findall('(90thrP|95thrP)').str[0]
#df['group'] = df['location'].str.findall('(all|FEP|NOR)').str[0]
#df['number'] = df['location'].str.findall('IC(\d{2})').str[0]
#df.head()
#df


#for index, row in df.iterrows():
    #get_brain_figures(row['location'], 
    #                  title='IC{}_wmSC_{}_{}_axial'.format(row['number'], row['thr'], row['group']),
    #                  outputDir='wmSC/{}/axial'.format(row['thr']), 
    #                  save=True)
    
#    get_brain_figures(row['location'], 
#                     title='IC{}_wmSC_{}_{}_sagittal'.format(row['number'],row['thr'], row['group']),
#                      outputDir='wmSC/{}/saggital'.format(row['thr']), 
#                      save=True,
#                      axial=False)




#images = glob.glob('step2_2group_tfce/cluster_t0.95_corrp/*_demea*') 
#images = glob.glob('/Users/yoobinkwak/Desktop/rsFC_Randomise_n80/ds3_bi_nosmooth_20ICs/two_step_randomise/nocov_1_sample_tfce/step2_2group_tfce/*_demeaned_tfce_corrp_*') 

#df = pd.DataFrame({'location':images})
#df['stat'] = df['location'].str.findall('(tstat1|tstat2)').str[0]
#df['number'] = df['location'].str.findall('IC(\d{2})').str[0]
#df.head()
#df



#for index, row in df.iterrows():
    #get_brain_figures(row['location'], 
    #                  title='IC{}_rsFC_{}_axial'.format(row['number'], row['stat']),
    #                  outputDir='IC_rsFC/axial', 
    #                  save=True)
    
#    get_brain_figures(row['location'], 
#                     title='IC{}_rsFC_{}_sagittal'.format(row['number'], row['stat']),
#                      outputDir='/IC_rsFC/saggital', 
#                      save=False,
#                      axial=False)

