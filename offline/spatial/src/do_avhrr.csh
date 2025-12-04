#!/bin/csh

setenv expver $1
setenv  yyyymmdd $2
setenv hh $3

set echo on

#module load python/GEOSpyD/Ana2019.10_py3.7
#AVHRR CASES
# O-A PLOTS (2 in all omabc qc0 , omabc qc1)
set yyyy = `echo $yyyymmdd | cut -c1-4`
set mm = `echo $yyyymmdd | cut -c5-6`
set dd = `echo $yyyymmdd | cut -c7-8`

foreach synop_hr ($hh)
   set archive = /home/dao_ops/${expver}/run/.../scratch/obs/Y${yyyy}/M${mm}/D${dd}/H${synop_hr}
   foreach sat (metop-a metop-b n18 n19)
      ./ln_s ${archive}/${expver}.diag_avhrr_${sat}_anl.${yyyymmdd}_${synop_hr}z.nc4
      ./pyradmon_spatial_driver_oma.py ${expver}.diag_avhrr_${sat}_anl.${yyyymmdd}_${synop_hr}z.nc4

# All other plots (8 in all - including totbc, tbobs, omgbc, omgnbc; qc0 and qc1)
      ./ln_s ${archive}/${expver}.diag_avhrr_${sat}_ges.${yyyymmdd}_${synop_hr}z.nc4
      ./pyradmon_spatial_driver_omf.py ${expver}.diag_avhrr_${sat}_ges.${yyyymmdd}_${synop_hr}z.nc4
   end
end

foreach psensor (AVHRR)
    foreach psatellite ( METOP-A METOP-B NOAA-19 NOAA-18)
      mkdir -p $yyyymmdd/${psensor}_${psatellite}
      mv *${psensor}_${psatellite}*.png $yyyymmdd/${psensor}_${psatellite}
    end
end
