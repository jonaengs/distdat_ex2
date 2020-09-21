import os
import sys
from collections import namedtuple
from datetime import datetime
from pprint import pprint

max_line_size = 114  # max line size i 000s første fil iaf
data_offset = 6
max_lines_limit = 2500 + data_offset
num_users = 182
data_path = "dataset/Data"
get_trackpoints_path = lambda uid: f"{data_path}/{uid:03}/Trajectory/"
get_labels_path = lambda uid: f"{data_path}/{uid:03}/labels.txt"
datetime_format = r"%Y-%m-%d %H:%M:%S"
parse_date_time = lambda date, time: datetime.strptime(f"{date} {time}", datetime_format)
trackpoint_data_indices = [0, 1, 3, 5, 6]
max_file_size_limit = max_line_size * max_lines_limit
is_below_max_size = lambda fp: os.stat(fp).st_size < max_file_size_limit

User = namedtuple("User", ("id", "has_labels"))
Trackpoint = namedtuple("Trackpoint", ("latitude", "longtitude", "altitude", "datetime"))
Label = namedtuple("Label", ("start_datetime", "end_datetime", "mode"))
Activity = namedtuple("Activity", ("start_date_time", "end_date_time", "transportation_mode", "trackpoints"))

def create_trackpoint(lat, longt, alt, date, time):
    return Trackpoint(float(lat), float(longt), int(alt), parse_date_time(date, time))

def create_label(start_date, start_time, end_date, end_time, activity):
    return Label(parse_date_time(start_date, start_time), parse_date_time(end_date, end_time), activity)

def create_activity(start_date, start_time, end_date, end_time, activity):
    return Activity(parse_date_time(start_date, start_time), parse_date_time(end_date, end_time), activity, [])

def activity_from_trackpoints(first, last):
    return Activity(first.datetime, last.datetime, "N/A", [])

def trackpoint_from_line(line):
    data = line.strip().split(",")
    return create_trackpoint(*(data[i] for i in trackpoint_data_indices))

users = [User(i, False) for i in range(num_users)]
with open("dataset/labeled_ids.txt", mode="r") as labels_file:
    for uid in map(int, labels_file.readlines()):
        users[uid] = User(uid, True)

for user in users[0:1]:
    print(user)
    trackpoints_path = get_trackpoints_path(user.id)
    trackpoint_files = os.listdir(trackpoints_path)
    if user.has_labels:
        labels_file_path = get_labels_path(user.id)
        with open(labels_file_path) as labels_file:
            activities = {(activity.start_datetime): activity for activity in map(create_activity, labels_file.readlines()[1:])}
    else:
        activities = {}
    for file_path in filter(is_below_max_size, (trackpoints_path + fn for fn in trackpoint_files)):
        with open(file_path) as f:
            lines = f.readlines()[data_offset:]
            first_trackpoint = trackpoint_from_line(lines[0])
            trackpoints = None
            if user.has_labels:
                activity = activities.get((first_trackpoint.datetime))
                if activity:
                    trackpoints = activity.trackpoints
            if trackpoints is None:
                activity = activity_from_trackpoints(first_trackpoint, trackpoint_from_line(lines[-1]))
                activities[activity.start_date_time] = activity
                trackpoints = activity.trackpoints
            trackpoints += lines


    pprint(activities.keys())



