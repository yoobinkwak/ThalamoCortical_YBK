import sys, os
from os.path import join, basename
import numpy as np
from scipy.sparse import csr_matrix, coo_matrix
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as plt
import scipy.stats

DATA = np.loadtxt('fdt_matrix2.dot', dtype='int')		## DATA.shape (29569382, 3)
dims = DATA.shape[1] - 1						## dims = 2
shape = [np.max(DATA[:,i]) for i in range(dims)]		## shape = [1031, 228483]
M = np.zeros(shape=shape)
for row in DATA:
	index = tuple(row[:-1] - 1)
	M.itemset(index, row[-1])
# M.shape (1031, 228483)
np.savetxt('Lambert_MxN.txt', M)

MM_corr = np.corrcoef(M)
# MM_corr.shape (1031, 1031)
np.savetxt('Lambert_MxM.txt', MM_corr)

ED = euclidean_distances(MM_corr)
# ED.shape (1031, 1031) 
np.savetxt('Lambert_MxM_ED.txt', ED)





## "a[0,:]" OR "a[0,:]" to select 1st row, "a[:,0]" to select 1st column

m1 = ED[0]
#stats.describe(m1)
mean = np.sum(abs(m1)) / len(m1)
variance = np.var(abs(m1))
skewness = scipy.stats.skew(abs(m1))
kurtosis = scipy.stats.kurtosis(abs(m1))
median = np.median(m1)


m_feature_maps = []
for m in range(ED.shape[1]):
	row = []
	for n in range(ED.shape[1]):
		vox = ED[n]
		row.append(np.sum(abs(vox)) / len(vox))
		row.append(np.var(abs(vox)))
		row.append(scipy.stats.skew(abs(vox)))
		row.append(scipy.stats.kurtosis(abs(vox))
		row.append(np.median(vox)) 
	m_feature_maps.append(row)
m_feature_maps = np.array(m_feature_maps)








sx_prev = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype = np.float)
sx_mid = np.array([[-2, 0, 2], [-4, 0, 4], [-2, 0, 2]], dtype = np.float)
sx_aft = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype = np.float)



-1 0 1      -2 0 2      -1 0 1
-2 0 2      -4 0 4      -2 0 2
-1 0 1      -2 0 2      -1 0 1
(x-1)       (x)         (x+1)

1 2 1       2 4 2       1 2 1
0 0 0       0 0 0       0 0 0
-1 -2 -1    -2 -4 -2    -1 -2 -1
(y-1)       (y)         (y+1)

-1 -2 -1    0 0 0       1 2 1
-2 -4 -2    0 0 0       2 4 2
-1 -2 -1    0 0 0       1 2 1
(t-1)       (t)         (t+1)




















#b= np.ndarray.flatten(ED)
#xi = [i for i in range(0, len(b))]
#plt.plot(xi, b)
#plt.show()
#
#m = ED.shape[0]
#x = np.arange(m)
#y = ED[[0]].T
#plt.plot(x, y)
#plt.show
#
#r = []
#for i in np.nditer(x):
#	r.append((100-0)*(i-min(x))/(max(x)-min(x))+0)
#
#r = np.hstack(r)
#plt.plot(r, y)
#plt.show
#
#
#def scale_number(unscaled, to_min, to_max, from_min, from_max):
#	    return (to_max-to_min)*(unscaled-from_min)/(from_max-from_min)+to_min
#def scale_list(l, to_min, to_max):
#	    return [scale_number(i, to_min, to_max, min(l), max(l)) for i in l]

