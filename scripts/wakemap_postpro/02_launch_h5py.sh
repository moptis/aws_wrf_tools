#!/bin/bash

for n in {1..179}
#for n in 15
do
  export n
  sbatch 02_submit_h5.sbatch
done