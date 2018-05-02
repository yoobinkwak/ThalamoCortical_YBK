#melodic -i list_tractogram_ds3_left.txt -o wmSC_ICA_cmd/ds3_left -v --nobet --bgthreshold=10 --report --bgimage=mni_brain_ds3.nii.gz --Ostats --mmthresh=0.5 -a tica
#melodic -i list_tractogram_ds3_left.txt -o wmSC_ICA_cmd/ds3_left_20IC -v --nobet --bgthreshold=10 -d 20 --report --bgimage=mni_brain_ds3.nii.gz --Ostats --mmthresh=0.5 -a tica



#melodic -i list_rsFC_ds3_left.txt -o rsFC_ICA_cmd/ds3_left -v --nobet --bgthreshold=10 --tr=1 --report --Ostats -a concat
#melodic -i list_rsFC_ds3_right.txt -o rsFC_ICA_cmd/ds3_right -v --nobet --bgthreshold=10 --tr=1 --report --Ostats -a concat


#melodic -i list_rsFC_ds3_left.txt -o rsFC_ICA_cmd/ds3_left_10ICs -v --nobet --bgthreshold=10 -d 10 --tr=1 --report --Ostats -a concat
#melodic -i list_rsFC_ds3_left.txt -o rsFC_ICA_cmd/ds3_left_20ICs -v --nobet --bgthreshold=10 -d 20 --tr=1 --report --Ostats -a concat
#melodic -i list_rsFC_ds3_right.txt -o rsFC_ICA_cmd/ds3_right_10ICs -v --nobet --bgthreshold=10 -d 10 --tr=1 --report --Ostats -a concat
#melodic -i list_rsFC_ds3_right.txt -o rsFC_ICA_cmd/ds3_right_20ICs -v --nobet --bgthreshold=10 -d 20 --tr=1 --report --Ostats -a concat



#melodic -i list_rsFC_ds3_bi.txt -o rsFC_ICA_cmd/ds3_bi -v --nobet --bgthreshold=10 --tr=1 --report --Ostats -a concat
#melodic -i list_rsFC_ds3_bi.txt -o rsFC_ICA_cmd/ds3_bi_10ICs -v --nobet --bgthreshold=10 -d 10 --tr=1 --report --Ostats -a concat
#melodic -i list_rsFC_ds3_bi.txt -o rsFC_ICA_cmd/ds3_bi_20ICs -v --nobet --bgthreshold=10 -d 20 --tr=1 --report --Ostats -a concat



#melodic -i list_rsFC_ds3_fwhm6_bi.txt -o rsFC_ICA_cmd/ds3_bi_fwhm6 -v --nobet --bgthreshold=10 --tr=1 --report --Ostats -a concat
#melodic -i list_rsFC_ds3_fwhm6_bi.txt -o rsFC_ICA_cmd/ds3_bi_fwhm6_10ICs -v --nobet --bgthreshold=10 -d 10 --tr=1 --report --Ostats -a concat
#melodic -i list_rsFC_ds3_fwhm6_bi.txt -o rsFC_ICA_cmd/ds3_bi_fwhm6_20ICs -v --nobet --bgthreshold=10 -d 20 --tr=1 --report --Ostats -a concat


#melodic -i list_rsFC_ds3_fwhm6_bi.txt -o rsFC_ICA_cmd/ds3_bi_fwhm6_20ICs_masked -v --nobet --bgthreshold=10 -d 20 --tr=1 --report --Ostats -a concat -m mni_brain_ds3.nii.gz --bgimage=mni_brain_ds3.nii.gz
#melodic -i list_rsFC_ds3_fwhm6_bi.txt -o rsFC_ICA_cmd/ds3_bi_fwhm6_masked -v --nobet --bgthreshold=10 --tr=1 --report --Ostats -a concat -m mni_brain_ds3.nii.gz --bgimage=mni_brain_ds3.nii.gz
#melodic -i list_rsFC_ds3_fwhm6_bi.txt -o rsFC_ICA_cmd/ds3_bi_fwhm6_10ICs_masked -v --nobet --bgthreshold=10 -d 10 --tr=1 --report --Ostats -a concat -m mni_brain_ds3.nii.gz --bgimage=mni_brain_ds3.nii.gz




