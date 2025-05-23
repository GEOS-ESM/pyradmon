import logging
import os
import yaml
import argparse
from datetime import datetime, timedelta
import subprocess

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

        with open(config_yaml_path, 'r') as file:
            config = yaml.safe_load(file)
            #print(f'config: {config}')
        
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
        self.expid = config['expid'] #e5303_m21c_jan18
        self.startdate = config['startdate'] # 20190530 000000
        self.enddate = config['enddate'] # 20190531 180000
        self.arcbase = config['arcbase'] #/home/dao_ops/m21c/archive/
        self.expbase = config['expbase'] #/discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/time_series/m21c_radmon/

        # Defaults ~ user should not need to change these values
        ## Executables and Code and .rc files
        self.pyradmon = '/home/dao_ops/pyradmon/'
        self.gsidiagsrc = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/etc/gsidiags.rc'

        ## Existing Data Files
        ### created from: self.arcbase = config['arcbase'] #/home/dao_ops/m21c/archive/
        self.data_dirbase = os.path.join(self.arcbase, self.expid, 'obs') #config['data_dirbase'] #/home/dao_ops/m21c/archive/e5303_m21c_jan18/obs
        self.runbase = os.path.join(self.arcbase, self.expid, 'run') # /home/dao_ops/e5303_m21c_jan18/run/
        self.runbase = config['runbase'] # /home/dao_ops/e5303_m21c_jan18/run/

        ## User working directories (created and deleted during main process later)
        ### created from: self.expbase = config['expbase'] 
        self.scratch_dir = os.path.join(self.expbase, 'scratch') #config['scratch_dir']
        self.output_dir = os.path.join(self.expbase, 'radmon') #config['output_dir'] 
        
        ## Exisitng (master?) .rc files
        ## These are just a copy of th confing_input_yaml. Should be changed.
        self.exprc = config_yaml_path
        self.rcfile = config_yaml_path

        #optional

        #########
        #self.mstorage = config['mstorage'] #
        #self.instruments = config['instruments'] #
        #self.bin2txt_exec = config['bin2txt_exec'] #
        #self.bin2txt_nl = config['bin2txt_nl'] #
        #self.rename_date_dir = config['rename_date_dir'] #

       
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

    #def __repr__(self):
     #   return 
        print(f'''
              pyradmon = {self.pyradmon},
              expid = {self.expid}, 
              expbase = {self.expbase},
              arcbase = {self.arcbase}, 
              data_dirbase = {self.data_dirbase},
              startdate = {self.startdate}, 
              enddate = {self.enddate}, 
              scratch_dir = {self.scratch_dir},
              output_dir = {self.output_dir}, 
              rcfile = {self.rcfile},
              exprc = {self.exprc}, 
              gsidiagsrc = {self.gsidiagsrc}, 
              self.runbase  = {self.runbase }
              )'''
              )


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


        def directory_setup_base(directory_path):

            # Check if the directory exists
            if not os.path.exists(directory_path):
                # Create the directory if it does not exist
                os.makedirs(directory_path)
                print(f"Directory '{directory_path}' created successfully.")
            else:
                print(f"Directory '{directory_path}' already exists.")

        def exec_directory_setup(self):
            # make expbase dir
            directory_setup_base(self.expbase)
            # make scratch dir
            directory_setup_base(self.scratch_dir)
            # make output dir
            directory_setup_base(self.output_dir)
            # make log dir
            log_dir = os.path.join(self.expbase, 'log')
            directory_setup_base(log_dir)


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
        """

    # m21c_radmon.csh equivalent
    ############################
    def exec_m21c_radmon():
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
    def exec_bin2txt_driver(self):
        """        
        execute pyradmon_bin2txt_driver.csh
                
                set exprc=$argv[1]
                ./pyradmon_bin2txt_driver.csh $exprc
        """
        print(f'----------- self ---- : {self}')

        try:
            
            subprocess.run(["./pyradmon_bin2txt_driver.csh", self.exprc]) #'test_config_yaml_path.yaml']) #exprc])
            #subprocess.run([os.path.join(self.pyradmon, 'pyradmon_bin2txt_driver.csh'), self.exprc]) #exprc])
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)


        print(f'exec_bin2txt_driver finished  ------------------------------------------------------------------')

    # pyradmon_img_driver.csh equivalent
    ####################################
    def exec_img_driver(self):
        """
        execute pyradmon_img_driver.csh
        """

        #os.environ['rcfile'] = self

        try:
            subprocess.run(["./pyradmon_img_driver.csh", self.exprc]) # 'test_config_yaml_path.yaml'])
            #subprocess.run([os.path.join(self.pyradmon, 'pyradmon_img_driver.csh'), self.exprc]) #exprc])
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)
        print(f'exec_img_driver finished  ------------------------------------------------------------------')


# python script.py config.yaml
if __name__ == "__main__":

    print(os.path.basename(__file__))
    parser = argparse.ArgumentParser(description="configuration YAML file.")
    parser.add_argument("config", help="Path to the YAML configuration file.")
    args = parser.parse_args()
    print(args)
    
    PyRadmonConfig = PyRadmonBase(args.config)
    PyRadmonConfig.exec_bin2txt_driver()
    #PyRadmonConfig.exec_img_driver()

    # pipe
    #process1 = subprocess.Popen(['source', './pyradmon_bin2txt_driver.csh','test_config_yaml_path.yaml'])# , stdout=subprocess.PIPE)
    #process2 = subprocess.Popen(['source', './pyradmon_img_driver.csh','test_config_yaml_path.yaml']) #, stdin=process1.stdout, stdout=subprocess.PIPE)

    

"""

if __name__ == "__main__":
    uploader = S3Uploader('config.yaml')  # Specify the path to your YAML config file
    uploader.upload_directory()
"""