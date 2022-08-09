#!/bin/bash

#SBATCH --job-name=real
#SBATCH --output=real-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --exclusive

spack load intel-oneapi-mpi
spack load wrf
module load libfabric-aws
set -x
ulimit -s unlimited
ulimit -a

#for n in {001..179}
#do

  cd /shared/wrf_runs/$domain/$t/$n/
  srun ./real.exe
  #mpirun -np 1 ./real.exe
#done
#wait
