
#for j in bp_fnirt 3ds_bp_fnirt 4ds_bp_fnirt
for j in 3ds_bp_fnirt 4ds_bp_fnirt
do
#    for k in 10 20 auto 
    for k in 10 20 
    do
        melodic_img=melodic_output/${j}_${k}/melodic_IC.nii.gz

        if [ ! -d ${melodic_img} ]
        then
            echo ${melodic_img}

            for i in $@
            do
                mkdir ${i}/dual_reg
                
                output_dir=${i}/dual_reg
                
                thal_img=${i}/preprocess/ds_filter/L_thal_on_${j}.nii.gz


                fsl_glm -i ${thal_img} -d ${melodic_img} -o ${output_dir}/spatial_reg_${j}_${k}
                fsl_glm -i ${thal_img} -d ${output_dir}/spatial_reg_${j}_${k} -o ${output_dir}/temporal_reg_${j}_${k}

            done

        fi

    done

done
        




