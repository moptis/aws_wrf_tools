
#!/bin/bash

domain='glacier'

for type in target_only distant
do

for d in {001..179}
do
    echo $d
    cd /shared/wrf_runs/${domain}/${type}/$d
    ln -sf /shared/wrf_runs/${domain}/all_farms/$d/wrfb* .
    ln -sf /shared/wrf_runs/${domain}/all_farms/$d/wrfi* .
    cp /shared/wrf_runs/${domain}/all_farms/$d/namelist.input .
done
done




