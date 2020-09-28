from DbConnector import DbConnector
from tabulate import tabulate

# with DbConnector as cursor
class QueryRunner:
    def query_printer(self, query_number, rows, column_names):
        print("Query %s:\n" % query_number)
        print(tabulate(rows, headers=column_names))
        print("\n")

    def create_table(self, table_name):
        query = """CREATE TABLE IF NOT EXISTS %s (
                   id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                   name VARCHAR(30))
                """
        # This adds table_name to the %s variable and executes the query
        self.cursor.execute(query % table_name)
        self.connection.db_connection.commit()

    def insert_data(self, table_name):
        names = ['Bobby', 'Mc', 'McSmack', 'Board', 'Mc']
        for name in names:
            # Take note that the name is wrapped in '' --> '%s' because it is a string,
            # while an int would be %s etc
            query = "INSERT INTO %s (name) VALUES ('%s')"
            self.cursor.execute(query % (table_name, name))
        self.connection.db_connection.commit()

    def query_1(self):
        # table_names = ["User", "Activity", "TrackPoint"]
        # table_name_mapping = {"User": "users", "Activity": "activities", "TrackPoint": "trackpoints"}
        table_names = ["Person"]
        table_name_mapping = {"Person": "persons"}
        
        for table_name in table_names:
            query = "SELECT COUNT(*) AS Number_of_%s FROM %s" # Kanskje bytt ut * med ID elns
            self.cursor.execute(query % (table_name_mapping[table_name], table_name))
            rows = self.cursor.fetchall()

            self.query_printer(query_number=1, rows=rows, column_names=self.cursor.column_names)
    
    def query_2(self):
        # Find the average number of activities per user.

        # query = """SELECT AVG(Number_of_activities) AS Average_activities_per_user FROM (
        #                 SELECT user_id, Count(user_id) as Number_of_activities
        #                 FROM Acvtivity
        #                 GROUP BY user_id
        #             ) AS Number_of_activities;"""
        query = """SELECT AVG(Number_of_names) AS Average_number_of_names FROM (
                        SELECT name, Count(name) as Number_of_names
                        FROM Person
                        GROUP BY name
                    ) AS test_names;"""      
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.query_printer(query_number=2, rows=rows, column_names=self.cursor.column_names)

    def query_3(self):
        # Find the top 20 users with the highest number of activities
        
        # query = """SELECT user_id, Count(user_id) as Number_of_activities
        #             FROM Activity
        #             GROUP BY user_id
        #             ORDER BY Count(user_id) DESC
        #             LIMIT 20;"""
        query = """SELECT name, Count(name) as Number_of_names
                    FROM Person
                    GROUP BY name
                    ORDER BY Count(name) DESC
                    LIMIT 3;"""
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.query_printer(query_number=3, rows=rows, column_names=self.cursor.column_names)
    
    def query_4(self):
        # Find all users who have taken a taxi.

        transportation_mode = "taxi" # -> Taxi is found in transportation_mode???? (not listed as "one of the possible values")

        # query = """SELECT user_id, transportation_mode
        #             FROM Activity
        #             WHERE transportation_mode = "%s";""" % transportation_mode
        name = "Bobby"
        query = """SELECT id, name
                    FROM Person
                    WHERE name = "%s";""" % name
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.query_printer(query_number=4, rows=rows, column_names=self.cursor.column_names)

    def query_5(self):
        # Find the top 20 users with the highest number of activities
        # HER ANTAR JEG AT DET IKKE FINNES NOEN MED NULL

        # query = """SELECT transportation_mode, Count(transportation_mode) as Number_of_transportation_modes
        #             FROM Activity
        #             GROUP BY transportation_mode
        #             ORDER BY Count(transportation_mode) DESC;"""
        query = """SELECT id, Count(id) as Number_of_ids
                    FROM Person
                    GROUP BY id
                    ORDER BY Count(id) ASC;"""
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.query_printer(query_number=5, rows=rows, column_names=self.cursor.column_names)

    def query_6(self):
        # Find the top 20 users with the highest number of activities
        
        #SELECT EmployeeID, DATE_FORMAT(BirthDate, "%Y") FROM Employees;

        # query = """SELECT transportation_mode, Count(transportation_mode) as Number_of_transportation_modes
        #             FROM Activity
        #             GROUP BY transportation_mode
        #             ORDER BY Count(transportation_mode) DESC;"""
        query = """SELECT id, Count(id) as Number_of_ids
                    FROM Person
                    GROUP BY id
                    ORDER BY Count(id) ASC;"""
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.query_printer(query_number=6, rows=rows, column_names=self.cursor.column_names)

    def drop_table(self, table_name):
        # print("Dropping table %s..." % table_name)
        query = "DROP TABLE %s"
        self.cursor.execute(query % table_name)

    def show_tables(self):
        self.cursor.execute("SHOW TABLES")
        rows = self.cursor.fetchall()
        # print(tabulate(rows, headers=self.cursor.column_names))


def main():
    connector = DbConnector()
    with connector as cursor:
        program = QueryRunner()
        program.connection = connector
        program.cursor = cursor
        program.create_table(table_name="Person")
        program.insert_data(table_name="Person")
        program.query_1()
        program.query_2()
        program.query_3()
        program.query_4()
        program.query_5()
        program.show_tables()
        program.drop_table(table_name="Person")
        # Check that the table is dropped
        program.show_tables()


if __name__ == '__main__':
    main()
