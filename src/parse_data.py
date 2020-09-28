import os
import sys
from collections import namedtuple
from datetime import datetime
from settings import altitude_default_value as altitude_default
from settings import activity_tranportation_mode_default as transport_default

from utils import *

def create_trackpoint(lat, longt, alt, date_time):
    return Trackpoint(float(lat), float(longt), alt, parse_tp_date_time(date_time))

def create_string_trackpoint(line):
    trackpoint_data = extract_trackpoint_data(line)
    # surround datetiem with single-quotes for easy mysql-insertion
    trackpoint_data[-1] = "'" + trackpoint_data[-1] + "'"
    return Trackpoint(*trackpoint_data)

def create_activity(line):
    start_date_time, end_date_time, activity = line.strip().split("\t")
    activity = activity if activity else transport_default
    return Activity(activity, parse_label_date_time(start_date_time), parse_label_date_time(end_date_time), [])

def activity_from_trackpoints(first, last):
    return Activity(transport_default, first.datetime, last.datetime, [])

def trackpoint_from_line(line):
    return create_trackpoint(*extract_trackpoint_data(line))

def extract_trackpoint_data(line):
    data = line.strip().split(",")
    lat, longt = data[:2]
    alt = data[3]
    datetime = " ".join(data[-2:])
    alt = alt if alt != "-777" else altitude_default

    return [lat, longt, alt, datetime]

def get_users(max_count=None):
    users = [User(i, False, []) for i in range(num_users)]
    with open("../dataset/labeled_ids.txt", mode="r") as labels_file:
        for uid in map(int, labels_file.readlines()):
            users[uid] = User(uid, True, [])
    return users[:max_count if max_count is not None else len(users)]

def get_user_data(max_count=None):
    for user in get_users(max_count):
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

        user.activities.extend([a for a in activities.values() if a.trackpoints])
        yield user
