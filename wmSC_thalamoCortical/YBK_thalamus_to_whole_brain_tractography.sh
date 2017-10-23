#!/bin/sh
Usage() {
    echo ""
    echo "Usage: 9_thalamus_to_whole_brain_tractography.sh <subjDir> <lh>"
    echo ""
    exit 1
}

[ "$1" = "" ] && Usage

################################
# Input from commandline
################################
subj=${1}
side_s=${2}

if [ ${side_s} == 'lh' ]
then
    side=left
elif [ ${side_s} == 'rh' ]
then
    side=right
else
    Usage
fi

echo ${subj} ${side}

# Edit here for different folder structure

fsDir=${subj}/FREESURFER
regDir=${subj}/registration
dtiDir=${subj}/DTI
roiDir=${subj}/ROI
tractDir=${subj}/thalamus_tractography
tractDir_MNI=${subj}/wb_thalamus_tractography
bedpostDir=${subj}/DTI.bedpostX
rawT1=${subj}/T1/20*.nii.gz
reorient_rawT1=${subj}/T1/reorient_rawT1.nii.gz
if [ ! -e ${reorient_rawT1} ] 
then
	fslreorient2std ${rawT1} ${reorient_rawT1}
fi
#swapdim_rawT1=${subj}/T1/swapdim_rawT1.nii.gz
#if [ ! -e ${swapdim_rawT1} ]
#then
#	fslswapdim ${rawT1} RL PA IS ${swapdim_rawT1}
#fi
rawT1_mask=${fsDir}/mri/brainmask_in_rawavg.nii.gz
reorient_rawT1_mask=${fsDir}/mri/brainmask_in_rawavg_reorient.nii.gz
reorient_rawT1_mask_bin=${fsDir}/mri/bin_brainmask_in_rawavg_reorient.nii.gz
#swapdim_rawT1_mask=${fsDir}/mri/brainmask_in_rawavg_swapdim.nii.gz
#swapdim_rawT1_mask_bin=${fsDir}/mri/bin_brainmask_in_rawavg_swapdim.nii.gz
rawT1_mask_mgz=${fsDir}/mri/brainmask.mgz
nodif_brain=${dtiDir}/nodif_brain.nii.gz

#sourceImg=${rawT1}
mni=${FSLDIR}/data/standard/MNI152_T1_2mm_brain.nii.gz
mniMask=${FSLDIR}/data/standard/MNI152_T1_2mm_brain_mask.nii.gz

################################################################
# 0. brainmask from freesurfer
################################################################

if [ ! -e ${rawT1_mask} ]
then
    mri_vol2vol --mov ${rawT1_mask_mgz} --targ ${fsDir}/mri/rawavg.mgz --regheader --o ${fsDir}/mri/brainmask_in_rawavg.mgz --no-save-reg
    mri_convert ${fsDir}/mri/brainmask_in_rawavg.mgz ${rawT1_mask}
fi

if [ -e ${rawT1_mask} ] && [ ! -e ${reorient_rawT1_mask_bin} ] 
then
    fslreorient2std ${rawT1_mask} ${reorient_rawT1_mask}
    fslmaths ${reorient_rawT1_mask} -bin ${reorient_rawT1_mask_bin}
fi

#if [ -e ${rawT1_mask} ] && [ ! -e ${swapdim_rawT1_mask_bin} ] 
#then
#    fslswapdim ${rawT1_mask} RL PA IS ${swapdim_rawT1_mask}
#    fslmaths ${swapdim_rawT1_mask} -bin ${swapdim_rawT1_mask_bin}
#fi

################################################################
# 1.1 Registration : t1w --> mni fnirt
################################################################
t1w2mni_flirt="${regDir}/reorient_t1w2mni"
#flirt & fnirt
if [ ! -e "${t1w2mni_flirt}".mat ]
then
	flirt \
		-in ${reorient_rawT1} \
        	-ref ${mni} \
        	-omat ${t1w2mni_flirt}.mat \
        	-out ${t1w2mni_flirt}.nii.gz \
		-cost mutualinfo \
		-dof 6 \
		-searchrx -180 180 \
		-searchry -180 180 \
		-searchrz -180 180 
fi

t1w2mni_fnirt=${regDir}/reorient_t1w2mni_fnirt_coeff.nii.gz
t1w2mni_fnirt_img=${regDir}/reorient_t1w2mni_fnirt_img.nii.gz
if [ ! -e ${t1w2mni_fnirt} ]
then
	fnirt \
		--in=${reorient_rawT1} \
        	--ref=${mni} \
        	--aff=${t1w2mni_flirt}.mat  \
        	--inmask=${reorient_rawT1_mask_bin} \
        	--refmask=${mniMask} \
        	--cout=${t1w2mni_fnirt}  \
        	--iout=${t1w2mni_fnirt_img}
fi

mni2t1w_fnirt=${regDir}/mni2reorient_t1w_fnirt_coeff.nii.gz
if [ ! -e ${mni2t1w_fnirt} ]
then
    invwarp \
        -w ${t1w2mni_fnirt} \
        -o ${mni2t1w_fnirt} \
        -r ${reorient_rawT1}
fi

################################################################
# 1.2 Registration : t1w --> DTI flirt
################################################################
t1w2nodif="${regDir}/reorient_t1w2nodif"
if [ ! -e ${t1w2nodif}.mat ]
then
    flirt \
        -in ${reorient_rawT1} \
        -ref ${nodif_brain} \
        -omat ${t1w2nodif}.mat \
        -out ${t1w2nodif}.nii.gz \
	-cost mutualinfo \
	-dof 6 \
	-searchrx -180 180 \
	-searchry -180 180 \
	-searchrz -180 180 
