#!/bin/bash

cp /shared/mys3/key_inputs/run_indices.csv .
cp /shared/aws_wrf_tools/key_inputs/farm_info.json .

for n in {2..179}
#for n in 1
do
  echo $n
  sbatch process_wrf_cluster_v2.py 'red_pine' $n 
done
