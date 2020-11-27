#!/usr/bin/env perl
#=======================================================================
# name - pyradmon_driver.pl
# purpose - 
#=======================================================================
use strict;
use warnings;

use Cwd qw(abs_path);
use File::Basename qw(basename dirname);
use File::Compare qw(compare);
use File::Copy qw(copy);
use File::Path qw(mkpath rmtree);
use FindBin qw($Bin);
use Getopt::Long qw(GetOptions);

# global variables
#-----------------
my ($bin2img_j, $bin2img_log, $bin2txt_csh, $clean, $clean_txt_csh);
my ($debug, $enddate, $endtime, $esmadir, $expbase, $getbins_err);
my ($getbins_j, $getbins_log, $inquire, $label, $noprompt, $outtmp);
my ($pid, $rcIN, $startdate, $starttime, $workdir);
my (%rc, %xtrCR, @rcVars);

# this array determines order of variables written to rcfile
#-----------------------------------------------------------
@rcVars = qw( expid
              fvhome
              fvroot
              archive
              pyradmon
              pytmpl
              workhead
              outdir
              startdatetime
              enddatetime
              mstorage
              gsidiagsrc
              bin2txt_exec
              bin2txt_options
              scp_userhost
              scp_path
              groupID
              send_plots
              queue_jobs
              clean
              instruments );

# extra <cr>'s in output rcfile after these variables
#----------------------------------------------------
%xtrCR = ( "pytmpl"           => 1,
           "outdir"           => 1,
           "enddatetime"      => 1,
           "bin2txt_options"  => 1,
           "clean"            => 1 );

# main program
#-------------
{
    my ($message);
    init();
    write_rcOUT();

    get_binfiles();
    bin2img();

    $message = "Ready to run pyradmon package";
    $message = "Ready to submit sbatch jobs" if $rc{"queue_jobs"};
    print "\n$message\n"; pause(); print "\n";

    run_jscript($getbins_j, $getbins_log);
    run_jscript($bin2img_j, $bin2img_log);

}

#=======================================================================
# name - init
# purpose - get runtime options and parameters
#=======================================================================
sub init {
    my ($append_txt, $archive, $bin2txt_opts, $bin2txt_x, $bindir);
    my ($debugB2T, $expid, $fvhome, $fvroot, $groupID, $gsidiagsrc);
    my ($help, $iversion, $merra2flag, $mstorage, $nc4, $npred);
    my ($outdir, $passivebc, $pyradmon, $pytmpl_name, $queue_jobs);
    my ($scp_host, $scp_path, $send_plots, $sst_ret, $workhead);
    my (@inst, %opts);

    $inquire = 1 unless @ARGV;
    GetOptions( "expid=s"      => \$expid,
                "fvhome=s"     => \$fvhome,
                "fvroot=s"     => \$fvroot,
                "archive=s"    => \$archive,
                "pyradmon=s"   => \$pyradmon,
                "pytmpl=s"     => \$pytmpl_name,
                "workhead"     => \$workhead,
                "outdir"       => \$outdir,
                "startdate=i"  => \$startdate,
                "starttime=i"  => \$starttime,
                "enddate=i"    => \$enddate,
                "endtime=i"    => \$endtime,
                "mstorage=s"   => \$mstorage,
                "gsidiagsrc=s" => \$gsidiagsrc,
                "inst=s"       => \@inst,
                "scp_host=s"   => \$scp_host,
                "scp_path=s"   => \$scp_path,
                "grpid=s"      => \$groupID,
                "send_plots!"  => \$send_plots,
                "q|qjobs!"     => \$queue_jobs,
                "clean!"       => \$clean,

                "bin2txt_x=s"  => \$bin2txt_x,
                "nc4"          => \$nc4,
                "debugB2T"     => \$debugB2T,
                "sst_ret"      => \$sst_ret,
                "passivebc"    => \$passivebc,
                "npred=i"      => \$npred,
                "iversion=i"   => \$iversion,
                "merra2"       => \$merra2flag,
                "append_txt"   => \$append_txt,

                "i"            => \$inquire,
                "np"           => \$noprompt,
                "db|debug"     => \$debug,
                "h|help"       => \$help );
    usage() if $help;
    $inquire = 0 if $noprompt;
    $debug = 0 unless $debug;

    # read from input resource file, if given
    #----------------------------------------
    $rcIN = shift(@ARGV);
    if ($rcIN) {
        die "Error. Cannot find input rcfile, $rcIN;" unless -e $rcIN;
        read_rcIN();
    }

    # input options take precedence over resource file
    #-------------------------------------------------
    if (@inst) {
        @inst = split(/,/,join(',',@inst));
        $rc{"instruments"} = "@inst";
    }
    $rc{"expid"}        = $expid       if $expid;
    $rc{"fvhome"}       = $fvhome      if $fvhome;
    $rc{"fvroot"}       = $fvroot      if $fvroot;
    $rc{"archive"}      = $archive     if $archive;
    $rc{"pyradmon"}     = $pyradmon    if $pyradmon;
    $rc{"pytmpl"}       = $pytmpl_name if $pytmpl_name;
    $rc{"workhead"}     = $workhead    if $workhead;
    $rc{"outdir"}       = $outdir      if $outdir;
    $rc{"mstorage"}     = $mstorage    if $mstorage;
    $rc{"gsidiagsrc"}   = $gsidiagsrc  if $gsidiagsrc;
    $rc{"bin2txt_exec"} = $bin2txt_x   if $bin2txt_x;
    $rc{"scp_userhost"} = $scp_host    if $scp_host;
    $rc{"scp_path"}     = $scp_path    if $scp_path;
    $rc{"groupID"}      = $groupID     if $groupID;
    $rc{"send_plots"}   = $send_plots  if defined($send_plots);
    $rc{"queue_jobs"}   = $queue_jobs  if defined($queue_jobs);
    $rc{"clean"}        = $clean       if defined($clean);

    # bin2txt options
    #----------------
    if ($merra2flag) { $iversion = 19180 unless $iversion }
    $bin2txt_opts = "";
    $bin2txt_opts .= " -nc4"                if $nc4;
    $bin2txt_opts .= " -debug"              if $debugB2T;
    $bin2txt_opts .= " -sst_ret"            if $sst_ret;
    $bin2txt_opts .= " -passivebc"          if $passivebc;
    $bin2txt_opts .= " -npred $npred"       if $npred;
    $bin2txt_opts .= " -iversion $iversion" if $iversion;
    $bin2txt_opts .= " -merra2"             if $merra2flag;
    $bin2txt_opts .= " -append_txt"         if $append_txt;
    $bin2txt_opts =~ s/^\s+// if $bin2txt_opts;

    $rc{"bin2txt_options"} = "$bin2txt_opts" if $bin2txt_opts;

    # fill in missing values
    #-----------------------
    get_missing_rc_vals();
    $rc{"startdatetime"} = "$startdate $starttime";
    $rc{"enddatetime"} = "$enddate $endtime";

    # remove trailing '/' from directory names
    #-----------------------------------------
    foreach (qw(fvhome fvroot archive pyradmon scp_path)) {
        $rc{$_} =~ s/\/$// if $rc{$_};
    }

    # source g5_modules
    #------------------
    {
        $bindir = "$rc{fvroot}/bin";
        local @ARGV = ("$bindir");
        do "$bindir/g5_modules_perl_wrapper";
    }

    # label info
    #-----------
    $label = "$startdate.$enddate";

    # work, outtmp, and output directories
    #-------------------------------------
    $workdir = "$rc{workhead}/radmon.work.$rc{expid}.$startdate.$$";
    rmtree($workdir, \%opts) if -d $workdir;

    %opts = ("debug" => 1);

    $outtmp = "$workdir/radmon";
    mkpath($outtmp, \%opts) or die "Error mkpath($outtmp);";

    unless (-d $rc{"outdir"}) {
        mkpath($rc{outdir}, \%opts) or die "Error mkpath($rc{outdir});" }

    print_rcinfo() if $debug;
}

