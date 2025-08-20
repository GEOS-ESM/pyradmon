import yaml
import os
import re
from typing import Dict, Any, List
from datetime import datetime
import subprocess

class RadmonConfig:
    # Define valid observation types as a class constant
    VALID_OBSTYPES = [
        'atms', 'amsr2', 'amsua', 'amsua_n15', 'avhrr', 'gmi', 
        'hirs', 'mhs', 'seviri', 'ssmis', 'cris', 'airs', 'iasi'
    ]
    
    def __init__(self, config_file: str, strict_validation: bool = True):
        """
        Initialize RadmonConfig with a YAML configuration file
        
        Args:
            config_file (str): Path to the YAML configuration file
            strict_validation (bool): If True, raises exceptions for validation errors.
                                    If False, only prints warnings.
        """
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self.strict_validation = strict_validation
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []
        
        self.load_config()
        self._validate_config()
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
        pyradmon = self.config.get('PYRADMON')
        if pyradmon:
            os.environ['PYRADMON'] = str(pyradmon)
            env_vars_set.append(f"PYRADMON={pyradmon}")
        
        # Set EXPID environment variable
        expid = self.config.get('EXPID')
        if expid:
            os.environ['EXPID'] = str(expid)
            env_vars_set.append(f"EXPID={expid}")
        
        # Set Date environment variable
        date = self.config.get('Date')
        if date:
            os.environ['Date'] = str(date)
            env_vars_set.append(f"Date={date}")
        
        # Set hour environment variable
        hour = self.config.get('hour')
        if hour:
            os.environ['hour'] = str(hour)
            env_vars_set.append(f"hour={hour}")
        
        # Set obstypes environment variable (as space-separated string)
        obstypes = self.config.get('obstypes')
        if obstypes and isinstance(obstypes, list):
            obstypes_str = ' '.join(obstypes)
            os.environ['obstypes'] = obstypes_str
            env_vars_set.append(f"obstypes={obstypes_str}")
        
        if env_vars_set:
            print(f"Environment variables set: {', '.join(env_vars_set)}")
    
    def _validate_config(self) -> None:
        """
        Validate configuration parameters with detailed checks
        Raises ValidationError if strict_validation is True and errors are found
        """
        self.validation_errors = []
        self.validation_warnings = []
        
        # Check required fields
        required_fields = ['PYRADMON', 'EXPID', 'Date', 'hour']
        for field in required_fields:
            if field not in self.config:
                self.validation_errors.append(f"Missing required field: {field}")
            elif self.config[field] is None or self.config[field] == '':
                self.validation_errors.append(f"Required field '{field}' is empty or null")
        
        # Validate PYRADMON path
        self._validate_pyradmon_path()
        
        # Validate EXPID
        self._validate_expid()
        
        # Validate Date format
        self._validate_date()
        
        # Validate hour format
        self._validate_hour()
        
        # Validate obstypes (optional)
        self._validate_obstypes()
        
        # Handle validation results
        self._handle_validation_results()
    
    def _validate_pyradmon_path(self) -> None:
        """Validate PYRADMON path"""
        pyradmon = self.config.get('PYRADMON')
        
        if pyradmon is None:
            return  # Already handled in main validation
        
        if not isinstance(pyradmon, str):
            self.validation_errors.append("PYRADMON must be a string path")
            return
        
        # Check if path exists
        if not os.path.exists(pyradmon):
            self.validation_errors.append(f"PYRADMON path does not exist: {pyradmon}")
            return
        
        # Check if it's a directory
        if not os.path.isdir(pyradmon):
            self.validation_errors.append(f"PYRADMON must be a directory: {pyradmon}")
            return
        
        # Check if it ends with the expected path structure
        expected_suffix = os.path.join('pyradmon', 'offline', 'spatial', 'src')
        normalized_path = os.path.normpath(pyradmon)
        
        if not normalized_path.endswith(os.path.normpath(expected_suffix)):
            self.validation_warnings.append(
                f"PYRADMON path does not end with expected structure '{expected_suffix}': {pyradmon}"
            )
        
        # Check if path is readable
        if not os.access(pyradmon, os.R_OK):
            self.validation_errors.append(f"PYRADMON path is not readable: {pyradmon}")
    
    def _validate_expid(self) -> None:
        """Validate EXPID format"""
        expid = self.config.get('EXPID')
        
        if expid is None:
            return  # Already handled in main validation
        
        if not isinstance(expid, str):
            self.validation_errors.append("EXPID must be a string")
            return
        
        # Check for reasonable EXPID format (alphanumeric, underscores, hyphens)
        if not re.match(r'^[a-zA-Z0-9_-]+$', expid):
            self.validation_errors.append(
                "EXPID contains invalid characters. Only alphanumeric characters, "
                "underscores, and hyphens are allowed"
            )
        
        # Check length (reasonable limits)
        if len(expid) < 1:
            self.validation_errors.append("EXPID cannot be empty")
        elif len(expid) > 50:
            self.validation_warnings.append(f"EXPID is unusually long ({len(expid)} characters): {expid}")
    
    def _validate_date(self) -> None:
        """Validate Date format (YYYYMMDD)"""
        date = self.config.get('Date')
        
        if date is None:
            return  # Already handled in main validation
        
        # Convert to string if it's a number
        if isinstance(date, int):
            date = str(date)
            self.config['Date'] = date  # Update config with string version
        elif not isinstance(date, str):
            self.validation_errors.append("Date must be a string or integer")
            return
        
        # Check format YYYYMMDD
        if not re.match(r'^\d{8}$', date):
            self.validation_errors.append(
                f"Date must be in format YYYYMMDD (8 digits): got '{date}'"
            )
            return
        
        # Validate actual date
        try:
            year = int(date[:4])
            month = int(date[4:6])
            day = int(date[6:8])
            
            # Basic range checks
            if year < 1900 or year > 2100:
                self.validation_warnings.append(f"Date year seems unusual: {year}")
            
            if month < 1 or month > 12:
                self.validation_errors.append(f"Invalid month in date: {month}")
                return
            
            if day < 1 or day > 31:
                self.validation_errors.append(f"Invalid day in date: {day}")
                return
            
            # Validate actual date exists
            datetime(year, month, day)
            
        except ValueError as e:
            self.validation_errors.append(f"Invalid date: {date} - {str(e)}")
    
    def _validate_hour(self) -> None:
        """Validate hour format (HH)"""
        hour = self.config.get('hour')
        
        if hour is None:
            return  # Already handled in main validation
        
        # Convert to string if it's a number
        if isinstance(hour, int):
            hour = str(hour).zfill(2)  # Add leading zero if needed
            self.config['hour'] = hour  # Update config with formatted version
        elif not isinstance(hour, str):
            self.validation_errors.append("Hour must be a string or integer")
            return
        
        # Check format HH (2 digits)
        if not re.match(r'^\d{2}$', hour):
            self.validation_errors.append(
                f"Hour must be in format HH (2 digits): got '{hour}'"
            )
            return
        
        # Validate hour range (00-23)
        try:
            hour_int = int(hour)
            if hour_int < 0 or hour_int > 23:
                self.validation_errors.append(f"Hour must be between 00 and 23: got {hour}")
        except ValueError:
            self.validation_errors.append(f"Hour must be numeric: got '{hour}'")
    
    def _validate_obstypes(self) -> None:
        """Validate obstypes list (optional)"""
        obstypes = self.config.get('obstypes')
        
        if obstypes is None:
            # obstypes is optional
            return
        
        if not isinstance(obstypes, list):
            self.validation_errors.append("obstypes must be a list")
            return
        
        if len(obstypes) == 0:
            self.validation_warnings.append("obstypes list is empty")
            return
        
        # Check each obstype
        invalid_obstypes = []
        for obstype in obstypes:
            if not isinstance(obstype, str):
                self.validation_errors.append(f"All obstypes must be strings: got {type(obstype)} for '{obstype}'")
                continue
            
            if obstype not in self.VALID_OBSTYPES:
                invalid_obstypes.append(obstype)
        
        if invalid_obstypes:
            self.validation_errors.append(
                f"Invalid obstypes found: {invalid_obstypes}. "
                f"Valid obstypes are: {self.VALID_OBSTYPES}"
            )
        
        # Check for duplicates
        duplicates = []
        seen = set()
        for obstype in obstypes:
            if obstype in seen:
                duplicates.append(obstype)
            seen.add(obstype)
        
        if duplicates:
            self.validation_warnings.append(f"Duplicate obstypes found: {duplicates}")
    
    def _handle_validation_results(self) -> None:
        """Handle validation results based on strict_validation setting"""
        # Print warnings
        for warning in self.validation_warnings:
            print(f"WARNING: {warning}")
        
        # Handle errors
        if self.validation_errors:
            error_message = "Configuration validation failed:\n" + "\n".join(
                f"  - {error}" for error in self.validation_errors
            )
            
            if self.strict_validation:
                raise ValidationError(error_message)
            else:
                print(f"ERROR: {error_message}")
    
    def is_valid(self) -> bool:
        """Check if configuration is valid (no errors)"""
        return len(self.validation_errors) == 0


# Custom exception for validation errors
class ValidationError(Exception):
    """Custom exception for configuration validation errors"""
    pass




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




# Example usage:
if __name__ == "__main__":
    # Create an example YAML file
    example_config = """
PYRADMON: /discover/nobackup/sicohen/RADMON/develop/pyradmon/offline/spatial/src
EXPID: f5295_fp
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
        
        print(f"\nConfiguration valid: {config.is_valid()}")
        
        # Check if environment variables were set
        print("\n=== Environment Variables Set ===")
        for key in ['PYRADMON', 'EXPID', 'Date', 'hour', 'obstypes']:
            value = os.environ.get(key, 'Not set')
            print(f"{key}: {value}")

        # subprocess.run(['./test_driver.csh'])

        subprocess.run(['./test_driver.csh'])

    except ValidationError as e:
        print(f"Validation failed: {e}")
    except Exception as e:
        print(f"Error: {e}")