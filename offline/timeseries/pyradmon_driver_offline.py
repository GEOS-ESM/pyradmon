import logging
import os
import yaml
import argparse
from datetime import datetime, timedelta
import subprocess

# Global Constants, Modules and Environment Setup

# source radmon_process.config equivalent
#############################
ESMADIR = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/' # from ramon_process.conf

# echorc equivalent
#############################
echorc=os.path.join(ESMADIR,'install/bin/echorc.x') # could keep echorc around for now
# python version echorc
def echorc(rc_file_path, rcstring):
    start_marker = rcstring + '::'
    end_marker = '::'
    section_lines = []
    inside_section = False
    with open(rc_file_path, 'r') as file:
        for line in file:
            if start_marker in line:
                inside_section = True
            elif end_marker in line:
                inside_section = False
            elif inside_section:
                section_lines.append(line.strip())
    #print(section_lines)
    return section_lines

sats = echorc(
        '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/etc/gsidiags.rc',
        rcstring='satlist'
        )


# Environment Modules
g5_modules = os.path.join(ESMADIR,'install/bin/g5_modules')
os.environ['ESMADIR'] = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/'
#print(f'g5_modules: {g5_modules}  ----------------')
#subprocess.Popen([g5_modules])
command = 'source $ESMADIR/install/bin/g5_modules'
process = subprocess.run(command, shell=True, executable='/bin/bash')
#subprocess.run(["source", "./pyradmon_bin2txt_driver.csh", exprc])
print(f'g5_modules loaded  ----------------')

# m21c.current.rc.tmpl equivalent 
#############################
class PyRadmonBase:
    # m21c.current.rc.tmpl equivalent
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
        self.gsidiagsrc = config['gsidiagsrc']
        #optional
        #########
        self.mstorage = config['mstorage'] #
        #self.instruments = config['instruments'] #
        self.bin2txt_exec = config['bin2txt_exec'] #
        self.bin2txt_nl = config['bin2txt_nl'] #
        #self.rename_date_dir = config['rename_date_dir'] #
        #try:
            #self.scp_userhost = config['scp_userhost'] #
            #self.scp_path = config['scp_path'] #
        #
        self.ndstartdate = config['startdate'][:-4].replace(" ", "") #
        self.ndenddate = config['enddate'][:-4].replace(" ", "") #
        # ???
        bin2txtnl = os.path.join(self.pyradmon,'/gsidiag/gsidiag_bin2txt/gsidiag_bin2txt.nl')
        #
        self.exprc = config_yaml_path
        self.rcfile = config_yaml_path

        # pyradmon_bin2txt_driver while loop line 74 equivalent
        def parse_mstorage(file_path, search_string):
            """
            Reads a file line by line and prints lines containing a specified string.

            Args:
                file_path (str): The path to the file.
                search_string (str): The string to search for in each line.
            """
            try:
                section_lines = []
                with open(file_path, 'r') as file:
                    for line in file:
                        if search_string in line and '.bin' in line:
                            print(line, end='')
                            section_lines.append(line)
                return section_lines
            except FileNotFoundError:
                print(f"Error: File not found: {file_path}")

        """
        for sat in sats:
            template = parse_mstorage(file_path, search_string)
            os.environ['PESTOROOT'] = self.arcbase
            os.environ['PESTOROOT'] = self.arcbase
            print(template)
        """

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
        print(f' ----- rcfile : {self.rcfile}')
        
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

        # Print all environment variables
        #for key, value in os.environ.items():
        #    print(f'{key}: {value}')    

        # Constants?
        # x = " " 
        # y = " " ...

        # g5 modules
        #subprocess.run(["source", "$ESMADIR/install/bin/g5_modules"]) 

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
        #exprc = ''
        #os.environ['exprc'] = self
        """
        execute pyradmon_bin2txt_driver.csh
        """
        try:
            #subprocess.run(["source", "./pyradmon_bin2txt_driver.csh", 'test_config_yaml_path.yaml']) #exprc])
            subprocess.run(["./pyradmon_bin2txt_driver.csh", 'test_config_yaml_path.yaml']) #exprc])
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)

    # pyradmon_img_driver.csh equivalent
    def exec_img_driver(self):
        """
        execute pyradmon_img_driver.csh
        """

        #os.environ['rcfile'] = self

        try:
            subprocess.run(["./pyradmon_img_driver.csh", 'test_config_yaml_path.yaml']) #exprc])
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)


# python script.py config.yaml
if __name__ == "__main__":

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