from DbConnector import DbConnector
from tabulate import tabulate


class TableCreator:

    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor

    # Param fields: {"field_name": "DATATYPE [NOT NULL]", ...}
    # Ex: {"user_id": "VARCHAR(3)", "start_date_time": "DATETIME NOT NULL"}
    # Param foreign_key (optional): ("field_name", "foreign_table_name")
    # EX: ("user_id", "User")
    def create_table(self, table_name, fields, foreign_key=(), auto_id=True):

        query = "CREATE TABLE IF NOT EXISTS %s ("

        # Auto-incremented ID field is added unless otherwise specified
        if auto_id:
            query += "id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,"

        # All field names and their datatypes are added to the query
        for field, datatype in fields.items():
            query += "%s %s," % (field, datatype)

        # Optional foreign key reference is added to the query
        if foreign_key:
            query += "FOREIGN KEY (%s) REFERENCES %s(id)," % (
                foreign_key[0], foreign_key[1])

        query = query[:-1] + ")"
        print(query)
        # This adds table_name to the %s variable and executes the query
        self.cursor.execute(query % table_name)
        # self.db_connection.commit()

    def drop_table(self, table_name):
        print("Dropping table %s..." % table_name)
        query = "DROP TABLE %s"
        self.cursor.execute(query % table_name)

    def show_tables(self):
        self.cursor.execute("SHOW TABLES")
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=self.cursor.column_names))

    def show_create_table(self, table_name):
        print("Table schema for table %s" % table_name)
        query = "SHOW CREATE TABLE %s"
        self.cursor.execute(query % table_name)
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=self.cursor.column_names))


def main():
    program = None
    try:
        program = TableCreator()
        user_table = "User"
        activity_table = "Activity"
        trackpoint_table = "TrackPoint"
        program.create_table(table_name=user_table,
                             fields={
                                 "id": "VARCHAR(3) NOT NULL PRIMARY KEY",
                                 "has_labels": "BOOLEAN"}, auto_id=False)
        program.show_create_table(table_name=user_table)
        program.create_table(table_name=activity_table,
                             fields={
                                 "user_id": "VARCHAR(3)",
                                 "transportation_mode": "VARCHAR(30)",
                                 "start_date_time": "DATETIME NOT NULL",
                                 "end_date_time": "DATETIME NOT NULL"},
                             foreign_key=("user_id", user_table))
        program.show_create_table(table_name=activity_table)
        program.create_table(table_name=trackpoint_table,
                             fields={
                                 "activity_id": "INT",
                                 "lat": "DOUBLE NOT NULL",
                                 "lon": "DOUBLE NOT NULL",
                                 "altitude": "INT NOT NULL",
                                 "date_days": "DOUBLE NOT NULL",
                                 "date_time": "DATETIME NOT NULL"
                             },
                             foreign_key=("activity_id", activity_table))
        # program.drop_table(table_name=trackpoint_table)
        # program.drop_table(table_name=activity_table)
        # program.drop_table(table_name=user_table)
        # Check that the table is dropped
        program.show_tables()
    except Exception as e:
        print("ERROR: Failed to use database:", e)
    finally:
        if program:
            program.connection.close_connection()


if __name__ == '__main__':
    main()