#=======================================================================
# name - read_rcIN
# purpose - read input resource file, $rcIN
#=======================================================================
sub read_rcIN {
    my ($var);
    open RC, "< $rcIN" or die "Error opening file, $rcIN;";
  line: foreach (<RC>) {
      foreach $var (@rcVars) {
          if ( /^\s*$var\s*:\s*(.*)\s*$/ ) {
              $rc{$var} = $1;
              next line;
          }
      }
  }
    close RC;
    if ($rc{"startdatetime"}) {
        ($startdate, $starttime) = split /\s+/, $rc{"startdatetime"};
    }
    if ($rc{"enddatetime"}) {
        ($enddate, $endtime) = split /\s+/, $rc{"enddatetime"};
    }

    # substitute for variables within value strings
    #----------------------------------------------
    foreach (@rcVars) { $rc{$_} = var_subst($rc{$_}) }
}

#=======================================================================
# name - var_subst
# purpose - substitute values for variables contained within a string
#=======================================================================
sub var_subst {
    my ($string);
    $string = shift @_;
    return unless defined($string);
    return $string unless $string =~ m/\$/;

    foreach (@rcVars) {
        next unless $rc{$_};
        $string =~ s/\$$_/$rc{$_}/;
        $string =~ s/\${$_}/$rc{$_}/;
    }
    return $string;
}        

