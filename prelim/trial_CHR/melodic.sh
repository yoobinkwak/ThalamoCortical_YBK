#mkdir melodic_output

#melodic -i for_melodic/bp_flirt.txt -o melodic_output/bp_flirt_10 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 10 --Ostats -a concat
#melodic -i for_melodic/bp_flirt.txt -o melodic_output/bp_flirt_20 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 20 --Ostats -a concat
#melodic -i for_melodic/bp_fnirt.txt -o melodic_output/re_bp_fnirt_10 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 10 --Ostats -a concat
#melodic -i for_melodic/bp_fnirt.txt -o melodic_output/re_bp_fnirt_20 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 20 --Ostats -a concat

#melodic -i for_melodic/hp_flirt.txt -o melodic_output/hp_flirt_10 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 10 --Ostats -a concat
#melodic -i for_melodic/hp_flirt.txt -o melodic_output/hp_flirt_20 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 20 --Ostats -a concat
#melodic -i for_melodic/hp_fnirt.txt -o melodic_output/hp_fnirt_10 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 10 --Ostats -a concat
#melodic -i for_melodic/hp_fnirt.txt -o melodic_output/hp_fnirt_20 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 20 --Ostats -a concat



#melodic -i for_melodic/3ds_bp_flirt.txt -o melodic_output/3ds_bp_flirt_10 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 10 --Ostats -a concat
#melodic -i for_melodic/3ds_bp_flirt.txt -o melodic_output/3ds_bp_flirt_20 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 20 --Ostats -a concat
#melodic -i for_melodic/3ds_bp_fnirt.txt -o melodic_output/3ds_bp_fnirt_10 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 10 --Ostats -a concat
#melodic -i for_melodic/3ds_bp_fnirt.txt -o melodic_output/3ds_bp_fnirt_20 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 20 --Ostats -a concat

#melodic -i for_melodic/3ds_hp_flirt.txt -o melodic_output/3ds_hp_flirt_10 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 10 --Ostats -a concat
#melodic -i for_melodic/3ds_hp_flirt.txt -o melodic_output/3ds_hp_flirt_20 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 20 --Ostats -a concat
#melodic -i for_melodic/3ds_hp_fnirt.txt -o melodic_output/3ds_hp_fnirt_10 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 10 --Ostats -a concat
#melodic -i for_melodic/3ds_hp_fnirt.txt -o melodic_output/3ds_hp_fnirt_20 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 20 --Ostats -a concat



#melodic -i for_melodic/4ds_bp_flirt.txt -o melodic_output/4ds_bp_flirt_10 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 10 --Ostats -a concat
#melodic -i for_melodic/4ds_bp_flirt.txt -o melodic_output/4ds_bp_flirt_20 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 20 --Ostats -a concat
#melodic -i for_melodic/4ds_bp_fnirt.txt -o melodic_output/re_4ds_bp_fnirt_10 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 10 --Ostats -a concat
#melodic -i for_melodic/4ds_bp_fnirt.txt -o melodic_output/4ds_bp_fnirt_20 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 20 --Ostats -a concat

#melodic -i for_melodic/4ds_hp_flirt.txt -o melodic_output/4ds_hp_flirt_10 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 10 --Ostats -a concat
#melodic -i for_melodic/4ds_hp_flirt.txt -o melodic_output/4ds_hp_flirt_20 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 20 --Ostats -a concat
#melodic -i for_melodic/4ds_hp_fnirt.txt -o melodic_output/4ds_hp_fnirt_10 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 10 --Ostats -a concat
#melodic -i for_melodic/4ds_hp_fnirt.txt -o melodic_output/4ds_hp_fnirt_20 -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report -d 20 --Ostats -a concat



#melodic -i for_melodic/bp_fnirt.txt -o melodic_output/re_bp_fnirt_auto -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report #--Ostats -a concat
melodic -i for_melodic/3ds_bp_fnirt.txt -o melodic_output/re_3ds_bp_fnirt_auto -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report --Ostats -a concat
#melodic -i for_melodic/4ds_bp_fnirt.txt -o melodic_output/4ds_bp_fnirt_auto -v --nobet --bgthreshold=10 --mmthresh=0.5 --tr=1 --report --Ostats -a concat
