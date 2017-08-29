for i in C*
do

#    mkdir ${i}/preprocess

#    cp -r preprocess_dpabi/FunImgAR/${i}/ra* ${i}/preprocess/
#    cp -r missed_preprocess_dpabi/FunImgAR/${i}/ra* ${i}/preprocess/
    
#    fslsplit ${i}/preprocess/ra* ${i}/preprocess/to_fix_tr_ra
#    fslmerge -tr ${i}/preprocess/tr_fixed_ra ${i}/preprocess/to_fix_tr_ra* 3.5

    mkdir ${i}/preprocess/registration

    cp -r ${i}/preprocess/tr_fixed_ra* ${i}/preprocess/registration/




done

