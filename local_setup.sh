#!/bin/bash

# variabler
DATABASE="db"
PASSWORD="db"

# Standard
sudo apt update
sudo apt upgrade

# Fiks lokal database
sudo apt install mysql-server
sudo /etc/init.d/mysql start # bare nødvendig om du kjører WSL, men gjør ingen skade ellers tror jeg
sudo mysql -e "UPDATE mysql.user SET Password=PASSWORD('${PASSWORD}') WHERE User='root';FLUSH PRIVILEGES;"
sudo mysql -uroot -p${PASSWORD} -e "CREATE DATABASE ${DATABASE};"
sudo mysql -uroot -p${PASSWORD} -e "CREATE USER '${DATABASE}'@'localhost' IDENTIFIED BY '${PASSWORD}';"
sudo mysql -uroot -p${PASSWORD} -e "GRANT ALL PRIVILEGES ON ${DATABASE}.* TO '${DATABASE}'@'localhost';"
sudo mysql -uroot -p${PASSWORD} -e "FLUSH PRIVILEGES;"
sudo service mysql restart

# Fiks python
sudo apt-get upgrade python3
sudo apt install python3-pip
python3 -m pip install virtualenv
python3 -m virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
export PYTHONDONTWRITEBYTECODE=1  # ikke lag .pyc-filer