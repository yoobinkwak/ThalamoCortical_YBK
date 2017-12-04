import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image


def GroupAvePerIC(side, voxelsize):

    ave_dir = '37FEP36HC_averaged_rsFC'
    if not os.path.exists(ave_dir):
        os.mkdir(ave_dir)
    out_dir = join(ave_dir, '{side}_ds{voxelsize}'.format(side=side, voxelsize=voxelsize))
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    melodicIC_loc = 'tica_results/mICA_HCvsFEP_{side}_ds{voxelsize}/dim0/melodic_IC.nii.gz'.format(side=side, voxelsize=voxelsize)
    melodicIC_map = nb.load(melodicIC_loc)
    componentNum = melodicIC_map.shape[3]

    log = 'subject_list_rsFC.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()
    
    imgInputs = []
    for subj in subjects:
        dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_thalamusICs_rsFC/Regressed/'.format(side=side, voxelsize=voxelsize)
        ICs=["%02d" % x for x in range(1,componentNum+1)]
        for ic in ICs:
            dataFile = 'split_{subj}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subj=subj, ic=ic)
            imgInputs.append(dataLoc+dataFile)
    FEPimgInputs = []
    for subj in subjects:
        if subj.startswith('FEP'):
            FEP_dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_thalamusICs_rsFC/Regressed/'.format(side=side, voxelsize=voxelsize)
            ICs=["%02d" % x for x in range(1,componentNum+1)]
            for ic in ICs:
                FEP_dataFile = 'split_{subj}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subj=subj, ic=ic)
                FEPimgInputs.append(FEP_dataLoc+FEP_dataFile)
    NORimgInputs = []
    for subj in subjects:
        if subj.startswith('NOR'):
            NOR_dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_thalamusICs_rsFC/Regressed/'.format(side=side, voxelsize=voxelsize)
            ICs=["%02d" % x for x in range(1,componentNum+1)]
            for ic in ICs:
                NOR_dataFile = 'split_{subj}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subj=subj, ic=ic)
                NORimgInputs.append(NOR_dataLoc+NOR_dataFile)

    for ic in ICs:
        averaged_perIC = join(out_dir, 'all_ave_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
        if not os.path.isfile(averaged_perIC):
            perSubj_perIC = [x for x in imgInputs if '00{ic}'.format(ic=ic) in x]
            ave_perIC = nilearn.image.mean_img(perSubj_perIC)
            ave_perIC.to_filename(averaged_perIC)
        FEP_averaged_perIC = join(out_dir, 'FEP_ave_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
        if not os.path.isfile(FEP_averaged_perIC):
            FEP_perSubj_perIC = [x for x in FEPimgInputs if '00{ic}'.format(ic=ic) in x]
            print(len(FEP_perSubj_perIC))
            FEP_ave_perIC = nilearn.image.mean_img(FEP_perSubj_perIC)
            FEP_ave_perIC.to_filename(FEP_averaged_perIC)
        NOR_averaged_perIC = join(out_dir, 'NOR_ave_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
        if not os.path.isfile(NOR_averaged_perIC):
            NOR_perSubj_perIC = [x for x in NORimgInputs if '00{ic}'.format(ic=ic) in x]
            print(len(NOR_perSubj_perIC))
            NOR_ave_perIC = nilearn.image.mean_img(NOR_perSubj_perIC)
            NOR_ave_perIC.to_filename(NOR_averaged_perIC)


def nosmoothGroupAvePerIC(side, voxelsize):

    ave_dir = '37FEP36HC_averaged_rsFC_nosmooth'
    if not os.path.exists(ave_dir):
        os.mkdir(ave_dir)
    out_dir = join(ave_dir, '{side}_ds{voxelsize}'.format(side=side, voxelsize=voxelsize))
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    melodicIC_loc = 'tica_results/mICA_HCvsFEP_{side}_ds{voxelsize}_nosmooth/dim0/melodic_IC.nii.gz'.format(side=side, voxelsize=voxelsize)
    melodicIC_map = nb.load(melodicIC_loc)
    componentNum = melodicIC_map.shape[3]

    log = 'subject_list_rsFC.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()
    
    imgInputs = []
    for subj in subjects:
        dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_nosmooth_thalamusICs_rsFC/Regressed/'.format(side=side, voxelsize=voxelsize)
        ICs=["%02d" % x for x in range(1,componentNum+1)]
        for ic in ICs:
            dataFile = 'split_{subj}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subj=subj, ic=ic)
            imgInputs.append(dataLoc+dataFile)
    FEPimgInputs = []
    for subj in subjects:
        if subj.startswith('FEP'):
            FEP_dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_nosmooth_thalamusICs_rsFC/Regressed/'.format(side=side, voxelsize=voxelsize)
            ICs=["%02d" % x for x in range(1,componentNum+1)]
            for ic in ICs:
                FEP_dataFile = 'split_{subj}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subj=subj, ic=ic)
                FEPimgInputs.append(FEP_dataLoc+FEP_dataFile)
    NORimgInputs = []
    for subj in subjects:
        if subj.startswith('NOR'):
            NOR_dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_nosmooth_thalamusICs_rsFC/Regressed/'.format(side=side, voxelsize=voxelsize)
            ICs=["%02d" % x for x in range(1,componentNum+1)]
            for ic in ICs:
                NOR_dataFile = 'split_{subj}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subj=subj, ic=ic)
                NORimgInputs.append(NOR_dataLoc+NOR_dataFile)

    for ic in ICs:
        averaged_perIC = join(out_dir, 'all_ave_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
        if not os.path.isfile(averaged_perIC):
            perSubj_perIC = [x for x in imgInputs if '00{ic}'.format(ic=ic) in x]
            ave_perIC = nilearn.image.mean_img(perSubj_perIC)
            ave_perIC.to_filename(averaged_perIC)
        FEP_averaged_perIC = join(out_dir, 'FEP_ave_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
        if not os.path.isfile(FEP_averaged_perIC):
            FEP_perSubj_perIC = [x for x in FEPimgInputs if '00{ic}'.format(ic=ic) in x]
            print(len(FEP_perSubj_perIC))
            FEP_ave_perIC = nilearn.image.mean_img(FEP_perSubj_perIC)
            FEP_ave_perIC.to_filename(FEP_averaged_perIC)
        NOR_averaged_perIC = join(out_dir, 'NOR_ave_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
        if not os.path.isfile(NOR_averaged_perIC):
            NOR_perSubj_perIC = [x for x in NORimgInputs if '00{ic}'.format(ic=ic) in x]
            print(len(NOR_perSubj_perIC))
            NOR_ave_perIC = nilearn.image.mean_img(NOR_perSubj_perIC)
            NOR_ave_perIC.to_filename(NOR_averaged_perIC)



def znormGroupAvePerIC(side, voxelsize):

    ave_dir = '37FEP36HC_averaged_rsFC'
    if not os.path.exists(ave_dir):
        os.mkdir(ave_dir)
    out_dir = join(ave_dir, '{side}_ds{voxelsize}'.format(side=side, voxelsize=voxelsize))
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    melodicIC_loc = 'tica_results/mICA_HCvsFEP_{side}_ds{voxelsize}/dim0/melodic_IC.nii.gz'.format(side=side, voxelsize=voxelsize)
    melodicIC_map = nb.load(melodicIC_loc)
    componentNum = melodicIC_map.shape[3]

    log = 'subject_list_rsFC.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()
    
    imgInputs = []
    for subj in subjects:
        dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_thalamusICs_rsFC/Regressed/'.format(side=side, voxelsize=voxelsize)
        ICs=["%02d" % x for x in range(1,componentNum+1)]
        for ic in ICs:
            dataFile = 'split_znorm_{subj}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subj=subj, ic=ic)
            imgInputs.append(dataLoc+dataFile)
    FEPimgInputs = []
    for subj in subjects:
        if subj.startswith('FEP'):
            FEP_dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_thalamusICs_rsFC/Regressed/'.format(side=side, voxelsize=voxelsize)
            ICs=["%02d" % x for x in range(1,componentNum+1)]
            for ic in ICs:
                FEP_dataFile = 'split_znorm_{subj}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subj=subj, ic=ic)
                FEPimgInputs.append(FEP_dataLoc+FEP_dataFile)
    NORimgInputs = []
    for subj in subjects:
        if subj.startswith('NOR'):
            NOR_dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_thalamusICs_rsFC/Regressed/'.format(side=side, voxelsize=voxelsize)
            ICs=["%02d" % x for x in range(1,componentNum+1)]
            for ic in ICs:
                NOR_dataFile = 'split_znorm_{subj}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subj=subj, ic=ic)
                NORimgInputs.append(NOR_dataLoc+NOR_dataFile)

    for ic in ICs:
        averaged_perIC = join(out_dir, 'znorm_all_ave_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
        if not os.path.isfile(averaged_perIC):
            perSubj_perIC = [x for x in imgInputs if '00{ic}'.format(ic=ic) in x]
            ave_perIC = nilearn.image.mean_img(perSubj_perIC)
            ave_perIC.to_filename(averaged_perIC)
        FEP_averaged_perIC = join(out_dir, 'znorm_FEP_ave_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
        if not os.path.isfile(FEP_averaged_perIC):
            FEP_perSubj_perIC = [x for x in FEPimgInputs if '00{ic}'.format(ic=ic) in x]
            print(len(FEP_perSubj_perIC))
            FEP_ave_perIC = nilearn.image.mean_img(FEP_perSubj_perIC)
            FEP_ave_perIC.to_filename(FEP_averaged_perIC)
        NOR_averaged_perIC = join(out_dir, 'znorm_NOR_ave_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
        if not os.path.isfile(NOR_averaged_perIC):
            NOR_perSubj_perIC = [x for x in NORimgInputs if '00{ic}'.format(ic=ic) in x]
            print(len(NOR_perSubj_perIC))
            NOR_ave_perIC = nilearn.image.mean_img(NOR_perSubj_perIC)
            NOR_ave_perIC.to_filename(NOR_averaged_perIC)


def nosmoothZnormGroupAvePerIC(side, voxelsize):

    ave_dir = '37FEP36HC_averaged_rsFC_nosmooth'
    if not os.path.exists(ave_dir):
        os.mkdir(ave_dir)
    out_dir = join(ave_dir, '{side}_ds{voxelsize}'.format(side=side, voxelsize=voxelsize))
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    melodicIC_loc = 'tica_results/mICA_HCvsFEP_{side}_ds{voxelsize}_nosmooth/dim0/melodic_IC.nii.gz'.format(side=side, voxelsize=voxelsize)
    melodicIC_map = nb.load(melodicIC_loc)
    componentNum = melodicIC_map.shape[3]

    log = 'subject_list_rsFC.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()
    
    imgInputs = []
    for subj in subjects:
        dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_nosmooth_thalamusICs_rsFC/Regressed/'.format(side=side, voxelsize=voxelsize)
        ICs=["%02d" % x for x in range(1,componentNum+1)]
        for ic in ICs:
            dataFile = 'split_znorm_{subj}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subj=subj, ic=ic)
            imgInputs.append(dataLoc+dataFile)
    FEPimgInputs = []
    for subj in subjects:
        if subj.startswith('FEP'):
            FEP_dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_nosmooth_thalamusICs_rsFC/Regressed/'.format(side=side, voxelsize=voxelsize)
            ICs=["%02d" % x for x in range(1,componentNum+1)]
            for ic in ICs:
                FEP_dataFile = 'split_znorm_{subj}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subj=subj, ic=ic)
                FEPimgInputs.append(FEP_dataLoc+FEP_dataFile)
    NORimgInputs = []
    for subj in subjects:
        if subj.startswith('NOR'):
            NOR_dataLoc = subj+'/37FEP36HC/{side}_ds{voxelsize}_nosmooth_thalamusICs_rsFC/Regressed/'.format(side=side, voxelsize=voxelsize)
            ICs=["%02d" % x for x in range(1,componentNum+1)]
            for ic in ICs:
                NOR_dataFile = 'split_znorm_{subj}_thresh_zstat00{ic}_ts_regressed0000.nii.gz'.format(subj=subj, ic=ic)
                NORimgInputs.append(NOR_dataLoc+NOR_dataFile)

    for ic in ICs:
        averaged_perIC = join(out_dir, 'znorm_all_ave_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
        if not os.path.isfile(averaged_perIC):
            perSubj_perIC = [x for x in imgInputs if '00{ic}'.format(ic=ic) in x]
            ave_perIC = nilearn.image.mean_img(perSubj_perIC)
            ave_perIC.to_filename(averaged_perIC)
        FEP_averaged_perIC = join(out_dir, 'znorm_FEP_ave_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
        if not os.path.isfile(FEP_averaged_perIC):
            FEP_perSubj_perIC = [x for x in FEPimgInputs if '00{ic}'.format(ic=ic) in x]
            print(len(FEP_perSubj_perIC))
            FEP_ave_perIC = nilearn.image.mean_img(FEP_perSubj_perIC)
            FEP_ave_perIC.to_filename(FEP_averaged_perIC)
        NOR_averaged_perIC = join(out_dir, 'znorm_NOR_ave_{side}_ds{voxelsize}_IC{ic}.nii.gz'.format(side=side, voxelsize=voxelsize, ic=ic))
        if not os.path.isfile(NOR_averaged_perIC):
            NOR_perSubj_perIC = [x for x in NORimgInputs if '00{ic}'.format(ic=ic) in x]
            print(len(NOR_perSubj_perIC))
            NOR_ave_perIC = nilearn.image.mean_img(NOR_perSubj_perIC)
            NOR_ave_perIC.to_filename(NOR_averaged_perIC)




if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--voxelsize', '-vox', nargs=1, help = 'e.g., 3mm', type=str)
	args = parser.parse_args()

        GroupAvePerIC(args.side[0], args.voxelsize[0])
        nosmoothGroupAvePerIC(args.side[0], args.voxelsize[0])
        znormGroupAvePerIC(args.side[0], args.voxelsize[0])
        nosmoothZnormGroupAvePerIC(args.side[0], args.voxelsize[0])

