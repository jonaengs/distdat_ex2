import os
import sys
from collections import namedtuple
from datetime import datetime

max_line_size = 114  # max line size i 000s første fil iaf
data_offset = 6
max_lines_limit = 2500 + data_offset
num_users = 182
data_path = "dataset/Data"
get_trackpoints_path = lambda uid: f"{data_path}/{uid:03}/Trajectory/"
datetime_format = r"%Y-%m-%d %H:%M:%S"
data_indices = [0, 1, 3, 5, 6]
max_file_size_limit = max_line_size * max_lines_limit

Activity = namedtuple("Activity", ("transportation_mode", "start_date_time", "end_date_time"))
Trackpoint = namedtuple("Trackpoint", ("latitude", "longtitude", "altitude", "datetime"))
Label = namedtuple("Label", ("start_time", "end_time", "mode"))
User = namedtuple("User", ("id", "has_labels"))

strptime = datetime.strptime
def create_trackpoint(lat, longt, alt, date, time):
    return Trackpoint(float(lat), float(longt), int(alt), strptime(" ".join((date, time)), datetime_format))

users = [User(i, False) for i in range(num_users)]
with open("dataset/labeled_ids.txt", mode="r") as labels_file:
    for uid in map(int, labels_file.readlines()):
        users[uid] = User(uid, True)

"""
for user_id in range(num_users):
    above, below = [], []
    user_trackpoints_path = get_trackpoints_path(user_id)
    files = os.listdir(user_trackpoints_path)
    for fp in (user_trackpoints_path + fn for fn in files):
        with open(fp) as f:
            if os.stat(fp).st_size >= max_file_size_limit:
                above.append(len(f.readlines()))
            else:
                below.append(len(f.readlines()))
    print(len(above), len(below), max(above) if above else 0)

    print(f"UID:{user_id}, min_above={min(above) if above else 0}, max_below={max(below) if below else 0}")
"""
