# pyradmon spatial driver simplest form

import os
import yaml
import argparse
import subprocess
import shutil
from pathlib import Path
import sys


# Auto-detect repository root (works from any location)
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent  # Go up to pyradmon/

# Add offline directory to Python path for imports
sys.path.insert(0, str(REPO_ROOT / 'offline'))
from utils.logging_config import setup_logging, get_logger

# Pyradmon Spatial Basic Form - offline , test_driver.csh
# -------------------------------------------------------------------------------------------------------------------------------------

class PyRadmonBase:
    def __init__(self, config_yaml_path): 
        """
        Initialize the PyRadmonBase class using a YAML configuration file.
        :param config_yaml_path: Path to the YAML configuration file. See PyRadmonBase_template.yaml
        
        """

        log_dir = REPO_ROOT / 'offline' / 'spatial' / 'log'
        
        try:
            self.logger = setup_logging(
                log_dir=log_dir,
                log_filename='pyradmon.spatial.log',
                level='INFO',
                component='spatial',
                console_output=True
            )
        except (OSError, PermissionError) as e:
            # Fallback to console-only logging if file logging fails
            import logging
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger('pyradmon.spatial')
            self.logger.warning(f"Failed to set up file logging: {e}. Using console logging only.")
    # --------------------------------------------------------------------------------------------------


        # Input yaml config
        # -------------------------------
        with open(config_yaml_path, 'r') as file:
            config = yaml.safe_load(file)
        
        self.expver = config['expver']      # $1
        self.yyyymmdd = config['yyyymmdd']  # $2
        self.hh = config['hh']              # $3
        # self.pyradmon = config['pyradmon']  # $4


        # Obs Types Switches (Off = 0, On = 1)
        # Set value in yaml or to 0 if dne
        # equivalent to : self.atms = config['atms']
        # ------------------------------------------
        obs_types = ['atms', 'amsr2', 'amsua', 'amsua_n15', 'avhrr', 'gmi', 
                    'hirs', 'mhs', 'seviri', 'ssmis', 'cris', 'airs', 'iasi']      
        
        for obs_type in obs_types:
            setattr(self, obs_type, config.get(obs_type, 0))

    # --------------------------------------------------------------------------------------------------

    def exec_spatial_driver(self):
        """
        execute ./do_{obs_type}.csh scripts
        """

        try:
            # Load proper FVDAS_Run_Config for $EXPID
            os.environ['EXPID'] = self.expver
            command = 'source /home/dao_ops/$EXPID/run/FVDAS_Run_Config'
            process = subprocess.run(command, shell=True, executable='/bin/csh')

            # Get EXPID from environment (set above)
            expid = os.environ.get('EXPID')
            
            if not expid:
                raise ValueError("Required environment variable 'EXPID' must be set")

            # Set up paths using auto-detected REPO_ROOT
            run_path = REPO_ROOT / 'offline' / 'spatial' / 'run' 
            target_dir = run_path / expid / 'build'
            src_dir = REPO_ROOT / 'offline' / 'spatial' / 'src'

            # Create target directory for the build of pyradmon
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy src code into build
            command = f'cp -r {src_dir}/* {target_dir}/.'
            self.logger.info(f'Copying source files: {command}')
            process = subprocess.run(command, shell=True, executable='/bin/csh')
            
            if process.returncode != 0:
                self.logger.warning(f'Copy command returned non-zero exit code: {process.returncode}')

            # Change to the build directory
            os.chdir(target_dir)
            self.logger.info(f'Changed to build directory: {target_dir}')
        except Exception as e:
            error_message = f"Error during setup: {e}"
            self.logger.error(error_message, exc_info=True)
            raise

            # ----------------------------------------------------------------------------------------------------------------
        # TODO: add logging to the subprocess.run
        try:
            # Run script if obs type enabled in yaml input
            # --------------------------------------------

            # atms
            if self.atms == 1 or str(self.atms).lower() == 'on':
                subprocess.run(['./do_atms.csh', self.expver, self.yyyymmdd, self.hh]) 
            # amsr2
            if self.amsr2 == 1 or str(self.amsr2).lower() == 'on':
                subprocess.run(['./do_amsr2.csh', self.expver, self.yyyymmdd, self.hh]) 
            # amsua
            if self.amsua == 1 or str(self.amsua).lower() == 'on':
                subprocess.run(['./do_amsua.csh', self.expver, self.yyyymmdd, self.hh]) 
            # avhrr
            if self.avhrr == 1 or str(self.avhrr).lower() == 'on':
                subprocess.run(['./do_avhrr.csh', self.expver, self.yyyymmdd, self.hh]) 
            # gmi
            if self.gmi == 1 or str(self.gmi).lower() == 'on':
                subprocess.run(['./do_gmi.csh', self.expver, self.yyyymmdd, self.hh]) 
            # hirs
            if self.hirs == 1 or str(self.hirs).lower() == 'on':
                subprocess.run(['./do_hirs.csh', self.expver, self.yyyymmdd, self.hh]) 
            # mhs
            if self.mhs == 1 or str(self.mhs).lower() == 'on':
                subprocess.run(['./do_mhs.csh', self.expver, self.yyyymmdd, self.hh]) 
            # seviri
            if self.seviri == 1 or str(self.seviri).lower() == 'on':
                subprocess.run(['./do_seviri.csh', self.expver, self.yyyymmdd, self.hh]) 
            # ssmis
            if self.ssmis == 1 or str(self.ssmis).lower() == 'on':
                subprocess.run(['./do_gmi.csh', self.expver, self.yyyymmdd, self.hh]) 
            # cris
            if self.cris == 1 or str(self.cris).lower() == 'on':
                subprocess.run(['./do_cris.csh', self.expver, self.yyyymmdd, self.hh]) 
            # airs
            if self.airs == 1 or str(self.airs).lower() == 'on':
                subprocess.run(['./do_airs.csh', self.expver, self.yyyymmdd, self.hh]) 
            # iasi
            if self.iasi == 1 or str(self.iasi).lower() == 'on':
                subprocess.run(['./do_iasi.csh', self.expver, self.yyyymmdd, self.hh]) 

            # ----------------------------------------------------------------------------------------------------------------

            # Move output directory to somewhere more accesible
            # -------------------------------------------------
            # Set up paths using auto-detected REPO_ROOT
            expid = os.environ.get('EXPID')
            
            run_path = REPO_ROOT / 'offline' / 'spatial' / 'run' 
            target_dir = run_path / expid
            output_path = self.yyyymmdd 
            
            # move the completed run for given date to the $EXPID dir
            destination_path = os.path.join(target_dir, output_path)

            # Move the directory
            shutil.move(output_path, destination_path)
            self.logger.info(f'Output files moved to: {destination_path}')

        except Exception as e:
            error_message = f"Error in exec_spatial_driver: {e}"
            self.logger.error(error_message, exc_info=True)
            self.logger.error('FAILED: exec_spatial_driver')
            raise
        

# --------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------
# $ python3 pyradmon_driver_obstypes.py [user_input_config.yaml]
# --------------------------------------------------------------
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="configuration YAML file.")
    parser.add_argument("config", help="Path to the YAML configuration file.")
    args = parser.parse_args()

    # Run Pyradmon
    PyRadmonConfig = PyRadmonBase(args.config)
    PyRadmonConfig.exec_spatial_driver()

    # PyRadmonBase(args.config).exec_spatial_driver()