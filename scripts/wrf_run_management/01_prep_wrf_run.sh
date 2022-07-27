
#!/bin/bash

domain='fenton'

for d in {001..179}
do
for t in all_farms distant target_only
do
    echo $d
    mkdir -p ./$t/$d

    ln -sf /shared/aws_wrf_tools/turbines/$domain/wind-t* ./$t/$d

    ln -sf $WRF_ROOT/*DATA ./$t/$d
    ln -sf $WRF_ROOT/*DBL ./$t/$d
    ln -sf $WRF_ROOT/*rain ./$t/$d
    ln -sf $WRF_ROOT/*TBL ./$t/$d
    ln -sf $WRF_ROOT/*formatted ./$t/$d
    ln -sf $WRF_ROOT/real.exe ./$t/$d
    ln -sf $WRF_ROOT/wrf.exe ./$t/$d

done
ln -sf /shared/aws_wrf_tools/turbines/$domain/windturbines_${domain}_only.txt ./target_only/$d/windturbines.txt
ln -sf /shared/aws_wrf_tools/turbines/$domain/windturbines_${domain}_all_farms.txt ./all_farms/$d/windturbines.txt
ln -sf /shared/aws_wrf_tools/turbines/$domain/windturbines_${domain}_distant.txt ./distant/$d/windturbines.txt
done





