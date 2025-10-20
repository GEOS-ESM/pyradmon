========
# pyradmon

</div>

Python Radiance Monitoring Tool. Contains both spatial and timeseries pyradmon.


The Radiance monitoring tool, `pyradmon`, has been overhauled after compatibility issues caused by the transition from SLES12 to SLES15. Most of the changes were the addition of python scripts for the front end and edits to make backend shell scripts work with the new python scripts. The edits on the backend were to only a few, albeit important, scripts. Backend python scripts were also edited slightly to account for changes to the directory structure within the repository and to account for updates to packages like matplotlib which were part of the issues during the OS transition. 

Returning users can expect the final outputs (plots) pyradmon produces to be the same as it did previously – plots should be formatted in the same style, etc. While pyradmon is running, users should expect to see similar – but different - output in the terminal. The location of the output images and .tar file will be in a different location – the .tar file will have the same structure as it did previously.

The current version of pyradmon: ~~(_version number?_):~~
- is working for both timeseries and spatial plotting.
- is a 'pointer' - the python wrappers _point_ to the backend scripts that are in `/home/dao_ops/pyradmon/` NOT the ones that are in the source directories in this repository. 

<!-- ~~Further explanation of the _'pointer'_ version and why it was made this way:~~ -->

More changes are being made to make it more flexible and user friendly. 

**Users should be careful not overwrite their initial source code of this repo when there is an update.**

</div>

# Installation and Environment Setup


Pyradmon is a package consisting of Python wrappers (drivers) that take user created yamls as input on the front end and a combination of python, shell, and perl scripts on the backend. 

Once setup is complete users will use, or interact with, **5 files** when running `pyradmon`: **3 scripts and 2 yamls.**
-	One .sh script for loading pyradmon
-	Two python scripts ~ one for running pyradmon timeseries & one for running pyradmon spatial
-	Two yaml files ~ one for running pyradmon timeseries & one for running pyradmon spatial

### First time installing pyradmon:
Clone pyradmon to wherever you want to live, for example:

### Make sure you are cloning/using the *feature/dao-ops-pointer* branch (temporary until merged with main)
```sh
cd $NOBACKUP
mkdir -p radmon && cd radmon
git clone -b feature/dao-ops-pointer https://github.com/GEOS-ESM/pyradmon.git pyradmon-dao-ops-pointer
cd $NOBACKUP/radmon/pyradmon-dao-ops-pointer
```
<!-- 
This will be for after the feature/dao-ops-pointer branch has been merged to the main branch


~~mkdir -p radmon && cd radmon~~
~~git clone https://github.com/GEOS-ESM/pyradmon.git pyradmon~~
~~cd pyradmon~~ -->
<!-- 
After running the venv steps above, from now on use `load_radmon_config.sh` to load and activate the pyradmon virtual environment. It contains the line `source .venv/radmon_sles15_venv/bin/activate.csh` and defines other environment variables that will be used by the pyradmon scripts. There should be no need to edit `load_radmon_config.sh` unless you need to change which `activate` line for your shell.
 -->

<!-- 
#### Part 1: virtual environment

1) Switch to your folder where pyradmon is cloned: `cd $NOBACKUP/radmon/pyradmon-dao-ops-pointer`.
2) Create a Python virtual environment: `python3 -m venv .venv`
3) Activate the virtual environment - this step will vary depending on the shell you're using. 
  - `source .venv/bin/activate`
  - `source .venv/bin/activate.csh` for csh users 
4) Install pyradmon dependencies `pip install -r requirements.txt`
5) (_Optional_) Deactivate the virtual environment: `deactivate`

#### Part 2: Load pyradmon (virtual environment & environment variables)

 You will no longer need to activate your virtual environment directly. 
 
 From now on, in order to load `pyradmon` you must use the appropriate `load_radmon_config.*sh` script. These scripts runs the `source .venv/bin/activate` command for activating your virtual environment and sets environment variables that the `pyradmon` scripts will use.

6) Load with the appropriate `load_radmon_config` script: `source load_radmon_config.csh` -->

<!-- 2) Load all the modules that pyradmon needs: `mod_load_pyradmon` (this is the `bash` function created in the preliminary steps) -->

#### Load pyradmon (virtual environment & environment variables)

 You will no longer need to create or activate your virtual environment directly. 
 
 From now on, in order to load `pyradmon` you must use the appropriate `load_radmon_config.*sh` script. These scripts runs the command for activating loading the `g5_modules` and sets environment variables that the `pyradmon` scripts will use.

