#COUNT=0
#for temp in `ls $OUTPUT/dr_stage3_ic*_tfce_corrp_tstat1.nii.gz`; do 
#	RESULTS[$COUNT]=$temp; 
#	let COUNT=$COUNT+1; 
#done
#
#COUNT=0
#for temp in `ls $ICADIR/groupmelodic.ica/stats/thresh_zstat*.nii.gz`; do 
#	INPUTCOMPS[$COUNT]=$temp; 
#	let COUNT=$COUNT+1; 
#done
#
#inputimages=''
#for (( COUNT=0; COUNT < ${#RESULTS[*]}; COUNT++ )); do   
#	DRIMAGE=`echo ${RESULTS[$COUNT]}`;
#	echo "DRIMAGE: " $DRIMAGE   
#	ICAMAP=`echo ${INPUTCOMPS[$COUNT]}`;
#	echo "ICAMAP: " $ICAMAP   
#	let ZSTATNUM=$COUNT+1; 
#	echo "ZSTATNUM: " $ZSTATNUM  
#
#	inputimages=`echo $inputimages ica$ZSTATNUM"_bin.nii.gz dr"$ZSTATNUM"_bin.nii.gz "`
#done
#
#echo "Inputimages is: " $inputimages
#
#slicesdir -o $inputimages






COUNT=0
for temp in `ls left_ds3/*stage2.nii.gz`; do 
	RESULTS[$COUNT]=$temp; 
	let COUNT=$COUNT+1; 
done

inputimages=''
for (( COUNT=0; COUNT < ${#RESULTS[*]}; COUNT++ )); do   
	DRIMAGE=`echo ${RESULTS[$COUNT]}`;
	echo "DRIMAGE: " $DRIMAGE   
	ICAMAP=lh_thalamus_HOSC_60_ds3.nii.gz;
	echo "ICAMAP: " $ICAMAP   
	let ZSTATNUM=$COUNT+1; 
	echo "ZSTATNUM: " $ZSTATNUM  

	inputimages=`echo $inputimages $ICAMAP $DRIMAGE`
done

echo "Inputimages is: " $inputimages

slicesdir -o $inputimages

