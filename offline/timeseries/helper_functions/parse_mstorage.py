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
    print(f'echorc satlist: {section_lines}')
    return section_lines

sats = echorc(
        rc_file_path ='/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/etc/gsidiags.rc',
        rcstring='satlist'
        )

# pyradmon_bin2txt_driver while loop line 74 equivalent
def parse_mstorage(file_path, search_string):
    """
    Reads a file line by line and prints lines containing a specified string.

    Args:
        file_path (str): The path to the file.
        search_string (str): The string to search for in each line.
    """
    try:
        section_lines = []
        with open(file_path, 'r') as file:
            for line in file:
                if search_string in line and '.bin' in line:
                    print(line, end='')
                    section_lines.append(line)
        return section_lines
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")

file_path = '/home/dao_ops/e5303_m21c_jan18/run/mstorage.arc'
template = parse_mstorage(file_path, 'amsua_n15')

#for sat in sats:
    #template = parse_mstorage(file_path, sat)
    #os.environ['PESTOROOT'] = self.arcbase
    #os.environ['PESTOROOT'] = self.arcbase
    #print(f'template: {template}')


