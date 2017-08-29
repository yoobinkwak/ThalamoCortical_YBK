import sys
import os
import numpy as np
import nibabel as nb
import nilearn
import scipy


#for subject in os.listdir(os.getcwd()):

def corr_map(subject):    
    if subject.startswith(('C','F','N')):

        output_directory = '{subject}/corr_map'.format(subject=subject)

        if not os.path.exists(output_directory):

            os.makedirs(output_directory)

        count = os.listdir(output_directory)
        number_files = len(count)

        if number_files != 3:


            img_directory = '{subject}/preprocess/ds_filter'.format(subject=subject)
            ds_rate = '', '3ds_', '4ds_'
#            filter_rate = 'hp_', 'bp_'
#            registration = 'flirt', 'fnirt'

            for ds in ds_rate:
#                for filtering in filter_rate:
#                    for register in registration:

                wb_img = '{subject}/preprocess/ds_filter/{ds}bp_fnirt.nii.gz'.format(subject=subject, ds=ds)
                thal_img = '{subject}/preprocess/ds_filter/L_thal_on_{ds}bp_fnirt.nii.gz'.format(subject=subject, ds=ds)
                
                print(wb_img)
                print(thal_img)
                
                
                wb = nb.load(wb_img)
                thal = nb.load(thal_img)
        
                wbd = wb.get_data()
                thald = thal.get_data()
                
                print(wbd.shape)
                print(thald.shape)
        
                volume_shape = wbd.shape[:-1]
                coords = list(np.ndindex(volume_shape))
                print(volume_shape)
                print(len(coords))
                
                thal_x, thal_y, thal_z = np.where(thald[:,:,:,0] != 0)
                thal_coords = np.array((thal_x, thal_y, thal_z)).T
                print(thal_coords)
                
                thald_nonzero = thald[np.where(thald[:,:,:,0] != 0)]
                print(thald_nonzero.shape)

                wbd_reshape = wbd.reshape(len(coords), wbd.shape[3])
                thald_reshape = thald_nonzero.reshape(len(thal_coords), wbd.shape[3])
                print(wbd_reshape)
                print(thald_reshape)
                
                
                m_wb_ts = wbd_reshape - wbd_reshape.mean(1)[:,None] 
                m_thal_ts = thald_nonzero - thald_nonzero.mean(1)[:,None]

                ss_wb_ts = (m_wb_ts**2).sum(1)
                ss_thal_ts = (m_thal_ts**2).sum(1)

                corrMap = np.dot(m_wb_ts,m_thal_ts.T)/np.sqrt(np.dot(ss_wb_ts[:,None],ss_thal_ts[None]))
                print(corrMap.shape)
                
#                corrMap_reshape = corrMap.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))        
#                img = nb.Nifti1Image(corrMap_reshape, affine=thal.affine)
#                img.to_filename(os.path.join(output_directory, 'not_fisherZ_{ds}bp_fnirt.nii.gz').format(ds=ds))
                
                
                fisherZ = np.arctanh(corrMap)
                fisherZ_reshape = fisherZ.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))
                img = nb.Nifti1Image(fisherZ_reshape, affine=thal.affine)
                img.to_filename(os.path.join(output_directory, 'fisherZ_{ds}bp_fnirt.nii.gz').format(ds=ds))


if __name__== "__main__":
    corr_map(sys.argv[1])
