from DbConnector import DbConnector
from tabulate import tabulate
from tables_metadata import all_table_names

def query_printer(query_number, rows, column_names):
    print("Query %s:\n" % query_number)
    print(tabulate(rows, headers=column_names))
    print("\n")

def query_1(cursor):
    table_name_mapping = {
        "User": "users", "Activity": "activities", "TrackPoint": "trackpoints"}

    for table_name in all_table_names:
        # Kanskje bytt ut * med ID elns
        query = "SELECT COUNT(*) AS Number_of_%s FROM %s"
        cursor.execute(
            query % (table_name_mapping[table_name], table_name))
        rows = cursor.fetchall()

        query_printer(query_number=1, rows=rows,
                            column_names=cursor.column_names)

def query_2(cursor):
    # Find the average number of activities per user.
    query = """ SELECT AVG(Number_of_activities) AS Average_activities_per_user 
                FROM (
                    SELECT user_id, Count(user_id) as Number_of_activities
                    FROM Activity
                    GROUP BY user_id
                ) 
                AS Number_of_activities
            """
    cursor.execute(query)
    rows = cursor.fetchall()

    query_printer(query_number=2, rows=rows,
                        column_names=cursor.column_names)

def query_3(cursor):
    # Find the top 20 users with the highest number of activities
    query = """SELECT user_id, Count(user_id) as Number_of_activities
                FROM Activity
                GROUP BY user_id
                ORDER BY Count(user_id) DESC
                LIMIT 20"""
    cursor.execute(query)
    rows = cursor.fetchall()

    query_printer(query_number=3, rows=rows,
                        column_names=cursor.column_names)

def query_4(cursor):
    # Find all users who have taken a taxi.

    transportation_mode = "taxi"
    query = """SELECT user_id
                FROM Activity
                WHERE transportation_mode = "%s"
            """ % transportation_mode
    cursor.execute(query)
    rows = cursor.fetchall()

    query_printer(query_number=4, rows=rows,
                        column_names=cursor.column_names)

def query_5(cursor):
    # Find the top 20 users with the highest number of activities

    query = """SELECT transportation_mode, Count(transportation_mode) as Number_of_transportation_modes
                FROM Activity
                WHERE transportation_mode is not NULL
                GROUP BY transportation_mode
                ORDER BY Number_of_transportation_modes DESC
            """
    cursor.execute(query)
    rows = cursor.fetchall()

    query_printer(query_number=5, rows=rows,
                        column_names=cursor.column_names)

def query_6(cursor):
    # a) Find the year with the most activities.
    query_a = """SELECT YEAR(start_date_time) AS Year   
                FROM Activity
                WHERE YEAR(end_date_time) = YEAR(start_date_time)
                GROUP BY Year
                ORDER BY COUNT(*) DESC
                LIMIT 1
            """

    cursor.execute(query_a)
    rows_a = cursor.fetchall()

    query_printer(query_number="6a", rows=rows_a,
                        column_names=cursor.column_names)

    # b) Find year with most recorded hours
    query_b = """
                SELECT YEAR(start_date_time) AS Year
                FROM Activity
                WHERE YEAR(end_date_time) = YEAR(start_date_time)
                GROUP BY Year
                ORDER BY ROUND(SUM(TIMEDIFF(end_date_time, start_date_time)) / 3600) DESC
                LIMIT 1
            """
    cursor.execute(query_b)
    rows_b = cursor.fetchall()

    query_printer(query_number="6b", rows=rows_b,
                        column_names=cursor.column_names)

    is_or_is_not = "IS" if rows_a[0][0] == rows_b[0][0] else "is NOT"
    print("6b) The year with most activities",
            is_or_is_not, "the year with most recorded hours")

