#!/bin/bash

# MAKE SURE THE NUMBER OF SUBMISSIONS MATCHES ntasks ABOVE


#python grib_to_interm_old.py 2018-06-01 2018-06-02
#for y in {2020..2021}
#for y in 2018
#do
#  for m in {01..07}
#  do
#    m_next=$((m+1))
#    echo ${m_next}
    #python grib_to_interm_old.py $y-$m-01 $y-${m_next}-01
#  done
#  y_next=$((y+1))
  #python grib_to_interm_old.py $y-12-01 ${y_next}-01-01
#done

#for y in {2018..2021}
#do
#  for m in {1..8}
#  do
#    m_next=$((m+1))
    #python grib_to_interm_old.py $y-0$m-01 $y-0${m_next}-01
    #echo $y-0$m-01
    #echo ${m_next}
#  done
  #for 
#done
#y=2019
#y_next=2020
#python grib_to_interm_old.py $y-01-01 $y-02-01

y=2021
y_next=2022
python grib_to_interm_old.py $y-01-01 $y-02-01
python grib_to_interm_old.py $y-02-01 $y-03-01
python grib_to_interm_old.py $y-03-01 $y-04-01
python grib_to_interm_old.py $y-04-01 $y-05-01
python grib_to_interm_old.py $y-05-01 $y-06-01
python grib_to_interm_old.py $y-06-01 $y-07-01
python grib_to_interm_old.py $y-07-01 $y-08-01
python grib_to_interm_old.py $y-08-01 $y-09-01
python grib_to_interm_old.py $y-09-01 $y-10-01
python grib_to_interm_old.py $y-10-01 $y-11-01
python grib_to_interm_old.py $y-11-01 $y-12-01
python grib_to_interm_old.py $y-12-01 ${y_next}-01-01
#  python grib_to_interm_old.py $y-10-01 $y-11-01
#  python grib_to_interm_old.py $y-11-01 $y-12-01
#  ynext=$((y+1))
#  python grib_to_interm_old.py $y-12-01 ${ynext}-01-01
#done
