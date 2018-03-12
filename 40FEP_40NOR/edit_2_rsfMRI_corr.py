import sys
import os
from os.path import join, basename, isfile, isdir
import argparse
import numpy as np
import nibabel as nb
import nilearn
import scipy


def corr_map(subject, side, voxsize):    
    out_dir = '{subject}/RSFC'.format(subject=subject)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    output = join(out_dir, '{side}_ds{voxsize}_fisherZ.nii.gz').format(side=side, voxsize=voxsize)
    if not os.path.isfile(output):

        in_dir = '{subject}/REST/Preprocess'.format(subject=subject)
        
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
      
        #wb_x, wb_y, wb_z = np.where(wbd[:,:,:,0] != 0)
        #wb_coords = np.array((wb_x, wb_y, wb_z)).T
        #wbd_nonzero = wbd[np.where(wbd[:,:,:,0] != 0)]
        
        wbd_reshape = wbd.reshape(len(coords), wbd.shape[3])
        thald_reshape = thald_nonzero.reshape(len(thal_coords), wbd.shape[3])
        
        #wbd_reshape = wbd_nonzero.reshape(len(wb_coords), wbd.shape[3])
                
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


def nodsCorr_map(subject, side):    
    out_dir = '{subject}/RSFC'.format(subject=subject)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    output = join(out_dir, '{side}_2mm_fisherZ.nii.gz').format(side=side)
    if not os.path.isfile(output):

        in_dir = '{subject}/REST/Preprocess'.format(subject=subject)
        
        wb_img = join(in_dir, 'bp2mni/bp2mni.nii.gz')
        thal_img = join(in_dir, '{side}_thal_on_bp.nii.gz').format(side=side)
                
        wb = nb.load(wb_img)
        thal = nb.load(thal_img)
        
        wbd = wb.get_data()
        thald = thal.get_data()
        
        volume_shape = wbd.shape[:-1]
        coords = list(np.ndindex(volume_shape))
                
        thal_x, thal_y, thal_z = np.where(thald[:,:,:,0] != 0)
        thal_coords = np.array((thal_x, thal_y, thal_z)).T
                
        thald_nonzero = thald[np.where(thald[:,:,:,0] != 0)]
      
        #wb_x, wb_y, wb_z = np.where(wbd[:,:,:,0] != 0)
        #wb_coords = np.array((wb_x, wb_y, wb_z)).T
        #wbd_nonzero = wbd[np.where(wbd[:,:,:,0] != 0)]
        
        wbd_reshape = wbd.reshape(len(coords), wbd.shape[3])
        thald_reshape = thald_nonzero.reshape(len(thal_coords), wbd.shape[3])
        
        #wbd_reshape = wbd_nonzero.reshape(len(wb_coords), wbd.shape[3])
                
        m_wb_ts = wbd_reshape - wbd_reshape.mean(1)[:,None] 
        m_thal_ts = thald_nonzero - thald_nonzero.mean(1)[:,None]

        ss_wb_ts = (m_wb_ts**2).sum(1)
        ss_thal_ts = (m_thal_ts**2).sum(1)

        corrMap = np.dot(m_wb_ts,m_thal_ts.T)/np.sqrt(np.dot(ss_wb_ts[:,None],ss_thal_ts[None]))
        
        corrMap_reshape = corrMap.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))        
        img = nb.Nifti1Image(corrMap_reshape, affine=thal.affine)
        img.to_filename(os.path.join(out_dir, '{side}_2mm_nonfisherZ.nii.gz').format(side=side))
                
                
        fisherZ = np.arctanh(corrMap)
        fisherZ_reshape = fisherZ.reshape(volume_shape[0], volume_shape[1], volume_shape[2], len(thal_coords))
        img = nb.Nifti1Image(fisherZ_reshape, affine=thal.affine)
        img.to_filename(output)


    ds_output = join(out_dir, '{side}_3mm_fisherZ.nii.gz').format(side=side)
    if not os.path.isfile(ds_output):
        command = 'flirt -in {output} -ref {output} -applyisoxfm 3 -out {ds_output}'.format(output=output, ds_output=ds_output)
        os.popen(command).read()



if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--subject', '-subj', nargs=1, help = 'subject', type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'L or R', type=str)
	parser.add_argument('--voxsize', '-voxsize', nargs=1, help = '3 or 4', type=str)
	args = parser.parse_args()

	corr_map(args.subject[0], args.side[0],  args.voxsize[0])
	nodsCorr_map(args.subject[0], args.side[0])

