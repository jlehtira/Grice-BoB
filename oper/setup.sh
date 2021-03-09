#!/bin/bash

export RUNROOT=~/code/Grice-BoB/runs
export OPERROOT=~/code/Grice-BoB/oper

export SCRIPTDIR=$OPERROOT/scripts
export BINDIR=$OPERROOT/bin
export TEMPLATEDIR=$OPERROOT/template

if [ "$#" -eq "1" ]
then
    export YYYY=${1:0:4}
    export MM=${1:4:2}
    export DD=${1:6:2}
elif [ "$#" -eq "0" ]
then
    nowdate=$(date +%Y%m%d)
    export YYYY=${nowdate:0:4}
    export MM=${nowdate:4:2}
    export DD=${nowdate:6:2}
fi

echo Setting up run for $YYYY $MM $DD


RUNDIR=$RUNROOT/run-$YYYY$MM$DD
mkdir -p $RUNDIR

################################################# Run files

cp $TEMPLATEDIR/Landmask.SPHysics.xml $TEMPLATEDIR/gCaseBoB500mTest1_linux64_GPU.sh \
    $RUNDIR

# This I couldn't make work for now.
# sed "s/OPERROOTHERE/$OPERROOT/" $TEMPLATEDIR/gCaseBoB500mTest1_linux64_GPU.sh \
#     > $RUNDIR/gCaseBoB500mTest1_linux64_GPU.sh

chmod a+x $RUNDIR/gCaseBoB500mTest1_linux64_GPU.sh

################################################# Winds

WINDFILE=ecmwf_0-54_$YYYY$MM$DD.grb

echo Wind file: $WINDFILE
echo Wind file with dir: $OPERROOT/winds/$WINDFILE


if [ ! -f $RUNDIR/ecmwf_0-54_$YYYY$MM$DD.csv ]
then
    cd $RUNDIR
    if [ -f $OPERROOT/winds/$WINDFILE ]
    then
        cp $OPERROOT/winds/$WINDFILE $RUNDIR
    else
        python3 $SCRIPTDIR/getwinds_ec.py $YYYY$MM $DD
    fi

    $SCRIPTDIR/makeWindForcing.sh
else
    echo Wind forcing file found
fi

################################################# Initial state

ICECHARTZIP=$OPERROOT/icecharts/$YYYY/FMI_Sigrid-3_$YYYY$MM$DD.zip

unzip $ICECHARTZIP FMI_Sigrid-3_$YYYY$MM$DD/FMI_baltic_$YYYY$MM${DD}_pl_a.shp \
    FMI_Sigrid-3_$YYYY$MM$DD/FMI_baltic_$YYYY$MM${DD}_pl_a.dbf \
    -d $RUNDIR

cd $RUNDIR
python $SCRIPTDIR/icechart_BoB2xml.py \
    FMI_Sigrid-3_$YYYY$MM$DD/FMI_baltic_$YYYY$MM${DD}_pl_a.shp


################################################# Settings

icechart=FMI_Sigrid-3_$YYYY$MM$DD/FMI_baltic_$YYYY$MM${DD}_pl_a.SPHysics.xml
icetypes=FMI_Sigrid-3_$YYYY$MM$DD/FMI_baltic_$YYYY$MM${DD}_pl_a.icetypes.xml
landmask=Landmask.SPHysics.xml

srcfile=Grice-BoB_Def.xml.nomask
tgtfile=Grice-BoB_Def.xml

tempfile1=temp-$(date +%Y%m%d-%H%M).xml
tempfile2=temp2-$(date +%Y%m%d-%H%M).xml

cd $RUNDIR
if [ -f $tgtfile ]
then
    mv $tgtfile .${tgtfile}.bak$(date +%Y%m%d-%H%M)
fi

nice sed "/<\!--LANDMASK-->/ r $landmask" $TEMPLATEDIR/$srcfile > $tempfile1
nice sed "/<\!--ICECHART-->/ r $icechart" $tempfile1 > $tempfile2
nice sed "/<\!--ICETYPES-->/ r $icetypes" $tempfile2 > $tempfile1
nice sed "s/WINDFILENAME/ecmwf_0-54_$YYYY$MM$DD.csv/" $tempfile1 > $tempfile2
nice sed "s/ACCFLUIDS/$(cat accfluids.txt)/" $tempfile2 > $tgtfile

rm -rf $tempfile $tempfile2


