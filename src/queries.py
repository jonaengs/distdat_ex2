from DbConnector import DbConnector
from tabulate import tabulate
from tables_metadata import all_table_names

# with DbConnector as cursor


class QueryRunner:
    @staticmethod
    def query_printer(query_number, rows, column_names):
        print("Query %s:\n" % query_number)
        print(tabulate(rows, headers=column_names))
        print("\n")

    def query_1(self):
        table_name_mapping = {
            "User": "users", "Activity": "activities", "TrackPoint": "trackpoints"}

        for table_name in all_table_names:
            # Kanskje bytt ut * med ID elns
            query = "SELECT COUNT(*) AS Number_of_%s FROM %s"
            self.cursor.execute(
                query % (table_name_mapping[table_name], table_name))
            rows = self.cursor.fetchall()

            self.query_printer(query_number=1, rows=rows,
                               column_names=self.cursor.column_names)

    def query_2(self):
        # Find the average number of activities per user.
        query = """SELECT AVG(Number_of_activities) AS Average_activities_per_user FROM (
                        SELECT user_id, Count(user_id) as Number_of_activities
                        FROM Activity
                        GROUP BY user_id
                    ) AS Number_of_activities;"""
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.query_printer(query_number=2, rows=rows,
                           column_names=self.cursor.column_names)

    def query_3(self):
        # Find the top 20 users with the highest number of activities
        query = """SELECT user_id, Count(user_id) as Number_of_activities
                    FROM Activity
                    GROUP BY user_id
                    ORDER BY Count(user_id) DESC
                    LIMIT 20;"""
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.query_printer(query_number=3, rows=rows,
                           column_names=self.cursor.column_names)

    def query_4(self):
        # Find all users who have taken a taxi.

        transportation_mode = "taxi"
        query = """SELECT user_id
                    FROM Activity
                    WHERE transportation_mode = "%s"
                ;""" % transportation_mode
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.query_printer(query_number=4, rows=rows,
                           column_names=self.cursor.column_names)

    def query_5(self):
        # Find the top 20 users with the highest number of activities

        query = """SELECT transportation_mode, Count(transportation_mode) as Number_of_transportation_modes
                    FROM Activity
                    WHERE transportation_mode is not NULL
                    GROUP BY transportation_mode
                    ORDER BY Number_of_transportation_modes DESC
                ;"""
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.query_printer(query_number=5, rows=rows,
                           column_names=self.cursor.column_names)

    def query_6(self):
        # a) Find the year with the most activities.

        query_a = """SELECT YEAR(start_date_time) AS Year   
                    FROM Activity
                    WHERE YEAR(end_date_time) = YEAR(start_date_time)
                    GROUP BY Year
                    ORDER BY COUNT(*) DESC
                    LIMIT 1
                ;"""

        self.cursor.execute(query_a)
        rows_a = self.cursor.fetchall()

        self.query_printer(query_number="6a", rows=rows_a,
                           column_names=self.cursor.column_names)

        # b) Is this also the year with most recorded hours?

        query_b = """
                    SELECT YEAR(start_date_time) AS Year
                    FROM Activity
                    WHERE YEAR(end_date_time) = YEAR(start_date_time)
                    GROUP BY Year
                    ORDER BY ROUND(SUM(TIMEDIFF(end_date_time, start_date_time)) / 3600)
                    LIMIT 1;
                """
        self.cursor.execute(query_b)
        rows_b = self.cursor.fetchall()

        self.query_printer(query_number="6b", rows=rows_b,
                           column_names=self.cursor.column_names)

        # (2008 != 2000)
        is_OR_is_not = "IS" if rows_a[0][0] == rows_b[0][0] else "is NOT"
        print("6b) The year with most activities",
              is_OR_is_not, "the year with most recorded hours")

    def query_7(self):
        # a) Find the year with the most activities.

        query = """SELECT
                        Activity.user_id,
                        SUM(ST_Distance_Sphere(
                            ST_GeomFromText(ST_AsText(Point(From_points.lon, From_points.lat))),
                            ST_GeomFromText(ST_AsText(Point(To_points.lon, To_points.lat)))) / 1000 AS Total_distance_km
                    FROM TrackPoint AS From_points
                        INNER JOIN TrackPoint AS To_points
                        ON From_points.id = To_points.id - 1
                        INNER JOIN Activity
                        ON From_points.activity_id = Activity.id
                    WHERE Activity.user_id = 112 AND Activity.transportation_mode = "walk";
                ;"""

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.query_printer(query_number="7", rows=rows,
                           column_names=self.cursor.column_names)

    def query_9(self):
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
                ;"""
        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.query_printer(query_number="9", rows=rows,
                           column_names=self.cursor.column_names)

    def query_10(self):
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
                ;"""
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.query_printer(query_number=10, rows=rows,
                           column_names=self.cursor.column_names)


def main():
    program = QueryRunner()
    connector = DbConnector()
    program.connection = connector
    with connector as cursor:
        program.cursor = cursor

        # program.query_1()
        # program.query_2()
        # program.query_3()
        # program.query_4()
        # program.query_5()
        # program.query_6()
        # program.query_7()
        # program.query_9()
        # program.query_10()


if __name__ == '__main__':
    main()
