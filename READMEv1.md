
========
# pyradmon

Python Radiance Monitoring Tool. Contains both spatial and timeseries pyradmon.

The Radiance monitoring tool, `pyradmon`, has been overhauled after compatibility issues caused by the transition from SLES12 to SLES15. Most of the changes were the addition of python scripts for the front end and edits to make backend shell scripts work with the new python scripts. The edits on the backend were to only a few, albeit important, scripts. Backend python scripts were also edited slightly to account for changes to the directory structure within the repository and to account for updates to packages like matplotlib which were part of the issues during the OS transition. 

Returning users can expect the final outputs (plots) pyradmon produces to be the same as it did previously – plots should be formatted in the same style, etc. While pyradmon is running, users should expect to see similar – but different - output in the terminal. The location of the output images and .tar file will be in a different location – the .tar file will have the same structure as it did previously.

/
The current version of pyradmon (version number?):
- is working for both timeseries and spatial plotting.
- is a 'pointer' - the python wrappers _point_ to the backend scripts that are in /home/dao_ops/pyradmon/ NOT the ones that are in the source directories in this repository. 

Further explination of the _'pointer'_ version and why it was made this way:


More changes are being made to make it more flexible and user friendly. 

**Users should be careful not overwrite their initial source code of this repo when there is an update.**


### Installation and Environment Setup


Pyradmon is a package consisting of Python wrappers that take user created yamls as input on the front end and a combination of python, shell, and perl scripts on the backend. 

Once setup is complete users will use, or interact with, **5 files** when running `pyradmon`: **3 scripts and 2 yamls.**
-	1 .sh script for loading pyradmon
-	2 python scripts ~ one for running pyradmon timerseries & one for running pyradmon spatial
-	2 yaml files ~ one for running pyradmon timerseries & one for running pyradmon spatial



### First time installing pyradmon:
Clone pyradmon to wherever you want to live, for example:

### Make sure you are cloning/using the *feature/dao-ops-pointer* branch (temporary until merged with main)
```sh
cd $NOBACKUP
mkdir -p radmon && cd radmon
git clone -b feature/dao-ops-pointer https://github.com/GEOS-ESM/pyradmon.git pyradmon-dao-ops-pointer
cd $NOBACKUP/radmon/pyradmon-dao-ops-pointer
```

~~mkdir -p radmon && cd radmon~~
~~git clone https://github.com/GEOS-ESM/pyradmon.git pyradmon~~
~~cd pyradmon~~



Part 1: virtual environment

1) Switch to your folder where pyradmon is cloned: `cd $NOBACKUP/radmon/pyradmon-dao-ops-pointer`.
2) Load all the modules that pyradmon needs: `mod_load_pyradmon` (this is the `bash` function created in the preliminary steps)
3) Create a Python virtual environment: `python3 -m venv .venv`
4) Activate the virtual environment - this step will vary depending on the shell you're using. 
  - `source .venv/bin/activate`
  - `source .venv/bin/activate.csh` for csh users 
5) Install pyradmon dependencies `pip install -r requirements.txt`
6) (_Optional_) Deactivate the virtual environment: `deactivate`

 You will no longer need to activate your virtual environment directly. 
 
 From now on, in order to load `pyradmon` you must use the appropriate `load_radmon_config.*sh` script. These scripts runs the `source .venv/bin/activate` command for activating your virtual environment and sets environment variables that the `pyradmon` scripts will use.

7) Load with the appropriate `load_pyradmon_config` script: `source $NOBACKUP/radmon/pyradmon-dao-ops-pointer/load_pyradmon_config.csh`

<!-- Part 2: 

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

It is encouraged to use a virtual environment; however, you may choose to not use one. If you do you will have to locate all the references to the *'ACTIVATE_VENV'* variable, which will be explained later, and change them - this will end up being more time consuming.  -->


#


## How to run

### Spatial: 

```sh
python3 pyradmon_driver_spatial.py [user_input_yaml]
```