#=======================================================================
# name - get_missing_rc_vals
# purpose
#   1. get resource file values not given in rc or options
#   2. check for valid values
#=======================================================================
sub get_missing_rc_vals {
    my ($dflt, $etcdir, $gsidiag, $lastday, $mm);
    my ($prompt, $rundir, $uhdir, $user, $yyyy);

    # expid, fvhome, fvroot, archive, pyradmon
    #-----------------------------------------
    $rc{"expid"} = query("Experiment ID") unless $rc{"expid"};
    die "Error. No expid is given;" unless $rc{"expid"};

    $rc{"fvhome"} = query("Exp home directory") unless $rc{"fvhome"};
    die "Error. No fvhome is given;" unless $rc{"fvhome"};
    die "Error. Cannot find fvhome, $rc{fvhome};;" unless -d $rc{"fvhome"};

    $expbase = dirname($rc{"fvhome"});
    $rundir = "$rc{fvhome}/run";
    die "Error. Cannot find dir, $rundir;" unless -d $rundir;

    unless ($rc{"fvroot"} and -d $rc{"fvroot"}) {
        $dflt = $ENV{"FVROOT"};
        $dflt = read_radmon_config("FVROOT") unless $dflt;
        $rc{"fvroot"} = query("FVROOT", $dflt);
    }
    die "Error. Cannot find fvroot, $rc{fvroot};" unless -d $rc{fvroot};
    $esmadir = dirname($rc{"fvroot"});
    $etcdir = "$rc{fvroot}/etc";
        
    $rc{"archive"} = query("Archive directory", $ENV{"ARCHIVE"})
        unless $rc{"archive"};

    $rc{"pyradmon"} = query("pyradmon pathname", dirname($Bin))
        unless $rc{"pyradmon"};
    die "Error. Cannot find dir, $rc{pyradmon};" unless -d $rc{"pyradmon"};
    $gsidiag = "$rc{fvroot}/bin";

    unless ($rc{"pytmpl"}) {
        $dflt = "radiance_plots";
        $rc{"pytmpl"} = query("pyradmon plotting template name", $dflt)
    }

    # workhead, outdir
    #-----------------
    $rc{"workhead"} = query("Work directory head", $expbase)
        unless $rc{"workhead"};

    $rc{"outdir"} = query("Output directory", "$rc{fvhome}/radmon")
        unless $rc{"outdir"};

    # startdate, starttime, enddate, endtime
    #---------------------------------------
    $startdate = query("Start date, yyyymmdd")
        unless $startdate and $startdate =~ m/^\d{8}$/;
    die "Error. Start date not given;" unless $startdate;
    die "Error. Invalid start date format: $startdate;"
        unless $startdate =~ m/^\d{8}$/;

    $starttime = query("Start time, hhmmss", "000000")
        unless $starttime and $starttime =~ m/^\d{6}$/;
    die "Error. Invalid start time format: $starttime;"
        unless $starttime =~ m/^\d{6}$/;

    $yyyy = substr($startdate, 0, 4);
    $mm = substr($startdate, 4, 2);
    $lastday = num_days_in_month($yyyy, $mm);

    $enddate = query("End date, yyyymmdd", "$yyyy$mm$lastday")
        unless $enddate and $enddate =~ m/^\d{8}$/;
    die "Error. Invalid end date format: $enddate;" unless $enddate =~ m/^\d{8}$/;

    $endtime = query("End time, hhmmss", "180000")
        unless $endtime and $endtime =~ m/^\d{6}$/;
    die "Error. Invalid end time format: $endtime;" unless $endtime =~ m/^\d{6}$/;

    # bin2txt_exec
    #-------------
    $rc{"bin2txt_exec"} = query("bin2txt_exec", "$gsidiag/gsidiag_bin2txt.x")
        unless $rc{"bin2txt_exec"};
    die "Error. Cannot find file, $rc{bin2txt_exec};"
        unless -f $rc{"bin2txt_exec"};

    $rc{"bin2txt_options"} = query("gsidiag_bin2txt.x options", "")
        unless $rc{"bin2txt_options"};

    # mstorage, gsidiagsrc
    #---------------------
    $rc{"mstorage"} = query("mstorage.arc", "$rundir/mstorage.arc")
        unless $rc{"mstorage"};
    die "Error. Cannot find file, $rc{mstorage};" unless -f $rc{"mstorage"};

    $rc{"gsidiagsrc"} = query("gsidiags.rc", "$etcdir/gsidiags.rc")
        unless $rc{"gsidiagsrc"};
    die "Error. Cannot find file, $rc{gsidiagsrc};" unless -f $rc{"gsidiagsrc"};

    # scp_userhost, scp_path, send_plots
    #-----------------------------------
    $user = $ENV{"USER"};
    $uhdir = "/www/html/intranet/personnel/$user/radmon/radmon_data/";

    $rc{"scp_userhost"} = query("scp userhost", "$user\@polar")
        unless $rc{"scp_userhost"};
    $rc{"scp_path"} = query("scp path", $uhdir) unless $rc{"scp_path"};
    $rc{"send_plots"} = query("send plots (0=no,1=yes)", 0)
        unless defined($rc{"send_plots"});

    # queue_jobs, groupID, clean
    #---------------------------
    $rc{"queue_jobs"} = 1 unless -d $rc{"archive"};
    $rc{"queue_jobs"} = query("sbatch jobs (0=no,1=yes)", 0)
        unless defined($rc{"queue_jobs"});

    unless ($rc{"groupID"}) {
        $dflt = get_spcode();
        $rc{"groupID"} = query("group ID", $dflt);
    }
    unless (defined($rc{"clean"})) {
        $prompt = "delete txt files from expdir when complete? (0=no,1=yes)";
        $dflt = 1;
        $rc{"clean"} = query($prompt, $dflt);
    }
}

