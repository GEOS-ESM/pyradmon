
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


It is encouraged to use a virtual environment; however, you may choose to not use one. If you do you will have to locate all the references to the *'ACTIVATE_VENV'* variable, which will be explained later, and change them - this will end up being more time consuming. 


#


## How to run

### Spatial


### Timeseries
1. Open a txt file with a text editor (Notepad, Word, Stickies, etc.) on your laptop 
2. cd to offline/timeseries/src 
3. Run `echo $PWD` , copy the resulting path and paste it to the text file
4. Copy test_config_yaml_path.skeleton.yaml to test_config_yaml_path.tmpl.yaml
5. Open test_config_yaml_path.tmpl.yaml and make the necessary edits (All the placeholders in {}'s, including the brackets). Recommend that you use find and replace (ctrl-F).
6. Replace the `{{YYYYMMDD}` values for the start and end dates of the period you want
8. Replace all instances of `{expid}` with the `experiment id` of the data you want to plot (< how to say this the right way?) - for example you could put: `e5303_m21c_jan18`. Note that this is not an arbitrary value.
9. Replace all instances of `{timeseries_src_dir} ` with the path you saved from step 3
10. Replace all instances of `{expname}` with a name of your choosing for your working directory -

Note: 
- pyradmon will create a new directory using the value of `{expname}` in the timeseries_src_dir.
- This new directory will contain 3 subdirectories: `{expid}`, `radmon`, and `scratch`. All the output from pyradmon as well as the temporary files it creates and deletes (plotting yamls,...) get placed in these subdirectories.
- The `{expid}` directory will contain: Obs data diag txt files used for plotting organized by date - {expname}/{expid}/obs/Y%Y/M%m/D%d/H%H/
- The `radmon` directory will contain: Plots and tar archive of plots
- The `scratch` directory will contain: temporary files pyradmon creates, uses, and deletes (plotting yamls,...) 

11. python3 pyradmon_driver_offline.py test_config_yaml_path.tmpl.yaml
12. 
</div>


When finished using pyradmon you may deactivate the virtual environment by running:
```sh
$ deactivate
```

</div>

### Licence:

(C) Copyright 2021- United States Government as represented by the Administrator of the National
Aeronautics and Space Administration. All Rights Reserved.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


### Description:


Python Radiance Monitoring Tool. Contains both spatial and timeseries pyradmon.


