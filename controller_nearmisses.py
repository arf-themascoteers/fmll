import db_handler
import configs
from shapely.geometry import Polygon, Point


def get_paths_within(f,t,rows,start=0):
    to_return = []
    i = start
    for i in range(start,len(rows)):
        timestamp = rows[i][4]
        if f <= timestamp <= t:
            to_return.append(rows[i])
        elif timestamp > t:
            break
    if i >= len(rows)-1:
        i = None
    return to_return, i


def keep_crossing_only(rows, networkId):
    filtered = []
    boundary = configs.get_boundary_coords(networkId)
    polygon = Polygon(boundary)
    for r in rows:
        x = r[0]
        y = r[1]
        point = Point(x,y)
        if polygon.contains(point):
            filtered.append(rows)
    return filtered


def get_collision(rows):
    vehicles = [row for row in rows if (row[2] == 0)]
    peds = [row for row in rows if (row[2] == 1)]
    all = vehicles + peds
    collision = (len(vehicles) != 0 and len(peds) != 0)
    return collision, all


def plot(f,t,tw,n,canvas):
    collisions = []
    canvas.delete("all")
    rows = db_handler.get_data_by_from_to_netId(f,t,n)
    rows = keep_crossing_only(rows,n)
    start = f
    end = start + tw
    start_index = 0
    while end <= t:
        filtered_rows, start_index = get_paths_within(start, end, rows, start_index)
        collision, actors = get_collision(filtered_rows)
        if collision:
            collisions.append(actors)
        start = end+1
        end = start + tw

    print(len(collisions))
    # for x, y, channelId, objectId in rows:
    #     color = 'red' if channelId == 0 else 'green' if channelId == 1 else 'blue' if channelId == 2 else 'black'
    #     canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outline=color)
    # boundary = configs.get_boundary(n)
    # canvas.create_polygon(boundary, outline='yellow', fill='', width=2)