0) Load with the appropriate `load_radmon_config` script: `source load_radmon_config.csh`

# How to run

## Spatial: 

```sh
python3 pyradmon_driver_spatial.py [user_input_yaml]
```

1) Load with the appropriate `load_radmon_config` `source load_radmon_config.csh` this well set $pyradmon 
2) Change directory: `cd $pyradmon/offline/spatial/src`
3) Create the `user_input_yaml` by copying the existing example yaml. You may name the yaml file whatever you like: `cp test_config.geosfp.yaml user_input_yaml.yaml`
4) Open and edit yaml to the experiment and dates you wish to run pyradmon for. Set the Obs Types switches to `1 for ON` and `0 for OFF`
5) Run pyradmon spatial: `python3 pyradmon_driver_spatial.py user_input_yaml.yaml`

#### Example user_input_yaml: `test_config.geosfp.yaml`:

The example will only run pyradmon spatial for gmi.

```
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

pyradmon should be the full path to the users local clone of pyradmon: {userid}/.../pyradmon


## Timeseries: 

```sh
python3 pyradmon_driver_timeseries.py [user_input_yaml]
```


1) Change directory: `cd $NOBACKUP/radmon/pyradmon-dao-ops-pointer/offline/timeseries/src`
2) Load with the appropriate `load_pyradmon_config` `source $NOBACKUP/radmon/pyradmon-dao-ops-pointer/load_pyradmon_config.csh`
3) Create the `user_input_yaml` by copying the existing example yaml. You may name the yaml file whatever you like: `cp test_config.geosfp.yaml user_input_yaml.yaml`
4) Open and edit yaml to manually make the changes described below under _Timeseries yaml instructions_. 
5) Run pyradmon timeseries: `python3 pyradmon_driver_timeseries.py user_input_yaml.yaml`

User only needs to edit/make the configuration yaml file that is used in the command above. No other edits should be needed. To do so follow instructions below.

The timeseries yaml `[user_input_yaml]` requires a number of changes that must be made manually.

## Timeseries yaml instructions:

It is recommended you attempt `Option 1` below and successfully run pyradmon timeseries with it before attempting `Option 2`.

### Option 1: Yaml configs for M21C & GEOSIT:
Templates with proper pyradmon configuration for **m21c e5303_m21c_jan18** and **geosit d5294_geosit_jan18**. Change all instances of `{user_id}` to the value produced by running `echo $user`:
  - offline/timeseries/src/test_config_yaml_path.tmpl.geosit.yaml
  - offline/timeseries/src/test_config_yaml_path.tmpl.m21c.yaml

### Option 2: Construction your own yaml config:

All values within {}'s must be replaced by the user. The yaml should not have any brackets left once edits are completed.

IMPORTANT: The example is running pyradmon timeseries for M21C. _*Section 2: Input Observation Data (directory paths) will be specific to m2, geosit, m21c, AND the stream (expid)*_. The user may need to edit the entire path for the Section 2 variables not just the {}'s.


```
# From test_config_yaml_path.skeleton.yaml:
# -----------------------------------------

    """
    # Section 0: Variable descriptions
    # --------------------------------
    {YYYYMMDD} ~ 20190530
    {HH} ~ 00
    {path_to_pyradmon} ~ Users local clone of pyradmon 
    {expid} ~ e5303_m21c_jan18
    yaml file name ~ test_config_yaml_path.yaml
    """
    # --------------------------------


    
    # Section 1: Date Range
    # ---------------------
    startdate: {YYYYMMDD} {HH}0000
    enddate:  {YYYYMMDD} {HH}0000

    # Section 2: Input Observation Data (directory paths) ~ *will be specific* to m2, geosit, m21c, and the expid (stream)
    # --------------------------------------------------------------------------------------------------------------------
    expid: {expid}
    data_dirbase: /home/dao_ops/m21c/archive/{expid}/obs
    runbase: /home/dao_ops/{expid}/run/
    mstorage: /home/dao_ops/{expid}/run/mstorage.arc
    arcbase: /home/dao_ops/m21c/archive/ 

    # Section 3: Output Directories
    # -----------------------------
    expbase: /discover/nobackup/{user_id}/radmon/pyradmon-dao-ops-pointer/offline/timeseries/src/m21c_radmon
    scratch_dir: /discover/nobackup/{user_id}/radmon/pyradmon-dao-ops-pointer/offline/timeseries/src/m21c_radmon/scratch
    output_dir: /discover/nobackup/{user_id}/radmon/pyradmon-dao-ops-pointer/offline/timeseries/src/m21c_radmon/radmon

    # Section 4: rcfile is the path to this yaml file (the one you have open and are editing that will be used as the [user_input_yaml])
    # ----------------------------------------------------------------------------------------------------------------------------------
    rcfile: /discover/nobackup/{user_id}/radmon/pyradmon-dao-ops-pointer/offline/timeseries/src/user_input_yaml.yaml

    # Section 5: (Optional) Specific instruments - one, multiple or all
    # Optional ~ you may leave this commented out if you want to run for all. See the satlist.yaml for instrument list (ex: amsua_n15).
    # ---------------------------------------------------------------------------------------------------------------------------------
    #instruments: amsua_n15            # run one
    #instruments: amsua_n15,amsua_n16  # run multiple - separate instruments by comma 
    #instruments:                      # run all

    # Section 6: (Optional) Polar
    # ---------------------------
    #rename_date_dir: current
    #scp_userhost: {user_id}@polar
    #scp_path: /www/html/intranet/personnel/{user_id}/{dir}
  
    # Section 7: (No edits) Pyradmon Pointer
    # Section dao_ops version of pyradmon - scripts will point to this rather than the scripts in the locally installed/cloned pyradmon
    # ---------------------------------------------------------------------------------------------------------------------------------
    pyradmon: /home/dao_ops/pyradmon/

      
    # Section 8: (No edits) Default gsidiag exec and rc file
    # ------------------------------------------------------
    bin2txt_exec: /home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/bin/gsidiag_bin2txt.x
    gsidiagsrc: /home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/etc/gsidiags.rc


