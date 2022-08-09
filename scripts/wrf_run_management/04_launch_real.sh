#!/bin/bash

domain='spinning_spur'
t='distant'

export domain
export t

#for n in {001..179}
for n in {001..179}
do
   export n
   sbatch ./04b_submit_real.sbatch
done
