Introduction
============
Included here is the pyradmon_driver.pl script which runs the pyradmon package for for a time range for all or a subset of instruments.


Prior to running the script:
---------------------------
You must first build the gsidiag_bin2txt.x executable in the pyradmon/gsidiag/gsidiag_bin2txt directory. See the README.md file in that directory for build information.


To run pyradmon package:
-----------------------
> ./pyradmon_driver.pl rcfile

Look at radmon-f525_p6_fpp.20200501.20200531.rc for a sample rcfile.


Alt run method #1:
-----------------
> ./pyradmon_driver.pl

If you call the script without a rcfile or any options, then the script will prompt you for all the information it needs and will then run the pyradmon package. The script will also write a rcfile for you in the output directory. You can use this to rerun the job, or you can modify the rcfile to rerun with a different combination of expid, date range, and instrument selection.

The naming format for the rcfile written by the script is: radmon-expid.startdate.enddate.rc


Alt run method #2:
-----------------
> ./pyradmon_driver.pl options

The information needed to run the script can be entered using command-line options. See the script usage information for available options.

Notes:
1. If some information is given with options, but not all, then the script will use default values for missing information whenever a default is available. It will prompt for missing information that does not have a default.
2. If the -i flag is given, then the script will prompt for all missing information regardless of the defaults.


Alt run method #3:
-----------------
> ./pyradmon_driver.pl rcfile options

If an rcfile is given along with command-line options, then the information entered with the options will take precedence over information in the rcfile.


radmon_process.config
---------------------
You can enter the FVROOT information here, but this is not necessary if the information is given either in the rcfile or as a command-line option.
