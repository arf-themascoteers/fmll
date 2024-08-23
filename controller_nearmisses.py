import db_handler
import configs
from shapely.geometry import Polygon, Point


class NearmissController:
    def __init__(self, root):
        self.root = root
        self.all_windows = None
        self.nearmisses_windows = None
        self.nearvehicle_windows = None
        self.networkId = None

    def get_window(self, rows, start, tw, windowId):
        merged_frames = []
        start_timestamp = rows[start][4]
        end_timestamp = start_timestamp + tw
        i = start
        end = True
        for i in range(start,len(rows)):
            this_timestamp = rows[i][4]
            if this_timestamp > end_timestamp:
                end = False
                break
            merged_frames.append(rows[i])
        next_start_index = i
        if end:
            next_start_index = None
        window = {
            "start_timestamp":start_timestamp,
            "windowId":windowId,
            "actors":[],
            "hasVehicle": False,
            "hasPed": False,
            "hasBicycle": False,
            "isNearMiss": False,
            "isVehicleNearCollision": False
        }
        for mf in merged_frames:
            channelId = mf[2]
            if channelId == 0:
                window["hasVehicle"] = True
            elif channelId == 1:
                window["hasPed"] = True
            else:
                window["hasBicycle"] = True
            actor = {
                "x" : mf[0],
                "y" : mf[1],
                "channelId": channelId,
                "objectId": mf[3],
            }
            window["actors"].append(actor)
        if window["hasVehicle"] and window["hasPed"]:
            window["isNearMiss"] = True
        vehicleIds = [actor["objectId"] for actor in window["actors"] if actor["channelId"] == 0]
        vehicleIds = set(vehicleIds)
        if len(vehicleIds) > 1:
            window["isVehicleNearCollision"] = True
        return window, next_start_index

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
        return collision, all


    def plot(self, f,t,tw,n):
        self.root.show_loading()
        self.networkId = n
        windows = []
        self.root.canvas.delete("all")
        rows = db_handler.get_data_by_from_to_netId(f,t,n)
        rows = self.keep_crossing_only(rows,n)
        start_index = 0
        windowId = 1
        while start_index is not None and start_index < len(rows):
            window, start_index = self.get_window(rows, start_index, tw, windowId)
            windows.append(window)
            windowId = windowId + 1
        self.all_windows = windows
        self.nearmisses_windows = [window for window in self.all_windows if window["isNearMiss"]]
        self.nearvehicle_windows = [window for window in self.all_windows if window["isVehicleNearCollision"]]
        self.root.show_nearmisses(len(self.nearmisses_windows))

    def get_window_by_id(self, windowId):
        # for window in self.all_windows:
        #     if window["windowId"] == windowId:
        #         return window
        # return None
        return self.nearmisses_windows[windowId-1]

    def plot_near_miss(self, n):
        self.root.canvas.delete("all")
        self.root.canvas.create_polygon(configs.get_boundary(self.networkId), outline='yellow', fill='', width=2)
        window = self.get_window_by_id(n)
        for actor in window["actors"]:
            x = actor["x"]
            y = actor["y"]
            channelId = actor["channelId"]
            color = 'red' if channelId == 0 else 'green' if channelId == 1 else 'blue' if channelId == 2 else 'black'
            self.root.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outline=color)


