import logging
import os
import tempfile
import yaml
import argparse
from datetime import datetime, timedelta
import subprocess
import sys
from pathlib import Path

# Auto-detect repository root (works from any location)
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent  # timeseries/src/ -> timeseries/ -> offline/ -> pyradmon/

# Add offline directory to Python path for shared utilities
sys.path.insert(0, str(REPO_ROOT / 'offline'))
from utils.logging_config import setup_logging, get_logger
from utils.output_config import move_output

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

        config_yaml_path = str(Path(config_yaml_path).resolve())

        log_dir = REPO_ROOT / 'offline' / 'timeseries' / 'log'

        try:
            self.logger = setup_logging(
                log_dir=log_dir,
                log_filename='pyradmon.timeseries.log',
                level='INFO',
                component='timeseries',
                console_output=True
            )
        except (OSError, PermissionError) as e:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger('pyradmon.timeseries')
            self.logger.warning(f"Failed to set up file logging: {e}. Using console logging only.")

        user_id = os.environ.get('USER', os.environ.get('LOGNAME', ''))
        with open(config_yaml_path, 'r') as file:
            raw = file.read().replace('{user_id}', user_id)
        config = yaml.safe_load(raw)

        # Write a resolved copy of the config (with {user_id} substituted) for
        # the shell scripts, which read the file directly via echorc.x.
        tmp = tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False,
            dir=SCRIPT_DIR, prefix='.resolved_config_'
        )
        tmp.write(raw)
        tmp.close()
        self._resolved_config_path = tmp.name

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
        
        self.expbase = config['expbase'].rstrip('/') + '/'
        self.scratch_dir = config['scratch_dir'].rstrip('/') + '/'
        self.output_dir = config['output_dir'].rstrip('/')  + '/'

        self.gsidiagsrc = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/etc/gsidiags.rc'

        self.exprc = config_yaml_path
        self.rcfile = config_yaml_path 

        # Set Environment variables
        # -------------------------

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
    
        self.logger.info('Now running: exec_bin2txt_driver.csh')

        try:
            # Pointer version ~ hard coded ~ branch: feature/dao-ops-pointer
            # -------------------------------------------------------------
            subprocess.run(['./pyradmon_bin2txt_driver.csh', self._resolved_config_path], cwd=SCRIPT_DIR)
        except Exception as e:
            self.logger.error(f"Error in exec_bin2txt_driver: {e}", exc_info=True)

        self.logger.info('Finished: exec_bin2txt_driver')

    # pyradmon_img_driver.csh equivalent
    # --------------------------------------------------------
    def exec_img_driver(self):
        """
        execute pyradmon_img_driver.csh
        """
        self.logger.info('Now running: exec_img_driver.csh')
  
        try:
            # Pointer version ~ hard coded ~ branch: feature/dao-ops-pointer
            # -------------------------------------------------------------
            subprocess.run(['./pyradmon_img_driver.csh', self._resolved_config_path], cwd=SCRIPT_DIR)
        except Exception as e:
            self.logger.error(f"Error in exec_img_driver: {e}", exc_info=True)

        self.logger.info('Finished: exec_img_driver')

    def move_files(self) -> None:
        """
        Move output directory to the centralized run location.
        Destination: offline/run/timeseries/<expid>/<date_tag>/
        """
        date_tag = os.path.basename(self.output_dir.rstrip('/'))

        if not os.path.exists(self.output_dir.rstrip('/')):
            self.logger.warning(
                f'Output directory does not exist, skipping move: {self.output_dir} '
                f'(scripts may have failed to produce output)'
            )
            return

        try:
            move_output(
                source=self.output_dir,
                component='timeseries',
                expid=self.expid,
                date_tag=date_tag,
                logger=self.logger
            )
        except Exception as e:
            self.logger.error(f'move_files failed: {e}', exc_info=True)
 

# python script.py config.yaml
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="configuration YAML file.")
    parser.add_argument("config", help="Path to the YAML configuration file.")
    args = parser.parse_args()

    # Run Pyradmon
    PyRadmonConfig = PyRadmonBase(args.config)
    try:
        PyRadmonConfig.exec_bin2txt_driver()
        PyRadmonConfig.exec_img_driver()
        PyRadmonConfig.move_files()
    finally:
        os.unlink(PyRadmonConfig._resolved_config_path)

