
import logging
import os
import yaml
import argparse
from datetime import datetime, timedelta
import subprocess

# 
"""
def print_var(var):
    print(f' ----- var : {var}')
"""
#./pyradmon_driver.csh m21c.current.rc


# Global Constants
# source radmon_process.config
#############################
ESMADIR = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/' # from ramon_process.conf

# pyradmon_bin2txt_driver.csh
#############################
echorc=os.path.join(ESMADIR,'install/bin/echorc.x') # could keep echorc around for now
### satlist
gsidiagsrc=os.path.join(ESMADIR,'install/etc/gsidiags.rc')
gsidiagsrc_input=`$echorc -rc $exprc gsidiagsrc`
if ($status == 0) set gsidiagsrc=$gsidiagsrc_input
set sats=`$echorc -rc $gsidiagsrc satlist`
###

# Environment Modules
g5_modules = os.path.join(ESMADIR,'install/bin/g5_modules')
print(f'g5_modules: {g5_modules}  ----------------')
#subprocess.run(["source", "./pyradmon_bin2txt_driver.csh", exprc])

# echorc
#########
def echorc(rc_path):
    with open(rc_path, 'r') as file:
        config = readlines.safe_load(file)
        print(f'config: {config}')
        
$echorc -rc $exprc expid

echorc('/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/etc/gsidiags.rc')

# m21c.current.rc.tmpl
#############################
class PyRadmonBase:
    def __init__(self, config_yaml_path):
        """
        Initialize the PyRadmonBase class using a YAML configuration file.
        :param config_yaml_path: Path to the YAML configuration file. See PyRadmonBase_template.yaml
        
        """
        with open(config_yaml_path, 'r') as file:
            config = yaml.safe_load(file)
            print(f'config: {config}')
        
        """
        pyradmon: str | pyradmon top lvl dir | /home/dao_ops/pyradmon/
        expid: str \ path| experiment id | e5303_m21c_jan18
        expbase: str \ path | working dir (local experiment dir)? | /discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/time_series/m21c_radmon/
        arcbase: str \ path | /home/dao_ops/m21c/archive/
        data_dirbase: str \ path | /home/dao_ops/m21c/archive/e5303_m21c_jan18/obs
        startdate: 20190530 000000
        enddate:  20190531 180000

        scratch_dir: /discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/time_series/m21c_radmon/scratch
        output_dir: /discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/time_series/m21c_radmon/radmon

        #optional:
        mstorage: /home/dao_ops/e5303_m21c_jan18/run/mstorage.arc
        #instruments: amsua_n15
        bin2txt_exec: /home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/bin/gsidiag_bin2txt.x
        bin2txt_nl: /discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/time_series/m21c_radmon/radmon_diag_bin2txt.nl
        #rename_date_dir: current
        scp_userhost: aelakkra@polar
        scp_path: /www/html/intranet/personnel/aelakkra/m21c/radmon_data/
        """
        # echorc equivalent
        #########
        self.pyradmon = config['pyradmon'] #/home/dao_ops/pyradmon/
        self.expid = config['expid'] #e5303_m21c_jan18
        self.expbase = config['expbase'] #/discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/time_series/m21c_radmon/
        self.arcbase = config['arcbase'] #/home/dao_ops/m21c/archive/
        self.data_dirbase = config['data_dirbase'] #/home/dao_ops/m21c/archive/e5303_m21c_jan18/obs
        self.startdate = config['startdate'] # 20190530 000000
        self.enddate = config['enddate'] # 20190531 180000
        self.scratch_dir = config['scratch_dir'] #/discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/time_series/m21c_radmon/scratch
        self.output_dir = config['output_dir'] #/discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/time_series/m21c_radmon/radmon
     
        #optional
        #########
        self.mstorage = config['mstorage'] #
        #self.instruments = config['instruments'] #
        self.bin2txt_exec = config['bin2txt_exec'] #
        self.bin2txt_nl = config['bin2txt_nl'] #
        #self.rename_date_dir = config['rename_date_dir'] #
        self.scp_userhost = config['scp_userhost'] #
        self.scp_path = config['scp_path'] #



#########
gsidiagsrc
gsidiagsrc_input
set gsidiagsrc=$ESMADIR/install/etc/gsidiags.rc
set gsidiagsrc_input=`$echorc -rc $exprc gsidiagsrc`
bin2txt
bin2txtnl_input

ndstartdate = start_date[:2]
ndenddate = end_date[:2]
ndstartdate = start_date[:-4].replace(" ", "")
ndenddate = end_date[:-4].replace(" ", "")
#########

        #testing - delete
        print(f' ----- pyradmon : {self.pyradmon}')
        print(f' ----- expid : {self.expid}')
        print(f' ----- expbase : {self.expbase}')
        print(f' ----- arcbase : {self.arcbase}')
        print(f' ----- data_dirbase : {self.data_dirbase}')
        print(f' ----- startdate : {self.startdate}')
        print(f' ----- enddate : {self.enddate}')
        print(f' ----- scratch_dir : {self.scratch_dir}')
        print(f' ----- output_dir : {self.output_dir}')
        
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

        # Print all environment variables
        for key, value in os.environ.items():
            print(f'{key}: {value}')    

        # Constants?
        # x = " " 
        # y = " " ...


        # Generate log file name with date
        log_filename = f"log_pyradmon_driver_offline_{datetime.now().strftime('%Y-%m-%d')}.log"
        
        # Setup logging
        logging.basicConfig(filename=log_filename, level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Log initialization details
        log_message = f"Initialized PYRADMON-OFFLINE with configuration from {config_yaml_path}"
        logging.info(log_message)
        print(log_message)
    # m21c_radmon.csh equivalent
    ################# 
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

    # pyradmon_bin2txt_driver.csh equivalent
    #############################
    def exec_bin2txt_driver(self):
        """        
        ##!/bin/csh -X

        set exprc=$argv[1]

        ./pyradmon_bin2txt_driver.csh $exprc
        ./pyradmon_img_driver.csh $exprc
        """
        exprc = ''
        """
        execute pyradmon_bin2txt_driver.csh
        """
        try:
            subprocess.run(["source", "./pyradmon_bin2txt_driver.csh", exprc])
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)

    # pyradmon_img_driver.csh equivalent
    def exec_img_driver(self):
        """
        execute pyradmon_img_driver.csh
        """
        try:
            subprocess.run(["source", "./pyradmon_img_driver.csh", exprc])
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)


# python script.py config.yaml
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="configuration YAML file.")
    parser.add_argument("config", help="Path to the YAML configuration file.")
    args = parser.parse_args()
    
    uploader = PyRadmonBase(args.config)
    #uploader()
    

"""

if __name__ == "__main__":
    uploader = S3Uploader('config.yaml')  # Specify the path to your YAML config file
    uploader.upload_directory()
"""



