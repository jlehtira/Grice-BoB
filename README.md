# Grice-BoB

This is the Grice-BoB code repository. Grice-BoB is an experimental project
aimed at introducing an operational sea ice simulation framework using a
granular modelling paradigm. The project is built on top of the DualSPHysics
simulation engine available at
 - https://dual.sphysics.org/

DualSPHysics is kindly provided by an international team of programmers
working mostly in Spain and UK. It is a flexible solver for Smoothed Particle
Hydrodynamics (SPH) simulations. For relevant documentation, you should refer
to the DualSPHysics website, its own software repository or tar package, and
the excellent video tutorials on YouTube under the DualSPHysics site profile.

For ease of use, the DualSPHysics source code, as modified for Grice-BoB
simulations, is available under this directory.

Currently, the Grice-BoB toolbox can only be run on Linux.


Any questions or feedback should be sent to

jonni.lehtiranta@fmi.fi



## INSTALLING

### Get precompiled libraries

Some precompiled libraries are required. These are not included in the Grice-BoB
repository but should be copied from DualSPHysics repository. They are available
also at the GitHub web page at the following address:

- https://github.com/DualSPHysics/DualSPHysics/tree/master/src_mphase/DSPH_v5.0_NNewtonian/lib/linux_gcc

These libraries should be placed in the following directory:

- DualSPHysics/src_gbob/lib/linux_gcc/


### Install prerequisites

Install CUDA Toolkit, available from NVIDIA


### Compile

> cd DualSPHysics/src_gbob/source
> make -f Makefile.gbob
> cd -
> cp DualSPHysics/bin/linux/DualSPHysics5.0_gbob_linux64 oper/bin


### Get helper binaries

The GenCase_linux64, IsoSurface_linux64 and PartVTK_linux64 binaries are needed along
with libraries libChronoEngine_parallel.so, libChronoEngine.so and libdsphchrono.so .
These can be downloaded from

- https://github.com/DualSPHysics/DualSPHysics/tree/master/bin/linux

and placed in oper/bin .


### Install script prerequisites

It is recommended to set up a python environment using conda. The packages required
are (list possibly incomplete):

* numpy
* matplotlib
* basemap and basemap-data-hires
* libgdal
* proj
* pyshp
* ecmwf-api-client



## RUNNING

### Forcing files

Grice-BoB absolutely needs ice charts to operate. These should be copied or linked, as
zip files, under the oper directory, as such:

    oper/icecharts/2021/FMI_Sigrid-3_20210121.zip
    oper/icecharts/2021/FMI_Sigrid-3_20210122.zip
    ...

Wind forcing can be downloaded similarly to `oper/winds`, but it's easier to let the
setup script do the downloading.


### Running the model

When properly set up, you should be able to generate a run directory using

> oper/setup.sh YYYYMMDD

Then you can 

> cd runs/run-YYYYMMDD
> gCaseBoB500mTest1_linux64_GPU.sh





