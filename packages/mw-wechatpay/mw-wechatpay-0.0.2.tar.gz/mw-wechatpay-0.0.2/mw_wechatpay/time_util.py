from dateutil.parser import parse
from datetime import datetime

def convert_timestr_to_datetime(time_str):
    return parse(time_str)

def convert_timestr_to_ts(time_str):
    d = convert_timestr_to_datetime(time_str)
    return int(d.timestamp())

def linux_timestamp():
    return int(datetime.now().timestamp())