fi

################################################################
# 1.3 Registration : MNI --> t1w --> DTI 
################################################################
mni2t1w2nodif=${regDir}/mni2reorient_t1w2nodif_coeff.nii.gz
if [ ! -e ${mni2t1w2nodif} ]
then
    convertwarp \
        --ref=${nodif_brain} \
        --warp1=${mni2t1w_fnirt} \
        --postmat=${t1w2nodif}.mat \
        --out=${mni2t1w2nodif}

fi

nodif2t1w2mni=${regDir}/nodif2reorient_t1w2mni_coeff.nii.gz
if [ ! -e ${nodif2t1w2mni} ]
then
    invwarp \
        -w ${mni2t1w2nodif} \
        -o ${nodif2t1w2mni} \
        -r ${mni}
fi


################################################################
# 2. Extract thalamic ROI from the Harvard Oxford template
################################################################
if [ ! -e ${side_s}_thalamus_HOSC.nii.gz ] ; then
    fslroi ${FSLDIR}/data/atlases/HarvardOxford/HarvardOxford-sub-prob-2mm.nii.gz lh_thalamus_HOSC.nii.gz 3 1
    fslroi ${FSLDIR}/data/atlases/HarvardOxford/HarvardOxford-sub-prob-2mm.nii.gz rh_thalamus_HOSC.nii.gz 14 1
fi

mniThalROI_raw=${side_s}_thalamus_HOSC_60.nii.gz
mniThalROI=${roiDir}/${side_s}_thalamus_DTI_HO.nii.gz 
if [ ! -e ${mniThalROI_raw} ]
then
    fslmaths ${side_s}_thalamus_HOSC.nii.gz -thr 60 -bin ${side_s}_thalamus_HOSC_60.nii.gz
   # fslmaths lh_thalalmus_HOSC.nii.gz -thr 60 -bin lh_thalamus_HOSC_60.nii.gz
   # fslmaths rh_thalalmus_HOSC.nii.gz -thr 60 -bin rh_thalamus_HOSC_60.nii.gz
fi

if [ ! -e ${mniThalROI} ]
then 
    applywarp \
        --ref=${nodif_brain} \
        --in=${mniThalROI_raw} \
        --warp=${mni2t1w2nodif} \
        --out=${mniThalROI} \
        --interp=nn
fi

################################################################
# 3. Thalamus seeded whole-brain tractography
################################################################
#if [ ! -e ${tractDir_MNI}/${side}/fdt_paths.nii.gz ]
#then
#    rm -rf ${tractDir_MNI}/${side} 
#    mkdir -p ${tractDir_MNI}/${side}
#    probtrackx2 \
#        -x ${mniThalROI_raw} \
#        -l \
#        --onewaycondition \
#        --omatrix2 \
#        --target2=${mniMask} \
#        -c 0.2 \
#        -S 2000 \
#        --steplength=0.5 \
#        -P 5000 \
#        --fibthresh=0.01 \
#        --distthresh=0.0 \
#        --sampvox=0.0 \
#        --xfm=${mni2t1w2nodif} \
#        --invxfm=${nodif2t1w2mni} \
#        --forcedir \
#        --opd \
#        -s ${bedpostDir}/merged \
#        -m ${bedpostDir}/nodif_brain_mask \
#        --dir=${tractDir_MNI}/${side}
#    echo ${subj} MNI thalamo-whole brain tractography on the ${side} done
#else
#    echo ${subj} MNI thalamo-whole brain tractography on the ${side} done
#fi

################################################################
# 4. Downsampling --> requires editing 
################################################################
#reconImg=${tractDir_MNI}/${side}/fdt_matrix2_reconstructed.nii.gz
#reconImg_ds_3=${tractDir_MNI}/${side}/fdt_matrix2_reconstructed_ds_3.nii.gz
#reconImg_ds_4=${tractDir_MNI}/${side}/fdt_matrix2_reconstructed_ds_4.nii.gz
#reconImg4s=${tractDir_MNI}/${side}/fdt_matrix2_reconstructed_4s.nii.gz
#reconImg_ds_3_4s=${tractDir_MNI}/${side}/fdt_matrix2_reconstructed_ds_3_4s.nii.gz
#
## probtracks postprocessing
#if [ ! -e ${reconImg} ]
#then 
#    echo "Convert ${tractDir_MNI}/${side}/fdt_matrix2 --> ${i}"
#    python tracktography/postprocessing/probtrackx_postprocessing.py \
#        -i ${tractDir_MNI}/${side}
#        #-t ${FSLDIR}/data/standard/MNI152_T1_2mm_brain_mask.nii.gz
#fi
#
### smoothing
#fslmaths ${reconImg} -kernel gauss 1.69865806 -fmean ${reconImg4s}
#
#if [ ! -e ${reconImgMNI_ds} ]
#then
#echo 'Downsampling'
#flirt \
#    -in ${reconImg} \
#    -ref ${reconImg} \
#    -applyisoxfm 4 \
#    -out ${reconImg_ds_3}
#fi
#
#if [ ! -e ${reconImg_ds_4} ]
#then
#    flirt \
#        -in ${reconImg} \
#        -ref ${reconImg} \
#        -applyisoxfm 3 \
#        -out ${reconImg_ds_4}
#fi
#
#if [ ! -e ${reconImg_ds_3_4s} ]
#then
#    flirt \
#        -in ${reconImg4s} \
#        -ref ${reconImg4s} \
#        -applyisoxfm 3 \
#        -out ${reconImg_ds_3_4s}
#fi
