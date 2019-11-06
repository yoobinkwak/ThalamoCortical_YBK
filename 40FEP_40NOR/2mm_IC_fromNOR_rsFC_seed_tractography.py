import os
from os.path import join, basename, dirname, isfile, isdir
import re
from multiprocessing import Pool
import sys


dataLoc = '/Volumes/extHDD_YB/rsFC_to_wmSC'
sub_dir = ['ds3_bi_nosmooth_20ICs']



class subject:
    def __init__(self, subject):
        self.gpu_num = 0
        self.subject = subject
        self.subject_dir = join(dataLoc, subject)
        self.out_dir = join(self.subject_dir, '2mm_IC_fromNOR_rsFC_seed_tractography')
        self.bedpost_dir = join(self.subject_dir, 'DTI.bedpostX')
        self.reg_dir = join(self.subject_dir, 'DTI/Registration')


def run_commands(subject_class):

    commands = []

    for subdir in sub_dir:
        for outdir in [subject_class.out_dir]:
            if not os.path.exists(outdir):
                os.mkdir(outdir)
            directory = '{}/{}'.format(outdir, subdir)
            if not os.path.exists(directory):
                os.mkdir(directory)

        nocov_input_dir = '2mm_sig_clusters/NOR_only/{}/two_step_randomise/nocov_1_sample_tfce/sig_clusters'.format(subdir)
        nocov_imgs = [x for x in os.listdir(nocov_input_dir) if isfile(join(nocov_input_dir, x))]

        for nocov_img in nocov_imgs:
            nocov_filename = ''.join(nocov_img.replace('t0.95_concatenated_ds3_bi_',' ').replace('.nii.gz',' ').split())
            nocov_tract_dir = '{}/{}'.format(directory, nocov_filename)
            
            command = 'CUDA_VISIBLE_DEVICES={gpu_num} /usr/local/fsl/bin/probtrackx2_gpu \
                -x {nocov_thal_roi} \
                -l \
                --onewaycondition \
                --omatrix2 \
                -c 0.2 \
                -S 2000 \
                --steplength=0.5 \
                -P 5000 \
                --fibthresh=0.01 \
                --distthresh=0.0 \
                --sampvox=0.0 \
                --forcedir \
                --opd \
                -s {bedpostDir}/merged \
                -m {bedpostDir}/nodif_brain_mask \
                --xfm={reorient_mni2t1w2nodif} \
                --invxfm={reorient_nodif2t1w2mni} \
                --dir={tract_dir} \
                --target2={mniMask}'.format(gpu_num=subject_class.gpu_num,
                           nocov_thal_roi = '{}/{}'.format(nocov_input_dir, nocov_img),
                           bedpostDir = subject_class.bedpost_dir,
                           reorient_mni2t1w2nodif = join(subject_class.reg_dir, 'mni2reorient_t1w2nodif_coeff.nii.gz'),
                           reorient_nodif2t1w2mni = join(subject_class.reg_dir, 'reorient_nodif2t1w2mni_coeff.nii.gz'),
                           tract_dir = nocov_tract_dir,
                           mniMask = '/usr/local/fsl/data/standard/MNI152_T1_2mm_brain_mask.nii.gz')
        
            if not isfile(join(nocov_tract_dir, 'fdt_paths.nii.gz')):
                commands.append(re.sub('\s+', ' ', command))
        subject_class.commands = ';'.join(commands)
        os.popen(subject_class.commands).read()


def run_probtrackx_parallel(subject_classes):
    pool = Pool(processes=7)
    # minimum number of commands in different GPUs
    print(subject_classes.keys())
    min_num = min([len(x) for x in subject_classes.values()])
    print(min_num)
    for num in range(min_num):
        batch_subject_classes = [x[num] for x in subject_classes.values()]
        pool.map(run_commands, batch_subject_classes)

    batch_subject_classes = []
    for i in subject_classes.values():
        if len(i)>min_num:
            batch_subject_classes += i
    pool.map(run_commands, batch_subject_classes)

if __name__ == '__main__':
    data_dir = join(dirname(os.getcwd()), 'rsFC_to_wmSC')
    subject_classes = [subject(join(data_dir, x)) for x in os.listdir(data_dir) if re.search('(FEP|NOR)\d+', x)]

    for subject_class_tmp in subject_classes:
        run_commands(subject_class_tmp)
    # For multi-gpu support
    new_subject_classes = {0:[], 1:[], 2:[],
                           3:[], 4:[], 5:[], 6:[]}
    gpu_num=0
    for subject_class in subject_classes:
        current_subject_list = new_subject_classes[gpu_num]
        subject_class.gpu_num = gpu_num
        print(subject_class.gpu_num)
        current_subject_list += [subject_class]
        new_subject_classes[gpu_num] = current_subject_list
        if gpu_num == 6:
            gpu_num = 0
        else:
            gpu_num+=1

    #print([[y.gpu_num for y in x] for x in new_subject_classes.values()])
    run_probtrackx_parallel(new_subject_classes)
    #run_bedpostx(new_subject_classes)



