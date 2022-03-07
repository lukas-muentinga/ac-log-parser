# ac-log-parser
Parser for lap times from Assetto Corsa logs to SQLite 3 DB.

## DB Init
python3 create_ac_lap_table.py [db_filepath] [table_name]

## DB Update on Log Rotate
python3 ac_log_parser.py [log-filepath] [sqlite-filepath]