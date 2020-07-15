#!/bin/csh -f

if ($#argv != 3) then
    echo "usage: determine_inst.csh <experiment base directory with diags> <start YYYYMMDD> <end YYYYMMDD>"
    exit 99
endif

set dir       = $argv[1]
set startdate = $argv[2]
set enddate   = $argv[3]

set curdate = $startdate
set dirs = ()

while ( $curdate <= $enddate )
    set year = `echo $curdate |cut -c1-4`
    set mon  = `echo $curdate |cut -c5-6`
    set day  = `echo $curdate |cut -c7-8`

    set obsdir = $dir/obs/Y$year/M$mon/D$day
    if (-d $obsdir) set dirs = ($dirs $obsdir)

    set curdate  = `$ESMADIR/Linux/bin/tick $curdate`
end

set instList = ()
foreach file (`find $dirs | grep ges`)
   set base = `basename $file`
   set inst = `echo $base | cut -d. -f2 | sed -e "s/diag_//" -e "s/_ges//"`

   set found = 0
   foreach iii ( $instList )
       if ($iii == $inst) then
           set found = 1
           break
       endif
   end
   if (! $found) set instList = ($instList $inst)
end

echo $instList | sed 's/ /\n/g'



