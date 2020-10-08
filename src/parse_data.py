import os
from collections import defaultdict
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
    start_date_time, end_date_time = map(str, map(parse_label_date_time, (start_date_time, end_date_time)))
    return Activity(activity, start_date_time, end_date_time, [])


def activity_from_trackpoints(first, last):
    return Activity(transport_default, get_tp_datetime_str(first), get_tp_datetime_str(last), [])


def get_tp_datetime_str(line):
    data = line.strip().split(",")
    return " ".join(data[-2:])


def extract_trackpoint_data(line):
    data = line.strip().split(",")
    lat, longt = data[:2]
    alt = data[3]
    datetime = " ".join(data[-2:])
    alt = alt if alt != "-777" else altitude_default

    return [lat, longt, alt, datetime]


def get_has_labels(max_count=None):
    has_labels = defaultdict(bool)
    with open("../dataset/labeled_ids.txt", mode="r") as labels_file:
        for uid in map(int, labels_file.readlines()):
            has_labels[uid] = True
    return has_labels


def get_user_data(max_count=None):
    has_labels = get_has_labels(max_count)
    for i in range(num_users):
        user = User(i, has_labels[i], [])
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
                    activity_trackpoints = None
                    if user.has_labels:
                        activity = activities.get(get_tp_datetime_str(lines[0]))
                        if activity:
                            activity_trackpoints = activity.trackpoints
                    if activity_trackpoints is None:
                        activity = activity_from_trackpoints(lines[0], lines[-1])
                        activities[activity.start_date_time] = activity
                    activity.trackpoints.extend(map(create_string_trackpoint, lines))

        user.activities.extend([a for a in activities.values() if a.trackpoints])
        yield user
