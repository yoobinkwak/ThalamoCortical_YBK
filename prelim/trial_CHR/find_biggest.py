import nibabel as nb
import os
import scipy.stats as stats
import numpy as np

def find_biggest():
    subjects = [x for x in os.listdir(os.getcwd()) if x.startswith('CHR')]
    
    # 0, 1, 2 : coordinate
    # 3 : component
    maps_4d = [os.path.join(os.getcwd(), 
                       x, 
                       'dual_reg_eachIC',
                       'merged_temporal_reg_3ds_bp_fnirt_10.nii.gz') for x in subjects]

    maps_4d = [x for x in maps_4d if os.path.isfile(x)]

    egData = nb.load(maps_4d[0]).get_data()

    # 0, 1, 2 : coordinate
    # 3 : component
    # 4 : subject
    maps_5d = np.tile(egData[:,:,:,:, np.newaxis], len(maps_4d))
    for num, imgLoc in enumerate(maps_4d):
        print num
        img = nb.load(imgLoc)
        img_data = img.get_data()
        nonzeroInd = np.nonzero(img_data)
        print img_data[nonzeroInd].mean()
        img_data[nonzeroInd] = stats.zscore(img_data[nonzeroInd])
        print img_data[nonzeroInd].mean()
        # z-score
        maps_5d[:,:,:,:,num] = img_data

    # average over subjects
    mean_mat = maps_5d.mean(axis=4)
    #(60, 72, 60, 10)

    # find the biggest component
    biggest_mat = mean_mat.argmax(axis=3)
    biggest_mat_img = nb.Nifti1Image(biggest_mat, img.affine)
    biggest_mat_img.to_filename('prac.nii.gz')

if __name__=='__main__':
    find_biggest()
