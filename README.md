========

pyradmon

Python Radiance Monitoring Tool. Contains both spatial and timeseries pyradmon.

## TL;DR - Quick Start

**First time setup:**
```sh
cd $NOBACKUP
mkdir -p $NOBACKUP/pyradmon-project
cd pyradmon-project
git clone https://github.com/GEOS-ESM/pyradmon.git
cd pyradmon
```

**Every session - Load environment (must be in repo root):**
```csh
source load_radmon_config.csh  # or load_radmon_config.sh for bash/zsh
```


**Add mod_pyradmon alias:** Add `mod_pyradmon` alias to your shell rc file to load (see [Environment Setup](#load-pyradmon-environment-setup--environment-variables)).
```csh
alias mod_pyradmon ' setenv PYRADMON $NOBACKUP/pyradmon-project/pyradmon ; \
                     cd $PYRADMON ; \
                     module load miniforge ; \
                     source $PYRADMON/load_radmon_config.csh'  # or load_radmon_config.sh for bash/zsh
```

Resuming work from a previous - use the `mod_pyradmon` alias to load pyradmon 



**Run spatial:**
```sh
cd $PYRADMON_SPATIAL
cp test_config.geosfp.yaml user_geosfp_spatial_input.yaml
# Edit my_config.yaml: set dates, expver, turn obs switches on/off
python3 pyradmon_driver_spatial.py user_geosfp_spatial_input.yaml
```

**Run timeseries:**
```sh
cd $PYRADMON_TIMESERIES
# Auto-generated yamls ready to use: user_geosit_timeseries_input.yaml or user_m21c_timeseries_input.yaml
# Edit if needed: dates, expid, data paths, instruments
python3 pyradmon_driver_timeseries.py user_m21c_timeseries_input.yaml
```

---

## Table of Contents

1. [Overview](#overview)
2. [Installation and Environment Setup](#installation-and-environment-setup)
   - [First Time Installation](#first-time-installing-pyradmon)
   - [Load Environment](#load-pyradmon-environment-setup--environment-variables)
3. [How to Run](#how-to-run)
   - [Spatial](#spatial)
   - [Timeseries](#timeseries)
4. [License](#license)

---

## Overview

The Radiance monitoring tool, pyradmon, has been overhauled after compatibility issues caused by the transition from SLES12 to SLES15. Most of the changes were the addition of python scripts for the front end and edits to make backend shell scripts work with the new python scripts. The edits on the backend were to only a few, albeit important, scripts. Backend python scripts were also edited slightly to account for changes to the directory structure within the repository and to account for updates to packages like matplotlib which were part of the issues during the OS transition.

Returning users can expect the final outputs (plots) pyradmon produces to be the same as it did previously – plots should be formatted in the same style, etc. While pyradmon is running, users should expect to see similar – but different - output in the terminal. The location of the output images and .tar file will be in a different location – the .tar file will have the same structure as it did previously.

<!-- The current version of pyradmon:
- is working for both timeseries and spatial plotting.
- is a 'pointer' - the python wrappers point to the backend scripts that are in /home/dao_ops/pyradmon/ NOT the ones that are in the source directories in this repository. -->

<!-- More changes are being made to make it more flexible and user friendly. -->
Users should be careful not overwrite their initial source code of this repo when there is an update.

---

## Installation and Environment Setup

Pyradmon is a package consisting of Python wrappers (drivers) that take user created yamls as input on the front end and a combination of python, shell, and perl scripts on the backend.
<!-- 
Once setup is complete users will use, or interact with, 5 files when running pyradmon: 3 scripts and 2 yamls.
- One .csh or .sh script for loading pyradmon
- Two python scripts ~ one for running pyradmon timeseries & one for running pyradmon spatial
- Two yaml files ~ one for running pyradmon timeseries & one for running pyradmon spatial -->

### First time installing pyradmon:

Clone pyradmon to wherever you want to live, for example:

```sh
cd $NOBACKUP
mkdir -p pyradmon-project && cd pyradmon-project
git clone https://github.com/GEOS-ESM/pyradmon.git
cd $NOBACKUP/pyradmon-project/pyradmon
```

### Load pyradmon (environment setup & environment variables)

**IMPORTANT:** The load script must be run from the repository root directory (where `load_radmon_config.csh` and the `offline/` directory are located).

<!-- You will no longer need to create or activate your virtual environment directly.  -->
The load script handles environment setup automatically.

From now on, in order to load pyradmon you must use the appropriate `load_radmon_config.*` script. These scripts:
- Verify you are in the repository root directory
- Load the g5_modules
- Set environment variables that the pyradmon scripts will use ($PYRADMON, $PYRADMON_SPATIAL, $PYRADMON_TIMESERIES, $PYRADMON_RUN)
- Auto-generate personalized timeseries input yaml files

**For csh/tcsh users:**
```csh
source load_radmon_config.csh
```

**For bash/zsh users:**
```sh
source load_radmon_config.sh
```

**Optional - Add a convenience alias to your shell rc file:**

For csh/tcsh (.cshrc):
```csh
alias mod_pyradmon 'setenv PYRADMON $NOBACKUP/pyradmon-project/pyradmon ; \
                    cd $PYRADMON ; \
                    module load miniforge ; \
                    source $PYRADMON/load_radmon_config.csh'
```

For bash/zsh (.bashrc/.zshrc):
```sh
alias mod_pyradmon='export PYRADMON=$NOBACKUP/pyradmon-project/pyradmon ; \
                    cd $PYRADMON ; \
                    module load miniforge ; \
                    source $PYRADMON/load_radmon_config.sh'
```

Then you can simply run `mod_pyradmon` from anywhere to load the environment.

---

## How to run

### Spatial:

```sh
python3 pyradmon_driver_spatial.py [user_input_yaml]
```

1) Navigate to the repository root and load pyradmon:
   ```csh
   cd $NOBACKUP/pyradmon-project/pyradmon
   source load_radmon_config.csh
   ```

2) Change to the spatial source directory:
   ```sh
   cd $PYRADMON_SPATIAL
   ```

3) Create your user input yaml by copying an existing example yaml. You may name the yaml file whatever you like:
   ```sh
   cp test_config.geosfp.yaml user_input_yaml.yaml
   ```

4) Open and edit the yaml to the experiment and dates you wish to run pyradmon for. Set the Obs Types switches to 1 for ON and 0 for OFF

5) Run pyradmon spatial:
   ```sh
   python3 pyradmon_driver_spatial.py user_input_yaml.yaml
   ```

**Example user_input_yaml: test_config.geosfp.yaml:**

The example will only run pyradmon spatial for gmi.

```yaml
# config for pyradmon_driver_spatial.py
# -------------------------------------

expver: f5295_fp
yyyymmdd: '20250301'
hh: '18'

# Obs Types Switches (Off = 0, On = 1)
# ------------------------------------
atms: 0
amsr2: 0
amsua: 0
amsua_n15: 0
avhrr: 0
gmi: 1
hirs: 0
mhs: 0
seviri: 0
ssmis: 0
cris: 0
airs: 0
iasi: 0
```

### Timeseries:

```sh
python3 pyradmon_driver_timeseries.py [user_input_yaml]
```

1) Navigate to the repository root and load pyradmon:
   ```csh
   cd $NOBACKUP/pyradmon-project/pyradmon
   source load_radmon_config.csh
   ```
   
   **Note:** The load script automatically generates personalized timeseries input yamls:
   - `user_geosit_timeseries_input.yaml`
   - `user_m21c_timeseries_input.yaml`

2) Change to the timeseries source directory:
   ```sh
   cd $PYRADMON_TIMESERIES
   ```

3) (Optional) Edit the auto-generated user input yaml if you need to customize experiment settings, dates, output directories, or instruments:
   ```sh
   vi user_geosit_timeseries_input.yaml
   # or
   vi user_m21c_timeseries_input.yaml
   ```

4) Run pyradmon timeseries:
   ```sh
   python3 pyradmon_driver_timeseries.py user_geosit_timeseries_input.yaml
   # or
   python3 pyradmon_driver_timeseries.py user_m21c_timeseries_input.yaml
   ```

**Example user_input_yaml structure:**

All values within {}'s must be replaced by the user or are auto-populated by the load script.
- `{YYYYMMDD}` ~ 20190530
- `{path_to_pyradmon}` ~ Users local clone of pyradmon https://github.com/GEOS-ESM/pyradmon/tree/develop
- `{expid}` ~ e5303_m21c_jan18
- `{PYRADMON_TIMESERIES}` ~ the full path to the timeseries src directory (auto-set by load script)
- `{expname}` ~ can be anything, ex: m21c_radmon
- yaml file name ~ test_config_yaml_path.yaml

```yaml
# Section 1: Date Range
# ---------------------
startdate: 20200301 000000
enddate:  20200301 180000

# Section 2: Input Observation Data (directory paths) ~ *will be specific* to m2, geosit, m21c, and the expid (stream)
# --------------------------------------------------------------------------------------------------------------------
# M21C Specific
# -------------
expid: e5303_m21c_jan18
data_dirbase: /home/dao_ops/m21c/archive/e5303_m21c_jan18/obs
runbase: /home/dao_ops/e5303_m21c_jan18/run/
mstorage: /home/dao_ops/e5303_m21c_jan18/run/mstorage.arc 
arcbase: /home/dao_ops/m21c/archive/ 

# Section 3: Output Directories
# -----------------------------
expbase: {PYRADMON_TIMESERIES}/m21c_radmon/
scratch_dir: {PYRADMON_TIMESERIES}/m21c_radmon/scratch/
output_dir: {PYRADMON_TIMESERIES}/m21c_radmon/radmon/

# Section 4: rcfile is the path to this yaml file (the one you have open and are editing that will be used as the [user_input_yaml])
# ----------------------------------------------------------------------------------------------------------------------------------
rcfile: {PYRADMON_TIMESERIES}/test_config_yaml_path.tmpl.m21c.yaml 

# Section 5: (Optional) Specific instruments - one, multiple or all
# Optional ~ you may leave this commented out if you want to run for all. See the satlist.yaml for instrument list (ex: amsua_n15).
# ---------------------------------------------------------------------------------------------------------------------------------
instruments: atms_npp              # run one
#instruments: amsua_n15,amsua_n16  # run multiple - separate instruments by comma 
#instruments:                      # run all (leave commented out)

# Section 6: (Optional) Polar
# ---------------------------
#rename_date_dir: current
#scp_userhost: {user_id}@polar
#scp_path: /www/html/intranet/personnel/{user_id}/{dir}

# Section 7: (No edits) Pyradmon Pointer
# Section dao_ops version of pyradmon - scripts will point to this rather than the scripts in the locally installed/cloned pyradmon
# ---------------------------------------------------------------------------------------------------------------------------------
pyradmon: {PYRADMON_TIMESERIES}
  
# Section 8: (No edits) Default gsidiag exec and rc file
# ------------------------------------------------------
bin2txt_exec: /home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/bin/gsidiag_bin2txt.x
gsidiagsrc: /home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/etc/gsidiags.rc
```

---

## License

(C) Copyright 2021- United States Government as represented by the Administrator of the National Aeronautics and Space Administration. All Rights Reserved.

```
