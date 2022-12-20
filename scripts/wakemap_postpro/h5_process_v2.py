#####################################
# Script to process WTK-like output #
# into single hdf5 file             #
#####################################

import numpy as np
import h5py
import netCDF4 as nc
import json
import glob
import pandas as pd
import sys
from calendar import monthrange

domain = "national"

# Variables we want to end up with
#vars = ['windspeed_80m_all_farms', 'windspeed_120m_all_farms', 'windspeed_80m_no_farms', 'windspeed_120m_no_farms', 'power']
vars = ['windspeed_100m_all_farms', 'windspeed_100m_no_farms', 'winddirection', 'power']

# Wind farm neighbor scenarios
types = ['all_farms', 'no_farms']

# Set dimensions of data
xdim = 874
ydim = 549

hf = h5py.File('/scratch/moptis/national/processed/wakemap_production.h5', 'w')

# Now get list of dates to loop through for each month
nc_list = glob.glob('./all_farms/all/*.nc')
nc_list.sort(key = lambda x: x[-17:-3])

# Initialize data sets
h5_sets = {}
for v in vars:
    h5_sets[v] = hf.create_dataset(v, (8760*6, ydim, xdim))
hf.create_dataset('datetime', data = [c[-22:-3] for c in nc_list])


# Now loop through all_farms
nc_list = glob.glob('./all_farms/all/*.nc')
nc_list.sort(key = lambda x: x[-17:-3])
for j,d in enumerate(nc_list): # Loop through each file
    print(d)
    ndata = nc.Dataset(d)
    h5_sets['windspeed_100m_all_farms'][j,:,:] = ndata.variables['windspeed_100m'][0, :, :]
    h5_sets['power'][j,:,:] = ndata.variables['power'][0, :, :]


# Now loop through all_farms
nc_list = glob.glob('./no_farms/all/*.nc')
nc_list.sort(key = lambda x: x[-17:-3])
for j,d in enumerate(nc_list): # Loop through each file
    print(d)
    ndata = nc.Dataset(d)
    h5_sets['windspeed_100m_no_farms'][j,:,:] = ndata.variables['windspeed_100m'][0, :, :]
    h5_sets['winddirection'][j,:,:] = ndata.variables['winddirection_100m'][0, :, :]
    

hf.close()

'''
#for it, t in enumerate(types):
        # Specify the target nc file we want to process
        target_file = '/scratch/moptis/national/processed/%s/all/%s' % (t, d,)

        for pp in [0]: #
        #try:
            ndata = nc.Dataset(target_file)
            np_arrays['windspeed_80m_%s' % t][count, :, :] = ndata.variables['windspeed_80m'][0, :, :]
            np_arrays['windspeed_120m_%s' % t][count, :, :] = ndata.variables['windspeed_120m'][0, :, :]
            
            if t=="all_farms":
                 np_arrays['power'][count, :, :] = ndata.variables['power'][0, :, :]
        #except:
        #    print('data corrupt or not found')

    # Crucial counter to make sure the dates are aligned
    count = count + 1


for v in vars:
    hf.create_dataset(v, data = np_arrays[v])
hf.close()
'''
