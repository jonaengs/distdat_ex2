from tables_metadata import *
import settings
import db_functions as db_manager
from parse_data import get_user_data

def main():
    if settings.drop_tables:
        db_manager.drop_all_tables()

    for table_name, table_settings in tables_info:
        db_manager.create_table(**table_settings)
        db_manager.show_create_table(table_name=table_name)

    print("-------- Inserting user data --------")
    for user in get_user_data(10):
        db_manager.insert_user(user)
        for activity in user.activities:
            db_manager.insert_activity(activity, user.id)
            activity_id = cursor.lastrowid
            db_manager.insert_trackpoints(activity.trackpoints, activity_id)
        print(f"Insert user {user.id} data ok")

    if settings.commit:
        db_manager.commit()

if __name__ == '__main__':
    with db_manager.connection as cursor:
        db_manager.cursor = cursor
        main()
