#!/bin/zsh

# Activate venv and set pyradmon directory environment variable
source /home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/bin/g5_modules
export pyradmon="$PWD"

echo '$pyradmon set to:' "$pyradmon"