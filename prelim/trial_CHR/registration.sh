
for i in $@ 
do

#    cp -r ${i}/raw/co* ${i}/preprocess/registration/T1.nii.gz
#    cp -r ${i}/bet/*T1_co.nii.gz ${i}/preprocess/registration/T1_brain.nii.gz

    Reg_dir=${i}/preprocess/registration
#    if [ ! -d ${Reg_dir} ]
#    then
#        mkdir ${Reg_dir}
#    fi 
	EPI_image=${i}/preprocess/registration/tr_fixed_ra*
	T1=${i}/preprocess/registration/T1.nii.gz
	T1_brain=${i}/preprocess/registration/T1_brain.nii.gz
	MNI_brain=/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain
	MNI=/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm
    

    ## Registeration of resting image (EPI) onto T1 space
	epi_reg --epi=${EPI_image} --t1=${T1} --t1brain=${T1_brain} --out=${Reg_dir}/rs_to_t1
	##epi_reg --epi=example_func --t1=highres_head --t1brain=highres --out=example_func2highres

    ## Create and save inverse matrix of the output matrix from epi_reg
	convert_xfm -inverse -omat ${Reg_dir}/t1_to_rs.mat ${Reg_dir}/rs_to_t1.mat
	##convert_xfm -inverse -omat highres2example_func.mat example_func2highres.mat
	###t1_to_rs.mat not used in this script

    ## Linear Registeration of T1_brain onto MNI space
	flirt -in ${T1_brain} -ref ${MNI_brain} -out ${Reg_dir}/t1_to_mni_flirt -omat ${Reg_dir}/t1_to_mni_flirt.mat -cost corratio -dof 12 -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -interp trilinear
	##flirt -in highres -ref standard -out highres2standard -omat highres2standard.mat -cost corratio -dof 12 -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -interp trilinear 

   ## Create and save inverse matrix of the output matrix from flirt
	convert_xfm -inverse -omat ${Reg_dir}/mni_to_t1_flirt.mat ${Reg_dir}/t1_to_mni_flirt.mat
	##convert_xfm -inverse -omat standard2highres.mat highres2standard.mat
	###mni_to_t1_flirt.mat not used in this script

   ## Concatenate resulting matrix of epi_reg and flirt 
	convert_xfm -omat ${Reg_dir}/rs_to_mni.mat -concat ${Reg_dir}/t1_to_mni_flirt.mat ${Reg_dir}/rs_to_t1.mat
	##convert_xfm -omat example_func2standard.mat -concat highres2standard.mat example_func2highres.mat

   ## Create and save inverse matrix of the concatenated matrix
	convert_xfm -inverse -omat ${Reg_dir}/mni_to_rs.mat ${Reg_dir}/rs_to_mni.mat
	##convert_xfm -inverse -omat standard2example_func.mat example_func2standard.mat
	###mni_to_rs.mat not used not used in this script

   ## Non-linear registration of T1 onto MNI space, using output matrix of flirt as affine matrix 
    fnirt --iout=${Reg_dir}/t1_to_mni_head_fnirt --in=${T1} --aff=${Reg_dir}/t1_to_mni_flirt.mat --cout=${Reg_dir}/t1_to_mni_warp --iout=${Reg_dir}/t1_to_mni_fnirt --jout=${Reg_dir}/t1_to_t1_jac --ref=${MNI} --refmask=/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain_mask_dil 
	##fnirt --iout=highres2standard_head --in=highres_head --aff=highres2standard.mat --cout=highres2standard_warp --iout=highres2standard --jout=highres2highres_jac --config=T1_2_MNI152_2mm --ref=standard_head --refmask=standard_mask --warpres=10,10,10

    applywarp -i ${T1_brain} -r ${MNI_brain} -o ${Reg_dir}/t1_to_mni_brain_fnirt -w ${Reg_dir}/t1_to_mni_warp
	##applywarp -i highres -r standard -o highres2standard -w highres2standard_warp

   ## Create warp field coefficient for EPI to MNI registration
    convertwarp --ref=${MNI_brain} --premat=${Reg_dir}/rs_to_t1.mat --warp1=${Reg_dir}/t1_to_mni_warp --out=${Reg_dir}/rs_to_mni_warp
	##convertwarp --ref=standard --premat=example_func2highres.mat --warp1=highres2standard_warp --out=example_func2standard_warp

   ## Apply above to register EPI image onto MNI space
    applywarp --ref=${MNI_brain} --in=${EPI_image} --out=${Reg_dir}/rs_to_mni --warp=${Reg_dir}/rs_to_mni_warp
	##applywarp --ref=standard --in=example_func --out=example_func2standard --warp=example_func2standard_warp

done
