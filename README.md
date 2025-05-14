
========
# pyradmon

Python Radiance Monitoring Tool. Contains both spatial and timeseries pyradmon.



### Installation and Environment Setup

Clone the repo.
```sh
$ git clone https://github.com/GEOS-ESM/pyradmon.git
$ cd pyradmon
```


Next, create virtual environment using venv - or any other preferred method; however, this will only cover venv.
The venv name is arbitrary but it is encouraged to keep the name as is because the repo is fragile at the moment.

```sh
$ python3 -m venv .venvs/radmon_sles15_venv
```

Note you may have to change this to match the shell you're using. Look at the other 'activate' scripts in .venv/bin/ 

To find the appropriate activate script run the following:
```sh
$ ls .venv/bin/activate*
```

Now activate the virtual environment by running the following (change 'activate.csh' to the appropriate script you just found for your shell):
```sh
$ source .venv/bin/activate.csh
```

Install the dependencies from the requirements.txt file by running:
```sh
$ python3 -m pip install -r requirements.txt
```


To deactivate the virtual environment simply run:
```sh
$ deactivate
```

It is encouraged to use a virtual environment; however, you may choose to not use one. If you do you will have to locate all the references to the *'ACTIVATE_VENV'* variable, which will be explained later, and change them - this will end up being more time consuming. 


Now, run: 
```sh
$ echo $PWD
```
Copy the path and open the `.env_example` file. Paste the copied path into the line 15 PYRADMON_HOME_DIR = '$PWD'. Now check the path for ACTIVATE_VENV on line 16 - if necessary replace the existing value with the same command you used to activate the venv a few steps prior. While you have .env open take a minute to read through the comments at the top for possibly useful context.

#### After editing close .env_example, and make a copy named *.env*. In order to ensure your edits will be saved even if you update the repo the new copy MUST be named '.env'. 

#### Open `pyradmon_driver_offline_spatial.py` to see how pyradmon will use the two values in the .env to make the rest of the relative paths needed by the rest of the repo- **YOU WILL NOT NEED TO MAKE ANY EDITS TO THIS FILE EVER**. On line 49 note that pyradmon will, from now on, activate the virtual envirnoment itself. You will only need to manually run 'source .venv/bin/activate.csh' once during the initial setup (which you should already have completed). After setup is complete the pyradmon scripts will do this automatically.

* `pyradmon_driver_offline_timeseries.py`* *is still in progress but will act the same way when complete. ~ SC 5/13/2025*

#


## How to run

### Spatial


### Timeseries
1. cd to .../pyradmon/offline/timeseries/src
2. Copy test_config_yaml_path.skeleton.yaml to test_config_yaml_path.tmpl.yaml
3. Open test_config_yaml_path.tmpl.yaml and make the necessary edits (everything in {}'s)
4. python3 pyradmon_driver_offline.py test_config_yaml_path.tmpl.yaml

</div>

### Licence:

(C) Copyright 2021- United States Government as represented by the Administrator of the National
Aeronautics and Space Administration. All Rights Reserved.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


### Description:

Software infrastructure for deploying cycling workflow for coupled data assimilation applications
using a workflow manager and scheduler.

### Documentation

Documentation for swell, which includes installation instructions, can be found at <a href="https://geos-esm.github.io/" target="_blank">https://geos-esm.github.io/</a>.