1) Change directory: `cd $NOBACKUP/radmon/pyradmon-dao-ops-pointer/offline/spatial/src`
2) Load with the appropriate `load_pyradmon_config` `source $NOBACKUP/radmon/pyradmon-dao-ops-pointer/load_pyradmon_config.csh`
3) Create the `user_input_yaml` by copying the existing example yaml. You may name the yaml file whatever you like. : `cp test_config.geosfp.yaml user_input_yaml.yaml`
4) Open and edit yaml to the experiment and dates you wish to run pyradmon for. 
5) Run pyradmon spatial: `python3 pyradmon_driver_spatial.py user_input_yaml.yaml`

# Example user_input_yaml: `test_config.geosfp.yaml` 
```
expver: f5295_fp
yyyymmdd: '20231201'
hh: '18'
pyradmon: '$NOBACKUP/radmon/pyradmon-dao-ops-pointer'
```

pyradmon should be the full path to the users local clone of pyradmon: {userid}/.../pyradmon


### Timeseries: 

```sh
python3 pyradmon_driver_timeseries.py [user_input_yaml]
```


1) Change directory: `cd $NOBACKUP/radmon/pyradmon-dao-ops-pointer/offline/timeseries/src`
2) Load with the appropriate `load_pyradmon_config` `source $NOBACKUP/radmon/pyradmon-dao-ops-pointer/load_pyradmon_config.csh`
3) Create the `user_input_yaml` by copying the existing example yaml. You may name the yaml file whatever you like. : `cp test_config.geosfp.yaml user_input_yaml.yaml`
4) Open and edit yaml to manually make the changes described below under _Timeseries yaml instructions_. 
5) Run pyradmon timeseries: `python3 pyradmon_driver_timeseries.py user_input_yaml.yaml`

User only needs to edit/make the configuration yaml file that is used in the command above. No other edits should be needed. To do so follow instructions below.

The timeseries yaml requires a number of changes that must be made manually.

#### Timeseries yaml instructions:

All values within {}'s must be replaced by the user. The yaml should not have any brackets left once edits are completed.

IMPORTANT: The example is running pyradmon timeseries for M21C. _*Section 2: Input Observation Data (directory paths) will be specific to m2, geosit, m21c, AND the stream (expid)*_. The user may need to edit the entire path for the Section 2 variables not just the {}'s.

Templates with proper pyradmon configuration for **m21c e5303_m21c_jan18** and **geosit d5294_geosit_jan18**. Change all instances of `{user_id}` to the value produced by running `echo $user`

```sh
  - offline/timeseries/src/test_config_yaml_path.tmpl.geosit.yaml
  - offline/timeseries/src/test_config_yaml_path.tmpl.m21c.yaml
```

```
    
    {YYYYMMDD} ~ 20190530
    {HH} ~ 00
    {path_to_pyradmon} ~ Users local clone of pyradmon 
    {expid} ~ e5303_m21c_jan18
    {timeseries_src_dir} ~ the full path to the directory src directory (i.e. /discover/nobackup/{user_id}/radmon/pyradmon-dao-ops-pointer/offline/timeseries/src)
    yaml file name ~ test_config_yaml_path.yaml
    
    # Section 1: Date Range
    startdate: {YYYYMMDD} {HH}0000
    enddate:  {YYYYMMDD} {HH}0000

    # Section 2: Input Observation Data (directory paths)
    ## Input data directories *will be specific* to m2, geosit, m21c, and the stream (expid)
    expid: {expid}
    data_dirbase: /home/dao_ops/m21c/archive/{expid}/obs
    runbase: /home/dao_ops/{expid}/run/
    mstorage: /home/dao_ops/{expid}/run/mstorage.arc
    arcbase: /home/dao_ops/m21c/archive/ 

    # Section 3: Output Directories
    expbase: /discover/nobackup/{user_id}/radmon/pyradmon-dao-ops-pointer/offline/timeseries/src/m21c_radmon
    scratch_dir: /discover/nobackup/{user_id}/radmon/pyradmon-dao-ops-pointer/offline/timeseries/src/m21c_radmon/scratch
    output_dir: /discover/nobackup/{user_id}/radmon/pyradmon-dao-ops-pointer/offline/timeseries/src/m21c_radmon/radmon

    # Section 4: rcfile is the path to this yaml file (the one you have open and are editing that will be used as the [user_input_yaml])
    rcfile: /discover/nobackup/{user_id}/radmon/pyradmon-dao-ops-pointer/offline/timeseries/src/user_input_yaml.yaml #{yaml file name} 

    # Section 5: (Optional) Specific instruments - one, multiple or all
    # Optional ~ you may leave this commented out if you want to run for all. See the satlist.yaml for insturment list (ex: amsua_n15).
    #instruments: amsua_n15            # run one
    #instruments: amsua_n15,amsua_n16  # run multiple - seperate instruments by comma 
    #instruments:                      # run all

    # Section 6: Polar
    #rename_date_dir: current
    #scp_userhost: {user_id}@polar
    #scp_path: /www/html/intranet/personnel/{user_id}/{dir}

```

