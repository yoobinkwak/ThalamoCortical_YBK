import os
import os.path.join as join
import pandas as pd
import numpy as np
import nibabel as nb

for subject in [x for x in os.listdir(os.getcwd()) if x.startswith(('C','F','N'))]:
    ts_directory = '{subject}/timeSeries'.format(subject=subject)
    ds_rate = '5ds', '4ds', '3ds'
    for ds in ds_rate:
        # meants text file
        wb_txt = join(ts_directory, '{ds}_filtered_func_showall.txt'.format(ds=ds))
        thal_txt = join(ts_directory, '{ds}_B_thalamus_masked_showall.txt'.format(ds=ds))

        # can use np.loadtxt
        a = pd.read_csv(wb_txt, delim_whitespace=True, header=None, skiprows=3, index_col=None)
        b = pd.read_csv(thal_txt, delim_whitespace=True, header=None, skiprows=3, index_col=None)

        # why save ?
        a.to_csv(join(ts_directory, 'edit_wb_{ds}_ts.csv').format(ds=ds), index=False, index_label=False)
        b.to_csv(join(ts_directory, 'edit_thal_{ds}_ts.csv').format(ds=ds), index=False, index_label=False)

        c = pd.read_csv('{subject}/timeSeries/edit_wb_{ds}_ts.csv'.format(subject=subject, ds=ds))
        wb_matrix = np.array(c)
        print(wb_matrix.shape)			

        d = pd.read_csv('{subject}/timeSeries/edit_thal_{ds}_ts.csv'.format(subject=subject, ds=ds))
        thal_matrix = np.array(d)
        print(thal_matrix.shape)

        #load downsampled image
        wb_img = '{subject}/downsampled/{ds}_filtered_func_data.nii.gz'.format(subject=subject, ds=ds)
        thal_img = '{subject}/downsampled/{ds}_B_thal_on_filtered_func_data.nii.gz'.format(subject=subject, ds=ds)

        wb = nb.load(wb_img)
        thal = nb.load(thal_img)

        wbd = wb.get_data()
        thald = thal.get_data()
        print(wbd.shape)
        print(thald.shape)

        volume_shape = wbd.shape[:-1]
        coords = list(np.ndindex(volume_shape))
        thal_x, thal_y, thal_z = np.where(thald[:,:,:,0] != 0)
        thal_coords = np.array((thal_x, thal_y, thal_z)).T
        print(thal_coords.shape)

        m_wb_ts = wb_matrix - wb_matrix.mean(1)[:,None]
        m_thal_ts = thal_matrix - thal_matrix.mean(1)[:,None]

        ss_wb_ts = (m_wb_ts**2).sum(0)
        ss_thal_ts = (m_thal_ts**2).sum(0)

        corrMap = np.dot(m_wb_ts.T,m_thal_ts)/np.sqrt(np.dot(ss_wb_ts[:,None],ss_thal_ts[None]))
        print(corrMap.shape)

        corrMap_reshape = corrMap.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))

        img = nb.Nifti1Image(corrMap_reshape, affine=thal.affine)
        img.to_filename(os.path.join(ts_directory, 'not_fisherZ_{ds}.nii.gz').format(ds=ds))


        fisherZ = np.arctanh(corrMap)
        fisherZ_reshape = fisherZ.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))
        img = nb.Nifti1Image(fisherZ_reshape, affine=thal.affine)
        img.to_filename(os.path.join(ts_directory, 'fisherZ_{ds}.nii.gz').format(ds=ds))




        



#### as array

#a = pd.read_csv('timeSeries/edit_thalamus_ts.csv', header=None)        ### should include "index_col=None", as well..?
#thal_matrix = np.array(a)
#
#b = pd.read_csv('timeSeries/edit_wb_ts.csv', header=None)              ### should include "index_col=None", as well..?
#wb_matrix = np.array(b)
#
#
#
###### correlation
#
#wb_img = 'downsampled/5ds_filtered_func_data.nii.gz'
#thal_img = 'downsampled/5ds_B_thal_on_filtered_func_data.nii.gz'
#
#wb = nb.load(wb_img)
#thal = nb.load(thal_img)
#
#wbd = wb.get_data()
#thald = thal.get_data()
#
#volume_shape = wbd.shape[:-1]
#coords = list(np.ndindex(volume_shape))
#thal_x, thal_y, thal_z = np.where(thald[:,:,:,0] != 0)
#thal_coords = np.array((thal_x, thal_y, thal_z)).T
#
#
#
#m_wb_ts = wb_matrix - wb_matrix.mean(1)[:,None]
#m_thal_ts = thal_matrix - thal_matrix.mean(1)[:,None]
#
#ss_wb_ts = (m_wb_ts**2).sum(0)
#ss_thal_ts = (m_thal_ts**2).sum(0)
#
#corrMap = np.dot(m_wb_ts.T,m_thal_ts)/np.sqrt(np.dot(ss_wb_ts[:,None],ss_thal_ts[None]))
#
#
#
#corrMap_reshape = corrMap.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))
#
#img = nb.Nifti1Image(corrMap_reshape, affine=thal.affine)
#img.to_filename('timeSeries/not_fisherZ_{ds}.nii.gz').format(ds=ds)
#
#
#fisherZ = np.arctanh(corrMap)
#fisherZ_reshape = fisherZ.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))
#img = nb.Nifti1Image(fisherZ_reshape, affine=thal.affine)
#img.to_filename('timeSeries/fisherZ_{ds}.nii.gz').format(ds=ds)


