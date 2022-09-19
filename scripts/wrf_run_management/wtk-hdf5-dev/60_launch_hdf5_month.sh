#!/bin/bash

domain="glacier"
export domain
#for m in {1..12}
#for m in 0 1 2 3 4 5 6 7 8 9 10 11
for m in 0
do
  export m
  sbatch 60b_submit_hdf5.sh glacier $m
done
