for i in [CNF]*
do

paste ${i}/nuisance/demeaned_CSF_noise.txt ${i}/nuisance/demeaned_WM_noise.txt > ${i}/nuisance/design.txt

Text2Vest ${i}/nuisance/design.txt ${i}/nuisance/design.mat

Text2Vest ${i}/nuisance/contrast.txt ${i}/nuisance/design.con


Text2Vest ${i}/motion/demeaned_mn.txt ${i}/motion/design.mat
Text2Vest ${i}/motion/contrast.txt ${i}/motion/design.con


done




