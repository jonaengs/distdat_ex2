# bestemmer om du kobler deg til server eller lokal database
local = False

# bestemmer om endringer lagres. 
# Hvis du tester og setter =True burde drop_tables også settes til True, ellers får du fort duplicate primary key errors
commit = True

# bestemmer om alle tabeller skal slettes først når create_tables kjøres
drop_tables = True

# Altitude default value (-777) substiute
altitude_default_value = "NULL"

# Activity transportation mode default/missing value
activity_tranportation_mode_default = None

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