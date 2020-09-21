from tables_metadata import *
from settings import *
import db_functions as db_manager

def main():
    for table_name, table_settings in tables_info:
        db_manager.create_table(**table_settings)
        db_manager.show_create_table(table_name=table_name)

    # db_manager.drop_all_tables()

    db_manager.show_tables()
    if commit:
        db_connection.commit()

if __name__ == '__main__':
    with db_manager.connection as cursor:
        db_manager.cursor = cursor
        main()