#=======================================================================
# name - read_radmon_config
# purpose - read variable value from $Bin/radmon_process.config file
#
# input parameters
# => $var: variable whose value is to be read
#
# notes
# 1. radmon_process.config must be in the same directory as the script
#=======================================================================
sub read_radmon_config {
    my ($var, $radmon_config, @info);
    $var = shift @_;

    $radmon_config = "$Bin/radmon_process.config";
    return unless -d $radmon_config;

    open CONF, "< $radmon_config" or die "Error opening $radmon_config;";
    while (<CONF>) {
        @info = split /\s+/;
        next unless scalar(@info) == 3;
        next unless $info[0] eq "setenv";
        next unless $info[1] eq $var;
        return $info[2];
    }
    close CONF;
}

#=======================================================================
# name - print_rcinfo
# purpose - print info in %rc hash (for debugging purposes)
#=======================================================================
sub print_rcinfo {
    foreach (sort keys %rc) {
        print "$_ = ";
        if (defined($rc{$_})) { print "$rc{$_}\n" }
        else                  { print "no value\n" }
    }
    pause();
}

#=======================================================================
# name - write_rcOUT
# purpose
# - write output rcfile to $outtmp
# - copy input rcfile to $outtmp, if the file exists
#
# note
# - The output rcfile is not used during this run, but it shows the values
#   that were used, and it can be used as input to rerun the job
#=======================================================================
sub write_rcOUT {
    my ($rcOUT, $rcORIG, $var, $value);

    $rcOUT = "$outtmp/radmon-$rc{expid}.$label.rc";

    # if input resource file is given, copy it to $outtmp
    #----------------------------------------------------
    if ($rcIN) {
        if (basename($rcIN) eq basename($rcOUT)) {
            $rcORIG = "$outtmp/$rcIN.orig";
        }
        else {
            $rcORIG = "$outtmp/" .basename($rcIN);
        }
        copy($rcIN, $rcORIG);
    }

    # write output resource file
    #---------------------------
    open RC, "> $rcOUT" or die "Error opening file, $rcOUT;";
    foreach $var (@rcVars) {
        $value = $rc{$var};
        if ($var eq "instruments") {
            print RC "# list instruments separated by spaces\n"
                .    "# otherwise, script will use insts found"
                .     " in experiment archive directory\n"
                .    "# " ."-"x70 ."\n" }
        if (defined($value)) { print RC "$var: ".display($var, $value)."\n" }
        else                 { print RC "#$var: no value set\n" }
        print RC "\n" if $xtrCR{$var};
    }
    close RC;

    # remove original rcfile if identical to output rcfile
    #-----------------------------------------------------
    if ($rcORIG) { unlink $rcORIG unless compare($rcORIG, $rcOUT) }
}

#=======================================================================
# name - display
# purpose - substitute variable names within other variable values
#=======================================================================
sub display {
    my ($var, $value, $vname, $vval);
    $var = shift @_;
    $value = shift @_;

    foreach (qw(pyradmon fvhome fvroot expid)) {
        next if $var eq $_;
        $vname = '$'."{$_}";
        $vval = $rc{$_};
        $value =~ s/$vval/$vname/;
    }
    return $value;
}

