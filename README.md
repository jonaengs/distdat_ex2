# Exercise 2, TDT4225 Store, distribuerte datamenger

## Running the code
Make sure you have a python3.6 or later installed.

Open a terminal of your choice.

Navigate into the source folder:
```
$ cd src
```

To create tables and insert data, run:
```
$ python setup_tables.py
```

To execute the queries, run:
```
$ python queries.py
```


# DistDat - Øving 2
Exercise 2, TDT4225 Store, distribuerte datamenger

# MySQL
## Installasjon
```
$ sudo apt update
$ sudo apt install mysql-server
$ sudo mysql_secure_installation
```

Hvis du kjører linux i WSL må også kjøre følgende:\
```
$ sudo /etc/init.d/mysql start
```

Vi setter alle verdier (brukernavn, passord, db-navn, ...) til "mysql", så slipper vi å styre så mye med det.