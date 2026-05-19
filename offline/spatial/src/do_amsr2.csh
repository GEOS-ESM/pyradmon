#!/bin/csh

setenv expver $1
setenv yyyymmdd $2
setenv hh $3

set echo on

# Don't Comment out #module load python
#module load python/GEOSpyD/Ana2019.10_py3.7
#AMSUA CASES
# O-A PLOTS (2 in all omabc qc0 , omabc qc1)
set yyyy = `echo $yyyymmdd | cut -c1-4`
set mm = `echo $yyyymmdd | cut -c5-6`
set dd = `echo $yyyymmdd | cut -c7-8` 

foreach synop_hr ($hh)
  if ($expver =~ *_fp*) then
     set archive = /home/dao_ops/${expver}/run/.../scratch/obs/Y${yyyy}/M${mm}/D${dd}/H${synop_hr}
  else if ($expver =~ e5303_m21c_jan*) then
     set archive = /home/dao_ops/${expver}/run/.../archive/obs/Y${yyyy}/M${mm}/D${dd}/H${synop_hr} 
  else
     set archive = /home/dao_ops/${expver}/run/.../obs/Y${yyyy}/M${mm}/D${dd}/H${synop_hr} 
  endif
  foreach sat (gcom-w1)
    ./ln_s ${archive}/${expver}.diag_amsr2_${sat}_anl.${yyyymmdd}_${synop_hr}z.nc4
    ./pyradmon_spatial_driver_oma.py ${expver}.diag_amsr2_${sat}_anl.${yyyymmdd}_${synop_hr}z.nc4

# All other plots (8 in all - including totbc, tbobs, omgbc, omgnbc; qc0 and qc1)
    ./ln_s ${archive}/${expver}.diag_amsr2_${sat}_ges.${yyyymmdd}_${synop_hr}z.nc4
    ./pyradmon_spatial_driver_omf.py ${expver}.diag_amsr2_${sat}_ges.${yyyymmdd}_${synop_hr}z.nc4
  end
end

foreach psensor (AMSR2)
    foreach psatellite ( GCOM-W)
      mkdir -p $yyyymmdd/${psensor}_${psatellite}
      mv *${psensor}_${psatellite}*.png $yyyymmdd/${psensor}_${psatellite}
    end
end
