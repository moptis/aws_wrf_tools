#!/bin/bash

# MAKE SURE THE NUMBER OF SUBMISSIONS MATCHES ntasks ABOVE


#python grib_to_interm_old.py 2018-06-01 2018-06-02
for y in {2020..2021}
#for y in 2018
do
  for m in {01..07}
  do
    m_next=$((m+1))
    echo ${m_next}
    #python grib_to_interm_old.py $y-$m-01 $y-${m_next}-01
  done
  y_next=$((y+1))
  #python grib_to_interm_old.py $y-12-01 ${y_next}-01-01
done

for y in {2018..2021}
do
  python grib_to_interm_old.py $y-08-01 $y-09-01
  python grib_to_interm_old.py $y-09-01 $y-10-01
  python grib_to_interm_old.py $y-10-01 $y-11-01
  python grib_to_interm_old.py $y-11-01 $y-12-01
  ynext=$((y+1))
  python grib_to_interm_old.py $y-12-01 ${ynext}-01-01
done
