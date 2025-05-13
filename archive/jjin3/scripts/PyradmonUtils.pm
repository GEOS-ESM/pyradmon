package PyradmonUtils;
#=======================================================================
# name: PyradmonUtils
# purpose:
#    This package provides utility routines needed by the Pyradmon perl scripts.
#=======================================================================
use strict;
use warnings;
use File::Basename;

require 5.000;
require Exporter;

our @ISA = qw(Exporter);
our @EXPORT = qw( load_balance substitute );

#=======================================================================
# name: load_balance
# purpose: Stall procesing until the number of active processes is less
#          then $MAX
#
# input parameters:
# => $pidArrPtr: pointer to list of process IDs to monitor
# => $MAX: maximum number of processes
#
# return value:
# => @pidArr: updated list of active process IDs
#=======================================================================
sub load_balance {
    use POSIX ":sys_wait_h";
    my ($pidArrPtr, $MAX);
    my ($check_counter, $pid, $status);
    my (@pidArr, @pidArr_);

    # get input parameters
    #---------------------
    $pidArrPtr = shift @_;
    $MAX = shift @_;
    $MAX = 1 if $MAX < 1;

    @pidArr = @$pidArrPtr;
    return @pidArr if scalar(@pidArr) < $MAX;

    # check status of process IDs
    #----------------------------
    # status equals 0   if still alive
    # status equals pid if complete
    # status equals -1  if not found
    #-------------------------------
    while (1) {
        @pidArr_ = ();
        foreach $pid (@pidArr) {
            $status = waitpid($pid, WNOHANG);
            push @pidArr_, $pid unless $status;
        }
        return @pidArr_ if scalar(@pidArr_) < $MAX;

        @pidArr = @pidArr_;
        sleep 1; # wait one second before looping through again
    }
}

#=======================================================================
# name - substitute
# purpose - substitute values for labels in a template file and write
#           result to an output file
#
# input parameters
# > $tmpl:  input template file
# > $outf:  output file
# > %values: substitute values where $values{$label} = $value
#=======================================================================
sub substitute {
    my ($tmpl, $outf, %values);
    my ($key);
    $tmpl = shift @_;
    $outf = shift @_;
    %values = @_;

    open (FH1, "< $tmpl") or die "Error opening input file, $tmpl;";
    open (FH2, "> $outf") or die "Error opening output file, $outf;";
    while (<FH1>) {
        foreach $key (reverse sort keys %values) {
            s/$key/$values{$key}/g if m/$key/;
        }
        print FH2 $_;
    }
    close FH1;
    close FH2;
}
1;
