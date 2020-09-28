import os
from collections import namedtuple
from datetime import datetime

max_line_size = 113
data_offset = 6
max_lines_limit = 2500 + data_offset
max_file_size_limit = max_line_size * max_lines_limit
is_below_max_size = lambda fp: os.stat(fp).st_size < max_file_size_limit

num_users = 182
data_path = "../dataset/Data"
get_trackpoints_path = lambda uid: f"{data_path}/{uid:03}/Trajectory/"
get_labels_path = lambda uid: f"{data_path}/{uid:03}/labels.txt"

tp_datetime_format = r"%Y-%m-%d %H:%M:%S"
label_datetime_format = r"%Y/%m/%d %H:%M:%S"
fn_datetime_format = r"%Y%m%d%H%M%S"
parse_tp_date_time = lambda s_datetime: datetime.strptime(s_datetime, tp_datetime_format)
parse_label_date_time = lambda s_datetime: datetime.strptime(s_datetime, label_datetime_format)
parse_fn_date_time = lambda fn: datetime.strptime(fn, fn_datetime_format)

User = namedtuple("User", ("id", "has_labels", "activities"))
Trackpoint = namedtuple("Trackpoint", ("latitude", "longtitude", "altitude", "datetime"))
Activity = namedtuple("Activity", ("transportation_mode", "start_date_time", "end_date_time", "trackpoints"))

def clear_file(filename):
    print(f"Clearing file: {filename}")
    f = open(filename, 'w')
    f.truncate(0)
    f.close()