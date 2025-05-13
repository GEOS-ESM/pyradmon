#!/bin/csh
  set date = '20230214'


  #set EXPID = 'd5294_geosit_jan18' # GEOS-IT
  #source /home/dao_ops/d5294_geosit_jan18/run/FVDAS_Run_Config #.SLES15
  set EXPID = 'f5295_fp' # GEOS FP
  source /home/dao_ops/f5295_fp/run/FVDAS_Run_Config
  
  #module purge
  #source /discover/nobackup/sicohen/RADMON/venvs/radmon_sles15_venv/bin/activate.csh
  #module load python/l
  #setenv G5MODULES "GEOSenv comp/gcc/10.1.0 comp/intel/2021.2.0 mpi/impi/2021.2.0 python/GEOSpyD/Min4.8.3_py2.7"
  #source $FVROOT/bin/g5_modules
  
  setenv FVWORK /discover/nobackup/sicohen/RADMON/work/aelakkra-sic/fvwork.RADMON 
                    # /discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/fvwork.RADMON
  
  /bin/rm -rf $FVWORK
  /bin/mkdir -p $FVWORK             # create working directory
  /bin/cp -r /discover/nobackup/sicohen/RADMON/work/aelakkra-sic/clean_plots $FVWORK
  cd $FVWORK/clean_plots
  
  foreach hour ( 00 )
     #set hour = '18'
     ./do_atms.csh $EXPID $date $hour 
     #./do_amsr2.csh $EXPID $date $hour 
     #./do_amsua.csh $EXPID $date $hour 
     #./do_amsua_n15.csh $EXPID $date $hour 
     #./do_avhrr.csh $EXPID $date $hour 
     #./do_gmi.csh $EXPID $date $hour 
     #./do_hirs.csh $EXPID $date $hour 
     #./do_mhs.csh $EXPID $date $hour 
     #./do_seviri.csh $EXPID $date $hour 
     #./do_ssmis.csh $EXPID $date $hour 
     #./do_cris.csh $EXPID $date $hour
     #./do_airs.csh $EXPID $date $hour 
     #./do_iasi.csh $EXPID $date $hour 
  end
