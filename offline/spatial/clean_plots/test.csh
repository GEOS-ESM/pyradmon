#!/usr/local/bin/csh



####bin/csh

@ x = 0
while (1)
   @ x++
   set log = log.$x
   if (! -e $log) break
end
     
./run_all.csh f5293_fpp 20210924 00 |& tee $log
