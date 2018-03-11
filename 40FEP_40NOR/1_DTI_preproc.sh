#!/bin/bash

FSLDIR=/usr/share/fsl/5.0

for subj in $@
do
    DTI=${subj}/DTI
    if [ ! -e ${DTI}/bvals ] ; then
        mv ${DTI}/*bval ${DTI}/bvals
        mv ${DTI}/*bvec ${DTI}/bvecs
        mv ${DTI}/*.nii.gz ${DTI}/data.nii.gz
    fi

    #### DTI Preprocessing ####
    ## 1.Eddy current ##
    if [ ! -e ${DTI}/data.ecclog ] ; then
        ${FSLDIR}/bin/eddy_correct ${DTI}/data.nii.gz ${DTI}/data 0
    fi
    
    ## 2.B0 image extraction ##
    if [ ! -e ${DTI}/nodif.nii.gz ] ; then
        fslroi ${DTI}/data.nii.gz ${DTI}/nodif 0 1
    fi
    
    ## 3.Bet brain extraction ##
    if [ ! -e ${DTI}/nodif_brain.nii.gz ] ; then
        bet ${DTI}/nodif ${DTI}/nodif_brain -m -f 0.30
    fi
    
    ## 4.FDT_DTIFIT ##
    if [ ! -e ${DTI}/dti_FA.nii.gz ] ; then
        dtifit -k ${DTI}/data -m ${DTI}/nodif_brain_mask -r ${DTI}/bvecs -b ${DTI}/bvals -o ${DTI}/dti
    fi
    
    ## 5.Bedpostx ##
    if [ ! -e ${subj}/DTI.bedpostX/merged_th2samples.nii.gz ] ; then
        bedpostx ${subj}/DTI    
        ## OM modelled 2 fibers per voxel (default is 3) & used burn-in of 5000 (default is 1000) 
    fi


	#### T1 brain extraction using FS output ####
    if [ ! -e ${subj}/FREESURFER/mri/brainmask.mgz ] ; then
        export SUBJECTS_DIR=${subj}
        recon-all -subjid FREESURFER -i ${subj}/T1/20*.nii.gz -autorecon1 
    fi


done
