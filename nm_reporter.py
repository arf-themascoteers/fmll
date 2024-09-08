import datetime
from datetime import datetime as dtx
from datetime import timedelta
import db_handler
import configs
from shapely.geometry import Polygon, Point
import csv


class NearMisses_Reporter:
    def __init__(self, netId="CM99V122139007597", time_window=1000, time_filter=None):
        self.networkId = netId
        self.time_window = time_window
        self.all_windows = None
        self.time_filter = time_filter #None, P,D,PD,O
        self.file_name = "nm"
        postfix = "_A"
        if self.time_filter is not None:
            postfix = self.time_filter
        self.file_name = self.file_name +  "_" + postfix + ".csv"

    def create_window(self, rows, start, windowId, last_window):
        merged_frames = []
        start_timestamp = rows[start]["timestamp"]
        end_timestamp = start_timestamp + self.time_window
        next_start_index = None
        for i in range(start,len(rows)):
            this_timestamp = rows[i]["timestamp"]
            if next_start_index is None and this_timestamp > start_timestamp:
                next_start_index = i
            if this_timestamp > end_timestamp:
                break
            merged_frames.append(rows[i])
        date_string = configs.timestamp_to_date(start_timestamp)
        date_obj = configs.date_str_to_obj(date_string)
        window = {
            "start_timestamp":start_timestamp,
            "windowId":windowId,
            "length": 1,
            "actors":[],
            "hasVehicle": False,
            "hasPed": False,
            "hasBicycle": False,
            "isNearMiss": False,
            "isVehicleNearCollision": False,
            "date":date_string,
            "date_obj": date_obj
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

        is_same = False

        if NearMisses_Reporter.if_similar_window(last_window, window):
            is_same = True
            last_window["length"] = last_window["length"] + 1
            window = last_window

        return window, next_start_index, is_same

    @staticmethod
    def if_similar_window(window1, window2):
        if window1 is None or window2 is None:
            return False
        if window1["isNearMiss"] == window2["isNearMiss"] and window1["isVehicleNearCollision"] == window2["isVehicleNearCollision"]:
            return True
        return False

    def mark_crossing(self, rows):
        boundary = configs.get_boundary_coords(self.networkId)
        polygon = Polygon(boundary)
        filtered_rows = []
        for i,r in enumerate(rows):
            x = r["x"]
            y = r["y"]
            point = Point(x,y)
            if polygon.contains(point):
                filtered_rows.append(r)
        return filtered_rows

    def filter_time(self, rows):
        if self.time_filter is None:
            return rows
        filtered_rows = []
        fun = None
        if self.time_filter == "P":
            fun = configs.is_within_pick_up
        elif self.time_filter == "D":
            fun = configs.is_within_drop_off
        elif self.time_filter == "PD":
            fun = configs.is_within_pick_up_or_drop_off
        elif self.time_filter == "O":
            fun = configs.is_not_within_pick_up_or_drop_off

        for row in rows:
            if fun(row["timestamp"]):
                filtered_rows.append(row)

        return filtered_rows

    def report(self):
        self.all_windows = []
        rows = db_handler.get_data_by_netId(self.networkId)
        rows = self.filter_time(rows)
        rows = self.mark_crossing(rows)
        start_index = 0
        windowId = 0
        window = None
        while start_index is not None and start_index < len(rows):
            window, start_index, is_same = self.create_window(rows, start_index, windowId, window)
            if not is_same:
                self.all_windows.append(window)
                windowId = windowId + 1
        ag_windows = self.ag_windows()
        self.export_to_csv(ag_windows,self.file_name)

    def ag_windows(self):
        aggregated_data = []
        last_date = None

        self.all_windows = sorted(self.all_windows, key=lambda x: x["date_obj"])
        for window in self.all_windows:
            if last_date is None or window["date_obj"] != last_date["date_obj"]:
                if last_date is not None:
                    aggregated_data.append(last_date)
                last_date = {
                    "date": window["date"],
                    "date_obj": window["date_obj"],
                    "totalNearmiss":0,
                    "totalVehicleNearCol":0,
                    "is_holiday": 0
                }
            if window["isNearMiss"]:
                last_date["totalNearmiss"] += 1

            if window["isVehicleNearCollision"]:
                last_date["totalVehicleNearCol"] += 1

            if configs.is_off_day(window["start_timestamp"]):
                last_date["is_holiday"] = 1

        if last_date is not None:
            aggregated_data.append(last_date)

        current_date = aggregated_data[0]["date_obj"]
        end_date = aggregated_data[-1]["date_obj"]

        while current_date < end_date:
            if not self.has_date(aggregated_data, current_date):
                dt = {
                        "date": configs.format_date(current_date),
                        "date_obj": current_date,
                        "totalNearmiss": 0,
                        "totalVehicleNearCol":0,
                        "is_holiday":int(configs.is_off_day_day(current_date)),
                      }

                aggregated_data.append(dt)
            current_date = current_date + timedelta(days=1)

        aggregated_data = sorted(aggregated_data, key=lambda x: x["date_obj"])
        return aggregated_data

    def has_date(self, dates, current_date):
        for date in dates:
            if date["date_obj"] == current_date:
                return True
        return False

    def get_next_day(self, date_obj):
        return date_obj + timedelta(days=1)

    def export_to_csv(self, dates, filename):
        for d in dates:
            d.pop('date_obj', None)
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["date", "totalNearmiss","totalVehicleNearCol","is_holiday"])
            writer.writeheader()
            writer.writerows(dates)

    def get_window_by_id(self, windowId):
        for window in self.all_windows:
            if window["windowId"] == windowId:
                return window
        return None

    def convert_to_date(self, date_string):
        return dtx.strptime(date_string, "%Y-%m-%d").date()

    def convert_to_str(self, date_obj):
        return date_obj.strftime("%Y-%m-%d")


if __name__ == '__main__':
    n = "CM99V122139007597"
    #for f in [None,"P","D","PD","O"]:
    for f in ["O"]:
        reporter = NearMisses_Reporter(n,time_filter=f)
        reporter.report()
        print(f"Done {f}")