#=======================================================================
# name - get_binfiles
# purpose - run job to retrieve bin files from archive
#
# notes
# 1. This sub writes $getbins_j
# 2. This sub and $getbins_j write $bincopy_csh
# 3. This sub and $getbins_j write $bin2txt_csh
# 4. This sub and $getbins_j write $clean_txt_csh
#
# 5. $getbins_j is submitted or run from main program
# 6. $getbins_j runs $bincopy_csh
# 7. $bin2txt_csh is run in $bin2img_j *
# 8. $clean_txt_csh is run in $bin2img_j *
#
#  * written in sub bin2img()
#=======================================================================
sub get_binfiles {
    my ($instruments, $bin2txt_opts, $bincopy_csh);

    $instruments = "";
    $instruments = $rc{"instruments"} if $rc{"instruments"};

    $bin2txt_opts = "";
    $bin2txt_opts = "$rc{bin2txt_options}" if $rc{"bin2txt_options"};

    # bincopy script
    #---------------
    $bincopy_csh = "$workdir/bincopy.$label.csh";
    open(BCP, "> $bincopy_csh") or die "Error opening file, $bincopy_csh;";
    print BCP "#!/usr/bin/env tcsh\n";
    print BCP "set echo\n";
    print BCP "unalias cp\n\n";
    close BCP;
    chmod 0744, $bincopy_csh;

    # bin2txt script
    #---------------
    $bin2txt_csh = "$workdir/bin2txt.$label.csh";
    open(B2T, "> $bin2txt_csh") or die "Error opening file, $bin2txt_csh;";
    print B2T "#!/usr/bin/env tcsh\n";
    print B2T "set echo\n";
    print B2T "unalias rm\n\n";
    print B2T "set bin2txt = $rc{bin2txt_exec}\n";
    print B2T "set options = ( $bin2txt_opts )";
    close B2T;
    chmod 0744, $bin2txt_csh;

    # clean_txt script
    #-----------------
    $clean_txt_csh = "$workdir/clean_txt.$label.csh";
    open(XOBS, "> $clean_txt_csh") or die "Error opening file, $clean_txt_csh;";
    print XOBS "#!/usr/bin/env tcsh\n";
    print XOBS "set echo\n";
    print XOBS "unalias rm\n\n";
    close XOBS ;
    chmod 0744, $clean_txt_csh;

    # getbins error file
    #-------------------
    $getbins_err = "$workdir/GETBINS_ERR";

    # getbins jobscript
    #------------------
    $getbins_j = "$outtmp/$rc{expid}.getbins.$label.j";
    $getbins_log = "$rc{outdir}/$rc{expid}.getbins.$label.log.txt";
    unlink $getbins_log if -e $getbins_log;

    open SCR, "> $getbins_j" or die "Error opening file, $getbins_j;";
    print SCR << "EOF";
#!/usr/bin/env tcsh
#SBATCH --account=$rc{groupID}
#SBATCH --export=NONE
#SBATCH --time=1:00:00
#SBATCH --output=$getbins_log
#SBATCH --partition=datamove

unalias cd
unalias cp

setenv FVROOT $rc{"fvroot"}
set echorc = \$FVROOT/bin/echorc.x

setenv ESMADIR $esmadir
source \$ESMADIR/src/g5_modules

set expid   = $rc{"expid"}
set fvhome  = $rc{"fvhome"}
set archive = $rc{"archive"}
set expbase = $expbase

set startdate = ( $rc{"startdatetime"} )
set enddate   = ( $rc{"enddatetime"} )

set pyradmon  = $rc{"pyradmon"}
set bin2txt   = $rc{"bin2txt_exec"}

set mstorage   = $rc{"mstorage"}
set gsidiagsrc = $rc{"gsidiagsrc"}
set workdir    = $workdir

set ndstartdate = \$startdate[1]`echo \$startdate[2] | cut -c1-2`
set ndenddate   = \$enddate[1]`echo \$enddate[2] | cut -c1-2`

set getbins_err = $getbins_err

if (! -d \$archive) then
   unset echo
   echo "\$getbins_err found"
   set msg = "Error. \$archive not found in getbins job"
   echo \$msg |& tee \$getbins_err
   exit 1
endif

set insts = ($instruments)
if ("\$insts" == "") then
   set insts = (`\$echorc -rc \$gsidiagsrc satlist`)
endif
echo insts = \$insts

set tick = \$FVROOT/bin/tick
if (! -e \$tick) then
   unset echo
   echo "Unable to find \$tick"
   exit
endif

cd \$workdir

set binfiles = ()
set bincopy_csh = $bincopy_csh
set bin2txt_csh = $bin2txt_csh
set clean_txt_csh = $clean_txt_csh

\@ arcnt = 0
while (\$ndstartdate <= \$ndenddate)
   echo; echo; echo "date: \$ndstartdate"
   set arcfiles = ()

   foreach inst (\$insts)
      echo "looking for binfiles: \$inst"
      set template = `cat \$mstorage | grep \$inst | grep bin\$`

      foreach tmpl (\$template)
         setenv PESTOROOT \$archive/
         set afile = `\$echorc -template \$expid \$startdate -fill \$tmpl`

         setenv PESTOROOT \$expbase/
         set bfile = `\$echorc -template \$expid \$startdate -fill \$tmpl`
         set tfile = `echo \$bfile | sed 's/bin\$/txt/'`

         # check for bin file in archive and experiment directories
         #---------------------------------------------------------
         if (! -e \$tfile && (-e \$afile || -e \$bfile)) then

            # add to list of bin files to copy from archive
            #----------------------------------------------
            if (! -e \$bfile) then
               \@ arcnt ++
               set arcfiles = (\$arcfiles \$afile)
               echo "echo"                             >> \$bincopy_csh
               echo "set afile = \$afile"              >> \$bincopy_csh
               echo "set bfile = \$bfile"              >> \$bincopy_csh
               echo 'set edir = \`dirname \$bfile\`'   >> \$bincopy_csh
               echo 'if (! -d \$edir) mkdir -p \$edir' >> \$bincopy_csh
               echo 'cp \$afile \$bfile'               >> \$bincopy_csh
               echo ''                                 >> \$bincopy_csh
            endif

            # list of bin files to convert to txt
            #------------------------------------
            set binfiles = (\$binfiles \$bfile)

            # txt files to delete when processing is complete
            #------------------------------------------------
            echo "rm -f \$tfile" >> \$clean_txt_csh

         endif
      end
   end

   # dmget archive files
   #--------------------
   if ("\$arcfiles" != "") then
      echo dmget arcfiles
      dmget \$arcfiles &
   endif

   set startdate = `\$tick \$startdate 0 060000`
   set ndstartdate = \$startdate[1]`echo \$startdate[2] | cut -c1-2`
end

if (! \$arcnt) then
   echo "No need to copy bin files from archive." >> \$bincopy_csh
endif

if ("\$binfiles" != "") then

   # copy bin files from archive
   #----------------------------
   set bincopy_csh = $bincopy_csh
   echo \$bincopy_csh
   \$bincopy_csh

   # write bin2txt script (used in bin2img jobscript)
   #-------------------------------------------------
   foreach bfile (\$binfiles)
      echo ""                            >> \$bin2txt_csh
      echo "echo"                        >> \$bin2txt_csh
      echo "set bfile = \$bfile"         >> \$bin2txt_csh
      echo '\$bin2txt \$options \$bfile' >> \$bin2txt_csh
      echo 'rm \$bfile'                  >> \$bin2txt_csh
   end

else
      echo "echo No need to convert bin files to txt." >> \$bin2txt_csh;
endif
EOF
;
    close SCR;
}