def query_7(cursor):
    query = """SELECT
                    Activity.user_id,
                    SUM(ST_Distance_Sphere(
                        ST_GeomFromText(ST_AsText(Point(From_points.lon, From_points.lat))),
                        ST_GeomFromText(ST_AsText(Point(To_points.lon, To_points.lat))))) / 1000 AS Total_distance_km
                FROM TrackPoint AS From_points
                    INNER JOIN TrackPoint AS To_points
                    ON From_points.id = To_points.id - 1
                    INNER JOIN Activity
                    ON From_points.activity_id = Activity.id
                WHERE Activity.user_id = 112 AND Activity.transportation_mode = "walk"
            """

    cursor.execute(query)
    rows = cursor.fetchall()

    query_printer(query_number="7", rows=rows,
                        column_names=cursor.column_names)

def query_8(cursor):
    query = """
                SELECT 
                    Activity.user_id, 
                    SUM(To_points.altitude - From_points.altitude) / 3.2808 
                        AS Altitude_gained
                FROM TrackPoint AS From_points
                    INNER JOIN TrackPoint AS To_points
                    ON From_points.id = To_points.id - 1
                        AND From_points.activity_id = To_points.activity_id
                        AND To_points.altitude > From_points.altitude
                    INNER JOIN Activity
                    ON From_points.activity_id = Activity.id
                GROUP BY Activity.user_id
                ORDER BY Altitude_gained DESC
                LIMIT 20
            """

    cursor.execute(query)
    rows = cursor.fetchall()

    query_printer(query_number="8", rows=rows,
                        column_names=cursor.column_names)

def query_9(cursor):
    query = """
                SELECT Activity.user_id, Count(Activity.id) as Num_invalid
                FROM TrackPoint AS From_points
                    INNER JOIN TrackPoint AS To_points
                    ON From_points.id = To_points.id - 1
                        AND From_points.activity_id = To_points.activity_id 
                    INNER JOIN Activity
                    ON From_points.activity_id = Activity.id
                WHERE
                    TIMEDIFF(To_points.date_time, From_points.date_time) >= TIME('00:05:00')
                GROUP BY user_id
            """
    
    cursor.execute(query)
    rows = cursor.fetchall()

    query_printer(query_number="9", rows=rows,
                        column_names=cursor.column_names)

def query_10(cursor):
    # Find the users who have tracked an activity in the Forbidden City of Beijing (lat 39.916, lon 116.397)
    # Exaclty lat=39.916 and lon=116.397 gives no answer, so we rounded the values to two decimals and made a range

    query = """
                SELECT DISTINCT user_id
                FROM Activity as A
                INNER JOIN (
                    SELECT activity_id
                    FROM TrackPoint
                    WHERE 
                        lat BETWEEN 39.916 AND 39.918 
                        AND 
                        lon BETWEEN 116.396 AND 116.398
                )
                as TP on A.id=TP.activity_id
            """
    cursor.execute(query)
    rows = cursor.fetchall()

    query_printer(query_number=10, rows=rows,
                        column_names=cursor.column_names)

def query_11(cursor):
    # Find all users who have registered transportation_mode and their most used transportation_mode
    query = """
                SELECT DISTINCT a.user_id, a.transportation_mode
                FROM Activity a
                WHERE a.transportation_mode = 
                ( /* Selects most popular transportation mode for a given user */
                    SELECT a2.transportation_mode 
                    FROM Activity a2
                    WHERE a2.user_id = a.user_id
                    GROUP BY a2.transportation_mode
                    ORDER BY 
                        COUNT(a2.transportation_mode) DESC, 
                        a2.transportation_mode ASC
                    LIMIT 1
                )
            """
    
    cursor.execute(query)
    rows = cursor.fetchall()

    query_printer(query_number=11, rows=rows, column_names=cursor.column_names)


def main():
    connector = DbConnector()
    with connector as cursor:
        for query in [query_1, query_2, query_3, query_4, query_5, query_6, query_7, query_8, query_9, query_10, query_11]:
            query(cursor)

if __name__ == '__main__':
    main()
