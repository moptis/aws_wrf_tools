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

domain = sys.argv[1]

# Get hdf5 attributes from JSON file
f_h5_attrs = open('/shared/aws_wrf_tools/key_inputs/h5_attrs.json')
h5_attrs = json.load(f_h5_attrs)

# Variables we want to extract
vars = ['windspeed_100m', 'wind_power']

# Wind farm neighbor scenarios
types = ['all_farms', 'target_only', 'distant']

mo_df = pd.read_csv('/shared/aws_wrf_tools/key_inputs/model_months.csv')
df = mo_df.loc[mo_df['windfarm'] == domain]
df.reset_index(inplace = True)

print(df)
#for m in np.arange(12):
for m in [int(sys.argv[2])]:
    print(m)
    count = 0
    month = df.loc[m, 'month']
    year = df.loc[m, 'year']
    print(month, year)

    hf = h5py.File('/shared/processed/%s/%s_%s_%s.h5' % (domain, domain, year, str(month).zfill(2)), 'w')
    
    st_date = pd.to_datetime('%s-%s-01' % (year, month,))
    dpm = monthrange(year, month)[1]
    end_date = pd.to_datetime('%s-%s-%s 23:50:00' % (year, month, dpm,))
    print(st_date, end_date)

    # Now get list of dates to loop through for each month
    date_range = pd.date_range(st_date, end_date, freq = '10T')
    
    hf.create_dataset('datetime', data = [str(d) for d in date_range])
    np_arrays = {}
    for v in vars:
        for t in types:
            np_arrays[v] = np.empty((dpm*24*6, 3, 150, 150), dtype = 'float32')
            np_arrays[v][:] = np.nan
    
    # Loop through each date
    for d in date_range:
        sub_folder = str(d).split(' ')[0]
        for it, t in enumerate(types):
            target_file = '/shared/processed/%s/wtk/%s/all/wrfout_d02_%s-%s-%s_%s_%s_00.nc' \
                % (domain, t, d.year, str(d.month).zfill(2), str(d.day).zfill(2), str(d.hour).zfill(2), str(d.minute).zfill(2),)

            #for pp in [0]: #
            try:
                ndata = nc.Dataset(target_file)
                for v in vars:
                    np_arrays[v][count, it, :, :] = ndata.variables[v][0, :, :]
            except:
                print('data corrupt or not found')
        
        # Crucial counter to make sure the dates are aligned
        count = count + 1    


    for v in vars:
        hf.create_dataset(v, data = np_arrays[v])
    hf.close()





