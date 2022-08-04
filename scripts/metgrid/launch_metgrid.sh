#!/bin/bash

domain="pilot_hill"
export domain

for d in {2018..2021}
do
  export d
#for d in 2018_01 2019_02 2020_03 2018_04 2021_05 2021_06 2018_07 2018_08 2021_09 2020_10 2021_11 2019_12
  for m in {01..12}
  do
    export m
    sbatch submit_metgrid.sbatch
  done
done
