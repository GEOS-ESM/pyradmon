#!/bin/csh

# Activate venv and set pyradmon directory environment variable
source /home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/bin/g5_modules
source pyradmon-modules

setenv pyradmon $PWD

echo 'g5_modules loaded'

echo 'pyradmon-modules loaded'
ml

echo '$pyradmon set to:' $pyradmon
