#!/bin/bash

#for y in {2018..2020}
for y in 2021
do
  for m in 12
#for m in {01..09}
  do
    mkdir -p /shared/era5_data/$y/$m/
    aws s3 cp s3://nwpm/era5_data/interm/$y/$m/ /shared/era5_data/$y/$m --recursive --exclude "*" --include "ERA5_*"
  done
done 
