import datetime


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