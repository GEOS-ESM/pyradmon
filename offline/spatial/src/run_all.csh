#!/bin/csh

# /discover/nobackup/aconaty/new_pyradmon_spatial/clean_plots
# Will McCarty's spatial pyradmon plot scripts
# input: reads the *diag*nc4 files from FP obs
# output: creates coverage plots for all radiance obs

# THESE NUMBERS ARE OLD UPDATE THEM 20210311

# HYPERSPECTRAL DISK SPACE, IMAGE COUNT, and TIMING INFO:
# based on interactive work ondiscover nodes
#
# CrIS about 1.75 hours to run
# 5447.968u 621.333s 1:44:19.60 96.9%	0+0k 2160672+0io 21pf+0w
# 3.7G	CrIS_NOAA-20   13792 images
# 3.7G	CrIS_SNPP      13792 images

# AIRS about 31 minutes ro run
# 1611.285u 207.445s 30:52.97 98.1%        0+0k 599584+0io 0pf+0w
# 2.3G AIRS_AQUA  8992 images

# IASI about 2.5 hours to run
# 7680.211u 931.965s 2:26:54.79 97.7%	0+0k 2417472+0io 24pf+0w
# 5.1G IASI_METOP-A   19712 images
# 5.1G IASI_METOP-B   19712 images

setenv expver $1
setenv yyyymmdd $2
setenv hh $3

set argv = ()
set configFile = /home/dao_ops/$expver/run/FVDAS_Run_Config
if (-e $configFile) source $configFile

set echo on


time do_amsr2.csh $expver $yyyymmdd $hh 
time do_amsua.csh $expver $yyyymmdd $hh
time do_amsua_n15.csh $expver $yyyymmdd $hh
time do_atms.csh $expver $yyyymmdd $hh
time do_avhrr.csh $expver $yyyymmdd $hh
time do_gmi.csh $expver $yyyymmdd $hh
time do_hirs.csh $expver $yyyymmdd $hh
time do_mhs.csh $expver $yyyymmdd $hh
time do_seviri.csh $expver $yyyymmdd $hh
time do_ssmis.csh $expver $yyyymmdd $hh
time do_cris.csh $expver $yyyymmdd $hh
time do_airs.csh $expver $yyyymmdd $hh
time do_iasi.csh $expver $yyyymmdd $hh
