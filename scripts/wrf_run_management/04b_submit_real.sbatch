#!/bin/bash

#SBATCH --job-name=real
#SBATCH --output=conus-%j.out
#SBATCH --ntasks=179

spack load intel-oneapi-mpi
spack load wrf
module load libfabric-aws
set -x
ulimit -s unlimited
ulimit -a

for n in {001..179}
do

  cd /shared/wrf_runs/$domain/$t/$n/
  srun --ntasks=1 -c 1 --exclusive ./real.exe &
done
wait
