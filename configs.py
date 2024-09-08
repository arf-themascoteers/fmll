from datetime import datetime

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
    date_obj = datetime.strptime(date_obj, '%Y-%m-%d')
    timestamp = int(date_obj.timestamp() * 1000)
    return is_weekend(timestamp) or is_in_holiday_range(timestamp)

if __name__ == "__main__":
    print(is_off_day(1716879591644))