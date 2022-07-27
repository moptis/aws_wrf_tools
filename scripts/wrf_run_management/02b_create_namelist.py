
import pandas as pd
import sys
import os
import numpy as np
from calendar import monthrange
import sys

domain = sys.argv[1]
type = sys.argv[2]
root_dir = "./"

mo_df = pd.read_csv('/shared/aws_wrf_tools/key_inputs/model_months.csv')
df = mo_df.loc[mo_df['windfarm'] == domain]

# Turn integer month into string
def ID(x):
    if x < 10:
        return '0'+ str(x)[0:1]
    else:
        return str(x)[0:2]

dir = '001' # starting directory
for n in np.arange(0,12):
    year = df.loc[n, 'year']
    month = df.loc[n, 'month']
    dpm = monthrange(year, month)[1]
    st_date = pd.datetime(year, month, 1, 0, 0) - pd.Timedelta(12, 'H') # 12 hour spin up
    en_date = pd.datetime(year, month, 1, 0, 0) + pd.Timedelta(2, 'D') # 2-day sim 
    final_end = pd.datetime(year, month, 1, 0, 0) + pd.Timedelta(dpm, 'D') #+ pd.Timedelta(2, 'D') # Where we stop plus one day buffer
    print(final_end)

    while en_date <= final_end:
        end_diff = pd.Timedelta(final_end - en_date).days
        if end_diff < 2:
           en_date = final_end
        dirpath = root_dir + '/%s/' % type + dir
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        with open('/shared/aws_wrf_tools/namelists/namelist.input.template.3km', 'r') as file:
            filedata = file.read()
        
            # Write start and end dates
            filedata = filedata.replace('yst', str(st_date.year)) 
            filedata = filedata.replace('mst', ID(st_date.month))
            filedata = filedata.replace('dst', ID(st_date.day))                                                                                                  
            filedata = filedata.replace('hst', ID(st_date.hour))
            filedata = filedata.replace('yend', str(en_date.year))
            filedata = filedata.replace('mend', ID(en_date.month))
            filedata = filedata.replace('dend', ID(en_date.day))
            filedata = filedata.replace('hsty', str(year))
            filedata = filedata.replace('hstm', ID(month))        
            filedata = filedata.replace('rn_type', type)        

            with open('%s/%s/%s/namelist.input' % (root_dir,type,dir,), 'w') as file:
                file.write(filedata)
	    
            run_df = pd.read_csv('/shared/aws_wrf_tools/key_inputs/run_indices.csv', index_col = 0)
            run_df.loc[int(dir), domain] = st_date
            run_df.to_csv('/shared/aws_wrf_tools/key_inputs/run_indices.csv', index = True)
            # Update directory
            st_date = st_date + pd.Timedelta(2, 'D')
            en_date = en_date + pd.Timedelta(2, 'D')
            dir = str(int(dir) + 1).zfill(3)
