import pandas as pd
import numpy as np

for v in ['gcf', 'A', 'k']:
    print(v)
    for t in ['no_farms', 'all_farms']:
        print(t)
        df_final = pd.DataFrame(columns = np.arange(549), index = np.arange(874))
        for n in np.arange(549): # Loop through saved latitude slices
            df = pd.read_csv('./weibull_output/%s_%s_%s.csv' % (v, t, str(n).zfill(3),), index_col = 0, header = None)
        #print(df.values[0])
            df_final[n] = df

        df_final.transpose().to_csv('./processed_output/%s_%s.csv' % (v,t))