```


#### Description and expected values for {variable}'s:
- pyradmon will create a new directory using the value of `{expname}` in the timeseries src directory.
- This new directory will contain 3 subdirectories: `{expid}`, `radmon`, and `scratch`. All the output from pyradmon as well as the temporary files it creates and deletes (plotting yamls,...) get placed in these subdirectories.
- The `{expid}` directory will contain: Obs data diag txt files used for plotting organized by date - {expname}/{expid}/obs/Y%Y/M%m/D%d/H%H/
- The `radmon` directory will contain: Plots and tar archive of plots
- The `scratch` directory will contain: temporary files pyradmon creates, uses, and deletes (plotting yamls,...)
- *Optional*: User may edit these but is not required to do in order to run pyradmon. See the `satlist.yaml` for instrument list if you wish to use this option.
- *Polar* : Only for those who wish to run `online version of pyradmon`. Leave commented out or fill in your discover & polar information and uncomment.


</div> 
</div>

### License:

(C) Copyright 2021- United States Government as represented by the Administrator of the National
Aeronautics and Space Administration. All Rights Reserved.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)





</div> 
</div>


<!-- Part 2: extra steps for loading pyradmon

2) Load pyradmon, `mod_pyradmon` you can either create the following function or use the command directly:
```bash
mod_pyradmon() {
  module purge
  source $NOBACKUP/radmon/pyradmon-dao-ops-pointer/load_pyradmon_config.sh
}
```
This can be put in `~/.bashrc` to ensure it is always active every time the user logins to Discover or in an alternate location, such as `~/.bash_functions` but the user needs to activate these functions via `source ~/.bash_functions`. -->

<!-- 
To find the appropriate activate script run the following:
```sh
ls .venv/radmon_sles15_venv/bin/activate*
``` -->

<!-- Now activate the virtual environment by running the following (change 'activate.csh' to the appropriate script you just found for your shell):
```sh
source .venv/radmon_sles15_venv/bin/activate.csh
```

Install the dependencies from the requirements.txt file by running:
```sh
python3 -m pip install -r requirements.txt
``` -->
<!-- 

It is encouraged to use a virtual environment; however, you may choose to not use one. If you do you will have to locate all the references to the *'ACTIVATE_VENV'* variable, which will be explained later, and change them - this will end up being more time consuming. 



    """
    # Section 0: Variable descriptions
    # --------------------------------
    {YYYYMMDD} ~ 20190530
    {HH} ~ 00
    {path_to_pyradmon} ~ Users local clone of pyradmon 
    {expid} ~ e5303_m21c_jan18
    {timeseries_src_dir} ~ the full path to the directory src directory (i.e. /discover/nobackup/{user_id}/radmon/pyradmon-dao-ops-pointer/offline/timeseries/src)
    yaml file name ~ test_config_yaml_path.yaml
    """
-->
