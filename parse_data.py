import os
import sys
from collections import namedtuple
from datetime import datetime

from utils import *

def create_trackpoint(lat, longt, alt, date_time):
    return Trackpoint(float(lat), float(longt), float(alt), parse_tp_date_time(date_time))

def create_string_trackpoint(line):
    return Trackpoint(*extract_trackpoint_data(line))

def create_activity(line):
    start_date_time, end_date_time, activity = line.strip().split("\t")
    return Activity(parse_label_date_time(start_date_time), parse_label_date_time(end_date_time), activity, [])

def activity_from_trackpoints(first, last):
    return Activity(first.datetime, last.datetime, "N/A", [])

def trackpoint_from_line(line):
    return create_trackpoint(*extract_trackpoint_data(line))

def extract_trackpoint_data(line):
    data = line.strip().split(",")
    return data[:2]  + [data[3]] + [" ".join(data[-2:])]

def get_users():
    users = [User(i, False, {}) for i in range(num_users)]
    with open("dataset/labeled_ids.txt", mode="r") as labels_file:
        for uid in map(int, labels_file.readlines()):
            users[uid] = User(uid, True, {})
    return users

def get_user_data():
    for user in get_users():
        trackpoints_path = get_trackpoints_path(user.id)
        trackpoint_files = os.listdir(trackpoints_path)
        if user.has_labels:
            labels_file_path = get_labels_path(user.id)
            with open(labels_file_path) as labels_file:
                activities = {
                    (activity.start_date_time): activity 
                    for activity in map(create_activity, labels_file.readlines()[1:])
                }
        else:
            activities = {}
        for file_path in filter(is_below_max_size, (trackpoints_path + fn for fn in trackpoint_files)):
            with open(file_path, mode="r") as f:
                lines = f.readlines()[data_offset:]
                if len(lines) <= 2500:
                    trackpoints = None
                    if user.has_labels:
                        filename = os.path.basename(f.name).split(".")[0]
                        activity = activities.get(parse_fn_date_time(filename))
                        if activity:
                            trackpoints = activity.trackpoints
                    if trackpoints is None:
                        first_trackpoint, last_trackpoint = map(trackpoint_from_line, [lines[0], lines[-1]])
                        activity = activity_from_trackpoints(first_trackpoint, last_trackpoint)
                        activities[activity.start_date_time] = activity
                        trackpoints = activity.trackpoints
                    trackpoints += map(create_string_trackpoint, lines)
        user.activities.update(activities)
        yield user
