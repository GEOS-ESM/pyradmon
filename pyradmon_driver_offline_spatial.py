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
#PYRADMON_HOME_DIR = os.getenv['PYRADMON_HOME_DIR'] # PYRADMON_HOME_DIR = os.getcwd
#ACTIVATE_VENV = os.getenv("ACTIVATE_VENV") # the path to your virtual environment's activate script
############################################################################################################
# ATTENTION PYRADMON USER:
# These two variables: PYRADMON_HOME_DIR & ACTIVATE_VENV should be the only items which need user inputs/validation
# .... aside from the date ranges ....
# BEWARE of your shell and make changes if necessary
# 
#
# NOTE: This is NOT the INPUT YAML File. This will only needed to be edited once.
#       It will be called by other scripts when handling/manipulating directories.
#
############################################################################################################
# User should have already edited them to the appropriate paths.
# Both can be found in the .env file in the pyradmon dir 
# These should be the only two changes the user needs to make .... WHAT ABOUT THE DATES??
# Everthing else should be created using relative paths wrt PYRADMON_HOME_DIR
PYRADMON_HOME_DIR = '/discover/nobackup/sicohen/RADMON/develop/pyradmon' # 
ACTIVATE_VENV = '/discover/nobackup/sicohen/RADMON/develop/pyradmon/.venvs/radmon_sles15_venv/bin/activate.csh'
#os.path.join(PYRADMON_HOME_DIR,'.venvs/radmon_sles15_venv/bin/activate.csh') # the path to your virtual environment's activate script
ESMADIR = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/' # from radmon_process.conf
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



# Set environment variable
##########################
os.environ['PYRADMON_HOME_DIR'] = PYRADMON_HOME_DIR
os.environ['ACTIVATE_VENV'] = ACTIVATE_VENV
os.environ['ESMADIR'] = ESMADIR
os.environ['PYRADMON_SPATIAL_DIR'] = PYRADMON_SPATIAL_DIR
os.environ['PYRADMON_SPATIAL_SRC_DIR'] = PYRADMON_SPATIAL_SRC_DIR
os.environ['PYRADMON_SPATIAL_WRK_DIR'] = PYRADMON_SPATIAL_WRK_DIR
os.environ['PYRADMON_SPATIAL_OUTPUT_DIR'] = PYRADMON_SPATIAL_OUTPUT_DIR


#####################
# run_test_driver.csh   ~  SPATIAL DRIVER
#####################
print(f'NOW RUNNING: pyradmon_driver_offline_spatial.py  ------------------------------------------------------------------')
#command = 'source $ACTIVATE_VENV && cd $PYRADMON_SPATIAL_SRC_DIR && source test_driver.csh'
#command = 'source ${ACTIVATE_VENV} && cd $PYRADMON_SPATIAL_SRC_DIR && source test_driver.csh'

#command = 'source /discover/nobackup/sicohen/RADMON/develop/pyradmon/.venvs/radmon_sles15_venv/bin/activate.csh && cd $PYRADMON_SPATIAL_SRC_DIR && source test_driver.csh'
#process = subprocess.run(command, shell=True, executable='/bin/csh')
command1 = 'source /discover/nobackup/sicohen/RADMON/develop/pyradmon/.venvs/radmon_sles15_venv/bin/activate.csh'
command2 = 'cd $PYRADMON_SPATIAL_SRC_DIR'
command3 = 'source test_driver.csh'

try:
    #subprocess.run(["source", "/discover/nobackup/sicohen/RADMON/develop/pyradmon/.venvs/radmon_sles15_venv/bin/activate.csh"]) # 'test_config_yaml_path.yaml'])
    subprocess.run([command1])
    subprocess.run([command2])
    subprocess.run([command3])
except Exception as e:
    error_message = f"Error: {e}"
    print(error_message)
    logging.error(error_message)
print(f'exec_img_driver finished  ------------------------------------------------------------------')
