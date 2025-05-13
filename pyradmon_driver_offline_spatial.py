import logging
import os
import yaml
import argparse
from datetime import datetime, timedelta
import subprocess



############################################################################################################
# User should have already edited them to the appropriate paths.
# Both can be found in the .env file in the pyradmon dir 
# These should be the only two changes the user needs to make .... WHAT ABOUT THE DATES??
# Everthing else should be created using relative paths wrt PYRADMON_HOME_DIR
PYRADMON_HOME_DIR = os.getenv['PYRADMON_HOME_DIR'] # PYRADMON_HOME_DIR = os.getcwd
ACTIVATE_VENV = os.getenv("ACTIVATE_VENV") # the path to your virtual environment's activate script
############################################################################################################


# Environment Configuration
###########################
PYRADMON_SPATIAL_DIR = os.path.join(PYRADMON_HOME_DIR,'offline/spatial/')
PYRADMON_SPATIAL_SRC_DIR = PYRADMON_SPATIAL_CLEAN_PLOTS_DIR = os.path.join(PYRADMON_SPATIAL_DIR,'clean_plots/')
PYRADMON_SPATIAL_WRK_DIR = os.path.join(PYRADMON_SPATIAL_DIR,'fvwork.RADMON/')
PYRADMON_SPATIAL_OUTPUT_DIR = os.path.join(PYRADMON_SPATIAL_WRK_DIR,'clean_plots/%Y%m%d/')

print(
    f''' ----------------PyRadmonSpatial Configuration (.env file) ------------------------------
    PYRADMON_HOME_DIR: {PYRADMON_HOME_DIR}
    ACTIVATE_VENV: {ACTIVATE_VENV}
    PYRADMON_SPATIAL_DIR: {PYRADMON_SPATIAL_DIR}
    PYRADMON_SPATIAL_SRC_DIR: {PYRADMON_SPATIAL_SRC_DIR} 
            --PYRADMON_SPATIAL_CLEAN_PLOTS_DIR--: ^ 
    PYRADMON_SPATIAL_WRK_DIR: {PYRADMON_SPATIAL_WRK_DIR}
    PYRADMON_SPATIAL_OUTPUT_DIR: {PYRADMON_SPATIAL_OUTPUT_DIR}
    ---------------------------------------------------------------------------------------------
    Help: 
    PYRADMON_SPATIAL_SRC_DIR and PYRADMON_SPATIAL_CLEAN_PLOTS_DIR are the same thing. Only replicated to help follow the previous version of the code.'
    -- These are what is usually called the 'src' directory within a repo. 
    -- This ./clean_plots/ directory will be COPIED into a temporary working directory ./fvwork.RADMON/clean_plots/
    -- The output will be in the directories named for the day (YYYYMMDD) within ./fvwork.RADMON/clean_plots/%Y%m%d/
    -
    ''')

#####################
# run_test_driver.csh   ~  SPATIAL DRIVER
#####################
print(f'NOW RUNNING: pyradmon_driver_offline_spatial.py  ------------------------------------------------------------------')
command = 'source $ACTIVATE_VENV && cd $PYRADMON_SPATIAL_SRC_DIR && source test_driver.csh'
process = subprocess.run(command, shell=True, executable='/bin/bash')

