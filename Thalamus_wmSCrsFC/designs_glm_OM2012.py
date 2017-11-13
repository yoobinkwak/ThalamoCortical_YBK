import os
import re
import pandas as pd
import numpy as np


demo = pd.read_csv('37FEP_36HC_demo.csv')
sex = demo[['sex']]
age = demo[['age']]

age_demeaned = age.sub(age.mean(axis=0), axis=1)
sex_demeaned = sex.sub(sex.mean(axis=0), axis=1)
sex_demeaned.to_csv('demeaned_sex.txt', sep='\t', index=False, header=False)
age_demeaned.to_csv('demeaned_age.txt', sep='\t', index=False, header=False)

a = np.array([1, 0])
b = np.tile(a, (37, 1))
c = np.array([0, 1])
d = np.tile(c, (36, 1))
e = np.concatenate((b, d), axis=0)
np.savetxt('group_matrix.txt', e, fmt='%1.2f')

f = np.loadtxt('demeaned_age.txt')
g = np.loadtxt('demeaned_sex.txt')
z = np.stack((f, g), axis=1)
y = np.concatenate((e, z), axis=1)
np.savetxt('design_mat.txt', y)


