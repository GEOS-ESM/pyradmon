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
my ($bin2img_j, $bin2img_log, $bin2txt_pl, $clean, $clean_txt_csh);
my ($debug, $enddate, $endtime, $esmadir, $expbase, $getbins_err);
my ($getbins_j, $getbins_log, $inquire, $label, $noprompt, $pngdir);
my ($pid, $rcIN, $startdate, $starttime, $workdir);
my (%rc, %xtrCR, @rcVars);

# bin2txt flags
#--------------
my ($append_txt, $debugB2T, $iversion, $merra2FLG);
my ($nc4, $npred, $passivebc, $sst_ret);

my $MAX = 6;  # maximum number of parallel jobs

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
    my ($archive, $bin2txt_opts, $bin2txt_x, $bindir);
    my ($expid, $fvhome, $fvroot, $groupID, $gsidiagsrc);
    my ($help, $mstorage, $outdir, $pyradmon, $pytmpl_name);
    my ($queue_jobs, $scp_host, $scp_path, $send_plots, $workhead);
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
                "merra2"       => \$merra2FLG,
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
    if ($merra2FLG) {
        $npred = 7 unless $npred;
        $iversion = 19180 unless $iversion;
    }
    $npred = 12 unless $npred;

    $bin2txt_opts = "";
    $bin2txt_opts .= " -nc4"                if $nc4;
    $bin2txt_opts .= " -debug"              if $debugB2T;
    $bin2txt_opts .= " -sst_ret"            if $sst_ret;
    $bin2txt_opts .= " -passivebc"          if $passivebc;
    $bin2txt_opts .= " -npred $npred"       if $npred;
    $bin2txt_opts .= " -iversion $iversion" if $iversion;
    $bin2txt_opts .= " -merra2"             if $merra2FLG;
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

    # work, pngdir, and output directories
    #-------------------------------------
    %opts = ("debug" => 1);
    $workdir = "$rc{workhead}/radmon.work.$rc{expid}.$startdate.$$";
    rmtree($workdir, \%opts) if -d $workdir;

    $pngdir = "$workdir/pngdir";
    mkpath($pngdir, \%opts) or die "Error mkpath($pngdir);";

    unless (-d $rc{"outdir"}) {
        mkpath($rc{outdir}, \%opts) or die "Error mkpath($rc{outdir});" }

    print_rcinfo() if $debug;
}

