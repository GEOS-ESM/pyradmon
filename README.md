
========
# pyradmon

Python Radiance Monitoring Tool. Contains both spatial and timeseries pyradmon.



### Installation and Environment Setup

Clone the repo. 
### Make sure you are cloning/using the *develop* branch (temporary)
```sh
$ git clone -b develop https://github.com/GEOS-ESM/pyradmon.git
$ cd pyradmon
```


Next, create virtual environment using venv - or any other preferred method; however, this will only cover venv.
The venv name is arbitrary but it is encouraged to keep the name as is because the repo is fragile at the moment.

```sh
$ python3 -m venv .venv/radmon_sles15_venv
```

Note you may have to change this to match the shell you're using. Look at the other 'activate' scripts in .venv/bin/ 

To find the appropriate activate script run the following:
```sh
$ ls .venv/radmon_sles15_venv/bin/activate*
```

Now activate the virtual environment by running the following (change 'activate.csh' to the appropriate script you just found for your shell):
```sh
$ source .venv/radmon_sles15_venv/bin/activate.csh
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


#


## How to run

### Spatial


### Timeseries
1. cd to .../pyradmon/offline/timeseries/src
2. Copy test_config_yaml_path.skeleton.yaml to test_config_yaml_path.tmpl.yaml
3. Open test_config_yaml_path.tmpl.yaml and make the necessary edits (everything in {}'s)
4. python3 pyradmon_driver_offline.py test_config_yaml_path.tmpl.yaml

</div>


</div>

### Licence:

(C) Copyright 2021- United States Government as represented by the Administrator of the National
Aeronautics and Space Administration. All Rights Reserved.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


### Description:


Python Radiance Monitoring Tool. Contains both spatial and timeseries pyradmon.


