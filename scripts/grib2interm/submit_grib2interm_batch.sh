#!/bin/bash

# MAKE SURE THE NUMBER OF SUBMISSIONS MATCHES ntasks ABOVE

for y in {2018..2021}
do
  for m in {01..11}
  do
    m_next=$((m+1))
    python grib_to_interm_old.py $y-$m-01 $y-${m_next}-01
  done
  y_next=$((y+1))
  python grib_to_interm_old.py $y-12-01 ${y_next}-01-01
done