#=======================================================================
# name - read_rcIN
# purpose - read input resource file, $rcIN
#=======================================================================
sub read_rcIN {
    my (@b2t_split, $b2tFLG, $var);
    
    open(RC, "< $rcIN") or die "Error opening file, $rcIN;";
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
    if ($rc{"bin2txt_options"}) {
        @b2t_split = split /\s+/, $rc{"bin2txt_options"};
        while (@b2t_split) {
            $b2tFLG = shift @b2t_split;

            $nc4       = 1 if $b2tFLG eq "-nc4";
            $debugB2T  = 1 if $b2tFLG eq "-debugB2T";
            $sst_ret   = 1 if $b2tFLG eq "-sst_ret";
            $passivebc = 1 if $b2tFLG eq "-passivebc";
            $merra2FLG = 1 if $b2tFLG eq "-merra2";
            
            if ($b2tFLG eq "-npred") {
                $npred = shift @b2t_split unless $npred;
            }
            if ($b2tFLG eq "-iversion") {
                $iversion = shift @b2t_split unless $iversion;
            }
        }
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

    open(CONF, "< $radmon_config") or die "Error opening $radmon_config;";
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
# - write output rcfile to outdir
# - copy input rcfile to outdir if the file exists
#
# note
# - The output rcfile is not used during this run, but it shows the values
#   that were used, and it can be used as input to rerun the job
#=======================================================================
sub write_rcOUT {
    my ($rcOUT, $rcORIG, $var, $value);

    $rcOUT = "$rc{outdir}/radmon-$rc{expid}.$label.rc";

    # if input resource file is given, copy it to outdir
    #---------------------------------------------------
    if ($rcIN) {
        if (basename($rcIN) eq basename($rcOUT)) {
            $rcORIG = "$rc{outdir}/$rcIN.orig";
        }
        else {
            $rcORIG = "$rc{outdir}/" .basename($rcIN);
        }
        copy($rcIN, $rcORIG);
    }

    # write output resource file
    #---------------------------
    open(RC, "> $rcOUT") or die "Error opening file, $rcOUT;";
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
# 2. $getbins_j is submitted or run from main program
# 3. $getbins_j writes $bin2txt_pl
# 4. $getbins_j writes $clean_txt_csh
# 5. $getbins_j copies bin files from archive to the experiment directory
# 6. $bin2txt_pl is run in $bin2img_j *
# 7. $clean_txt_csh is run in $bin2img_j *
#
#  * written in sub bin2img()
#=======================================================================
sub get_binfiles {
    my ($instruments, $bin2txt_opts);

    $instruments = "";
    $instruments = $rc{"instruments"} if $rc{"instruments"};

    $bin2txt_opts = "";
    $bin2txt_opts = "$rc{bin2txt_options}" if $rc{"bin2txt_options"};

    $bin2txt_pl = "$workdir/bin2txt.$label.pl";
    $getbins_err = "$workdir/GETBINS_ERR";
    $clean_txt_csh = "$workdir/clean_txt.$label.csh";

    $getbins_j = "$rc{outdir}/$rc{expid}.getbins.$label.j";
    $getbins_log = "$rc{outdir}/$rc{expid}.getbins.$label.log.txt";
    unlink $getbins_log if -e $getbins_log;

    # getbins jobscript
    #------------------
    open(SCR, "> $getbins_j") or die "Error opening file, $getbins_j;";
    print SCR << "EOF";
#!/usr/bin/env perl
#SBATCH --account=$rc{groupID}
#SBATCH --export=NONE
#SBATCH --time=2:00:00
#SBATCH --output=$getbins_log
#SBATCH --partition=datamove
use strict;
use warnings;
use File::Basename qw(dirname);
use File::Copy qw(copy);
use File::Path qw(mkpath rmtree);
use Scalar::Util qw(openhandle);
use lib ("$rc{pyradmon}/scripts");
use LoadBalance qw(load_balance);
my (\$B2T, \$BCP, \$CLN);
my (\$ESMADIR, \$FVROOT, \$PESTOROOT);
my (\$afile, \$archive, \$archroot, \$atmpl);
my (\$bfile, \$bin2txt_x, \$bin2txt_pl, \$btmpl);
my (\$clean_txt_csh, \$echorc, \$edir, \$expbase, \$expid, \$exproot);
my (\$fvhome, \$getbins_err, \$gsidiagsrc, \$inst);
my (\$msg, \$mstorage, \$ndenddate, \$ndstartdate);
my (\$pid, \$pyradmon, \$tfile, \$tick, \$tmpl, \$workdir);
my (\%arc2binH, \%bin2txtH, \%opts);
my (\@arcfiles, \@dmgetlist, \@enddate, \@insts, \@pidArr, \@startdate, \@template);
my \$MAX = $MAX;

\$| = 1;  # flush buffer after each output operation
\%opts = ( "verbose" => 1 );

\$FVROOT = "$rc{fvroot}";
\$pyradmon = "$rc{pyradmon}";

#\$echorc = "\$FVROOT/bin/echorc.x";
\$echorc = "\$pyradmon/scripts/echorc.pl";

{
    local \@ARGV = ("\$FVROOT/bin");
    do "\$FVROOT/bin/g5_modules_perl_wrapper";
}
\$expid   = "$rc{expid}";
\$fvhome  = "$rc{fvhome}";
\$archive = "$rc{archive}";
\$expbase = "$expbase";

\@startdate = qw( $rc{"startdatetime"} );
\@enddate   = qw( $rc{"enddatetime"} );

\$bin2txt_x  = "$rc{bin2txt_exec}";

\$mstorage   = "$rc{mstorage}";
\$gsidiagsrc = "$rc{gsidiagsrc}";
\$workdir    = "$workdir";

\$ndstartdate = \$startdate[0] .substr(\$startdate[1],0,2);
\$ndenddate   = \$enddate[0] .substr(\$enddate[1],0,2);

\$getbins_err = "\$workdir/GETBINS_ERR";

if (! -d \$archive) {
    print "\$getbins_err found\\n";
    \$msg = "Error. \$archive not found in getbins job";
    system("echo \$msg \|\& tee \$getbins_err");
    die "\$msg;";
}

\@insts = (qw($instruments));
unless (\@insts) {
    \@insts = (split /\\s+/, `\$echorc -rc \$gsidiagsrc satlist`);
}
print "insts = \@insts\\n";

\$tick = "\$FVROOT/bin/tick";
die "Unable to find \$tick;" unless -e \$tick;

mkpath(\$workdir, \\\%opts) unless -d \$workdir;
chdir \$workdir;

\$bin2txt_pl = "$bin2txt_pl";
\$clean_txt_csh = "$clean_txt_csh";

\%arc2binH = ();
\%bin2txtH = ();

while (\$ndstartdate <= \$ndenddate) {
    print "\\n\\ndate: \$ndstartdate\\n";
    \@dmgetlist = ();

    \$archroot = "\$archive/";
    \$exproot = "\$expbase/";
    foreach \$inst (\@insts) {
        print "looking for binfiles: \$inst\\n";
        \@template = (`cat \$mstorage | grep \$inst | grep -P bin\\\$`);

        foreach \$tmpl (\@template) {
            \$ENV{"PESTOROOT"} = \$archroot;
            \$atmpl = ( `\$echorc -template \$expid \@startdate -fill \$tmpl` );
            chomp(\$atmpl);
            foreach \$afile (glob(\$atmpl)) {
                next unless -e \$afile;
                (\$bfile = \$afile) =~ s/\$archroot/\$exproot/;
                (\$tfile = \$bfile) =~ s/bin\$/txt/;
                next if \$bin2txtH{\$bfile};
                next if -e \$tfile;
                unless (-e \$bfile) {
                    \$arc2binH{\$afile} = \$bfile;
                    push \@dmgetlist, \$afile;
                }
                \$bin2txtH{\$bfile} = \$tfile;
            }

            \$ENV{"PESTOROOT"} = \$exproot;
            \$btmpl = ( `\$echorc -template \$expid \@startdate -fill \$tmpl` );
            chomp(\$btmpl);
            foreach \$bfile (glob(\$btmpl)) {
                next unless -e \$bfile;
                next if \$bin2txtH{\$bfile};
                (\$tfile = \$bfile) =~ s/bin\$/txt/;
                next if -e \$tfile;
                \$bin2txtH{\$bfile} = \$tfile;
            }
        }
    }
    if (\@dmgetlist) {
        print "dmget \@dmgetlist\\n";
        \@pidArr = load_balance(\\\@pidArr, \$MAX);
        defined(\$pid=fork) or die "Error. Cannot fork: \$!";
        unless (\$pid) {
            exec("dmget \@dmgetlist");
        }
        push \@pidArr, \$pid;
    }
    chomp(\@startdate = (split /\\s+/, `\$tick \@startdate 0 060000`));
    \$ndstartdate = \$startdate[0] .substr(\$startdate[1], 0, 2);
}

# copy bin files from archive
#----------------------------
if (\%arc2binH) {
    \@arcfiles = (sort keys \%arc2binH);
    foreach \$afile (\@arcfiles) {
        \$bfile = \$arc2binH{\$afile};
        \$edir = dirname(\$bfile);
        print "\\n";
        mkpath(\$edir, \\\%opts) unless -d \$edir;
        print "afile: \$afile\\n";
        print "bfile: \$bfile\\n";
        print "copy(afile, bfile)\\n";

        \@pidArr = load_balance(\\\@pidArr, \$MAX);
        defined(\$pid=fork) or die "Error. Cannot fork: \$!";
        unless (\$pid) {
            copy(\$afile, \$bfile);
            exit;
        }
        push \@pidArr, \$pid;
    }
    print "\\n";
    load_balance(\\\@pidArr, 0);
} else { print "No need to copy bin files from archive.\\n" }

if (%bin2txtH) {

    # write bin2txt script
    #---------------------
    unlink \$bin2txt_pl if -e \$bin2txt_pl;
    open(\$B2T, "> \$bin2txt_pl") or die "Error opening file, \$bin2txt_pl;";
    print \$B2T qq(#!/usr/bin/env perl\\n);
    print \$B2T qq(use strict;\\n);
    print \$B2T qq(use warnings;\\n);
    print \$B2T qq(use lib ("$rc{pyradmon}/scripts");\\n);
    print \$B2T qq(use LoadBalance qw(load_balance);\\n);
    print \$B2T qq(my (\\\$bfile, \\\$bin2txt_x, \\\$options);\\n);
    print \$B2T qq(my (\\\$pid, \\\@pidArr);\\n);
    print \$B2T qq(my \\\$MAX = $MAX;\\n);
    print \$B2T qq(\\n);
    print \$B2T qq(\\\$bin2txt_x = "$rc{bin2txt_exec}";\\n);
    print \$B2T qq(\\\$options = "$bin2txt_opts";\\n);
    print \$B2T qq(\\\@pidArr = ();\\n);
    print \$B2T qq(\\n);
    print \$B2T qq(sub b2t {\\n);
    print \$B2T qq(   my \\\$bfile = shift \\\@_;\\n);
    print \$B2T qq(   \\\@pidArr = load_balance(\\\\\\\@pidArr, \\\$MAX);\\n);
    print \$B2T qq(   defined(\\\$pid=fork) or die "Error. Cannot fork: \\\\\\\$!";\\n);
    print \$B2T qq(   unless (\\\$pid) {\\n);
    print \$B2T qq(       exec("\\\$bin2txt_x \\\$options \\\$bfile");\\n);
    print \$B2T qq(   }\\n);
    print \$B2T qq(   push \\\@pidArr, \\\$pid;\\n);
    print \$B2T qq(}\\n);
    print \$B2T qq(\\\@pidArr = load_balance(\\\\\\\@pidArr, 0);\\n\\n);

    foreach \$bfile (sort keys \%bin2txtH) {
        print \$B2T qq(b2t("\$bfile");\\n);
    }
    close \$B2T;

    # write clean_text script
    #------------------------
    unlink \$clean_txt_csh if -e \$clean_txt_csh;
    open(\$CLN, "> \$clean_txt_csh") or die "Error opening file, \$clean_txt_csh;";
    print \$CLN "#!/usr/bin/env tcsh\\n";
    print \$CLN "set echo\\n";
    print \$CLN "unalias rm\\n\\n";

    foreach \$afile (sort keys \%arc2binH) {
        print \$CLN qq(rm -f \$arc2binH{\$afile}\\n);
    }
    foreach \$bfile (sort keys \%bin2txtH) {
        print \$CLN qq(rm -f \$bin2txtH{\$bfile}\\n);
    }
    close \$CLN;
    chmod 0744, \$bin2txt_pl;
    chmod 0744, \$clean_txt_csh;
} else { print "No need to convert bin files to txt.\\n" }
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
# 4. $bin2img_j runs $bin2txt_pl *
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

    open(SCR, "> $scp_data_j") or die "Error opening file, $scp_data_j;";
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
    $bin2img_j = "$rc{outdir}/$rc{expid}.bin2img.$label.j";
    $bin2img_log = "$rc{outdir}/$rc{expid}.bin2img.$label.log.txt";
    unlink $bin2img_log if -e $bin2img_log;

    $instruments = "";
    $instruments = $rc{"instruments"} if $rc{"instruments"};

    open(SCR, "> $bin2img_j") or die "Error opening file, $bin2img_j;";
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
setenv FVROOT $rc{"fvroot"}
source \$FVROOT/bin/g5_modules
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
set output_dir      = $pngdir

set label           = $label

if (! -d \$output_dir) then
   mkdir -p \$output_dir
endif

if (! -d \$outdir) then
   mkdir -p \$outdir
endif

set data_dirbase = \$expbase/\$expid
echo \$data_dirbase
cd \$workdir

set getbins_err = $getbins_err
if (-e \$getbins_err) then
    echo \$getbins_err found
    cat \$getbins_err
    exit 1
endif

set bin2txt_pl = $bin2txt_pl
set clean_txt_csh = $clean_txt_csh
set scp_data_j = $scp_data_j

# run bin2txt script
#-------------------
\$bin2txt_pl

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

bin2txt options
  -bin2txt_x b2tx  Pathname of gsidiags_bin2txt.x program
                   (default: pyradmon/gsidiag/gsidiag_bin2txt/gsidiag_bin2txt.x)
  -nc4             Read NC4 Diag (instead of binary)
  -debugB2T        Set debug verbosity
  -sst_ret         SST BC term is included (default: not included)
  -passivebc       Do Bias Correction calculations for passive channels
                   (by default these fields are reported as missing values)
  -npred INT       Number of predictors (default: 12)
  -iversion INT    Override iversion with INT (default: use internal iversion)
  -merra2          MERRA-2 file format; same as "-iversion 19180 -npred 7"
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
