#!/home/ec2-user/miniconda3/envs/wrf/bin/python3

#SBATCH --output=postpro.log
#SBATCH --ntasks 1 # 1 core per run

# This script is used to post-process raw WRF runs using the cluster
# We create two files - a time series file at a selected point (usually a met mast grid cell)
# which contains power and met data for the target farm
# We also create 2D matrices of the whole domain for targeted variables like wind speed
# which we use mainly to observe wake losses on a map


from netCDF4 import Dataset
from wrf import getvar, interplevel, latlon_coords
import glob
import pickle as pk
import numpy as np
import multiprocessing as mp
import pandas as pd
import sys
import os
import json
from multiprocessing import Pool, Process

def process_wrf(d):
    # The main script that does the post-processing
    # d(str): the WRF run number

    data_dict = {} # Save processed data into single dictionary item
    ts_df = pd.DataFrame() # Save single point time series data as data frame
    #ts_df = pd.read_csv('/shared/processed/%s/timeseries/power_ts_%s.csv' % (domain, d,), index_col = 0)
    #ts_df.set_index(pd.to_datetime(ts_df.index), inplace = True)
    
    run_types = ['all_farms', 'target_only', 'distant'] # Which run type do we want to process
    #run_types = ['target_only']

    for r in run_types:
        # Where is data located
        run_dir = '/shared/wrf_runs/%s/%s/%s/' % (domain, r, d)
        #run_dir = '/shared/mys3/wrf_runs/%s/%s/%s/' % (domain,r,d)
    
        # Where are we saving to
        save_dir = '/shared/processed/%s/' % domain
        #save_dir = '/shared/mys3/processed_results/%s/' % domain

        # Create single-point timeseries folder
        save_ts = "%s/timeseries/" % save_dir
        os.makedirs(save_ts, exist_ok = True)
 
        # Get list of wrf output files in run directory and loop through them
        ncfiles = glob.glob('%s/wrfout_d02*' % run_dir)
        for i,n in enumerate(ncfiles):
            #for p in [0]:
            try:
                # Get the timestamp of the WRF output file
                date_str = n.split('/')[-1][11:]
                dt = pd.to_datetime(date_str, format = "%Y-%m-%d_%H:%M:%S")
            
                # Save domain data path
                save_path = "%s/domain/%s" % (save_dir, d,)
                os.makedirs(save_path, exist_ok = True)
                save_domain = "%s/%s_%s.p" % (save_path, r, date_str,)

                # Only process data if we're at or past our valid start date
                # I.e., don't include spin-up time
                if (dt>=st_date): # & (not os.path.exists(save_domain)):
                    print(st_date, dt)
                    # Load the netcdf file
                    ncfile = Dataset(n)
                    # Grab the variables we need for post-processing
                    ws = getvar(ncfile, "uvmet_wspd")
                    wd = getvar(ncfile, "uvmet_wdir")
                    pw = getvar(ncfile, "POWER")
                    th = getvar(ncfile, "theta")
                    temp = getvar(ncfile, "tc") # Temp in celsius
                    h = getvar(ncfile, "height_agl")
                    lats, lons = latlon_coords(h)
                    times = getvar(ncfile, 'xtimes')
                    tm = int(times.values)
                
                    # Interpolate data to the heights we need
                    ws_hh = interplevel(ws, h, ws_height) # Hub height wind speed
                    wd_hh = interplevel(wd, h, ws_height) # Hub height wind direction
                    th2 = interplevel(th, h, th_height2) # top pot. temp.
                    th1 = interplevel(th, h, th_height1) # lower pot. temp.
                    t2 = interplevel(temp, h, th_height2) # top pot. temp.
                    t1 = interplevel(temp, h, th_height1) # lower pot. temp.
    
                    # Assign data to our dictionary
                    data_dict['ws'] = ws_hh.to_numpy()
                    data_dict['wd'] = wd_hh.to_numpy()
                    data_dict['th2'] = th2.to_numpy()
                    data_dict['th1'] = th1.to_numpy()
                    data_dict['t2'] = t2.to_numpy()
                    data_dict['t1'] = t1.to_numpy()
                    data_dict['power'] = pw.to_numpy()
                
                    # Extract time series
                    fields = data_dict.keys()
                    for f in fields:
                        dtemp = data_dict[f]
                        if f=='power':
                            tot = 0
                            for c in coords:
                                
                                tot = tot + float(dtemp[c['lat'], c['lon']])
                                
                            dfinal = tot/1e6
                        else:
                            dsub = dtemp[fs_lat, fs_lon].values
                            dfinal = dsub

                        ts_df.loc[dt, '%s_%s' %(r,f,)] = dfinal
                    #print(ts_df)
                    # Now save data and close out netcdf file
                    pk.dump(data_dict, open(save_domain, "wb" ) )
                    ncfile.close()

                #ts_df.to_csv("%s/power_ts_%s.csv" % (save_ts, d,))
            except:
                print('corrupt')
        ts_df.to_csv("%s/power_ts_%s.csv" % (save_ts, d,))



# Let's grab the info we need for data extraction

domain = sys.argv[1] # Domain name given at input
n = int(sys.argv[2])

# Load run indices CSV that gives us the start dates for each 2-day run
#run_indices = pd.read_csv('/shared/key_inputs/run_indices.csv', index_col = 0)
run_indices = pd.read_csv('./run_indices.csv', index_col = 0)
domain_indices = run_indices.loc[:, domain]

# Now load the extraction data for each wind farm
farm_file = open('./farm_info.json', 'r')
farm_data = json.load(farm_file)

# Lat and lon ranges across the wind farm we'll need for power data extraction
coords = farm_data[domain]['pw_coords']

# Height of the wind speed we want to extract (should match highest available from site met tower)
ws_height = farm_data[domain]['ws_height']

# Heights where we extract potential temperature (again matching with met tower)
th_height1 = farm_data[domain]['th_height1']
th_height2 = farm_data[domain]['th_height2']

# Coordinate close to met tower with free stream sector but contains no turbines
fs_lat = farm_data[domain]['fs_lat']
fs_lon = farm_data[domain]['fs_lon']

## Main script that we could try to set up in parallel
if __name__=='__main__':
    st_date = pd.to_datetime(domain_indices.loc[n]) + pd.Timedelta(12, 'H')
    print(st_date)
    nf = str(n).zfill(3) # convert integer to 3-digit run code
    process_wrf(nf) # Call processing function
