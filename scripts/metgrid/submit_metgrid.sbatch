#!/bin/bash

#SBATCH --job-name=WRF
#SBATCH --output=conus-%j.out
#SBATCH --ntasks=48
#SBATCH --exclusive

spack load intel-oneapi-mpi
spack load wrf
module load libfabric-aws
set -x
ulimit -s unlimited
ulimit -a

python ${d}_${m}/wps_ensemble.py $domain
