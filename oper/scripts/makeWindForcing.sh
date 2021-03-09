#!/bin/bash

echo Making wind forcing for $YYYY $MM $DD

LEN=54

FNAME=ecmwf_0-${LEN}_$YYYY$MM$DD.grb

grib_ls -l 64,21,1 -p "" -w paramId=165 $FNAME |head -n $((LEN+3)) |tail -n $((LEN+1)) > temp-10u.txt
grib_ls -l 64,21,1 -p "" -w paramId=166 $FNAME |head -n $((LEN+3)) |tail -n $((LEN+1)) > temp-10v.txt
grib_ls -l 64,21,1 -p "" -w paramId=167 $FNAME |head -n $((LEN+3)) |tail -n $((LEN+1)) > temp-2T.txt

rm -f temp-zeros.txt temp-tsteps.txt

for (( i=0; i<=$LEN; i++ )); do echo 0 >> temp-zeros.txt; done
for (( i=0; i<=$LEN; i++ )); do echo $((i * 3600)) >> temp-tsteps.txt; done

paste -d ";" temp-tsteps.txt temp-10u.txt temp-zeros.txt temp-10v.txt temp-zeros.txt temp-zeros.txt temp-zeros.txt >ecmwf_0-${LEN}_$YYYY$MM$DD.csv
