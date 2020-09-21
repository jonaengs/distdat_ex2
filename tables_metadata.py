user_table_name = "User"
user_table_settings = {
    "table_name": user_table_name,
    "fields": {
        "id": "VARCHAR(3) NOT NULL PRIMARY KEY",
        "has_labels": "BOOLEAN"
    }, 
    "auto_id": False
}
user_table_fields = tuple(user_table_settings["fields"].keys())

activity_table_name = "Activity"
activity_table_settings = {
    "table_name": activity_table_name,
    "fields": {
        "user_id": "VARCHAR(3)",
        "transportation_mode": "VARCHAR(30)",
        "start_date_time": "DATETIME NOT NULL",
        "end_date_time": "DATETIME NOT NULL"
    },
    "foreign_key": ("user_id", user_table_name)
}
activity_table_fields = tuple(activity_table_settings["fields"].keys())

trackpoint_table_name = "TrackPoint"
trackpoint_table_settings = {
    "table_name": trackpoint_table_name,
    "fields": {
        "activity_id": "INT",
        "lat": "DOUBLE NOT NULL",
        "lon": "DOUBLE NOT NULL",
        "altitude": "INT NOT NULL",
        "date_time": "DATETIME NOT NULL"
    },
    "foreign_key": ("activity_id", activity_table_name)
}
trackpoint_table_fields = tuple(trackpoint_table_settings["fields"].keys())

all_table_names = (user_table_name, activity_table_name, trackpoint_table_name)
all_table_settings = (user_table_settings, activity_table_settings, trackpoint_table_settings)
tables_info = zip(all_table_names, all_table_settings)
