from datetime import datetime
from datetime import time as dtime
import time

holidays = [
    ["2024-01-01","2024-01-29"],
    ["2024-03-29","2024-04-14"],
    ["2024-06-29","2024-07-14"],
    ["2024-09-21","2024-10-06"],
    ["2024-01-01","2024-01-01"],
    ["2024-01-26","2024-01-26"],
    ["2024-03-11","2024-03-11"],
    ["2024-03-29","2024-03-29"],
    ["2024-03-31","2024-03-31"],
    ["2024-04-01","2024-04-01"],
    ["2024-04-25","2024-04-25"],
    ["2024-06-10","2024-06-10"],
    ["2024-09-28","2024-09-28"],
    ["2024-11-05","2024-11-05"],
    ["2024-12-25","2024-12-25"],
    ["2024-12-26","2024-12-26"],
]

def get_boundary(netId):
    if netId == "CM99V122139007597":
        return [553, 271, 644, 304, 1008, 206, 890, 210]
    if netId == "CM27V122149004668":
        return [216, 274, 549, 162, 146, 737, 16, 678]
    if netId == "CM99V122113000052":
        return [1257, 161, 1761, 209, 1673, 292, 999, 215]


def get_boundary_coords(netId):
    xys = get_boundary(netId)
    coords = []
    for i in range(0, len(xys), 2):
        coords.append((xys[i],xys[i+1]))
    return coords

def from_timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp / 1000.0)

def is_weekend(dt):
    dt = datetime.fromtimestamp(dt / 1000.0)
    return dt.weekday() >= 5

def is_in_holiday_range(dt):
    dt = datetime.fromtimestamp(dt / 1000.0).date()
    for start, end in holidays:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        if start_date <= dt <= end_date:
            return True
    return False

def is_off_day(dt):
    return is_weekend(dt) or is_in_holiday_range(dt)

def is_off_day_day(date_obj):
    timestamp = int(date_obj.timestamp() * 1000)
    return is_weekend(timestamp) or is_in_holiday_range(timestamp)


def date_to_epoch(date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    epoch_time = int(time.mktime(dt.timetuple()) * 1000)
    return epoch_time


def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')


def date_str_to_obj(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')


def format_date(date_obj):
    return date_obj.strftime('%Y-%m-%d')


def is_within_time_range(timestamp,from_hr, from_min, to_hr, to_min):
    dt = datetime.fromtimestamp(timestamp / 1000.0)
    start_time = dtime(from_hr, from_min)
    end_time = dtime(to_hr, to_min)
    return start_time <= dt.time() <= end_time


def is_within_drop_off(timestamp):
    if is_off_day(timestamp):
        return False
    return is_within_time_range(timestamp,8,35,8,50)


def is_within_pick_up(timestamp):
    if is_off_day(timestamp):
        return False
    return is_within_time_range(timestamp,15,15,15,30)


def is_within_pick_up_or_drop_off(timestamp):
    return is_within_pick_up(timestamp) or is_within_drop_off(timestamp)

def is_not_within_pick_up_or_drop_off(timestamp):
    return not is_within_pick_up_or_drop_off(timestamp)


def to_epoch_milliseconds(date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return int(dt.timestamp() * 1000)


if __name__ == "__main__":
    #print(is_off_day(1716879591644))
    # ts = 1716879591644
    # ttd = timestamp_to_date(ts)
    # print(ttd)
    # ts = date_to_epoch(ttd)
    # print(ts)
    # d1 = date_str_to_obj("2024-08-29")
    # d2 = date_str_to_obj("2024-08-29")
    # print(d1==d2)
    ep1 = to_epoch_milliseconds("2024-08-29 21:56:46")
    print(is_within_drop_off(ep1))
    ep1 = to_epoch_milliseconds("2024-08-29 08:49:46")
    print(is_within_drop_off(ep1))
    ep1 = to_epoch_milliseconds("2024-06-01 08:49:46")
    print(is_within_drop_off(ep1))
