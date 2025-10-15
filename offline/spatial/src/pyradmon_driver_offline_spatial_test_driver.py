# pyradmon spatial driver simplest form

import logging
import os
import yaml
import argparse
import subprocess
# import shutil
# from datetime import datetime, timedelta

# Pyradmon Spatial Basic Form - offline , test_driver.csh
# --------------------------------------------------------------------------------------------------

class PyRadmonBase:
    def __init__(self, config_yaml_path): 
        """
        Initialize the PyRadmonBase class using a YAML configuration file.
        :param config_yaml_path: Path to the YAML configuration file. See PyRadmonBase_template.yaml
        
        """
        # logger
        # -------------------------------
        
        # Get with a default value if not found
        pyradmon = os.environ.get('pyradmon')
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

        # Input yaml config
        # -------------------------------
        with open(config_yaml_path, 'r') as file:
            config = yaml.safe_load(file)
        
        self.expver = config['expver']      # $1
        self.yyyymmdd = config['yyyymmdd']  # $2
        self.hh = config['hh']              # $3
        self.pyradmon = config['pyradmon']              # used in test_driver.csh to create work directories


    # --------------------------------------------------------------------------------------------------


    # run_all.csh equivalent
    # ----------------------
    def exec_test_driver(self):
        """
        execute run_all.csh
        """
        print(f'Now running: execute test_driver.csh $expver $yyyymmdd $hh')

        try:
            subprocess.run(['./test_driver.csh', self.expver, self.yyyymmdd, self.hh, self.pyradmon ]) 
            # run dir
            output_dir = self.pyradmon + '/offline/spatial/run/' + self.expver + '/tmp/' + self.yyyymmdd
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)
        print(f'finished: exec_test_driver   ------------------------------------------------------------------')
        print(f'exec_test_driver output files here: {output_dir}   ------------------------------------------------------------------')



# python script.py config.yaml
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="configuration YAML file.")
    parser.add_argument("config", help="Path to the YAML configuration file.")
    args = parser.parse_args()

    # Run Pyradmon
    PyRadmonConfig = PyRadmonBase(args.config)
    PyRadmonConfig.exec_test_driver()