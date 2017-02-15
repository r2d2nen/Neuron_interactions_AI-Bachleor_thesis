#!/bin/bash

L=(450 475 500 525 550 575 600)
T=(125 158 191 224 257 290)

#L=(450)
#T=(125)


for iL in "${L[@]}"
do
    for iT in "${T[@]}"
    do

	cp ppFusion.ini ppFusion_gA_GV-$iL-$iT.ini
	sed -i 's/N2LOsim-500-290.ini/N2LOsim-'"$iL"'-'"$iT"'.ini/g' ppFusion_gA_GV-$iL-$iT.ini
	cp mpi-scan_ppFusion_gA_GV.sh mpi-scan_ppFusion_gA_GV-$iL-$iT.sh
	sed -i 's/500/'"$iL"'/g' mpi-scan_ppFusion_gA_GV-$iL-$iT.sh 
	sed -i 's/290/'"$iT"'/g' mpi-scan_ppFusion_gA_GV-$iL-$iT.sh 
	sbatch mpi-scan_ppFusion_gA_GV-$iL-$iT.sh
    done
done