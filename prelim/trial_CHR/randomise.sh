#mkdir group_ave_FC
#mkdir group_ave_FC/to_concat
#mkdir group_ave_FC/concated


##for j in 3ds_bp_fnirt 4ds_bp_fnirt
##do




for ic in 0 1 2 3 4 5 6 7 8 9
do
    for ic2 in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19
    do
        for i in C*
        do

##                fslmerge -t group_ave_FC/concat_${j}_10_IC${ic}.nii.gz ${i}/dual_reg_eachIC/temporal_reg_${j}_10_IC${ic}.nii.gz*   
##                fslmerge -t group_ave_FC/concat_${j}_20_IC${ic2}.nii.gz ${i}/dual_reg_eachIC/temporal_reg_${j}_20_IC${ic2}.nii.gz*

##            randomise -i group_ave_FC/concat_${j}_10_IC${ic}.nii.gz -o group_ave_FC/randomised_${j}_10_IC${ic}.nii.gz -1 -T
##            randomise -i group_ave_FC/concat_${j}_20_IC${ic2}.nii.gz -o group_ave_FC/randomised_${j}_20_IC${ic2}.nii.gz -1 -T

            cp -r ${i}/dual_reg_eachIC/temporal_reg_3ds_bp_fnirt_10_IC${ic}.nii.gz group_ave_FC/to_concat/${i}_temporal_reg_3ds_bp_fnirt_10_IC${ic}.nii.gz 
            cp -r ${i}/dual_reg_eachIC/temporal_reg_3ds_bp_fnirt_20_IC${ic2}.nii.gz group_ave_FC/to_concat/${i}_temporal_reg_3ds_bp_fnirt_20_IC${ic2}.nii.gz 
            cp -r ${i}/dual_reg_eachIC/temporal_reg_4ds_bp_fnirt_20_IC${ic2}.nii.gz group_ave_FC/to_concat/${i}_temporal_reg_4ds_bp_fnirt_20_IC${ic2}.nii.gz 

        done
    done
done



for ic in 0 1 2 3 4 5 6 7 8 9
do

    fslmerge -t group_ave_FC/concated/concat_3ds_bp_fnirt_10_IC${ic}.nii.gz group_ave_FC/to_concat/*3ds_bp_fnirt_10_IC${ic}.nii.gz

    randomise -i group_ave_FC/concated/concat_3ds_bp_fnirt_10_IC${ic}.nii.gz -o group_ave_FC/randomised_3ds_bp_fnirt_10_IC${ic}.nii.gz -1 -T
    
    if [ ! -f group_ave_FC/randomised_3ds_bp_fnirt_10_IC${ic}.nii.gz ]
    then
        rm -rf group_ave_FC/to_concat/*_3ds_bp_fnirt_10_IC${ic}.nii.gz 
    fi
done



for ic2 in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19
do
 
    fslmerge -t group_ave_FC/concated/concat_3ds_bp_fnirt_20_IC${ic2}.nii.gz group_ave_FC/to_concat/*3ds_bp_fnirt_20_IC${ic2}.nii.gz                 
    fslmerge -t group_ave_FC/concated/concat_4ds_bp_fnirt_20_IC${ic2}.nii.gz group_ave_FC/to_concat/*4ds_bp_fnirt_20_IC${ic2}.nii.gz 

            
    randomise -i group_ave_FC/concated/concat_3ds_bp_fnirt_20_IC${ic2}.nii.gz -o group_ave_FC/randomised_3ds_bp_fnirt_20_IC${ic2}.nii.gz -1 -T
    randomise -i group_ave_FC/concated/concat_4ds_bp_fnirt_20_IC${ic2}.nii.gz -o group_ave_FC/randomised_4ds_bp_fnirt_20_IC${ic2}.nii.gz -1 -T


    if [ ! -f group_ave_FC/randomised_3ds_bp_fnirt_20_IC${ic2}.nii.gz ]
    then
        rm -rf group_ave_FC/to_concat/*3ds_bp_fnirt_20_IC${ic2}.nii.gz 
    fi

    if [ ! -f group_ave_FC/randomised_4ds_bp_fnirt_20_IC${ic2}.nii.gz ]
    then
        rm -rf group_ave_FC/to_concat/*4ds_bp_fnirt_20_IC${ic2}.nii.gz 
    fi
done





