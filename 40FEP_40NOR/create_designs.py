import os
import re
import pandas as pd
import numpy as np

#demo = pd.read_csv('subjects_demo.csv')

#sex = demo[['sex']]
#age = demo[['age']]

#age_demeaned = age.sub(age.mean(axis=0), axis=1)
#sex_demeaned = sex.sub(sex.mean(axis=0), axis=1)

#sex_demeaned.to_csv('designs/80n_demeaned_sex.txt', sep='\t', index=False, header=False)
#age_demeaned.to_csv('designs/80n_demeaned_age.txt', sep='\t', index=False, header=False)

#a = np.array([1, 0])
#b = np.tile(a, (40, 1))
#c = np.array([0, 1])
#d = np.tile(c, (40, 1))
#e = np.concatenate((b, d), axis=0)
#np.savetxt('designs/80n_2group_matrix.txt', e, fmt='%1.2f')

#f = np.loadtxt('designs/80n_demeaned_age.txt')
#g = np.loadtxt('designs/80n_demeaned_sex.txt')
#z = np.stack((f, g), axis=1)
#y = np.concatenate((e, z), axis=1)

#np.savetxt('designs/2group_80n_design_mat.txt', y)


#A = np.array([1, -1, 0, 0])
#B = np.array([-1, 1, 0, 0])
#C = np.concatenate((A, B), axis=0)
#con = C.reshape(2,4)
#np.savetxt('designs/2group_design_contrast.txt',con)


#input_mat = 'designs/2group_80n_design_mat.txt'
#output_mat = 'designs/2group_80n_design.mat'
#input_con = 'designs/2group_design_contrast.txt'
#output_con = 'designs/2group_design.con'

#mat = 'Text2Vest {input_mat} {output_mat}'.format(input_mat=input_mat, output_mat=output_mat)
#os.popen(mat).read
#con = 'Text2Vest {input_con} {output_con}'.format(input_con=input_con, output_con=output_con)
#os.popen(con).read



#x = np.array([1, -1])
#y = np.array([-1, 1])
#z = np.concatenate((x, y), axis=0)
#nocov_con = z.reshape(2,2)
#np.savetxt('designs/2group_nocov_design_contrast.txt',nocov_con)


#nocov_input_mat = 'designs/80n_2group_matrix.txt'
#nocov_output_mat = 'designs/2group_80n_nocov_design.mat'
#nocov_input_con = 'designs/2group_nocov_design_contrast.txt'
#nocov_output_con = 'designs/2group_nocov_design.con'

#nocov_mat = 'Text2Vest {nocov_input_mat} {nocov_output_mat}'.format(nocov_input_mat=nocov_input_mat, nocov_output_mat=nocov_output_mat)
#os.popen(nocov_mat).read
#nocov_con = 'Text2Vest {nocov_input_con} {nocov_output_con}'.format(nocov_input_con=nocov_input_con, nocov_output_con=nocov_output_con)
#os.popen(nocov_con).read


#X = np.array([1])
#Y = np.tile(X, (80,1))
#np.savetxt('designs/80n_1group_matrix.txt', Y)

#z = np.stack((f, g), axis=1)
#Z = np.append(Y, z, axis=1)
#np.savetxt('designs/1group_80n_design_mat.txt', Z)


#input_mat = 'designs/1group_80n_design_mat.txt'
#output_mat = 'designs/1group_80n_design.mat'

#mat = 'Text2Vest {input_mat} {output_mat}'.format(input_mat=input_mat, output_mat=output_mat)
#os.popen(mat).read

r = np.array([1, 0, 0])
r = r.reshape(1,3)
np.savetxt('designs/1group_nocov_design_contrast.txt', r)
input_mat = 'designs/1group_nocov_design_contrast.txt'
output_mat = 'designs/1group_nocov_design.con'

mat = 'Text2Vest {input_mat} {output_mat}'.format(input_mat=input_mat, output_mat=output_mat)
os.popen(mat).read
