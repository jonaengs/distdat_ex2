from tables_metadata import user_table_name, activity_table_name, trackpoint_table_name

# bestemmer om du kobler deg til server eller lokal database
local = True

# bestemmer om endringer lagres. 
# Hvis du tester og setter =True burde drop_tables også settes til True, ellers får du fort duplicate primary key errors
commit = False

# bestemmer om alle tabeller skal slettes først når create_tables kjøres
drop_tables = False

# Altitude default value (-777) substiute
altitude_default_value = "NULL"

# Activity transportation mode default/missing value
activity_tranportation_mode_default = None

""" NOTE: 
To get activity IDs to work correctly, we actually still execute the activity and user insertions, 
since these are only a small portion of the total data anyways. 
So every query is stored, but only trackpoint insertions are not executed when saving query 
"""
# Set to True to save all queries to a file instead of executing them
save_queries = True  # atm, queries are only saved if they are not read from file
read_queries_from_file = False
queries_file_path = "../queries/all_queries"

if local:
    DB_HOST="localhost"
    DB_DATABASE="db"
    DB_USER="db"
    DB_PASSWORD="db"
else:
    DB_HOST="tdt4225-02.idi.ntnu.no"
    DB_DATABASE="geolife_db"
    DB_USER="gruppe2admin"
    DB_PASSWORD="magnussitthemmeligepassord"