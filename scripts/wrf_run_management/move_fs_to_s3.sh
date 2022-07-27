#!/bin/bash

domain='red_pine'

aws s3 mv /shared/processed/$domain/power_ts_$domain.csv s3://nwpm/processed_results/$domain

aws s3 mv /shared/processed/$domain/timeseries s3://nwpm/processed_results/$domain/timeseries --recursive

for m in {001..179}
do
  echo $m
  aws s3 mv /shared/processed/$domain/domain/$m s3://nwpm/processed_results/$domain/domain/$m  --recursive
  #mv ./$domain/*_20*-$m-* ./$domain/$m
done
