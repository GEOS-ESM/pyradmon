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
pyradmon = PYRADMON_HOME_DIR
PYRADMON_TIMESERIES_DIR = os.path.join(PYRADMON_HOME_DIR,'offline/timeseries/')
PYRADMON_TIMESERIES_SRC_DIR = os.path.join(PYRADMON_TIMESERIES_DIR,'src/')
#PYRADMON_TIMESERIES_WRK_DIR = PYRADMON_TIMESERIES_EXPBASE_DIR = os.path.join(PYRADMON_TIMESERIES_SRC_DIR, expbase)
#PYRADMON_TIMESERIES_OUTPUT_DIR = os.path.join(PYRADMON_TIMESERIES_WRK_DIR,'clean_plots/%Y%m%d/')
#scratch_dir


print(
    f''' ----------------PyRadmonTimeseries Configuration (.env file) ------------------------------
    PYRADMON_HOME_DIR: {PYRADMON_HOME_DIR}
    ACTIVATE_VENV: {ACTIVATE_VENV}
    PYRADMON_TIMESERIES_DIR: {PYRADMON_TIMESERIES_DIR}
    PYRADMON_TIMESERIES_SRC_DIR: {PYRADMON_TIMESERIES_SRC_DIR} 
    PYRADMON_TIMESERIES_WRK_DIR: {PYRADMON_TIMESERIES_WRK_DIR}
    PYRADMON_TIMESERIES_OUTPUT_DIR: {PYRADMON_TIMESERIES_OUTPUT_DIR}
    ---------------------------------------------------------------------------------------------
   
    --
    -- 
    -- The output will be in the directories named for the day (YYYYMMDD) within ./fvwork.RADMON/clean_plots/%Y%m%d/
    -
    ''')

#####################
# run_test_driver.csh   ~  TIMESERIES DRIVER
#####################
print(f'NOW RUNNING: pyradmon_driver_offline_timeseries.py  ------------------------------------------------------------------')
command = 'source $ACTIVATE_VENV && cd $PYRADMON_TIMESERIES_SRC_DIR && source test_driver.csh'
process = subprocess.run(command, shell=True, executable='/bin/bash')


# Environment Configuration
###########################
PYRADMON_TIMESERIES_DIR = os.path.join(PYRADMON_HOME_DIR,'offline/timeseries/')
PYRADMON_TIMESERIES_SRC_DIR = os.path.join(PYRADMON_TIMESERIES_DIR,'src/')
PYRADMON_TIMESERIES_WRK_DIR = os.path.join(PYRADMON_TIMESERIES_DIR,'fvwork.RADMON/')
PYRADMON_TIMESERIES_OUTPUT_DIR = os.path.join(PYRADMON_TIMESERIES_WRK_DIR,'clean_plots/%Y%m%d/')
        
# Set Environment variables
###########################
# radmon_process.config equivalent
os.environ['ESMADIR'] = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/' #self.pyradmon
os.environ['expid'] = self.expid
os.environ['expbase'] = self.expbase
os.environ['arcbase'] = self.arcbase
os.environ['startdate'] = self.startdate
os.environ['enddate'] = self.enddate
os.environ['pyradmon'] = self.pyradmon
os.environ['exprc'] = self.exprc
os.environ['rcfile'] = self.rcfile


###############################



# Global Constants, Modules and Environment Setup

# source radmon_process.config equivalent
#########################################
ESMADIR = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/' # from radmon_process.conf


# Environment Modules
g5_modules = os.path.join(ESMADIR,'install/bin/g5_modules')
os.environ['ESMADIR'] = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/'
command = 'source $ESMADIR/install/bin/g5_modules'
process = subprocess.run(command, shell=True, executable='/bin/bash')
print(f'g5_modules loaded  ------------------------------------------------------------------')


# Set Environment variables
###########################

# radmon_process.config equivalent
os.environ['ESMADIR'] = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/' #self.pyradmon

