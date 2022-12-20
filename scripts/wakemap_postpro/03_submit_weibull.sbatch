#!/bin/bash
#SBATCH --output=weib-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=36
#SBATCH --partition=short
#SBATCH --time=01:30:00
#SBATCH --account=ca20

# Loop through lat dimension and process weibulls, save each as a csv

#for (( k = 0; k < 9; ++k )); do
#  start=$((72*k))
#  end=$((start+71))
#  for (( n=$start; n<=$end; n++ ))
#  do
#    echo $n
#    sleep 2

python process_weibull.py $n

#  wait
#done

#for k in 41 47 48 54 55 63 69 71 74 87 145
#for k in {363..400}
#do
#  python process_weibull.py $k &
#done
#wait

#for k in {1..8} # Loop through 72 tasks 8 times to cover all lat coordinates
#do
#  loop_start=
#for n in {0..71}
#do 
#  python process_weibull.py $n &
#done
#wait
