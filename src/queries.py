import sys
from tabulate import tabulate

from DbConnector import DbConnector

query_1 = """
            SELECT
                (SELECT COUNT(*) FROM User) AS Number_of_users,
                (SELECT COUNT(*) FROM Activity) AS Number_of_activities,
                (SELECT COUNT(*) FROM TrackPoint) AS Number_of_trackpoints
        """

query_2 = """ 
            SELECT AVG(Number_of_activities) AS Average_activities_per_user 
            FROM (
                SELECT user_id, Count(user_id) as Number_of_activities
                FROM Activity
                GROUP BY user_id
            ) 
            AS Number_of_activities
        """

query_3 = """
            SELECT user_id, Count(user_id) as Number_of_activities
            FROM Activity
            GROUP BY user_id
            ORDER BY Count(user_id) DESC
            LIMIT 20
        """

query_4 = """
            SELECT user_id
            FROM Activity
            WHERE transportation_mode = "taxi"
        """

query_5 = """
            SELECT transportation_mode, Count(transportation_mode) as Number_of_transportation_modes
            FROM Activity
            WHERE transportation_mode is not NULL
            GROUP BY transportation_mode
            ORDER BY Number_of_transportation_modes DESC
        """

query_6 = """
            SELECT
                (SELECT YEAR(start_date_time) AS Year
                FROM Activity
                WHERE YEAR(end_date_time) = YEAR(start_date_time)
                GROUP BY Year
                ORDER BY COUNT(*) DESC
                LIMIT 1) AS Most_activities_year, 

                (SELECT YEAR(start_date_time) AS Year
                FROM Activity
                WHERE YEAR(end_date_time) = YEAR(start_date_time)
                GROUP BY Year
                ORDER BY ROUND(SUM(TIMEDIFF(end_date_time, start_date_time)) / 3600) DESC
                LIMIT 1) AS Most_hours_year, 

                (SELECT IF(Most_activities_year = Most_hours_year, "Yes", "No")) 
                AS Years_are_equal
        """

query_7 = """
            SELECT
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

query_8 = """
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

query_9 = """
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

query_10 = """
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

query_11 = """
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

if __name__ == '__main__':
    with DbConnector() as cursor:
        for i in range(1, 12):
            query = getattr(sys.modules[__name__], f"query_{i}")
            cursor.execute(query)
            rows = cursor.fetchall()
            print(f"Query {i}:\n\n" +
                  tabulate(rows, headers=cursor.column_names) + "\n\n")
