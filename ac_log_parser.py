######################################################################
# REGEX PARSER FOR ASSETTO CORSO LOG FILES
# ----------------------------------------
#
######################################################################

import re, sys

LAP_END_FINDER_RE = r"""Dispatching\sTCP\smessage\sto\s(?P<car>\S+)\s\(\d\)\s\[(?P<player>\S+).*\n
                        Car.onLapCompleted\n
                        LAP\s\S+\s(?P<time>\S+)\n
                        SPLIT\sCOUNT:\s(?P<split_count>\S+)\n
                        Dynamic\strack\s(?P<dynamic_track>\S+)\n
                        Result.OnLapCompleted\.\sCuts:\s(?P<cuts>\S+)\n"""

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


    lap_end_parsed = [m.groupdict() for m in re.finditer(lap_end_finder_pattern, log_content)]
    print(lap_end_parsed)
