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
m = sys.argv[1] # Month to process

# Variables we want to end up with
vars = ['windspeed_80m_all_farms', 'windspeed_120m_all_farms', 'windspeed_80m_no_farms', 'windspeed_120m_no_farms', 'power']

# Variable names in wtk files
wtk_vars = ['windspeed_80m', 'windspeed_120m', 'power']

# Wind farm neighbor scenarios
types = ['all_farms', 'no_farms']

mo_df = pd.read_csv('/home/moptis/repos/aws_wrf_tools/key_inputs/model_months.csv', index_col = 0)
df = mo_df.loc[mo_df['windfarm'] == domain]
#df.reset_index(inplace = True)

print(df)

# Set dimensions of data
xdim = 874
ydim = 549


count = 0
month = int(m)
year = df.loc[month, 'year']
print(month, year)

# Set up our hdf5 file and temporary storage for data during processing
hf = h5py.File('/scratch/moptis/national/processed/wakemap_production.h5', 'w')
np_arrays = {}

for v in vars:
    for t in types:
        np_arrays[v] = np.empty((dpm*24*6, ydim, xdim), dtype = 'int16')
        np_arrays[v][:] = np.nan


st_date = pd.to_datetime('%s-%s-01' % (year, month,))
dpm = monthrange(year, month)[1]
end_date = pd.to_datetime('%s-%s-%s 23:50:00' % (year, month, dpm,))
print(st_date, end_date)

# Now get list of dates to loop through for each month
date_range = pd.date_range(st_date, end_date, freq = '10T')
hf.create_dataset('datetime', data = [str(d) for d in date_range])

for v in vars:
    for t in types:
        np_arrays[v] = np.empty((dpm*24*6, ydim, xdim), dtype = 'int16')
        np_arrays[v][:] = np.nan

# Loop through each date
for d in date_range:
    print(d)
    for it, t in enumerate(types):
        # Specify the target nc file we want to process
        target_file = '/scratch/moptis/national/processed/%s_tke_off/all/wrfout_d01_%s-%s-%s_%s_%s_00.nc' \
                % (t, d.year, str(d.month).zfill(2), str(d.day).zfill(2), str(d.hour).zfill(2), str(d.minute).zfill(2),)

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

