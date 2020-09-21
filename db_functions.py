from DbConnector import DbConnector
from tabulate import tabulate
from tables_metadata import all_table_names

cursor = None

def create_table(table_name, fields, foreign_key=(), auto_id=True):
    """
    :param fields: {"field_name": "DATATYPE [NOT NULL]", ...}
        Ex: {"user_id": "VARCHAR(3)", "start_date_time": "DATETIME NOT NULL"}
    :param foreign_key (optional): ("field_name", "foreign_table_name")
        Ex: ("user_id", "User")
    """
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

    # Auto-incremented ID field is added unless otherwise specified
    if auto_id:
        query += "id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,"

    # All field names and their datatypes are added to the query
    for field, datatype in fields.items():
        query += f"{field} {datatype},"

    # Optional foreign key reference is added to the query
    if foreign_key:
        fk_name, fk_target = foreign_key 
        query += f"FOREIGN KEY ({fk_name}) REFERENCES {fk_target}(id),"

    query = query[:-1] + ")"
    
    print(query)
    cursor.execute(query)       

def drop_table(table_name):
    print(f"Dropping table {table_name}...")
    query = f"DROP TABLE {table_name}"
    cursor.execute(query)

def drop_all_tables():
    print("DROPPING ALL TABLES")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    for table_name in all_table_names:
        drop_table(table_name)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

def show_tables():
    cursor.execute("SHOW TABLES")
    rows = cursor.fetchall()
    print(tabulate(rows, headers=cursor.column_names))

def show_create_table(table_name):
    print(f"Table schema for table {table_name}")
    query = f"SHOW CREATE TABLE {table_name}"
    cursor.execute(query)
    rows = cursor.fetchall()
    print(tabulate(rows, headers=cursor.column_names))