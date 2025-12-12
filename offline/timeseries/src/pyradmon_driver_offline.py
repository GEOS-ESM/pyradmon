import os
import yaml
import argparse
from datetime import datetime, timedelta
import subprocess
import shutil
from pathlib import Path
import sys

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.logging_config import setup_logging, get_logger

# Global Constants, Modules and Environment Setup

# Path configuration - can be overridden via environment variables
ESMADIR = os.environ.get('ESMADIR', '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/')
FVROOT = os.environ.get('FVROOT', '/home/dao_ops/GEOSadas-5_29_5/GEOSadas/install')
M2BASE = os.environ.get('M2BASE', '/home/dao_ops/m21c/archive/')

# Setup environment variables
os.environ['ESMADIR'] = ESMADIR
os.environ['FVROOT'] = FVROOT

# Create symlink for ndate executable (required dependency)
ndate_exec = os.path.join(ESMADIR, 'install-SLES15/bin/ndate_r4i4.x')
subprocess.run(['ln', '-sf', ndate_exec, './ndate'], check=False)

# Load g5_modules
g5_modules = os.path.join(ESMADIR, 'install/bin/g5_modules')
command = f'source {g5_modules}'
subprocess.run(command, shell=True, executable='/bin/bash', check=False)

# m21c.current.rc.tmpl equivalent 
#################################
class PyRadmonBase:
    def __init__(self, config_yaml_path): 
        """
        Initialize the PyRadmonBase class using a YAML configuration file.
        :param config_yaml_path: Path to the YAML configuration file. See PyRadmonBase_template.yaml
        
        """
        # -------------------------------
        # Setup centralized logging
        # -------------------------------
        # Try to use expbase for log directory, fallback to current directory
        log_dir = Path('.log')  # Default fallback
        
        try:
            with open(config_yaml_path, 'r') as file:
                config = yaml.safe_load(file)
            
            # Try to get expbase from config for better log location
            if 'expbase' in config:
                log_dir = Path(config['expbase']) / 'log'
            elif 'pyradmon' in config:
                log_dir = Path(config['pyradmon']) / 'offline' / 'timeseries' / 'log'
        except Exception:
            # If config read fails, we'll use default log_dir
            pass
        
        try:
            self.logger = setup_logging(
                log_dir=log_dir,
                log_filename='pyradmon.timeseries.log',
                level='INFO',
                component='timeseries',
                console_output=True
            )
        except (OSError, PermissionError) as e:
            # Fallback to console-only logging if file logging fails
            import logging
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger('pyradmon.timeseries')
            self.logger.warning(f"Failed to set up file logging: {e}. Using console logging only.")
        
        # Now load config (if not already loaded)
        if 'config' not in locals():
            with open(config_yaml_path, 'r') as file:
                config = yaml.safe_load(file)
        
        self.logger.info(f"Initialized PYRADMON-OFFLINE with configuration from {config_yaml_path}")
        
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
        self.gsidiagsrc = os.path.join(ESMADIR, 'install/etc/gsidiags.rc')

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
        # ESMADIR and FVROOT already set at module level

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
                            # Use logger if available, otherwise print
                            if hasattr(self, 'logger'):
                                self.logger.debug(line.rstrip())
                            else:
                                print(line, end='')
                            section_lines.append(line)
                return section_lines
            except FileNotFoundError:
                if hasattr(self, 'logger'):
                    self.logger.error(f'File not found: {file_path}')
                else:
                    logging.error(f'File not found: {file_path}')

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
                if hasattr(self, 'logger'):
                    self.logger.info(f"Directory '{directory_path}' created successfully.")
                else:
                    logging.info(f"Directory '{directory_path}' created successfully.")
            else:
                if hasattr(self, 'logger'):
                    self.logger.debug(f"Directory '{directory_path}' already exists.")
                else:
                    logging.debug(f"Directory '{directory_path}' already exists.")

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
    def exec_m21c_radmon(self) -> None:
        self.logger.info('Running NRT Radmon for MERRA21C')
        os.environ['FVROOT'] = FVROOT
        os.environ['M2BASE'] = M2BASE

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
        self.logger.info('exec_m21c_radmon finished')

    # pyradmon_bin2txt_driver.csh equivalent
    ########################################
    def exec_bin2txt_driver(self) -> None:
        """        
        execute pyradmon_bin2txt_driver.csh
                
                set exprc=$argv[1]
                ./pyradmon_bin2txt_driver.csh $exprc
        """
        self.logger.info('Now running: execute exec_bin2txt_driver.csh')

        try:
            # Self contained version ~ branch: develop
            # -----------------------
            #self.pyradmon_bin2txt_driver = os.path.join(self.pyradmon, 'offline/timeseries/src/pyradmon_bin2txt_driver.csh')
            #subprocess.run([self.pyradmon_bin2txt_driver, self.exprc]) #'test_config_yaml_path.yaml']) #exprc])
            
            # Pointer version ~ hard coded ~ branch: feature/dao-ops-pointer
            # -----------------------
            result = subprocess.run(
                ['./pyradmon_bin2txt_driver.csh', self.exprc],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info('Successfully completed exec_bin2txt_driver')
            else:
                self.logger.error(
                    f'exec_bin2txt_driver failed with return code {result.returncode}'
                )
                if result.stderr:
                    self.logger.error(f'stderr: {result.stderr}')
        except Exception as e:
            error_message = f"Error in exec_bin2txt_driver: {e}"
            self.logger.error(error_message, exc_info=True)
            raise

    # pyradmon_img_driver.csh equivalent
    ####################################
    def exec_img_driver(self):
        """
        execute pyradmon_img_driver.csh
        """
        self.logger.info('Now running: execute pyradmon_img_driver.csh')

        try:
            # Self contained version  ~ branch: develop
            # -----------------------
            #self.pyradmon_img_driver = os.path.join(self.pyradmon, 'offline/timeseries/src/pyradmon_img_driver.csh')
            #subprocess.run([self.pyradmon_img_driver, self.exprc]) # 'test_config_yaml_path.yaml'])

            # Pointer version ~ hard coded ~ branch: feature/dao-ops-pointer
            # -----------------------
            result = subprocess.run(
                ['./pyradmon_img_driver.csh', self.exprc],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info('Successfully completed exec_img_driver')
            else:
                self.logger.error(
                    f'exec_img_driver failed with return code {result.returncode}'
                )
                if result.stderr:
                    self.logger.error(f'stderr: {result.stderr}')
        except Exception as e:
            error_message = f"Error in exec_img_driver: {e}"
            self.logger.error(error_message, exc_info=True)
            raise

    def move_files(self) -> None:
        """Copy output files to pyradmon run directory."""
        src_dir = self.output_dir
        dst_dir = self.pyradmon_run_dir.rstrip('/')
        self.logger.info(f'Copying output from {src_dir} to {dst_dir}')

        try:
            os.makedirs(dst_dir, exist_ok=True)
            # Copy directory contents
            for item in os.listdir(src_dir):
                src_path = os.path.join(src_dir, item)
                dst_path = os.path.join(dst_dir, item)
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dst_path)
            self.logger.info('Successfully copied files')
        except Exception as e:
            self.logger.error(f'Copying failed: {e}', exc_info=True)
            raise
 

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

