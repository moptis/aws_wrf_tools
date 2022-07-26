#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 09:49:02 2019

@author: orybchuk

Split a large WPS file generation process into several smaller jobs by month
"""

from datetime import datetime, timedelta
from dateutil.rrule import rrule, MONTHLY
from dateutil.relativedelta import relativedelta
import os
import pandas as pd
from pathlib import Path
import sys

start_date = sys.argv[1] # YYYY-MM-DD format
end_date = sys.argv[2] # YYYY-MM-DD format
my_WPS = sys.argv[3] # WPS setup ('WPS1' for ERA5, 'WPS2' for MERRA2)

### Directory management
home_dir = os.getcwd()
scripts_dir = '/shared/aws_wrf_tools/scripts/interm2met/'
meta_data_dir = '/shared/aws_wrf_tools/key_inputs/'
# p = Path(home_dir)     # Note: this assumes the BOEM Pacific directory structure
# my_WPS = p.parts[-2]


assert ('WPS' in my_WPS), "WPS version is unknown"

### Dates for the entire run
start_date_str = '%s_00:00:00' % start_date    # MODIFY ME
end_date_str = '%s_00:00:00' % end_date      # MODIFY ME
start_date = datetime.strptime(start_date_str, '%Y-%m-%d_%H:%M:%S')
end_date = datetime.strptime(end_date_str, '%Y-%m-%d_%H:%M:%S')

### Split the large date range into month long periods
dir_list = []
my_date = start_date
while my_date < end_date:
    year = my_date.year
    month = my_date.month
    day = my_date.day
    dir_str = str(year)+'_'+str(month).zfill(2)
    if dir_str not in dir_list:
        dir_list.append(dir_str)

    my_date += timedelta(days=1)

### Make and populate a subdirectory for each month
for my_dir in dir_list:
    ## Make a subdirectory
    if not os.path.isdir(home_dir+'/'+my_dir):
        os.system('mkdir '+home_dir+'/'+my_dir)
    os.chdir(home_dir+'/'+my_dir)

    ## Populate with info for met_em
    # Buffer for initialization / post-initialization
    sbuffer = timedelta(days=1)
    ebuffer = timedelta(days=0)

    # Get start/end month
    sdate_sub = datetime.strptime(my_dir, '%Y_%m')
    edate_sub = sdate_sub+relativedelta(months=+1)

    # Add in the buffers
    sdate_sub -= sbuffer
    edate_sub += ebuffer
    sdate_sub_str = datetime.strftime(sdate_sub, '%Y-%m-%d_%H:%M:%S')
    edate_sub_str = datetime.strftime(edate_sub, '%Y-%m-%d_%H:%M:%S')

    # Store auxiliary info in a csv
    with open("aux_params.csv", "w") as f:
        f.write("WPS     start_date         end_date\n")
        f.write("{}     {}       {}".format(my_WPS,sdate_sub_str,edate_sub_str))

    ## Link met_em generation files
    os.system('cp '+scripts_dir+'init_namelist.py .')
    os.system('cp '+scripts_dir+'run_geogrid.py .')
    os.system('cp '+scripts_dir+'run_metgrid.py .')
    os.system('cp '+scripts_dir+'run_ungrib.py .')
    os.system('cp '+scripts_dir+'wps_ensemble.py .')
    os.system('cp '+scripts_dir+'namelist.wps.template .')
    os.system('cp '+meta_data_dir+'regions.csv .')
    os.system('cp '+meta_data_dir+'wps_setups.csv .')
