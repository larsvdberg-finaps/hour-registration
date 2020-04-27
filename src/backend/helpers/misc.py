from datetime import datetime

dt_string_format = "%Y-%m-%d, %H:%M:%S"

def timestamp_to_string(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    dt_string = dt_object.strftime(dt_string_format)
    return dt_string
