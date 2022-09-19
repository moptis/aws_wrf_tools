
from wtk.to_h5.wtk_to_h5 import NCtoH5, WTKtoH5

import sys

domain = sys.argv[1]
type = sys.argv[2]
'''
max_workers=1
var_attr_path="/shared/temp/test_hdf5/h5_attrs.json"
process_dir = "/shared/temp/test_hdf5"
h5_path="/shared/temp/test_hdf5/testing.h5"
wtk_root="/shared/temp/test_hdf5/wtk_data"
meta_path="/shared/temp/test_hdf5/glacier_h5_meta.csv"
lat_lon_path = "/shared/temp/test_hdf5/wrf_output_glacier.nc"
#t_extent = ('2018-01-01_00_00_00', '2018-01-03_00_00_00')

#WTKtoH5.run(h5_path, meta_path, wtk_root, var_attr_path=var_attr_path, process_dir = process_dir, year=2018, clobber = True, spinup_time=12, lat_lon_path = lat_lon_path, max_workers=max_workers)
#WTKtoH5.run(h5_path, meta_path, wtk_root, var_attr_path=var_attr_path, process_dir = process_dir, year=2018, clobber = True, spinup_time=12)
#NCtoH5.run(h5_path, meta_path, wtk_root, var_attr_path=var_attr_path, process_dir = process_dir, clobber = True, spinup_time=12, max_workers = 1)

'''

max_workers=16
var_attr_path="/shared/aws_wrf_tools/key_inputs/h5_attrs.json"
process_dir = "/shared/temp"
h5_path="/shared/processed/%s/%s_%s.h5" % (domain, domain, type,)
wtk_root="/shared/wrf_runs/%s/wtk/%s/" % (domain, type,)
meta_path="/shared/wrf_runs/%s/%s_h5_meta.csv" % (domain, domain,)
lat_lon_path = "/shared/wrf_runs/%s/wrf_output_%s.nc" % (domain, domain,)
#t_extent = ('2018-01-01_00_00_00', '2018-01-03_00_00_00')

NCtoH5.run(h5_path, meta_path, wtk_root, var_attr_path=var_attr_path, process_dir = process_dir, clobber = True, spinup_time=0, lat_lon_path = lat_lon_path, max_workers = max_workers)
