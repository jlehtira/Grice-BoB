import os
import sys
from ecmwfapi import ECMWFService
from calendar import monthrange


print (len(sys.argv[1]))

if (len(sys.argv[1]) == 8):
    arg = sys.argv[1]
    yyyymm = arg[0:6]
    yyyy_mm = yyyymm[0:4] +"-"+ yyyymm[4:]
    dd = arg[6:8]
    print (yyyymm, yyyy_mm, dd)
    (firstday, lastday) = monthrange(int(yyyymm[0:4]), int(yyyymm[4:].lstrip("0")))
    datestr = yyyy_mm + "-" + dd
    stepstr = "0/to/54/by/1"
    filestr = "0-54_" + yyyymm+dd
elif (len(sys.argv[1]) == 6 and len(sys.argv[2]) == 2):
    yyyymm = sys.argv[1]
    yyyy_mm = yyyymm[0:4] +"-"+ yyyymm[4:]
    dd = sys.argv[2]
    print (yyyymm, yyyy_mm, dd)
    (firstday, lastday) = monthrange(int(yyyymm[0:4]), int(yyyymm[4:].lstrip("0")))
    datestr = yyyy_mm + "-" + dd
    stepstr = "0/to/54/by/1"
    filestr = "0-54_" + yyyymm+dd
elif (len(sys.argv[1]) == 6):
    yyyymm = sys.argv[1]
    yyyy_mm = yyyymm[0:4] +"-"+ yyyymm[4:]
    print (yyyymm, yyyy_mm)
    (firstday, lastday) = monthrange(int(yyyymm[0:4]), int(yyyymm[4:].lstrip("0")))
    datestr = yyyy_mm + "-01/to/" + yyyy_mm + "-" + str(lastday).rjust(2,'0')
    stepstr = "0/to/23/by/1"
    filestr = "0-23_" + yyyymm
elif (len(sys.argv[1]) == 7):
    yyyy_mm = sys.argv[1]
    yyyymm = yyyy_mm[0:4] + yyyy_mm[5:]
    print (yyyymm, yyyy_mm)
    (firstday, lastday) = monthrange(int(yyyymm[0:4]), int(yyyymm[4:].lstrip("0")))
    datestr = yyyy_mm + "-01/to/" + yyyy_mm + "-" + str(lastday).rjust(2,'0')
    stepstr = "0/to/23/by/1"
    filestr = "0-23_" + yyyymm
else:
    print ("usage: "+sys.argv[0]+" YYYYMM")
    print ("   or: "+sys.argv[0]+" YYYYMMDD")
    sys.exit()


print ("Downloading EC forcing for " + datestr)


server = ECMWFService("mars")

server.execute( {
    "class": "od",
    "date": datestr,
    "expver": "1",
    "levtype": "sfc",
    "param": "165.128/166.128/167.128",
    "step": stepstr,
    "stream": "oper",
    "time": "00",
    "type": "fc",
    "grid": "0.2/0.1",
    "area": "66.0/17.5/62.5/26.0" },
    "ecmwf_" + filestr + ".grb")


print ("Downloaded forcing data!")

