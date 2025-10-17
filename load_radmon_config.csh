#!/bin/csh

# Activate venv and set pyradmon directory environment variable
source /home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/bin/g5_modules
setenv pyradmon $PWD

echo '$pyradmon set to:' $pyradmon



# python3 -m venv .venv
# source .venv/bin/activate.csh
# setenv pyradmon_spatial_src $pyradmon/offline/spatial/src
# setenv pyradmon_timeseries_src $pyradmon/offline/timeseries/src
# setenv run_dir $PWD/run_dir
# setenv log_dir $PWD/log_dir