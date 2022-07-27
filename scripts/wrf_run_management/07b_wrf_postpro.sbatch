#!/bin/bash

#SBATCH --job-name=postpro
#SBATCH --output=postpro-%j.out
#SBATCH --ntasks=179

domain = 'fenton'

cp /shared/aws_wrf_tools/key_inputs/run_indices.csv .
cp /shared/aws_wrf_tools/key_inputs/farm_info.json .

for n in {1..179}
#for n in 1
do
  echo $n
  srun --ntasks=1 -c 1 --exclusive 07c_post_process_wrf.py $domain $n 
done
