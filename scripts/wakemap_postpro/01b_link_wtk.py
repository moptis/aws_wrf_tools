import os
import sys
import glob
import numpy as np

domain="national"
types = ['all_farms', 'no_farms']

for type in types:
    link_dir = '/scratch/moptis/national/processed/%s/all/' % (type,)

    if not os.path.exists(link_dir):
        os.makedirs(link_dir)
    os.chdir(link_dir)

    for n in np.arange(1,180):
        nstr = str(n).zfill(3)
        link_dir = '/scratch/moptis/national/processed/%s/%s/all/' % (type,nstr)

        if not os.path.exists(link_dir):
            os.makedirs(link_dir)
            os.chdir(link_dir)
        print(n)
        ns = str(n).zfill(3)
        target_dir = '/scratch/moptis/national/processed/%s/%s/' % (type, ns)

        # Get list of daily directories
        dir_list = glob.glob(os.path.join(target_dir, '2*'))
        dir_list = sorted(dir_list)

        for d in dir_list[1:-1]:
            os.system("ln -sf %s ." % os.path.join(d, '*.nc'))
