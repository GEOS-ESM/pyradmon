package LoadBalance;
#=======================================================================
# name: LoadBalance
# purpose:
#    This package provides a function that will monitor a list of
#    process IDs and will wait until the number of active processes is
#    less than a MAX value.
#=======================================================================
use strict;
use warnings;
use File::Basename;

require 5.000;
require Exporter;

our @ISA = qw(Exporter);
our @EXPORT = qw( load_balance );

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
1;
