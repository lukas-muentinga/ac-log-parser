import sqlite3, sys

# Usage: python3 create_ac_lap_table.py [db_filepath] [table_name]

if __name__ == '__main__':
    con = sqlite3.connect(sys.argv[1])
    cur = con.cursor()
    cur.execute(f"""CREATE TABLE {sys.argv[2]} 
                    (player text,
                    car text,
                    lap_time int,
                    cuts int,
                    split_count int,
                    dynamic_track text)""")