import pandas as pd
import glob
import sys
import os

domain = sys.argv[1]

filepath = "/shared/processed/%s/timeseries" % domain

filelist = glob.glob(os.path.join(filepath,'*.csv'))

df_final = pd.DataFrame()
for f in filelist:
    df_final = df_final.append(pd.read_csv(f, index_col = 0))

df_final.to_csv(os.path.join(filepath, '/shared/processed/%s/power_ts_%s.csv' % (domain, domain)))


