#for j in bp_fnirt 3ds_bp_fnirt 4ds_bp_fnirt
#for j in 3ds_bp_fnirt 4ds_bp_fnirt
#do
#    for k in 10 20 auto
#    for k in 10 20 
#    do
#        melodic_dir=melodic_output/${j}_${k}
#        melodic_img=melodic_output/${j}_${k}/melodic_IC.nii.gz
        
#        if [ ! -d ${melodic_img} ]
#        then
#            echo ${melodic_img}
#
#            fslsplit ${melodic_img} ${melodic_dir}/${k}_IC -t
#        fi
#    done
#done


for i in $@
do
    mkdir ${i}/dual_reg_eachIC
        
    output_dir=${i}/dual_reg_eachIC
    thal_dir=${i}/preprocess/ds_filter
                
        
    for ic in 0 1 2 3 4 5 6 7 8 9
    do
        fsl_glm -i ${thal_dir}/L_thal_on_3ds_bp_fnirt.nii.gz -d melodic_output/3ds_bp_fnirt_10/10_IC000${ic}.nii.gz -o ${output_dir}/spatial_reg_3ds_bp_fnirt_10_IC${ic}
        fsl_glm -i ${thal_dir}/L_thal_on_3ds_bp_fnirt.nii.gz -d ${output_dir}/spatial_reg_3ds_bp_fnirt_10_IC${ic} -o ${output_dir}/temporal_reg_3ds_bp_fnirt_10_IC${ic}
    done
    
    
    for ic2 in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19
    do
        fsl_glm -i ${thal_dir}/L_thal_on_3ds_bp_fnirt.nii.gz -d melodic_output/3ds_bp_fnirt_20/20_IC00${ic2}.nii.gz -o ${output_dir}/spatial_reg_3ds_bp_fnirt_20_IC${ic2}
        fsl_glm -i ${thal_dir}/L_thal_on_3ds_bp_fnirt.nii.gz -d ${output_dir}/spatial_reg_3ds_bp_fnirt_20_IC${ic2} -o ${output_dir}/temporal_reg_3ds_bp_fnirt_20_IC${ic2}
        
        fsl_glm -i ${thal_dir}/L_thal_on_4ds_bp_fnirt.nii.gz -d melodic_output/4ds_bp_fnirt_20/20_IC00${ic2}.nii.gz -o ${output_dir}/spatial_reg_4ds_bp_fnirt_20_IC${ic2}            
        fsl_glm -i ${thal_dir}/L_thal_on_4ds_bp_fnirt.nii.gz -d ${output_dir}/spatial_reg_4ds_bp_fnirt_20_IC${ic2} -o ${output_dir}/temporal_reg_4ds_bp_fnirt_20_IC${ic2}
    done
    
done
    

                
