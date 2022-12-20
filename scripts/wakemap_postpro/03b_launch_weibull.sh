#!/bin/bash

#for n in {002..179}
for n in {180..550}
do
  export n
  sbatch 03_submit_weibull.sbatch	
done
