import numpy as np
from time import time
import multiprocessing as mp
import h5py
import scipy.stats as s
from multiprocessing import Pool
import sys
import pandas as pd
import scipy.interpolate as sp
import os

# Lat index where we start processing
n = int(sys.argv[1])

# Prepare data
h5_file = '../processed/wakemap_production.h5'
f = h5py.File(h5_file, 'r')

# Grab wind speed variables
ws_speeds = {}
ws_speeds['no_farms'] = f['windspeed_80m_no_farms'][:, n, :]
ws_speeds['all_farms'] = f['windspeed_80m_all_farms'][:, n, :]

# Number of indices across lon dimension
num_calcs = ws_speeds['no_farms'].shape[1]
#num_calcs = 10

# Create empty arrays that we'll fit with the Weibull data
A = np.empty((num_calcs))
k = np.empty((num_calcs))
gcf = np.empty((num_calcs))

# Load power curve we'll use for GCF assessment
pc = pd.read_csv('/home/moptis/repos/aws_wrf_tools/turbines/national/wind-turbine-2.tbl', skiprows = 2, header = None, sep = " ")
pc.columns = ['ws', 'thrust', 'power']
pc['power'] = pc['power']/1000
pc.loc[55] = [0,0,0]
pc.loc[56] = [30.1, 0., 0.]
pc.loc[57] = [1000., 0., 0.]

def calculate_weibull(ws):
    #print(row.shape)
    wfit = s.weibull_min.fit(ws, floc = 0)
    #print(wfit)
    return wfit

for key, item in ws_speeds.items():    
    test_path = "./weibull_output/gcf_%s_%s.csv" % (key, str(n).zfill(3),)
    if not os.path.exists(test_path): 
        for t in np.arange(num_calcs): # Loop through lon dimensions  
            # Get Weibull fit
            weib = calculate_weibull(item[:,t])

            # Assign fit results to variables
            A[t] = weib[2]
            k[t] = weib[0]

            # Sample from the distribution 10,000 times
            #ws_samp = s.weibull_min.rvs(k[t], 0, A[t], size = 100000)

            f = sp.interp1d(pc['ws'], pc['power'])
            pw_samp = f(item[:,t])
            gcf[t] = pw_samp.mean()
            #print(gcf)

        pd.DataFrame(A).to_csv('./weibull_output/A_%s_%s.csv' % (key,str(n).zfill(3),), header = None)
        pd.DataFrame(k).to_csv('./weibull_output/k_%s_%s.csv' % (key,str(n).zfill(3),), header = None)
        pd.DataFrame(gcf).to_csv('./weibull_output/gcf_%s_%s.csv' % (key,str(n).zfill(3),), header = None)
