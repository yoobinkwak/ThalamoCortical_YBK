for i in [CFN]*
do

    cp -r ${i}/downsampled/fisherZ_3ds.nii.gz ${i}/downsampled/edit_fisherZ_3ds.nii.gz
    fslhd -x ${i}/downsampled/edit_fisherZ_3ds.nii.gz > ${i}/downsampled/edit_fisherZ_3ds.txt

    cp -r ${i}/downsampled/fisherZ_4ds.nii.gz ${i}/downsampled/edit_fisherZ_4ds.nii.gz
    fslhd -x ${i}/downsampled/edit_fisherZ_4ds.nii.gz > ${i}/downsampled/edit_fisherZ_4ds.txt

    cp -r ${i}/downsampled/fisherZ_5ds.nii.gz ${i}/downsampled/edit_fisherZ_5ds.nii.gz
    fslhd -x ${i}/downsampled/edit_fisherZ_5ds.nii.gz > ${i}/downsampled/edit_fisherZ_5ds.txt

    sed -i -e "s/dt = '1'/dt = '3.50'/g" ${i}/downsampled/edit_fisherZ_3ds.txt
    sed -i -e "s/dt = '1'/dt = '3.50'/g" ${i}/downsampled/edit_fisherZ_4ds.txt
    sed -i -e "s/dt = '1'/dt = '3.50'/g" ${i}/downsampled/edit_fisherZ_5ds.txt


    fslcreatehd ${i}/downsampled/edit_fisherZ_3ds.txt ${i}/downsampled/edit_fisherZ_3ds.nii.gz
    fslcreatehd ${i}/downsampled/edit_fisherZ_4ds.txt ${i}/downsampled/edit_fisherZ_4ds.nii.gz
    fslcreatehd ${i}/downsampled/edit_fisherZ_5ds.txt ${i}/downsampled/edit_fisherZ_5ds.nii.gz


done
   



#    cp -r ${i}/timeSeries/fisherZ_3ds.nii.gz ${i}/timeSeries/edit_fisherZ_3ds.nii.gz
#    fslhd -x ${i}/timeSeries/edit_fisherZ_3ds.nii.gz > ${i}/timeSeries/edit_fisherZ_3ds.txt

#    cp -r ${i}/timeSeries/fisherZ_4ds.nii.gz ${i}/timeSeries/edit_fisherZ_4ds.nii.gz
#    fslhd -x ${i}/timeSeries/edit_fisherZ_4ds.nii.gz > ${i}/timeSeries/edit_fisherZ_4ds.txt

#    cp -r ${i}/timeSeries/fisherZ_5ds.nii.gz ${i}/timeSeries/edit_fisherZ_5ds.nii.gz
#    fslhd -x ${i}/timeSeries/edit_fisherZ_5ds.nii.gz > ${i}/timeSeries/edit_fisherZ_5ds.txt

#    sed -i -e "s/dt = '1'/dt = '3.50'/g" ${i}/timeSeries/edit_fisherZ_3ds.txt
#    sed -i -e "s/dt = '1'/dt = '3.50'/g" ${i}/timeSeries/edit_fisherZ_4ds.txt
#    sed -i -e "s/dt = '1'/dt = '3.50'/g" ${i}/timeSeries/edit_fisherZ_5ds.txt


#    fslcreatehd ${i}/timeSeries/edit_fisherZ_3ds.txt ${i}/timeSeries/edit_fisherZ_3ds.nii.gz
#    fslcreatehd ${i}/timeSeries/edit_fisherZ_4ds.txt ${i}/timeSeries/edit_fisherZ_4ds.nii.gz
#    fslcreatehd ${i}/timeSeries/edit_fisherZ_5ds.txt ${i}/timeSeries/edit_fisherZ_5ds.nii.gz

#done
