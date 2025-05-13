#!/bin/csh

# .... 

while ($ndstartdate <= $ndenddate)
   set arcfiles=''
   set expfiles=''
   foreach sat ($sats)
     set template=`cat $mstorage |grep $sat |grep bin$`
     foreach tmpl ($template)
#       set cfile=`$echorc -template $expid $startdate
        setenv PESTOROOT $arcbase
        set cfilearc=`$echorc -template $expid $startdate -fill $tmpl`
        setenv PESTOROOT $expbase
        set cfileexp=`$echorc -template $expid $startdate -fill $tmpl`
        #echo $tmpl
        if (-e $cfilearc) then
           set cfileout=`echo $cfileexp | sed 's/bin$/txt/'`
           #echo $cfileexp
           #echo $cfileout
           #echo --------------------
           mkdir -p `dirname $cfileout`
           echo asdf $cfileout
           if (! -e $cfileout) then
              set arcfiles=($arcfiles $cfilearc) 
              set expfiles=($expfiles $cfileexp)
              ln -sf $cfilearc $cfileexp
           endif
           echo asdf2
        endif
      end
   end

   echo dmgetting arcfiles $arcfiles

   if ("$arcfiles" != "" ) dmget $arcfiles

   echo processing expfiles

   foreach cfile ($expfiles)
      set cfileout=`echo $cfile | sed 's/bin$/txt/'`
#      if (! -e $cfileout) $bin2txt $cfile
#      $bin2txt $cfile
      $bin2txt -passivebc -npred 12 $cfile
      rm -f $cfile
   end

   echo ticking
   set ndstartdate=`../ndate +06 $ndstartdate`
   set startdate=( `echo $ndstartdate |cut -b1-8` `echo $ndstartdate |cut -b9-10`0000)

end

cd $startdir
rm -rf work.$exprc/*





