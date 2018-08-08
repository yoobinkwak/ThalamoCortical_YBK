import sys
import os
from os.path import join, basename, isfile, isdir
import argparse
import numpy as np
import nibabel as nb
import nilearn
import scipy


def corr_map(subject, side, voxsize, spatialsmoothing):    
    out_dir = '{subject}/RSFC'.format(subject=subject)
    #out_dir = '{subject}/test_RSFC'.format(subject=subject)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    in_dir = '{subject}/REST/Preprocess'.format(subject=subject)
    
    output = join(out_dir, '{side}_ds{voxsize}_fisherZ.nii.gz').format(side=side, voxsize=voxsize)
    if not os.path.isfile(output):
        
        wb_img = join(in_dir, 'bp2mni_ds{voxsize}.nii.gz').format(voxsize=voxsize)
        thal_img = join(in_dir, '{side}_thal_on_bp_ds{voxsize}.nii.gz').format(side=side,voxsize=voxsize)
                
        wb = nb.load(wb_img)
        thal = nb.load(thal_img)
        
        wbd = wb.get_data()
        thald = thal.get_data()
        
        volume_shape = wbd.shape[:-1]
        coords = list(np.ndindex(volume_shape))
                
        thal_x, thal_y, thal_z = np.where(thald[:,:,:,0] != 0)
        thal_coords = np.array((thal_x, thal_y, thal_z)).T
                
        thald_nonzero = thald[np.where(thald[:,:,:,0] != 0)]
        
        wbd_reshape = wbd.reshape(len(coords), wbd.shape[3])
        thald_reshape = thald_nonzero.reshape(len(thal_coords), wbd.shape[3])
        
        m_wb_ts = wbd_reshape - wbd_reshape.mean(1)[:,None] 
        m_thal_ts = thald_nonzero - thald_nonzero.mean(1)[:,None]

        ss_wb_ts = (m_wb_ts**2).sum(1)
        ss_thal_ts = (m_thal_ts**2).sum(1)

        corrMap = np.dot(m_wb_ts,m_thal_ts.T)/np.sqrt(np.dot(ss_wb_ts[:,None],ss_thal_ts[None]))
        
        corrMap_reshape = corrMap.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))        
        img = nb.Nifti1Image(corrMap_reshape, affine=thal.affine)
        img.to_filename(os.path.join(out_dir, '{side}_ds{voxsize}_nonfisherZ.nii.gz').format(side=side, voxsize=voxsize))
                
        fisherZ = np.arctanh(corrMap)
        fisherZ_reshape = fisherZ.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))
        img = nb.Nifti1Image(fisherZ_reshape, affine=thal.affine)
        img.to_filename(output)
    

    smooth = join (out_dir, '{side}_ds{voxsize}_fisherZ_s{spatialsmoothing}.nii.gz').format(side=side, voxsize=voxsize, spatialsmoothing=spatialsmoothing)
    if not os.path.isfile(smooth):
        command = 'fslmaths {output} -s 3.0 {smooth}'.format(output=output, smooth=smooth)
        os.popen(command).read

#    correct_mask_smooth = 'masks/{side}_thalamus_thalamus_HOSC_60_ds{voxsize}_s{spatialsmoothing}.nii.gz'.format(side=side, voxsize=voxsize, spatialsmoothing=spatialsmoothing)
#    if not os.path.isfile(correct_mask_smooth):
#        to_mask = 'masks/mni_brain_ds3_s3.nii.gz'
#        thal_mask = 'masks/bi_thalamus_HOSC_60_ds3.nii.gz'
#        command = 'fslmaths {to_mask} -mas {thal_mask} {correct_mask_smooth}'.format(to_mask=to_mask, thal_mask=thal_mask, correct_mask_smooth=correct_mask_smooth)
#        os.popen(command).read





def re_corr_map(subject, side, voxsize, spatialsmoothing):
    out_dir = '{subject}/RSFC/with_spatial_smoothing'.format(subject=subject)
    #out_dir = '{subject}/test_RSFC/with_spatial_smoothing'.format(subject=subject)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    in_dir = '{subject}/REST/Preprocess/with_spatial_smoothing'.format(subject=subject)

    output = join(out_dir, '{side}_ds{voxsize}_fisherZ.nii.gz').format(side=side, voxsize=voxsize)
    if not os.path.isfile(output):

        wb_img = join(in_dir, 'bp2mni_ds{voxsize}.nii.gz').format(voxsize=voxsize)
        thal_img = join(in_dir, '{side}_thal_on_bp_ds{voxsize}.nii.gz').format(side=side,voxsize=voxsize)

        wb = nb.load(wb_img)
        thal = nb.load(thal_img)

        wbd = wb.get_data()
        thald = thal.get_data()

        volume_shape = wbd.shape[:-1]
        coords = list(np.ndindex(volume_shape))

        thal_x, thal_y, thal_z = np.where(thald[:,:,:,0] != 0)
        thal_coords = np.array((thal_x, thal_y, thal_z)).T

        thald_nonzero = thald[np.where(thald[:,:,:,0] != 0)]

        wbd_reshape = wbd.reshape(len(coords), wbd.shape[3])
        thald_reshape = thald_nonzero.reshape(len(thal_coords), wbd.shape[3])

        m_wb_ts = wbd_reshape - wbd_reshape.mean(1)[:,None]
        m_thal_ts = thald_nonzero - thald_nonzero.mean(1)[:,None]

        ss_wb_ts = (m_wb_ts**2).sum(1)
        ss_thal_ts = (m_thal_ts**2).sum(1)

        corrMap = np.dot(m_wb_ts,m_thal_ts.T)/np.sqrt(np.dot(ss_wb_ts[:,None],ss_thal_ts[None]))

        corrMap_reshape = corrMap.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))
        img = nb.Nifti1Image(corrMap_reshape, affine=thal.affine)
        img.to_filename(os.path.join(out_dir, '{side}_ds{voxsize}_nonfisherZ.nii.gz').format(side=side, voxsize=voxsize))

        fisherZ = np.arctanh(corrMap)
        fisherZ_reshape = fisherZ.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))
        img = nb.Nifti1Image(fisherZ_reshape, affine=thal.affine)
        img.to_filename(output)





if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--subject', '-subj', nargs=1, help = 'subject', type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'L or R', type=str)
	parser.add_argument('--voxsize', '-voxsize', nargs=1, help = '3 or 4', type=str)
	parser.add_argument('--spatialsmoothing', '-sigma', nargs=1, help = 'e.g., 3 (when fwhm6) or 2 (when fwhm4)', type=str)
	args = parser.parse_args()

	corr_map(args.subject[0], args.side[0],  args.voxsize[0], args.spatialsmoothing[0])
	re_corr_map(args.subject[0], args.side[0],  args.voxsize[0], args.spatialsmoothing[0])


