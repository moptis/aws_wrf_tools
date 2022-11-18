#!/bin/bash


pip install cdsapi
pip install numpy

#for y in {2016..2021}
for y in 2022
do

#for i in {01..12}
#for i in {01..12}
for i in 01
do
#   python ./GetERA5-pl.py $y $i
   python ./GetERA5-sl.py $y $i 
   echo $i

done
done
