import logging
import os
import yaml
import argparse
from datetime import datetime, timedelta
import subprocess
import shutil

# Global Constants, Modules and Environment Setup
# --------------------------------------------------------
ESMADIR = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/' 

subprocess.run(['ln','-sf','/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install-SLES15/bin/ndate_r4i4.x', './ndate'])


# Environment Modules
g5_modules = os.path.join(ESMADIR,'install/bin/g5_modules')
os.environ['ESMADIR'] = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/'
command = 'source $ESMADIR/install/bin/g5_modules'
process = subprocess.run(command, shell=True, executable='/bin/bash')
print(f'g5_modules loaded  ------------------------------------------------------------------')

# 
# --------------------------------------------------------
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

        self.startdate = config['startdate'] 
        self.enddate = config['enddate'] 
        self.pyradmon = config['pyradmon'] 
        self.pyradmon_local_dir = config['expbase'].split('offline/')[0]
        self.pyradmon_run_dir = self.pyradmon_local_dir + 'run/'
        
        self.expid = config['expid'] 
        self.data_dirbase = config['data_dirbase'] 
        self.runbase = config['runbase']
        self.mstorage = config['mstorage'] 
        self.arcbase = config['arcbase'] 
        
        self.expbase = config['expbase'] 
        self.scratch_dir = config['scratch_dir'] 
        self.output_dir = config['output_dir'] 

        self.gsidiagsrc = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/etc/gsidiags.rc'

        self.exprc = config_yaml_path
        self.rcfile = config_yaml_path 

        # Set Environment variables
        ###########################

        # radmon_process.config equivalent
        os.environ['ESMADIR'] = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/'
        os.environ['FVROOT'] = '/home/dao_ops/GEOSadas-5_29_5/GEOSadas/install' 

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

    # --------------------------------------------------------
    def exec_m21c_radmon() -> None:
        print(f'Running NRT Radmon for MERRA21C')
        os.environ['FVROOT'] = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/'
        os.environ['M2BASE'] = '/home/dao_ops/m21c/archive/'
        print(f'exec_m21c_radmon finished  ------------------------------------------------------------------')

    # pyradmon_bin2txt_driver.csh equivalent
    # --------------------------------------------------------
    def exec_bin2txt_driver(self) -> None:
        """        
        execute pyradmon_bin2txt_driver.csh
                
                set exprc=$argv[1]
                ./pyradmon_bin2txt_driver.csh $exprc
        """
    
        logging.info(f'Now running: execute exec_bin2txt_driver.csh')
        #print(f'----------- self ---- : {self}')


        try:
            # Pointer version ~ hard coded ~ branch: feature/dao-ops-pointer
            # -------------------------------------------------------------
            subprocess.run(['./pyradmon_bin2txt_driver.csh', self.exprc])
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)
   

        print(f'finished: exec_bin2txt_driver   ------------------------------------------------------------------')

    # pyradmon_img_driver.csh equivalent
    # --------------------------------------------------------
    def exec_img_driver(self):
        """
        execute pyradmon_img_driver.csh
        """
        print(f'Now running: execute pyradmon_img_driver.csh')

        try:
            # Pointer version ~ hard coded ~ branch: feature/dao-ops-pointer
            # -------------------------------------------------------------
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

