#!/bin/csh
  set EXPID = $1 #'f5295_fp' # GEOS FP
  set Date = $2 #'yyymmdd'
  set hh = $3 #'yyymmdd'
  set pyradmon = $4 #'yyymmdd'
  
  source /home/dao_ops/$EXPID/run/FVDAS_Run_Config
  # setenv pyradmon /discover/nobackup/sicohen/RADMON/develop/pyradmon
  setenv FVWORK $pyradmon/offline/spatial/run
  
  /bin/mkdir -p $FVWORK/$EXPID/tmp             # create working directory
  /bin/cp -r $pyradmon/offline/spatial/src/* $FVWORK/$EXPID/tmp/.
  cd $FVWORK/$EXPID/tmp

  foreach hour ( 00 )
     set hour = '18'
     ./do_atms.csh $EXPID $Date $hour 
     ./do_amsr2.csh $EXPID $Date $hour 
     ./do_amsua.csh $EXPID $Date $hour 
     ./do_amsua_n15.csh $EXPID $Date $hour 
     ./do_avhrr.csh $EXPID $Date $hour 
     ./do_gmi.csh $EXPID $Date $hour 
     ./do_hirs.csh $EXPID $Date $hour 
     ./do_mhs.csh $EXPID $Date $hour 
     ./do_seviri.csh $EXPID $Date $hour 
     ./do_ssmis.csh $EXPID $Date $hour 
     ./do_cris.csh $EXPID $Date $hour
     ./do_airs.csh $EXPID $Date $hour 
     ./do_iasi.csh $EXPID $Date $hour 
  end


# move the completed run for given date to the $EXPID dir
mv $date $FVWORK/$EXPID/.
cd $FVWORK/$EXPID
echo $PWD
# remove the tmp working directory (duplicate of src)
# rm -rf $FVWORK/$EXPID/tmp
