##!/bin/csh -X

echo Running NRT Radmon for MERRA21C

cd /discover/nobackup/sicohen/RADMON/offline/work/r21c/TBR/radmon/time_series/
setenv FVROOT /home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/

setenv M2BASE /home/dao_ops/m21c/archive/

#set days_back=91 # number of days to plot in realtime MERRA-2 monitoring
set days_back=1 # number of days to plot in realtime MERRA-2 monitoring

#set enddate=`ndate`
set enddate=2019053118

set obsdir=$M2BASE/e5303_m21c_jan18/obs/

set eyyyy=`echo $enddate |cut -b1-4`
set emm=`echo $enddate   |cut -b5-6`
set edd=`echo $enddate   |cut -b7-8`
set ehh=`echo $enddate   |cut -b9-10`
set enddate=$eyyyy$emm$edd\18

set enddate_not_found=1
while ($enddate_not_found)
   set eyyyy=`echo $enddate |cut -b1-4`
   set emm=`echo $enddate   |cut -b5-6`
   set edd=`echo $enddate   |cut -b7-8`
   set ehh=`echo $enddate   |cut -b9-10`
   echo testing $obsdir/Y$eyyyy/M$emm/D$edd/H$ehh

   if (-d $obsdir/Y$eyyyy/M$emm/D$edd/H$ehh) then
      set enddate_not_found=0
   else
      set enddate=`./ndate -06 $enddate`
   endif

end

echo $enddate

@ days_back_hr = $days_back * 24

set startdate=`./ndate -$days_back_hr $enddate`

set syyyymmdd=`echo $startdate |cut -b1-8`
set eyyyymmdd=$eyyyy$emm$edd

cat m21c.current.rc.tmpl | sed "s/>>>STARTDATE<<</$syyyymmdd/g;s/>>>ENDDATE<<</$eyyyymmdd/g" > m21c.current.rc

./pyradmon_driver.csh m21c.current.rc
rm m21c.current.rc



