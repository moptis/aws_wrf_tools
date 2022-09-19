#!/bin/bash

#SBATCH --job-name=wtk
#SBATCH --output=wtk-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --exclusive

source activate wtk

#set -x
#ulimit -s unlimited
#ulimit -a


wrf_dir=/shared/wrf_runs/${domain}/$t/$n
echo ${wrf_dir}

wtk_dir=/shared/processed/${domain}/wtk/$t/$n
echo ${wtk_dir}
mkdir -p "${wtk_dir}"

prefix=wrfout_d02
wrf_file_size=0.002
workers=16
attr_path=/shared/aws_wrf_tools/key_inputs/wtk_attrs.json

#wtk --file_prefix=${prefix} --process_dir=/shared/temp run-wrf-to-wtk ${wrf_dir} ${wtk_dir} ${wrf_file_size} --max_workers=${workers} --var_attr_path=${attr_path}

wtk run-wrf-to-wtk --wrf_dir=${wrf_dir} --wtk_dir=${wtk_dir} --wrf_file_size=${wrf_file_size} --file_prefix=${prefix} --process_dir=${wrf_dir} --max_workers=${workers} --var_attr_path=${attr_path}