#### Instructions:
1. Open a txt file with a text editor (Notepad, Word, Stickies, etc.) on your laptop 
2. cd to offline/timeseries/src 
3. Run `echo $PWD` , copy the resulting path and paste it to the text file
4. Copy test_config_yaml_path.skeleton.yaml to test_config_yaml_path.tmpl.yaml
5. Open test_config_yaml_path.tmpl.yaml and make the necessary edits (All the placeholders in {}'s, including the brackets). Recommend that you use find and replace (ctrl-F).
6. Replace the `{YYYYMMDD}` values for the start and end dates of the period you want
7. ~~Replace `{path_to_pyradmon}` with the path to the local clone of pyradmon ~ ex. `path/to/local/pyradmon/`~~ Leave pyradmon set to /home/dao_ops/pyradmon/ for this 'pointer' branch - *it is pointing to /home/dao_ops/pyradmon/ rather being self contained*
8. Replace all instances of `{expid}` with the `experiment id` of the data you want to plot (< how to say this the right way?) - for example you could put: `e5303_m21c_jan18`. Note that this is not an arbitrary value.
9. Replace all instances of `{timeseries_src_dir} ` with the path you saved from step 3
10. Replace place all instances of `{expname}` with a name of your choosing for your working directory - this is an arbitrary value ex. `sicohen_m21c_radmon` or `m21_radmon`
11. At the bottom of the yaml file are other fields which were not edited in the previous steps:
- *Default Values*: Do not edit the *Default Values* unless you are certain of the implications.
- *Optional*: User may edit these but is not required to do in order to run pyradmon. See the `satlist.yaml` for insturment list if you wish to use this option.
- *Polar* : Only for those who wish to run `online version of pyradmon`. Leave commented out or fill in your discover & polar information and uncomment.

#### Description and expected values for {variable}'s:
- pyradmon will create a new directory using the value of `{expname}` in the timeseries_src_dir.
- This new directory will contain 3 subdirectories: `{expid}`, `radmon`, and `scratch`. All the output from pyradmon as well as the temporary files it creates and deletes (plotting yamls,...) get placed in these subdirectories.
- The `{expid}` directory will contain: Obs data diag txt files used for plotting organized by date - {expname}/{expid}/obs/Y%Y/M%m/D%d/H%H/
- The `radmon` directory will contain: Plots and tar archive of plots
- The `scratch` directory will contain: temporary files pyradmon creates, uses, and deletes (plotting yamls,...)
- See `test_config_yaml_path.example.yaml` for an example

  Once all edits to the yaml file are complete, pyradmon will be ready to run.
  You may change the name of the new yaml file you've created if you wish.
  

11. Run pyradmon in the command line with:
```sh
python3 pyradmon_driver_offline.py test_config_yaml_path.tmpl.yaml
```

</div> 



</div>


When finished using pyradmon you may deactivate the virtual environment by running:
```sh
deactivate
```

</div>

### Licence:

(C) Copyright 2021- United States Government as represented by the Administrator of the National
Aeronautics and Space Administration. All Rights Reserved.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


### Description:


Python Radiance Monitoring Tool. Contains both spatial and timeseries pyradmon.

