import logging
import os
import yaml
import argparse
from datetime import datetime, timedelta
import subprocess
import shutil

# Global Constants, Modules and Environment Setup

# source radmon_process.config equivalent
#########################################
ESMADIR = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/' # from radmon_process.conf

# Creaking symlink ~ REQUIRED DEPENDENCY
subprocess.run(['ln','-sf','/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install-SLES15/bin/ndate_r4i4.x', './ndate'])


# Environment Modules
g5_modules = os.path.join(ESMADIR,'install/bin/g5_modules')
os.environ['ESMADIR'] = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/'
command = 'source $ESMADIR/install/bin/g5_modules'
process = subprocess.run(command, shell=True, executable='/bin/bash')
print(f'g5_modules loaded  ------------------------------------------------------------------')

# m21c.current.rc.tmpl equivalent 
#################################
class PyRadmonBase:
    def __init__(self, config_yaml_path): 
        """
        Initialize the PyRadmonBase class using a YAML configuration file.
        :param config_yaml_path: Path to the YAML configuration file. See PyRadmonBase_template.yaml
        
        """
        #self.logger = logging.getLogger(self.__class__.__name__)
        # self.config = self._load_config(config_yaml_path)
        #self._setup_logging()

        log_dir='.log'
        log_filename='app.log'
        level=logging.INFO
        try:
            # Create the log directory if it doesn't exist
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # Create full path to log file
            log_file = os.path.join(log_dir, log_filename)
            
            # Set up logging configuration
            logging.basicConfig(
                level=level,
                filename=log_file,
                format='%(asctime)s - %(levelname)s - %(message)s',
                filemode='a'
            )
            
            # Log that logging has been initialized
            logging.info("Logging initialized successfully")
            
            #return True, os.path.abspath(log_file)
            
        except (OSError, PermissionError) as e:
            error_msg = f"Failed to set up logging: {e}"
            print(error_msg)
            #return False, error_msg

        with open(config_yaml_path, 'r') as file:
            config = yaml.safe_load(file)
        
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
        mstorage: 
        #instruments: 
        bin2txt_exec: 
        bin2txt_nl: 
        #rename_date_dir: current
        #scp_userhost: aelakkra@polar
        #scp_path: /www/html/intranet/personnel/aelakkra/m21c/radmon_data/
        """
        # m21c.current.rc.tmpl equivalent
        #################################
        self.startdate = config['startdate'] # 20190530 000000
        self.enddate = config['enddate'] # 20190531 180000
        #
        self.pyradmon = config['pyradmon'] 
        self.pyradmon_local_dir = config['expbase'].split('offline/')[0]
        self.pyradmon_run_dir = self.pyradmon_local_dir + 'run/'
        #
        self.expid = config['expid'] #e5303_m21c_jan18
        self.data_dirbase = config['data_dirbase'] #os.path.join(self.arcbase, self.expid) #, 'obs') #config['data_dirbase'] #/home/dao_ops/m21c/archive/e5303_m21c_jan18/obs
        self.runbase = config['runbase'] # /home/dao_ops/e5303_m21c_jan18/run/
        self.mstorage = config['mstorage'] #
        self.arcbase = config['arcbase'] #/home/dao_ops/m21c/archive/
        #
        self.expbase = config['expbase'] #/discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/time_series/m21c_radmon/
        self.scratch_dir = config['scratch_dir'] # os.path.join(self.expbase, 'scratch') #config['scratch_dir']
        self.output_dir = config['output_dir']  #os.path.join(self.expbase, 'radmon') #config['output_dir'] 

        # Defaults ~ user should not need to change these values
        ## Executables and Code and .rc files
        self.gsidiagsrc = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/etc/gsidiags.rc'

        ## Exisitng (master?) .rc files
        ## These are just a copy of th confing_input_yaml. Should be changed.
        self.exprc = config_yaml_path #config['rcfile'] 
        self.rcfile = config_yaml_path #config['rcfile'] 

        #optional

        #########
        #self.mstorage = config['mstorage'] #
        #self.instruments = config['instruments'] #
        #self.bin2txt_exec = config['bin2txt_exec'] #
        #self.bin2txt_nl = config['bin2txt_nl'] #
        #self.rename_date_dir = config['rename_date_dir'] #

       
        ## Existing Data Files
        ### created from: self.arcbase = config['arcbase'] #/home/dao_ops/m21c/archive/

        ## User working directories (created and deleted during main process later)
        ### created from: self.expbase = config['expbase'] 
        #elf.expid = config['expid'] # os.path.join(self.expbase, self.expid) #config['output_dir'] 
        #self.expid_dir = config['output_dir']  # os.path.join(self.expbase, self.expid) #
        
        # Set Environment variables
        ###########################

        # radmon_process.config equivalent
        os.environ['ESMADIR'] = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/' #self.pyradmon
        os.environ['FVROOT'] = '/home/dao_ops/GEOSadas-5_29_5/GEOSadas/install' #self.pyradmon

        # config_yaml (m21c.current.rc) equivalent
        os.environ['expid'] = self.expid
        os.environ['expbase'] = self.expbase
        os.environ['arcbase'] = self.arcbase
        os.environ['startdate'] = self.startdate
        os.environ['enddate'] = self.enddate
        os.environ['pyradmon'] = self.pyradmon
        os.environ['exprc'] = self.exprc
        os.environ['rcfile'] = self.rcfile


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
                logging.info('Error: File not found:'+file_path)

            """
            for sat in sats:
                template = parse_mstorage(file_path, search_string)
                os.environ['PESTOROOT'] = self.arcbase
                os.environ['PESTOROOT'] = self.arcbase
                print(template)
            """

        def directory_setup_base(directory_path)-> None:

            # Check if the directory exists
            if not os.path.exists(directory_path):
                # Create the directory if it does not exist
                os.makedirs(directory_path)
                logging.info(f"Directory '{directory_path}' created successfully.")
            else:
                logging.info(f"Directory '{directory_path}' already exists.")

        def exec_directory_setup(self)-> None:
            # make expbase dir
            directory_setup_base(self.expbase)
            # make expid data dir
            directory_setup_base(self.expid_dir)
            # make scratch dir
            directory_setup_base(self.scratch_dir)
            # make output dir
            directory_setup_base(self.output_dir)
            # pyradmon/run
            directory_setup_base(self.pyradmon_run_dir)

        # Execute the directory setup
        #exec_directory_setup(self)

        """
        ## Logs
        # Generate log file name with date
        log_dir = os.path.join(self.expbase, 'log')
        log_filename = os.path.join(self.expbase, f"log_pyradmon_driver_offline_{datetime.now().strftime('%Y-%m-%d')}.log")
        
        # Setup logging
        logging.basicConfig(filename=log_filename, level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Log initialization details
        log_message = f"Initialized PYRADMON-OFFLINE with configuration from {config_yaml_path}"
        logging.info(log_message)
        #print(log_message)
    
    def _setup_logging(self):
        if not self.logger.handlers:
            # Console output
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
            
            # File output - creates 'app.log' in current directory
            file_handler = logging.FileHandler('.log/app.log')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
            self.logger.setLevel(logging.INFO)
                    """

    # m21c_radmon.csh equivalent
    ############################
    def exec_m21c_radmon() -> None:
        print(f'Running NRT Radmon for MERRA21C')
        os.environ['FVROOT'] = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/'
        os.environ['M2BASE'] = '/home/dao_ops/m21c/archive/'

        # changing directory ------ !!! -------
        #os.chdir('/discover/nobackup/sicohen/RADMON/offline/work/r21c/TBR/radmon/time_series/')

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
    def exec_bin2txt_driver(self) -> None:
        """        
        execute pyradmon_bin2txt_driver.csh
                
                set exprc=$argv[1]
                ./pyradmon_bin2txt_driver.csh $exprc
        """
    
        logging.info(f'Now running: execute exec_bin2txt_driver.csh')
        #print(f'----------- self ---- : {self}')


        try:
            # Self contained version ~ branch: develop
            # -----------------------
            #self.pyradmon_bin2txt_driver = os.path.join(self.pyradmon, 'offline/timeseries/src/pyradmon_bin2txt_driver.csh')
            #subprocess.run([self.pyradmon_bin2txt_driver, self.exprc]) #'test_config_yaml_path.yaml']) #exprc])
            
            # Pointer version ~ hard coded ~ branch: feature/dao-ops-pointer
            # -----------------------
            subprocess.run(['./pyradmon_bin2txt_driver.csh', self.exprc]) #exprc])
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)
   

        print(f'finished: exec_bin2txt_driver   ------------------------------------------------------------------')

    # pyradmon_img_driver.csh equivalent
    ####################################
    def exec_img_driver(self):
        """
        execute pyradmon_img_driver.csh
        """
        print(f'Now running: execute pyradmon_img_driver.csh')

        try:

            # Self contained version  ~ branch: develop
            # -----------------------
            #self.pyradmon_img_driver = os.path.join(self.pyradmon, 'offline/timeseries/src/pyradmon_img_driver.csh')
            #subprocess.run([self.pyradmon_img_driver, self.exprc]) # 'test_config_yaml_path.yaml'])

            # Pointer version ~ hard coded ~ branch: feature/dao-ops-pointer
            # -----------------------
            subprocess.run(['./pyradmon_img_driver.csh', self.exprc]) #exprc])
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)
        print(f'finished: exec_img_driver   ------------------------------------------------------------------')

    def move_files(self) -> None:
        src_dir = self.output_dir
        dst_dir = self.pyradmon_run_dir +'/.'
        print(f'Copying  output to pyradmon/run directory. {src_dir} to: {dst_dir}')
        logging.info(f' Copying  file(s) from: {src_dir} to: {dst_dir}')

        try:
            logging.info(f' Copying  file(s) from:  {src_dir}')
            logging.info(f' Copying  file(s) to: {dst_dir}')
            shutil.copy(src_dir, dst_dir)

        except Exception:
            logging.info(f'Copying  failed, see if source files exist {src_dir} to {dst_dir}')
 

# python script.py config.yaml
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="configuration YAML file.")
    parser.add_argument("config", help="Path to the YAML configuration file.")
    args = parser.parse_args()

    # Run Pyradmon
    PyRadmonConfig = PyRadmonBase(args.config)
    #PyRadmonConfig.exec_directory_setup()
    PyRadmonConfig.exec_bin2txt_driver()
    PyRadmonConfig.exec_img_driver()
    PyRadmonConfig.move_files()

    # move output files to the run directory
    #move_files(PyRadmonConfig.output_dir, PyRadmonConfig.pyradmon_run_dir)

