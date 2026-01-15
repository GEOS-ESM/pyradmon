# utils.py for pyradmon spatial
# 
# # ----------------------------------------------------------------------------------------------------
import os
import shutil
from pathlib import Path

def directory_init():
    # Get environment variables
    pyradmon = os.environ.get('pyradmon')
    expid = os.environ.get('EXPID')

    os.environ['run_dir'] = os.environ.get('FVWORK')


    if not pyradmon or not expid:
        raise ValueError("Required environment variables 'pyradmon' and 'EXPID' must be set")

    # Set up paths
    pyradmon_path = Path(pyradmon)
    run_path = pyradmon_path / 'offline' / 'spatial' / 'run'
    target_dir = run_path / expid
    src_dir = pyradmon_path / 'offline' / 'spatial' / 'src'

    # Create target directory
    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy source files
    if src_dir.exists():
        for item in src_dir.iterdir():
            dst_path = target_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dst_path)

    # Make environment variables for directories
    os.environ['src_dir'] = src_dir
    os.environ['run_dir'] = run_dir
    os.environ['target_dir'] = target_dir

    # Change directory
    os.chdir(target_dir)
    print(f"Changed to directory: {target_dir}")

# ----------------------------------------------------------------------------------------------------
def move_output(self):
    # Get environment variables
    pyradmon = os.environ.get('pyradmon')
    expid = os.environ.get('EXPID')

    try:
        # move the completed run for given date to the $EXPID dir
        source_path = self.yyyymmdd  # equivalent to $date
        destination_path = os.path.join(self.run, self.expver)  # $run/$EXPID
        
        # Ensure destination directory exists
        os.makedirs(destination_path, exist_ok=True)
        
        # Move the directory
        shutil.move(source_path, destination_path)
        print(f"Successfully moved {source_path} to {destination_path}")
        
        # Change to the destination directory
        os.chdir(destination_path)
        
        # Print current working directory
        print(f"Current directory: {os.getcwd()}")
        
    except FileNotFoundError as e:
        print(f"File or directory not found: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
