import datetime

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

def get_date_str(timestamp):
    timestamp = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def is_drop_off(epoch_ms):
    dt = datetime.datetime.fromtimestamp(epoch_ms / 1000.0)
    return dt.time() >= datetime.time(8, 0) and dt.time() <= datetime.time(9, 30)

def is_pick_up(epoch_ms):
    dt = datetime.datetime.fromtimestamp(epoch_ms / 1000.0)
    return dt.time() >= datetime.time(14, 30) and dt.time() <= datetime.time(16, 0)

def is_busy_hour(timestamp):
    return is_pick_up(timestamp) or is_drop_off(timestamp)

def is_weekend(epoch_ms):
    dt = datetime.datetime.fromtimestamp(epoch_ms / 1000.0)
    return dt.weekday() >= 5

def is_in_holiday_range(epoch_ms):
    dt = datetime.datetime.fromtimestamp(epoch_ms / 1000.0).date()
    for start, end in holidays:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        if start_date <= dt <= end_date:
            return True
    return False

def is_off_day(timestamp):
    return is_weekend(timestamp) or is_in_holiday_range(timestamp)