for i in $@
do
	OM_dir=${i}/rsFC_OMuircheartaigh
	if [ ! -d ${OM_dir} ]
	then
		mkdir ${OM_dir}
	fi
#### rsfMRI preprocessing ####
	OM_rs=${OM_dir}/rs_preproc_OM
	if [ ! -d ${OM_rs} ]
	then
		mkdir ${OM_rs}
	fi
	#### discard initial 4 ts ####
	fslroi <raw> ${OM_rs}/<"prefiltered_func_data"> 4 112
	#### motion correction ####
	mcflirt -in ${OM_rs}/<prefiltered_func_data> -out ${OM_rs}/<"prefiltered_func_data_mcf"> -mats -plots -rmsrel -rmsabs -spline_final
	#### slice time correction ####
	slicetimer -i ${OM_rs}/<prefiltered_func_data_mcf> --out=${OM_rs}/<"prefiltered_func_data_st"> -r 3.500000 --odd
	##### brain extraction #####
	fslmaths ${OM_rs}/<prefiltered_func_data_st> -Tmean ${OM_rs}/<"mean_func">
	bet2 ${OM_rs}/<mean_func> ${OM_rs}/<"mask"> -f 0.3 -n -m
	fslmaths ${OM_rs}/<prefiltered_func_data_st> -mas ${OM_rs}/<mask_mask> ${OM_rs}/<"prefiltered_func_data_bet">
	#### included in FEAT GUI log ####
	fslstats ${OM_rs}/<prefiltered_func_data_bet> -p 2 -p 98
	0.000000 1118.926392
	fslmaths ${OM_rs}/<prefiltered_func_data_bet> -thr 111.8926392 -Tmin -bin ${OM_rs}/<mask_mask> -odt char
	fslstats ${OM_rs}/<prefiltered_func_data_st> -k ${OM_rs}/<mask_mask> -p 50
899.346130 
	fslmaths ${OM_rs}/<mask_mask> -dilF ${OM_rs}/<"mask_dilF">
	fslmaths ${OM_rs}/<prefiltered_func_data_st> -mas ${OM_rs}/<mask_dilF> ${OM_rs}/<"prefiltered_func_data_thresh">
	fslmaths ${OM_rs}/<prefiltered_func_data_thresh> -mul 11.1191894493 ${OM_rs}/<"prefiltered_func_data_intnorm">		### I don't get where 11.1191894493 came frome
	fslmaths ${OM_rs}/<prefiltered_func_data_intnorm> -Tmean ${OM_rs}/<"tempMean">
	#### temporal high pass filter (0.1Hz=100s) ####
	fslmaths ${OM_rs}/<prefiltered_func_data_intnorm> -bptf 14.2857142857 -1 -add ${OM_rs}/<tempMean> ${OM_rs}/<"filtered_func_data">
	fslmaths ${OM_rs}/<filtered_func_data> -Tmean ${OM_rs}/<"mean_func">		## feat process

#### rsfMRI, T1, & MNI 2mm registration ####
	OM_register=${OM_dir}/rs_register_OM
	if [ ! -d ${OM_register} ]
	then
		mkdir ${OM_register}
	fi
	EPI_hp=${OM_rs}/<filtered_func_data>
	T1=<T1>		### using oriented T1 (bc epi_reg does not have search options)
	T1_brain=<T1_brain>
	MNI=/usr/local/fsl/data/standard/MNI152_T1_2mm
	MNI_brain=/usr/local/fsl/data/standard/MNI152_T1_2mm_brain
	MNI_brain_mask=/usr/local/fsl/data/standard/MNI152_T1_2mm_brain_mask_dil
	epi_reg --noclean --epi=${EPI_hp} --t1=${T1} --t1brain=${T1_brain} --out=${OM_register}/rs_to_t1
	convert_xfm -inverse -omat ${OM_register}/t1_to_rs.mat ${OM_register}/rs_to_t1.mat
	flirt -in ${T1_brain} -ref ${MNI_brain} -out ${OM_register}/t1_to_mni_flirt -omat ${OM_register}/t1_to_mni_flirt.mat -cost corratio -dof 12 -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -interp trilinear
	convert_xfm -inverse -omat ${OM_register}/mni_to_t1_flirt.mat ${OM_register}/t1_to_mni_flirt.mat
	convert_xfm -omat ${OM_register}/rs_to_mni.mat -concat ${OM_register}/t1_to_mni_flirt.mat ${OM_register}/rs_to_t1.mat
	convert_xfm -inverse -omat ${OM_register}/mni_to_rs.mat ${OM_register}/rs_to_mni.mat
	fnirt --iout=${OM_register}/t1_to_mni_head_fnirt --in=${T1} --aff=${OM_register}/t1_to_mni_flirt.mat --cout=${OM_register}/t1_to_mni_warp --iout=${OM_register}/t1_to_mni_fnirt --jout=${OM_register}/t1_to_t1_jac --ref=${MNI} --refmask=${MNI_brain_mask}
	applywarp -i ${T1_brain} -r ${MNI_brain} -o ${OM_register}/t1_to_mni_brain_fnirt -w ${OM_register}/t1_to_mni_warp
	convertwarp --ref=${MNI_brain} --premat=${OM_register}/rs_to_t1.mat --warp1=${OM_register}/t1_to_mni_warp --out=${OM_register}/rs_to_mni_warp
	applywarp -i ${EPI_hp} -r ${MNI_brain} -o ${OM_register}/rs_to_mni -w ${OM_register}/rs_to_mni_warp

#### Regressions #####
	OM_regress=${OM_dir}/rs_regress_OM
	if [ ! -d ${OM_regress} ]
	then
		mkdir ${OM_regress}
	fi
	#### calculate functional ts for each thalamic IC segments ####	
	fsl_glm -i ${EPI_hp} -d <each thalamic IC> -o ${OM_regress}/<ts of each thalamic IC>
	##### for nuisance regression ####
	applywarp -r ${MNI_brain} -i ${OM_reg}/rs_to_t1_fast_pve_0.nii.gz -w ${OM_reg}/t1_to_mni_warp -o ${OM_regress}/CSF.nii.gz
	applywarp -r ${MNI_brain} -i ${OM_reg}/rs_to_t1_fast_pve_2.nii.gz -w ${OM_reg}/t1_to_mni_warp -o ${OM_regress}/WM.nii.gz
	fslmaths ${OM_regress}/CSF.nii.gz -thr 0.50 ${OM_regress}/thr_CSF.nii.gz
	fslmaths ${OM_regress}/WM.nii.gz -thr 0.75 ${OM_regress}/thr_WM.nii.gz
	fslmeants -i ${OM_register}/rs_to_mni -o ${OM_regress}/CSF_noise.txt -m ${OM_regress}/thr_CSF.nii.gz
	fslmeants -i ${OM_register}/rs_to_mni -o ${OM_regress}/WM_noise.txt -m ${OM_regress}/thr_WM.nii.gz
	
	paste ${OM_regress}/<ts of each thalamic IC> <expanded motion parameters> <scans with excessive motion> <WM noise> <CSF noise> > ${OM_regress}/<each_IC_design.txt>
	Text2Vest ${OM_regress}/<each_IC_design.txt> ${OM_regress}/<each_IC_design.mat>

	fsl_glm -i ${EPI_hp} -d ${OM_regress}/<each_IC_design.mat> -o ${OM_regress}/<each_IC_FCmap>
done

