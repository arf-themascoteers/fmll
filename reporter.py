import tkinter

import db_handler
import configs
from shapely.geometry import Polygon, Point


class Reporter:
    def __init__(self, netId="CM99V122139007597", time_window=1000):
        self.networkId = netId
        self.time_window = time_window
        self.all_windows = None

    def create_window(self, rows, start, windowId):
        merged_frames = []
        start_timestamp = rows[start]["timestamp"]
        end_timestamp = start_timestamp + self.time_window
        next_start_index = -1
        for i in range(start,len(rows)):
            this_timestamp = rows[i]["timestamp"]
            if next_start_index == -1 and this_timestamp > start_timestamp:
                next_start_index = i
            if this_timestamp > end_timestamp:
                break
            merged_frames.append(rows[i])
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

    def mark_crossing(self, rows):
        boundary = configs.get_boundary_coords(self.networkId)
        polygon = Polygon(boundary)
        for i,r in enumerate(rows):
            x = r["x"]
            y = r["y"]
            point = Point(x,y)
            if polygon.contains(point):
                rows[i]["crossing"] = True
            else:
                rows[i]["crossing"] = False
        return rows

    def mark_time(self, rows):
        for i,r in enumerate(rows):
            rows[i]["busy_hour"] = False
            if configs.is_weekend(r["timestamp"]):
                rows[i]["weekend"] = True
            else:
                rows[i]["weekend"] = False
                if configs.is_busy_hour(r["timestamp"]):
                    rows[i]["busy_hour"] = True
        return rows

    def get_collision(self, rows):
        vehicles = [row for row in rows if (row[2] == 0)]
        peds = [row for row in rows if (row[2] == 1)]
        all = vehicles + peds
        collision = (len(vehicles) != 0 and len(peds) != 0)
        return collision, all

    def report(self):
        self.all_windows = []
        rows = db_handler.get_data_by_netId(self.networkId)
        rows = self.mark_crossing(rows)
        rows = self.mark_time(rows)
        start_index = 0
        windowId = 0
        while start_index is not None and start_index < len(rows):
            window, start_index = self.create_window(rows, start_index, windowId)
            self.all_windows.append(window)
            windowId = windowId + 1

    def get_window_by_id(self, windowId):
        for window in self.all_windows:
            if window["windowId"] == windowId:
                return window
        return None

    def plot_window(self, n):
        self.root.canvas.delete("all")
        window = self.get_window_by_id(n)
        t = f"Timestamp: Between {window['start_timestamp']} and {window['start_timestamp'] + self.time_window}"
        t = (t + f"\nDate time: Between {configs.get_date_str(window['start_timestamp'])} "
             +f"and {configs.get_date_str(window['start_timestamp'] + self.time_window)}")
        self.root.canvas.create_text(50, 50, text=t, font=("Helvetica", 24), fill="blue", anchor=tkinter.NW)
        self.root.canvas.create_polygon(configs.get_boundary(self.networkId), outline='yellow', fill='', width=2)
        for actor in window["actors"]:
            x = actor["x"]
            y = actor["y"]
            channelId = actor["channelId"]
            color = 'red' if channelId == 0 else 'green' if channelId == 1 else 'blue' if channelId == 2 else 'black'
            self.root.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outline=color)
            self.root.canvas.create_text(x, y-10, text=actor["objectId"], font=("Helvetica", 7), fill=color, anchor=tkinter.CENTER)


if __name__ == '__main__':
    n = "CM99V122139007597"
    reporter = Reporter(n)
    reporter.report()