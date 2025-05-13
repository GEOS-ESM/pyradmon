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

rc_file_path = '/home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/etc/gsidiags.rc'
rcstring = 'satlist'

section_data = echorc(rc_file_path, rcstring)
if section_data:
    for line in section_data:
        print(line)
else:
    print(f"Section not found between '{start_marker}' and '{end_marker}'.")