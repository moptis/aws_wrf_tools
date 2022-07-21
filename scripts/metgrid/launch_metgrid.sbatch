#!/bin/bash

#SBATCH --job-name=WRF
#SBATCH --output=conus-%j.out
#SBATCH --ntasks=12
#SBATCH --exclusive

spack load intel-oneapi-mpi
spack load wrf
module load libfabric-aws
set -x
ulimit -s unlimited
ulimit -a

#for d in ./2*
for d in 2018_01 2019_02 2020_03 2018_04 2021_05 2021_06 2018_07 2018_08 2021_09 2020_10 2021_11 2019_12
do
  echo $d
  python $d/wps_ensemble.py red_pine &
done
wait
