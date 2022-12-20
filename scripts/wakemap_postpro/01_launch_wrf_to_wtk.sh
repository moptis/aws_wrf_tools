#!/bin/bash

source activate wtk

#for n in 001
for n in {001..179}
do
      export n
      sbatch ./wrf_to_wtk.sbatch
      sbatch ./wrf_to_wtk.sbatch_no_farms
done

