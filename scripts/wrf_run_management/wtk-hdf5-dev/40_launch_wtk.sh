#!/bin/bash

source activate wtk

domain='glacier'
export domain

#for t in 'all_farms' 'target_only' 'distant'
for t in all_farms
do
  export t

  for n in {001..179}
  #for n in 004
  do
    export n
    sbatch ./40b_submit_wtk.sbatch
  done
done
