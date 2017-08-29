import os
import numpy as np
import nibabel as nb
import nilearn
import scipy


for subject in os.listdir(os.getcwd()):
    if subject.startswith(('C','F','N')):
        img_directory = '{subject}/downsampled'.format(subject=subject)
        ds_rate = '5ds', '4ds', '3ds'
        for ds in ds_rate:
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

            thald_nonzero = thald[np.where(thald[:,:,:,0] != 0)]
            print(thald_nonzero.shape)

            wbd_reshape = wbd.reshape(len(coords), wbd.shape[3])
            thald_reshape = thald_nonzero.reshape(len(thal_coords), wbd.shape[3])


            m_wb_ts = wbd_reshape - wbd_reshape.mean(1)[:,None] 
            m_thal_ts = thald_nonzero - thald_nonzero.mean(1)[:,None]

            ss_wb_ts = (m_wb_ts**2).sum(1)
            ss_thal_ts = (m_thal_ts**2).sum(1)

            corrMap = np.dot(m_wb_ts,m_thal_ts.T)/np.sqrt(np.dot(ss_wb_ts[:,None],ss_thal_ts[None]))
            print(corrMap.shape)

            corrMap_reshape = corrMap.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))        
            img = nb.Nifti1Image(corrMap_reshape, affine=thal.affine)
            img.to_filename(os.path.join(img_directory, 'not_fisherZ_{ds}.nii.gz').format(ds=ds))
        
        
            fisherZ = np.arctanh(corrMap)
            fisherZ_reshape = fisherZ.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))
            img = nb.Nifti1Image(fisherZ_reshape, affine=thal.affine)
            img.to_filename(os.path.join(img_directory, 'fisherZ_{ds}.nii.gz').format(ds=ds))

        

######################## check fisherZ_3ds.nii.gz results for nan


