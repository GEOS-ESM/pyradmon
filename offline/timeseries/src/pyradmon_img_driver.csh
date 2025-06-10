#!/bin/csh



if ( $#argv > 1 || $#argv < 1 ) then
    echo "usage: pyradmon_driver.csh <experiment rc file>"
    echo "   example: ./pyradmon_driver.csh pyradmon_driver.example.rc"
    exit 99
endif

#set rcfile=$argv[1]

unset argv
setenv argv

#source radmon_process.config
source $ESMADIR/install/bin/g5_modules

#module load other/comp/gcc-4.6.3-sp1
#module load lib/mkl-13.0.1.117
#module load other/SIVO-PyD/spd_1.10.0_gcc-4.6.3-sp1

set data_dirbase=`$ESMADIR/install/bin/echorc.x -rc $rcfile data_dirbase`
set expid=`$ESMADIR/install/bin/echorc.x -rc $rcfile expid`
set expbase=`$ESMADIR/install/bin/echorc.x -rc $rcfile expbase`
set scratch_dir=`$ESMADIR/install/bin/echorc.x -rc $rcfile scratch_dir`
set output_dir=`$ESMADIR/install/bin/echorc.x -rc $rcfile output_dir`
set pyradmon_path=`$ESMADIR/install/bin/echorc.x -rc $rcfile pyradmon`
set startdate=`$ESMADIR/install/bin/echorc.x -rc $rcfile startdate`
set enddate=`$ESMADIR/install/bin/echorc.x -rc $rcfile enddate`

set rename_date_dir=`$ESMADIR/install/bin/echorc.x -rc $rcfile rename_date_dir`
if ($status != 0) set rename_date_dir=/dev/null

set scp_userhost=`$ESMADIR/install/bin/echorc.x -rc $rcfile scp_userhost`
if ($status != 0) set scp_userhost=/dev/null
set scp_path=`$ESMADIR/install/bin/echorc.x -rc $rcfile scp_path`
if ($status != 0) set scp_path=/dev/null



#set data_dirbase=$expbase/$expid

set startdate=$startdate[1]
set enddate=$enddate[1]

mkdir -p $scratch_dir

echo $data_dirbase

echo "Determining instruments for $expid from $startdate to $enddate.  This "
echo "  may take a while..."
set insts=`$ESMADIR/install/bin/echorc.x -rc $rcfile instruments`
if ($status != 0) then
   set insts=`$pyradmon_path/offline/timeseries/src/scripts/determine_inst.csh $data_dirbase $startdate $enddate`
   echo $pyradmon_path/offline/timeseries/src/scripts/determine_inst.csh $data_dirbase $startdate $enddate
endif

echo $insts
set syyyy = `echo $startdate |cut -b1-4`
set smm   = `echo $startdate |cut -b5-6`
set sdd   = `echo $startdate |cut -b7-8`
set shh   = "00z"

set eyyyy = `echo $enddate |cut -b1-4`
set emm   = `echo $enddate |cut -b5-6`
set edd   = `echo $enddate |cut -b7-8`
set ehh   = "18z"

set pyr_startdate="$syyyy-$smm-$sdd $shh"
set pyr_enddate="$eyyyy-$emm-$edd $ehh"

foreach inst ($insts) 
  echo $inst  
  if (-e $pyradmon_path/offline/timeseries/src/config/radiance_plots.$inst.yaml.tmpl) then
#    set configtmpl="$pyradmon_path/config/radiance_plots_emissbc.$inst.yaml.tmpl"
    set configtmpl="$pyradmon_path/offline/timeseries/src/config/radiance_plots.$inst.yaml.tmpl"
  else
#    set configtmpl="$pyradmon_path/config/radiance_plots_emissbc.yaml.tmpl"
    set configtmpl="$pyradmon_path/offline/timeseries/src/config/radiance_plots.yaml.tmpl"
  endif

  set configfile="$scratch_dir/$inst.$expid.$startdate.$enddate.plot.yaml"

  cp $configtmpl $configfile

  sed -i "s@>>>DATA_DIRBASE<<<@$expbase@g" $configfile
  sed -i "s/>>>STARTDATE<<</$pyr_startdate/g" $configfile 
  sed -i "s/>>>ENDDATE<<</$pyr_enddate/g" $configfile 
  sed -i "s/>>>EXPID<<</$expid/g" $configfile 
  sed -i "s@>>>OUTPUT_DIR<<<@$output_dir@g" $configfile 

  echo "Running PyRadMon for $inst from $pyr_startdate to $pyr_enddate"
  echo $configfile 
  echo $pyradmon_path/offline/timeseries/src/pyradmon.py
  $pyradmon_path/offline/timeseries/src/pyradmon.py --config-file $configfile plot --data-instrument-sat $inst
end

#echo '----------------------------------'
#echo $output_dir
#cd $output_dir
#echo $expid
echo '----------------------------------'

if ($rename_date_dir != '/dev/null') mv $expid/$startdate-$enddate $expid/$rename_date_dir


echo "--------- saving .png's in $expid.tar  "
#echo $PWD
cd $expbase
tar cvf $expid.tar $expid/


echo "--------- removing img directory (contains loose .png's): ----  $expid"
# echo $expid
rm -rf $expid/
echo '--------------- checking for polar option -------------------'

if ($scp_userhost != '/dev/null' && $scp_path != '/dev/null') then 
   scp $expid.tar $scp_userhost\:$scp_path
   ssh $scp_userhost "cd $scp_path ; tar xvf $expid.tar"
endif
