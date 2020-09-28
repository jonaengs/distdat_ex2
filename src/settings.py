# bestemmer om du kobler deg til server eller lokal database
local = False  

# bestemmer om endringer lagres. 
# Hvis du tester og setter =True burde drop_tables også settes til True, ellers får du fort duplicate primary key errors
commit = True  

# bestemmer om alle tabeller skal slettes først når create_tables kjøres
drop_tables = True  

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