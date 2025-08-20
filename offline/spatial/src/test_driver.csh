#!/bin/csh
  set Date = '20230214'
  #set EXPID = 'd5294_geosit_jan18' # GEOS-IT
  #source /home/dao_ops/d5294_geosit_jan18/run/FVDAS_Run_Config #.SLES15
  set EXPID = 'f5295_fp' # GEOS FP
  
  source /home/dao_ops/f5295_fp/run/FVDAS_Run_Config
  
  #module purge
  #source /discover/nobackup/sicohen/RADMON/venvs/radmon_sles15_venv/bin/activate.csh
  #source /discover/nobackup/sicohen/RADMON/develop/pyradmon/.venvs/radmon_sles15_venv/bin/activate.csh
  #module load python/l
  #setenv G5MODULES "GEOSenv comp/gcc/10.1.0 comp/intel/2021.2.0 mpi/impi/2021.2.0 python/GEOSpyD/Min4.8.3_py2.7"
  #source $FVROOT/bin/g5_modules
  setenv PYRADMON /discover/nobackup/sicohen/RADMON/develop/pyradmon/offline/spatial
  setenv FVWORK /discover/nobackup/sicohen/RADMON/develop/pyradmon/offline/spatial/run
                    # /discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/fvwork.RADMON
  
#  /bin/rm -rf $FVWORK
  /bin/mkdir -p $FVWORK/$EXPID/tmp             # create working directory
  /bin/cp -r /discover/nobackup/sicohen/RADMON/develop/pyradmon/offline/spatial/src/* $FVWORK/$EXPID/tmp/.
  cd $FVWORK/$EXPID/tmp
  #rm -rf do_*

  foreach hour ( 00 )1
     #set hour = '18'
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
# remove the tmp working directory (duplicate of src)
rm -rf $FVWORK/$EXPID/tmp
