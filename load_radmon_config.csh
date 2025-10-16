#!/bin/csh

source .venv/bin/activate.csh
setenv pyradmon $PWD
setenv pyradmon_spatial_src $pyradmon/offline/spatial/src
setenv pyradmon_timeseries_src $pyradmon/offline/timeseries/src
# setenv run_dir $PWD/run_dir