# config_yaml (m21c.current.rc) equivalent
os.environ['expid'] = self.expid
os.environ['expbase'] = self.expbase
os.environ['arcbase'] = self.arcbase
os.environ['startdate'] = self.startdate
os.environ['enddate'] = self.enddate
os.environ['pyradmon'] = self.pyradmon
os.environ['exprc'] = self.exprc
os.environ['rcfile'] = self.rcfile

        # Generate log file name with date
        log_filename = f"log_pyradmon_driver_offline_{datetime.now().strftime('%Y-%m-%d')}.log"
        
        # Setup logging
        logging.basicConfig(filename=log_filename, level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Log initialization details
        log_message = f"Initialized PYRADMON-OFFLINE with configuration from {config_yaml_path}"
        logging.info(log_message)
        #print(log_message)
    
    # m21c_radmon.csh equivalent
    ############################
    def exec_m21c_radmon():
        print(f'Running NRT Radmon for MERRA21C')
        os.environ['FVROOT'] = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/'
        os.environ['M2BASE'] = '/home/dao_ops/m21c/archive/'

        # changing directory ------ !!! -------
        os.chdir('/discover/nobackup/sicohen/RADMON/offline/work/r21c/TBR/radmon/time_series/')

        """    
        # Is any of this needed?:     
        days_back=1 # number of days to plot in realtime MERRA-2 monitoring
        set enddate=2019053118
        set obsdir=$M2BASE/e5303_m21c_jan18/obs/
        set eyyyy=`echo $enddate |cut -b1-4`
        set emm=`echo $enddate   |cut -b5-6`
        set edd=`echo $enddate   |cut -b7-8`
        set ehh=`echo $enddate   |cut -b9-10`
        set enddate=$eyyyy$emm$edd\18
        set enddate_not_found=1
        """        
        print(f'exec_m21c_radmon finished  ------------------------------------------------------------------')

    # pyradmon_bin2txt_driver.csh equivalent
    ########################################
    def exec_bin2txt_driver(self):
        """        
        execute pyradmon_bin2txt_driver.csh
                
                set exprc=$argv[1]
                ./pyradmon_bin2txt_driver.csh $exprc
        """
        print(f'----------- self ---- : {self}')

        try:
            subprocess.run(["./pyradmon_bin2txt_driver.csh", self.exprc]) #'test_config_yaml_path.yaml']) #exprc])
            #subprocess.run(["./pyradmon_bin2txt_driver.csh", self.exprc]) #exprc])
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)


        print(f'exec_bin2txt_driver finished  ------------------------------------------------------------------')

    # pyradmon_img_driver.csh equivalent
    ####################################
    def exec_img_driver(self):
        """
        execute pyradmon_img_driver.csh
        """

        #os.environ['rcfile'] = self

        try:
            subprocess.run(["./pyradmon_img_driver.csh", self.exprc]) # 'test_config_yaml_path.yaml'])
            #subprocess.run(["./pyradmon_img_driver.csh", self.exprc]) 
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)
        print(f'exec_img_driver finished  ------------------------------------------------------------------')


# python script.py config.yaml
if __name__ == "__main__":

    print(os.path.basename(__file__))
    parser = argparse.ArgumentParser(description="configuration YAML file.")
    parser.add_argument("config", help="Path to the YAML configuration file.")
    args = parser.parse_args()
    print(args)
    
    A = PyRadmonBase(args.config)
    A.exec_bin2txt_driver()
    A.exec_img_driver()

    # pipe
    #process1 = subprocess.Popen(['source', './pyradmon_bin2txt_driver.csh','test_config_yaml_path.yaml'])# , stdout=subprocess.PIPE)
    #process2 = subprocess.Popen(['source', './pyradmon_img_driver.csh','test_config_yaml_path.yaml']) #, stdin=process1.stdout, stdout=subprocess.PIPE)

    

"""

if __name__ == "__main__":
    uploader = S3Uploader('config.yaml')  # Specify the path to your YAML config file
    uploader.upload_directory()
"""