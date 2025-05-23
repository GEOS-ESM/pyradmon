# Configuration and Directory Setup
# 2025-05-02

import os

#
os.mkd('develop/pyradmon/offline/timeseries/r21c/TBR/radmon/time_series/m21c_radmon/e5303_m21c_jan18/obs/Y2019/M05/D30/H06/e5303_m21c_jan18.diag_amsua_n15_anl.20190530_06z.txt')

"""
set startdir=`pwd`
mkdir -p work.$exprc
cp $exprc work.$exprc
cd work.$exprc
"""

# Create the directory 
try:
    os.mkdir(os.path.join(self.expbase, self.exprc))
    print(f"Directory '{os.path.join(self.expbase, self.exprc)}' created.")
except FileExistsError:
    print(f"Directory '{os.path.join(self.expbase, self.exprc)}' already exists.")
except FileNotFoundError:
    print(f"Invalid path.")


# Create the directory 
try:
    os.mkdir(self.scratch_dir)
    print(f"Directory '{self.scratch_dir}' created.")
except FileExistsError:
    print(f"Directory '{self.scratch_dir}' already exists.")
except FileNotFoundError:
    print(f"Invalid path.")

# Create the directory 
try:
    os.mkdir(self.output_dir)
    print(f"Directory '{self.output_dir}' created.")
except FileExistsError:
    print(f"Directory '{self.output_dir}' already exists.")
except FileNotFoundError:
    print(f"Invalid path.")