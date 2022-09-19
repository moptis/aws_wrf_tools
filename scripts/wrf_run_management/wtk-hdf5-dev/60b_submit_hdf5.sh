#!/bin/bash

#SBATCH --job-name=post-pro
#SBATCH --output=hdf5-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --exclusive

srun python 60c_run_hdf5.py $domain $m
