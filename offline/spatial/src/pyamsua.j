#!/bin/csh -fx
#PBS -N RADMON
#SBATCH --job-name=RADMON
#PBS -l walltime=2:00:00
#SBATCH --time=2:00:00
#SBATCH --partition=compute
#SBATCH --constraint=hasw
##PBS -S /bin/tcsh
##PBS -r n
##PBS -j oe
#PBS -o /discover/nobackup/dao_ops/intermediate/SLURM/spool/%j.out
#SBATCH --output=/discover/nobackup/dao_ops/intermediate/SLURM/spool/%j.out
##PBS -W group_list=g2538
#SBATCH -A g2538
# To transfer previously generated plots:
#
# sbatch --partition=datamove --export=JOB_LOC="$FVHOME/run",date="20040501",push="only" --time=1:00:00 --ntasks=1 pyradmon.j
# To generate plots:
# sbatch --ntasks=1 --export=JOB_LOC="$FVHOME/run",date="20040501",push="qsub" pyradmon.j
  if ( ! $?SLURM_JOB_ID ) then
      set JOB_LOC = $1
      set date = $2
      set push = $3
  endif

  source $JOB_LOC/FVDAS_Run_Config
  setenv GROUP g2538
  umask 022
  @ exit_status = 0
  set queue_name = "RAQ"
  set ERR = "${FVROOT}/bin/Err_Log.pl -N ${EXPID}.job -I ops -X ${EXPID} -L DEFAULT"
  printenv


  if ( $?push ) then
       set rem_push = $push
  else
       set rem_push = "only"
  endif
  echo "rem_push = $rem_push"

# Create canary job script in FVHOME/run
# --------------------------------------
       if ( $rem_push == "qsub" ) set queue_name = "RAQ"
       if ( $rem_push == "only" ) set queue_name = "RAO"
   if ( $rem_push == "qsub" ) then 
       echo "sbatch -N 1  --export=JOB_LOC=$FVHOME/run,date=$date,push="$rem_push" --output=/discover/nobackup/dao_ops/intermediate/SLURM/spool/%j.out /home/dao_ops/operations/new_pyradmon_spatial/clean_plots/pyradmon.j" >! ${FVHOME}/run/pyradmon.${date}.j
       chmod a+x ${FVHOME}/run/pyradmon.${date}.j
       ls -l  ${FVHOME}/run/pyradmon.${date}.j
   endif

# Change queue name and set listing name
# ---------------------------------------
  if ( $?SLURM_JOB_ID ) then
     ${PBS_BIN}/qalter -N ${queue_name}.${date} $SLURM_JOB_ID
     set listing = `${FVROOT}/bin/token_resolve ${FVHOME}/etc/Y%y4/M%m2/pyradmon_spatial.${rem_push}.log.%y4%m2%d2 ${date}`
     ${PBS_BIN}/qalter -o ${listing}.${SLURM_JOB_ID}.FAILED ${SLURM_JOB_ID}
  endif

   if ( $rem_push == "qsub" ) then 
      $ERR -C 60 -E 0 -D "${EXPID} NOTICE: ${EXPID} pyradmon.${date}.j has started"
      setenv FVWORK /discover/nobackup/dao_ops/fvwork.$$
      /bin/rm -rf $FVWORK
      /bin/mkdir -p $FVWORK             # create working directory
      /bin/cp -r /home/dao_ops/operations/new_pyradmon_spatial/clean_plots $FVWORK
      cd $FVWORK/clean_plots
      foreach hour (00 06 12 18)
         ./do_amsua.csh $EXPID $date $hour &
      end
      wait
      if ( $status ) then
            set errmsg =  "${EXPID} pyradmon.${date}.j FATAL ERROR: plot generation failed "
            echo $errmsg
            $ERR -C 63 -E 5 -D "${errmsg}"
            exit 1
      endif
   set cmd = "sbatch -A "$GROUP" --export=JOB_LOC=$FVHOME/run,date=$date,push=only,oldfvwork=${FVWORK} --partition=datamove --output=/discover/nobackup/dao_ops/intermediate/SLURM/spool/%j.out /home/dao_ops/operations/new_pyradmon_spatial/clean_plots/pyradmon.j"
       echo $cmd
       echo $cmd  >! ${FVHOME}/run/pyradmon.${date}.j
       chmod a+x ${FVHOME}/run/pyradmon.${date}.j
       ls -l  ${FVHOME}/run/pyradmon.${date}.j
       $cmd
   endif
   if ( $rem_push == "only" ) then 
      set FVWORK = ${oldfvwork} 
      cd $FVWORK/clean_plots
# Transfer images via rsync
      rsync -r ${date} dao_ops@polar:/radmon/radmon/${EXPID}/coverage
      if ( $status ) then
            set errmsg =  "${EXPID} pyradmon.${date}.j FATAL ERROR: rsync failed "
            echo $errmsg
            $ERR -C 63 -E 5 -D "${errmsg}"
            exit 1
      endif
      /bin/rm -rf $FVWORK
      /bin/rm -f ${FVHOME}/run/pyradmon.${date}.j
      $ERR -C 64 -E 0 -D "${EXPID} NOTICE: pyradmon.${date}.j processing has completed successfully"
   endif
   if ( $?SLURM_JOB_ID ) ${PBS_BIN}/qalter -o ${listing}.txt ${SLURM_JOB_ID}
   exit 0
