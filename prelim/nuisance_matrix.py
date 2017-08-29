#!usr/bin/python

import os
import numpy as np


for subject in os.listdir(os.getcwd()):
    if subject.startswith(('C','F','N')):
        matrices = 'CSF_noise.txt', 'WM_noise.txt', 'mn.txt'
        for matrix in matrices:
            if matrix.startswith(('C', 'W')):
                nuisance_path = '{subject}/nuisance'.format(subject=subject)
                pre = np.loadtxt('{subject}/nuisance/{matrix}'.format(subject=subject, matrix=matrix)
#                demean = pre - pre.mean()       ###  NEED TO REDO (to do spearately for each column)
                np.savetxt(os.path.join(nuisance_path, 'demeaned_{matrix}').format(matrix=matrix), demean)

                nuisance_contrast = np.asmatrix('1 0')
                np.savetxt(os.path.join(nuisance_path, 'contrast.txt'), nuisance_contrast)

            if matrix.startswith('m'):
                mn_path = '{subject}/motion'.format(subject=subject)
                mn = np.loadtxt('{subject}/motion/{matrix}'.format(subject=subject, matrix=matrix))
                mn_delete = np.delete(mn, (114,115), 0)     ## need (112,113,114,115) if deleteing initial 4 volumes
                mn_demean = mn_delete - mn_delete.mean()
                np.savetxt(os.path.join(mn_path, 'demeaned_{matrix}').format(matrix=matrix), mn_demean)

                mn_contrast = np.asmatrix('1')
                np.savetxt(os.path.join(mn_path, 'contrast.txt'), mn_contrast)


