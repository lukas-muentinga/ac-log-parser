######################################################################
# REGEX PARSER FOR ASSETTO CORSO LOG FILES
# ----------------------------------------
# Usage: python3 ac_log_parser.py [log-filepath] [sqlite-filepath]
######################################################################

import re, sys, sqlite3
from datetime import datetime

LAP_END_FINDER_RE = r"""Dispatching\sTCP\smessage\sto\s(?P<car>\S+)\s\(\d\)\s\[(?P<player>\S+).*\n
                        Car.onLapCompleted\n
                        LAP\s\S+\s(?P<lap_time>\S+)\n
                        SPLIT\sCOUNT:\s(?P<split_count>\S+)\n
                        Dynamic\strack\s(?P<dynamic_track>\S+)\n
                        Result.OnLapCompleted\.\sCuts:\s(?P<cuts>\S+)\n"""

# DB Scheme
DB_TABLE = 'ac-rounds'


if __name__ == '__main__':

    # Get log file path from stdin
    logfile_path = sys.argv[1]
    lap_end_finder_pattern = re.compile(LAP_END_FINDER_RE, re.MULTILINE | re.VERBOSE)

    # Read logfile
    try:
        with open(logfile_path) as logfile:
            log_content = logfile.read()
    except IOError:
        # Catch file error
        print(f'File {logfile_path} could not be opened.')
        sys.exit(1)

    laps = [m.groupdict() for m in re.finditer(lap_end_finder_pattern, log_content)]

    # Parse datatypes
    for lap in laps:
        pt = datetime.strptime(lap['lap_time'], '%-M:%S:%f')
        lap['lap_time'] = pt.microsecond + ( pt.second * 1000 ) + ( pt.minute * 60000 ) 
        lap['cuts'] = int(lap['cuts'])
        lap['split_count'] = int(lap['split_count'])

    # Write laps to sqlite db
    try:
        con = sqlite3.connect(sys.argv[2])
        cur = con.cursor()
        for lap in laps:
            cur.execute(f"""INSERT INTO {DB_TABLE} ({lap['player']},{lap['car']},{lap['lap_time']},{lap['cuts']},{lap['split_count']},{lap['dynamic_track']})""")
    except IOError:
        print(f'SQLite file {sys.argv[2]} could not be opened.')


    
