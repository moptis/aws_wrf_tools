#!/bin/bash

# We'll download data from 2018 through 2021.
# We'll need a bit of 2017-12 and 2022-01 as well for spin-up

# Get 2017-12 first
for y in 2017
do
for m in 12
  do
    mkdir -p /shared/era5_data/$y/$m/
    aws s3 cp s3://nwpm/era5_data/interm/$y/$m/ /shared/era5_data/$y/$m --recursive --exclude "*" --include "ERA5_*"
  done
done

# Then get 2022-01
for y in 2022
do
for m in 01
  do
    mkdir -p /shared/era5_data/$y/$m/
    aws s3 cp s3://nwpm/era5_data/interm/$y/$m/ /shared/era5_data/$y/$m --recursive --exclude "*" --include "ERA5_*"
  done
done

# Now get the four full years of data
for y in {2018..2021}
do
for m in {01..12}
  do
    mkdir -p /shared/era5_data/$y/$m/
    aws s3 cp s3://nwpm/era5_data/interm/$y/$m/ /shared/era5_data/$y/$m --recursive --exclude "*" --include "ERA5_*"
  done
done 
