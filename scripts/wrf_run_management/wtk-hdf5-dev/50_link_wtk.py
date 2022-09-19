import os
import sys
import glob
import numpy as np

domain = sys.argv[1]
#type = sys.argv[2]

#types = ['all_farms', 'distant', 'target_only']
#types = ['target_only', 'distant']
types = ['all_farms']

for type in types:
    link_dir = '/shared/processed/%s/wtk/%s/all/' % (domain, type,)

    if not os.path.exists(link_dir):
        os.makedirs(link_dir)
    os.chdir(link_dir)

    for n in np.arange(1,180):
        print(n)
        ns = str(n).zfill(3)
        target_dir = '/shared/processed/%s/wtk/%s/%s/' % (domain, type, ns)
  
        # Get list of daily directories
        dir_list = glob.glob(os.path.join(target_dir, '2*'))
        dir_list = sorted(dir_list)

        for d in dir_list[1:-1]:
            os.system("ln -sf %s ." % os.path.join(d, '*.nc'))
  
    
