# pyradmon spatial driver simplest form

import logging
import os
import yaml
import argparse
import subprocess
import shutil
from pathlib import Path


# Pyradmon Spatial Basic Form - offline , test_driver.csh
# -------------------------------------------------------------------------------------------------------------------------------------

class PyRadmonBase:
    def __init__(self, config_yaml_path): 
        """
        Initialize the PyRadmonBase class using a YAML configuration file.
        :param config_yaml_path: Path to the YAML configuration file. See PyRadmonBase_template.yaml
        
        """
        # -------------------------------
        # logger
        # -------------------------------
        
        # Get with a default value if not found
        # pyradmon = os.environ['pyradmon']
        # log_dir= os.path.join(os.environ.get('pyradmon'), 'log')
        log_dir= os.path.join(os.environ.get('pyradmon'), 'offline/spatial/log')
        log_filename='pyradmon.spatial.log'
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
            os.environ['EXPID'] = self.expver #os.environ.get('expver')
            command = 'source /home/dao_ops/$EXPID/run/FVDAS_Run_Config'
            process = subprocess.run(command, shell=True, executable='/bin/csh -f')

            # Get environment variables
            pyradmon = os.environ.get('pyradmon')
            expid = os.environ.get('EXPID')

            if not pyradmon or not expid:
                raise ValueError("Required environment variables 'pyradmon' and 'EXPID' must be set")

            # Set up paths
            pyradmon_path = Path(pyradmon)
            run_path = pyradmon_path / 'offline' / 'spatial' / 'run' 
            target_dir = run_path / expid / 'build'
            src_dir = pyradmon_path / 'offline' / 'spatial' / 'src'

            # Create target directory for the build of pyradmon
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy src code into build
            command = f'cp -r {src_dir}/* {target_dir}/.'
            print(f' command : {command}')
            process = subprocess.run(command, shell=True, executable='/bin/csh -f')

            # Change to the build directory
            os.chdir(target_dir)
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)

            # ----------------------------------------------------------------------------------------------------------------

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
            # Set up paths
            pyradmon = os.environ.get('pyradmon')
            expid = os.environ.get('EXPID')

            pyradmon_path = Path(pyradmon)
            run_path = pyradmon_path / 'offline' / 'spatial' / 'run' 
            target_dir = run_path / expid
            output_path = self.yyyymmdd 
            
            # move the completed run for given date to the $EXPID dir
            destination_path = os.path.join(target_dir, output_path)

            # Move the directory
            shutil.move(output_path, destination_path)
            print(f'Output files moved to:  {destination_path}  ')

        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)
            print(f'FAILED: exec_spatial_driver   ------------------------------------------------------------------')
        

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