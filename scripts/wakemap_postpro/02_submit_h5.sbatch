#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --account=ca20
#SBATCH --qos=high
#SBATCH --partition=short

srun python3 h5_process_v3.py $n