#melodic -i list_rsFC_ds3_bi.txt -o rsFC_ICA_cmd/ds3_bi_20ICs_masked -v --nobet --bgthreshold=20 -d 20 --tr=1 --report --Ostats -a concat -m mni_brain_ds3.nii.gz --bgimage=mni_brain_ds3.nii.gz
#melodic -i list_rsFC_ds3_bi.txt -o rsFC_ICA_cmd/ds3_bi_masked -v --nobet --bgthreshold=20 --tr=1 --report --Ostats -a concat -m mni_brain_ds3.nii.gz --bgimage=mni_brain_ds3.nii.gz
#melodic -i list_rsFC_ds3_bi.txt -o rsFC_ICA_cmd/ds3_bi_10ICs_masked -v --nobet --bgthreshold=10 -d 10 --tr=1 --report --Ostats -a concat -m mni_brain_ds3.nii.gz --bgimage=mni_brain_ds3.nii.gz


#melodic -i list_NOR_rsFC_ds3_bi.txt -o rsFC_ICA_cmd/NOR_ds3_bi_20ICs_masked -v --nobet --bgthreshold=20 -d 20 --tr=1 --report --Ostats -a concat -m mni_brain_ds3.nii.gz --bgimage=mni_brain_ds3.nii.gz
#melodic -i list_NOR_rsFC_ds3_bi.txt -o rsFC_ICA_cmd/NOR_ds3_bi_10ICs_masked -v --nobet --bgthreshold=20 -d 10 --tr=1 --report --Ostats -a concat -m mni_brain_ds3.nii.gz --bgimage=mni_brain_ds3.nii.gz
#melodic -i list_NOR_rsFC_ds3_fwhm6_bi.txt -o rsFC_ICA_cmd/NOR_ds3_bi_fwhm6_20ICs_masked -v --nobet --bgthreshold=20 -d 20 --tr=1 --report --Ostats -a concat -m mni_brain_ds3.nii.gz --bgimage=mni_brain_ds3.nii.gz
#melodic -i list_NOR_rsFC_ds3_fwhm6_bi.txt -o rsFC_ICA_cmd/NOR_ds3_bi_fwhm6_10ICs_masked -v --nobet --bgthreshold=20 -d 10 --tr=1 --report --Ostats -a concat -m mni_brain_ds3.nii.gz --bgimage=mni_brain_ds3.nii.gz





#melodic -i list_thalTS_ds3_bi.txt -o thalTS_ICA_cmd/ds3_bi_10ICs -v --nobet --bgthreshold=20 -d 10 --tr=3.5 --report --Ostats -a concat 
#melodic -i list_thalTS_ds3_fwhm6_bi.txt -o thalTS_ICA_cmd/ds3_fwhm6_bi_10ICs -v --nobet --bgthreshold=20 -d 10 --tr=3.5 --report --Ostats -a concat 
#melodic -i list_thalTS_ds3_bi.txt -o thalTS_ICA_cmd/ds3_bi_20ICs -v --nobet --bgthreshold=20 -d 20 --tr=3.5 --report --Ostats -a concat 
#melodic -i list_thalTS_ds3_fwhm6_bi.txt -o thalTS_ICA_cmd/ds3_fwhm6_bi_20ICs -v --nobet --bgthreshold=20 -d 20 --tr=3.5 --report --Ostats -a concat 
#melodic -i list_thalTS_ds3_bi.txt -o thalTS_ICA_cmd/ds3_bi -v --nobet --bgthreshold=20 --tr=3.5 --report --Ostats -a concat 
#melodic -i list_thalTS_ds3_fwhm6_bi.txt -o thalTS_ICA_cmd/ds3_fwhm6_bi -v --nobet --bgthreshold=20 --tr=3.5 --report --Ostats -a concat 



melodic -i list_thalTS_bi.txt -o thalTS_ICA_cmd/bi_10ICs -v --nobet --bgthreshold=20 -d 10 --tr=3.5 --report --Ostats -a concat 
melodic -i list_thalTS_bi.txt -o thalTS_ICA_cmd/bi_20ICs -v --nobet --bgthreshold=20 -d 20 --tr=3.5 --report --Ostats -a concat 
melodic -i list_thalTS_bi.txt -o thalTS_ICA_cmd/bi -v --nobet --bgthreshold=20 --tr=3.5 --report --Ostats -a concat 
