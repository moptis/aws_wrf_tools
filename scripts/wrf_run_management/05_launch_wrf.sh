#!/bin/bash

domain="fenton"
type="all_farms"
#for n in 001
for n in {001..179}
do
  echo $n
  export n
  export domain
  export type
  sbatch ./05b_submit_wrf.sbatch
done
