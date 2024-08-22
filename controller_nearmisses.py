import db_handler
import configs
from shapely.geometry import Polygon, Point

class NearmissController:
    def __init__(self, root):
        self.root = root
        self.collisions = None

    def get_paths_within(self, f,t,rows,start=0):
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


    def keep_crossing_only(self, rows, networkId):
        filtered = []
        boundary = configs.get_boundary_coords(networkId)
        polygon = Polygon(boundary)
        for r in rows:
            x = r[0]
            y = r[1]
            point = Point(x,y)
            if polygon.contains(point):
                filtered.append(r)
        return filtered


    def get_collision(self, rows):
        vehicles = [row for row in rows if (row[2] == 0)]
        peds = [row for row in rows if (row[2] == 1)]
        all = vehicles + peds
        collision = (len(vehicles) != 0 and len(peds) != 0)
        return True, all


    def plot(self, f,t,tw,n):
        self.root.show_loading()
        collisions = []
        self.root.canvas.delete("all")
        rows = db_handler.get_data_by_from_to_netId(f,t,n)
        rows = self.keep_crossing_only(rows,n)
        start = f
        end = start + tw
        start_index = 0
        while end <= t and start_index is not None:
            filtered_rows, start_index = self.get_paths_within(start, end, rows, start_index)
            collision, actors = self.get_collision(filtered_rows)
            if collision:
                collisions.append(actors)
            start = end+1
            end = start + tw
        self.collisions = collisions
        self.root.show_nearmisses(len(self.collisions))

    def plot_near_miss(self, n):
        collision = self.collisions[n-1]
        print(collision)
