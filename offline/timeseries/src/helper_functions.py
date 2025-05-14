#!/usr/bin/env python3

# Helper Functions
# 2025-05-02
# Functions & Extras that are not required in the main pyradmon_offline_driver.py.
# These will be needed for the full conversion from csh to python


# echorc equivalent
#############################
# It essentially just parses an .rc file and prints the string or block that you tell it to search for
#############################
echorc=os.path.join(ESMADIR,'install/bin/echorc.x') # could keep echorc around for now

# python version echorc
def echorc(rc_file_path, rcstring):
    start_marker = rcstring + '::'
    end_marker = '::'
    section_lines = []
    inside_section = False
    with open(rc_file_path, 'r') as file:
        for line in file:
            if start_marker in line:
                inside_section = True
            elif end_marker in line:
                inside_section = False
            elif inside_section:
                section_lines.append(line.strip())
    #print(section_lines)
    return section_lines

# Using echorc to get the satlist from gsidiags.rc
sats = echorc(
        '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/etc/gsidiags.rc',
        rcstring='satlist'
        )
