import yaml
import os
import re
from typing import Dict, Any, List, Optional
from datetime import datetime

class RadmonConfig:
    # Define valid observation types as a class constant
    VALID_OBSTYPES = [
        'atms', 'amsr2', 'amsua', 'amsua_n15', 'avhrr', 'gmi', 
        'hirs', 'mhs', 'seviri', 'ssmis', 'cris', 'airs', 'iasi'
    ]
    
    def __init__(self, config_file: str, strict_validation: bool = True, set_env_vars: bool = True):
        """
        Initialize RadmonConfig with a YAML configuration file
        
        Args:
            config_file (str): Path to the YAML configuration file
            strict_validation (bool): If True, raises exceptions for validation errors.
                                    If False, only prints warnings.
            set_env_vars (bool): If True, automatically sets environment variables after loading
        """
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self.strict_validation = strict_validation
        self.set_env_vars = set_env_vars
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []
        
        self.load_config()
        self._validate_config()
        
        if self.set_env_vars and self.is_valid():
            self.set_environment_variables()
    
    def load_config(self) -> None:
        """Load configuration from YAML file"""
        try:
            with open(self.config_file, 'r') as file:
                self.config = yaml.safe_load(file) or {}
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file {self.config_file} not found")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")
    
    def set_environment_variables(self) -> None:
        """Set environment variables for all configuration fields"""
        env_vars_set = []
        
        # Set PYRADMON environment variable
        if self.pyradmon_path:
            os.environ['PYRADMON'] = str(self.pyradmon_path)
            env_vars_set.append(f"PYRADMON={self.pyradmon_path}")
        
        # Set EXPID environment variable
        if self.expid:
            os.environ['EXPID'] = str(self.expid)
            env_vars_set.append(f"EXPID={self.expid}")
        
        # Set Date environment variable
        if self.date:
            os.environ['Date'] = str(self.date)
            env_vars_set.append(f"Date={self.date}")
        
        # Set hour environment variable
        if self.hour:
            os.environ['hour'] = str(self.hour)
            env_vars_set.append(f"hour={self.hour}")
        
        # Set obstypes environment variable (as space-separated string)
        if self.obstypes:
            obstypes_str = ' '.join(self.obstypes)
            os.environ['obstypes'] = obstypes_str
            env_vars_set.append(f"obstypes={obstypes_str}")
        
        if env_vars_set:
            print(f"Environment variables set: {', '.join(env_vars_set)}")
  

# Example usage:
if __name__ == "__main__":
    # Create an example YAML file
    example_config = """
PYRADMON: /discover/nobackup/sicohen/RADMON/develop/pyradmon/offline/spatial/src
EXPID: test_experiment_123
Date: 20231201
hour: 18

obstypes:
  - atms 
  - amsr2 
  - amsua
  - amsua_n15
"""
    
    # Save example config
    with open('radmon_config.yaml', 'w') as f:
        f.write(example_config)
    
    try:
        print("=== Creating RadmonConfig ===")
        config = RadmonConfig('radmon_config.yaml', strict_validation=False)
        
        print("\n=== Current Environment Variables ===")
        env_vars = config.get_environment_variables()
        for key, value in env_vars.items():
            print(f"{key}: {value}")
        




    # test_driver.csh equivalent
    ############################
    def exec_test_driver(self):
        """
        execute test_driver.csh
        """
        print(f'Now running: execute test_driver.csh')

        try:
            # ----------------------------------
            subprocess.run(['./test_driver.csh'])
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)
        print(f'finished: exec_img_driver   ------------------------------------------------------------------')

