#!/bin/bash

#SBATCH --job-name=WRF
#SBATCH --output=conus-%j.out
#SBATCH --ntasks=16
#SBATCH --exclusive

spack load intel-oneapi-mpi
spack load wrf
module load libfabric-aws
set -x
ulimit -s unlimited
ulimit -a

cd /shared/wrf_runs/$domain/$type/$n/
mpirun -np 16 ./wrf.exe
