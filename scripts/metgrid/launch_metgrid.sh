#!/bin/bash

spack load intel-oneapi-mpi
spack load wrf
module load libfabric-aws
set -x
ulimit -s unlimited
ulimit -a

#for d in ./2*
for d in 2018_01 2020_02 2020_03 2019_04 2021_05 2020_06 2019_07 2018_08 2021_09 2018_10 2021_11 2019_12
do
  echo $d
  python $d/wps_ensemble.py wapsi
done
