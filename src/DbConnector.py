import sys
import mysql.connector as mysql
from traceback import print_exception
from settings import *

class DbConnector:
    def __enter__(self, HOST=DB_HOST, DATABASE=DB_DATABASE, USER=DB_USER, PASSWORD=DB_PASSWORD):
        # Connect to the database
        self.db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=3306)
                
        # Get the db cursor
        self.cursor = self.db_connection.cursor()
        print("Connected to:", self.db_connection.get_server_info())
        
        # get database information
        self.cursor.execute("select database();")
        database_name = self.cursor.fetchone()
        print("You are connected to the database:", database_name)
        print("-----------------------------------------------\n")

        return self.cursor

    def __exit__(self, exception_type, exception_val, traceback):
        if exception_type is not None:
            print("Encountered exception:\n")
            print_exception(exception_type, exception_val, traceback)
        
        print("\n-----------------------------------------------")
        if getattr(self, "db_connection", None):
            self.cursor.close()
            self.db_connection.close()
            print("Connection to %s closed" % self.db_connection.get_server_info())
        else:
            print("DB connection not closed (none found)")