#=======================================================================
# name - bin2img
# purpose - run program to convert bin files to txt and then txt to img files
#
# notes
# 1. This sub writes $bin2img_j
# 2. This sub writes $scp_data_j
#
# 3. $bin2img_j is submitted or run from main program
# 4. $bin2img_j runs $bin2txt_csh *
# 5. $bin2img_j runs $clean_txt_csh *
# 6. $bin2img_j submits $scp_data_j
#
#  * written in sub get_binfiles()
#=======================================================================
sub bin2img {
    my ($instruments, $scp_data_j, $scp_data_log);

    # scp_data_j script
    #--------------------
    $scp_data_j = "$rc{outdir}/$rc{expid}.scp_data.$label.j";
    $scp_data_log = "$rc{outdir}/$rc{expid}.scp_data.$label.log.txt";
    unlink($scp_data_j) if -e $scp_data_j;
    unlink($scp_data_log) if -e $scp_data_log;

    open SCR, "> $scp_data_j" or die "Error opening file, $scp_data_j;";
    print SCR << "EOF";
#!/usr/bin/env tcsh
#SBATCH --account=$rc{groupID}
#SBATCH --export=NONE
#SBATCH --time=1:00:00
#SBATCH --output=$scp_data_log
#SBATCH --partition=datamove

unalias cd

set echo
set expid        = $rc{"expid"}
set label        = $label
set outdir       = $rc{"outdir"}
set scp_path     = $rc{"scp_path"}
set scp_userhost = $rc{"scp_userhost"}

cd \$outdir

if (\$scp_userhost != '/dev/null' && \$scp_path != '/dev/null') then 
   scp \$expid.\$label.tar \${scp_userhost}\:\$scp_path
   ssh \$scp_userhost "cd \$scp_path ; tar xvf \$expid.\$label.tar"
endif
EOF
;
    close SCR;

    # bin2img jobscript
    #------------------
    $bin2img_j = "$outtmp/$rc{expid}.bin2img.$label.j";
    $bin2img_log = "$rc{outdir}/$rc{expid}.bin2img.$label.log.txt";
    unlink $bin2img_log if -e $bin2img_log;

    $instruments = "";
    $instruments = $rc{"instruments"} if $rc{"instruments"};

    open SCR, "> $bin2img_j" or die "Error opening file, $bin2img_j;";
    print SCR << "EOF";
#!/usr/bin/env tcsh
#SBATCH --account=$rc{groupID}
#SBATCH --export=NONE
#SBATCH --time=2:00:00
#SBATCH --output=$bin2img_log
#SBATCH --ntasks=28

unalias cd
unalias cp
unalias mv
unalias rm

setenv ESMADIR $esmadir
source \$ESMADIR/src/g5_modules
set echo

set expid           = $rc{"expid"}
set expbase         = $expbase

set startdatetime   = ( $rc{"startdatetime"} )
set enddatetime     = ( $rc{"enddatetime"} )

set startdate       = \$startdatetime[1]
set enddate         = \$enddatetime[1]

set pyradmon_path   = $rc{"pyradmon"}
set rename_date_dir = "/dev/null"

set send_plots      = $rc{"send_plots"}

set workdir         = $workdir
set outdir          = $rc{"outdir"}
set output_dir      = $outtmp

set label           = $label

set data_dirbase = \$expbase/\$expid
echo \$data_dirbase
cd \$workdir

set getbins_err = $getbins_err
if (-e \$getbins_err) then
    echo \$getbins_err found
    cat \$getbins_err
    exit 1
endif

set bin2txt_csh = $bin2txt_csh
set clean_txt_csh = $clean_txt_csh
set scp_data_j = $scp_data_j

# run bin2txt script
#-------------------
\$bin2txt_csh

# determine instruments
#----------------------
set insts = ($instruments)
if ("\$insts" == "") then
   unset echo
   echo -n "Determining instruments for \$expid from \$startdate to \$enddate. "
   echo "This may take a while..."
   set echo
   set insts = `\$pyradmon_path/scripts/determine_inst.csh \$data_dirbase \$startdate \$enddate`
endif
echo insts = \$insts

set syyyy = `echo \$startdate |cut -b1-4`
set smm   = `echo \$startdate |cut -b5-6`
set sdd   = `echo \$startdate |cut -b7-8`
set shh   = "00z"

set eyyyy = `echo \$enddate |cut -b1-4`
set emm   = `echo \$enddate |cut -b5-6`
set edd   = `echo \$enddate |cut -b7-8`
set ehh   = "18z"

set pyr_startdate="\$syyyy-\$smm-\$sdd \$shh"
set pyr_enddate="\$eyyyy-\$emm-\$edd \$ehh"

foreach inst (\$insts) 

  # yaml templates
  #---------------
  if (-e \$pyradmon_path/config/$rc{"pytmpl"}.\$inst.yaml.tmpl) then
    set configtmpl="\$pyradmon_path/config/$rc{"pytmpl"}.\$inst.yaml.tmpl"
  else
    set configtmpl="\$pyradmon_path/config/$rc{"pytmpl"}.yaml.tmpl"
  endif

  set configfile="\$workdir/\$inst.\$expid.\$startdate.\$enddate.plot.yaml"
  cp \$configtmpl \$configfile

  sed -i "s\@>>>DATA_DIRBASE<<<\@\$expbase\@g"    \$configfile
  sed -i "s\/>>>STARTDATE<<<\/\$pyr_startdate\/g" \$configfile 
  sed -i "s\/>>>ENDDATE<<<\/\$pyr_enddate\/g"     \$configfile 
  sed -i "s\/>>>EXPID<<<\/\$expid\/g"             \$configfile 
  sed -i "s\@>>>OUTPUT_DIR<<<\@\$output_dir\@g"   \$configfile 

  # run pyradmon.py program
  #------------------------
  unset echo
  echo
  echo "Running PyRadMon for \$inst from \$pyr_startdate to \$pyr_enddate"
  set echo
  \$pyradmon_path/pyradmon.py --config-file \$configfile plot --data-instrument-sat \$inst
end

# handle output
#--------------
cd \$output_dir
if (\$rename_date_dir != "/dev/null") then
   mv \$expid/\$startdate-\$enddate \$expid/\$rename_date_dir
endif

tar cvf \$expid.\$label.tar \$expid/
rm -rf \$expid/

# clean txt data files
#---------------------
set clean = $rc{"clean"}
if (\$clean) then
   \$clean_txt_csh
endif

# move output_dir files to outdir
#--------------------------------
mv \$output_dir/* \$outdir

# remove work directory
#----------------------
cd \$outdir
set debug = $debug
if (! \$debug) then
   rm -rf \$workdir
endif

# send plots
#-----------
if (\$send_plots) then
   sbatch \$scp_data_j
endif
EOF
;
    close SCR;
}

#=======================================================================
# name - get_spcode
# purpose - return first found sponsor code for user
#=======================================================================
sub get_spcode {
    my ($getsponsor, $spcode, @info);

    chomp($getsponsor = `which getsponsor 2>/dev/null`);
    return unless $getsponsor;

    $spcode = "";
    foreach (`$getsponsor`) {
        chomp; s/\s+//g;
        @info = split /\|/;
        if (scalar(@info) == 4 and $info[0] !~ m/SpCode/) {
            $spcode = $info[0];
            last;
        }
    }
    return $spcode;
}

#=======================================================================
# name - num_days_in_month
# purpose - return the number of days in a given year/month
#=======================================================================
sub num_days_in_month {
    my ($yr, $mnth);
    my %lastday = ( "01" => 31, "02" => 28, "03" => 31, "04" => 30,
                    "05" => 31, "06" => 30, "07" => 31, "08" => 31,
                    "09" => 30, "10" => 31, "11" => 30, "12" => 31 );

    # input parameters
    #-----------------
    $yr   = shift @_;
    $mnth = shift @_;

    $yr   = sprintf "%04i", $yr;
    $mnth = sprintf "%02i", $mnth;

    # check input for correct format
    #-------------------------------
    die "Error. Incorrect year value: $yr;"    unless $yr   =~ /^\d{4}$/;
    die "Error. Incorrect month value: $mnth;" unless $mnth =~ /^\d{2}$/;
    die "Error. Incorrect month value: $mnth;" if $mnth < 1 or $mnth > 12;

    # special handling for month of February
    #---------------------------------------
    if ($mnth eq "02") {
        $lastday{"02"} = 29 if $yr%4==0 and ($yr%100!=0 or $yr%400==0);
    }

    return $lastday{$mnth};
}

#=======================================================================
# name - query
# purpose - query user for a response; return the response
#
# input parameters
# => $prompt: user this line to prompt for a response
# => $dflt: (optional) default value to use for blank response
#=======================================================================
sub query {
    my ($prompt, $dflt, $ans);

    $prompt = shift @_;
    $dflt   = shift @_;

    # short-circuit query and return a result
    #----------------------------------------
    if (defined($dflt)) { return $dflt unless $inquire }
    else                { return if $noprompt }

    # prepare prompt
    #---------------
    $prompt .= ": ";
    $prompt .= "[$dflt] " if defined($dflt);
    print($prompt);

    # get user response
    #------------------
    chomp($ans = <STDIN>);
    $ans =~ s/^\s*|\s*$//g;
    unless ($ans ne "") { $ans = $dflt if defined($dflt) }

    return $ans;
}

#=======================================================================
# name - run_jscript
# purpose - execute jobscript either with sbatch or interactively
#=======================================================================
sub run_jscript {
    my ($jscript, $jscript_log);
    my ($depFLG, $cmd, $pidLINE);

    $jscript = shift @_;
    $jscript_log = shift @_;

    if ($rc{"queue_jobs"}) {
        if ($pid) { $depFLG = "--dependency=afterany:$pid" }
        else      { $depFLG = "" }

        $cmd = "sbatch $depFLG $jscript";
        print "$cmd\n";
        chomp($pidLINE = `$cmd`);

        print "$pidLINE\n\n";
        $pid = (split /\s+/, $pidLINE)[-1];
    }
    else {
        chmod 0744, $jscript;
        system("$jscript 2>&1 | tee $jscript_log");
    }
}

#=======================================================================
# name - pause
# purpose - pause interactive processing
#=======================================================================
sub pause {
    return if $noprompt;
    print "Hit <cr> to continue ... ";
    my $dummy = <STDIN>;
}

#=======================================================================
# name - usage
# purpose - print usage information to STDOUT
#=======================================================================
sub usage {
    my $script = basename($0);
    print << "EOF";
usage: $script [rcIN] [pyradmon options] [bin2txt options] [other options] 
where
  rcIN                  Radmon experiment input resource file

pyradmon options with no default value
  -expid expid          Experiment on which you are running the pyradmon programs
  -fvhome FVHOME        FVHOME directory of experiment
  -startdate startdate  Start date of pyradmon experiment

pyradmon options with a default value
  -fvroot FVROOT        FVROOT directory of the build used to run this experiment
  -archive archive      Archive directory where expid can be found
  -pyradmon pdir        Directory location of pyradmon programs
  -pytmpl pytmpl_name   Name for pyradmon plotting template
  -workhead workhead    Directory location for where to put the work directory
  -outdir outdir        Output directory location
  -starttime starttime  Start time of pyradmon experiment
  -enddate enddate      End date of pyradmon experiment
  -endtime endtime      End time of pyradmon experiment
  -mstorage mstorage    Pathname of mstorage.arc file
  -gsidiagsrc grcfile   Pathname of gsidiags.rc file
  -inst Ia,Ib,...       List of instruments to use for pyradmon experiment
  -scp_host scp_host    Userhost for scp\'ing output graphs
  -scp_path scp_path    Pathname of output directory on userhost
  -grpID gid            Account group ID for submitting queued jobs
  -[no]send_plots       Send plots to userhost (1=yes, 0=no)
  -[no]q                Queue bin2txt and txt2img jobs rather than running interactively
  -[no]clean            Remove obs files from expdir after processing complete

pyradmon option defaults
  -fvroot       [from \$Bin/radmon_process.config file]
  -archive      [\$ARCHIVE]
  -pyradmon     [\$Bin/..]
  -pytmpl       ["radiance_plots"]
  -workhead     [\$fvhome/..]
  -outdir       [\$fvhome/radmon]
  -starttime    [\"000000\"]
  -enddate      [last day of startdate month]
  -endtime      [\"180000\"]
  -mstorage     [\$fvhome/run/mstorage.arc]
  -gsidiagsrc   [\$fvroot/etc/gsidiags.rc]
  -inst         [all-insts-found-in-archive-expid-obs-dir]
  -scp_host     [\$user\@polar]
  -scp_path     [/www/html/intranet/personnel/\$user/radmon/radmon_data/]
  -grpID gid    [groupID from getsponsor utility]
  -send_plots   [0]
  -q            [1 if \$archive is visible; otherwise 0]
  -clean        [1]

gsidiag_bin2txt.x options
  -bin2txt_x b2tx  Pathname of gsidiags_bin2txt.x program
                   (default: pyradmon/gsidiag/gsidiag_bin2txt/gsidiag_bin2txt.x)
  -nc4             Read NC4 Diag (instead of binary)
  -debugB2T        Set debug verbosity
  -sst_ret         SST BC term is included (default: not included)
  -passivebc       Do Bias Correction calculations for passive channels
                   (by default these fields are reported as missing values)
  -npred INT       Number of predictors (default: 7)
  -iversion INT    Override iversion with INT (default: use internal iversion)
  -merra2          MERRA-2 file format; same as "-iversion 19180"
  -append_txt      Append .txt suffix, instead of replace last three characters
                   (default: replaced)
                   Note: The GMAO diag files end with .bin or .nc4, which is
                         where fixed 3-char truncation originates
other options
  -i            Inquire; Prompt for all values not supplied from rcIN or options
  -np           No prompt; Do not prompt for any values
  -db           Debug flag; do not remove work directory when job completes
  -h            Print usage information

Notes
1. If input rcfile is not given, then it will be built from the options.
2. If input rcfile is given, plus options, then options take precedence over
   values in input rcfile if there are duplications.
3. If variables without a default are not given in input rcfile or options, then
   script will prompt for them, unless the -np (noprompt) flag is given.
4. If variables with a default are not given in input rcfile or options, then
   the default will be used, unless the -i (inquire) flag is given.
5. The -np flag takes precedence over the -i flag.
6. If \$archive is visible, then bin2txt and txt2img jobs are run interactively,
   unless the -q flag is given.
7. If \$archive is not visible, then bin2txt and txt2img jobs are queued.
EOF
;
    exit();
}
