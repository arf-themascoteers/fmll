import tkinter
import datetime
from datetime import datetime as dtx
from datetime import timedelta
import db_handler
import configs
from shapely.geometry import Polygon, Point
from collections import defaultdict
import csv


class Reporter:
    def __init__(self, netId="CM99V122139007597", time_window=1000):
        self.networkId = netId
        self.time_window = time_window
        self.all_windows = None

    def create_window(self, rows, start, windowId):
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
        window = {
            "start_timestamp":start_timestamp,
            "windowId":windowId,
            "actors":[],
            "hasVehicle": False,
            "hasPed": False,
            "hasBicycle": False,
            "isNearMiss": False,
            "isVehicleNearCollision": False,
            "date":self.timestamp_to_date(start_timestamp)
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
        filtered_rows = []
        for i,r in enumerate(rows):
            x = r["x"]
            y = r["y"]
            point = Point(x,y)
            if polygon.contains(point):
                filtered_rows.append(r)
        return filtered_rows

    def report(self):
        self.all_windows = []
        rows = db_handler.get_data_by_netId(self.networkId)
        rows = self.mark_crossing(rows)
        print("Done crossing")
        print(len(rows))
        start_index = 0
        windowId = 0
        while start_index is not None and start_index < len(rows):
            print(start_index)
            window, start_index = self.create_window(rows, start_index, windowId)
            self.all_windows.append(window)
            windowId = windowId + 1
        print("Done windows")
        print(len(rows))
        ag_windows = self.ag_windows()
        self.export_to_csv(ag_windows,"report.csv")

    def ag_windows(self):
        aggregated_data = []
        last_date = None

        sorted(self.all_windows, key=lambda x: x["date"])
        for window in self.all_windows:
            if last_date is None or window["date"] != last_date["date"]:
                if last_date is not None:
                    aggregated_data.append(last_date)
                last_date = {
                    "date": window["date"],
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



        current_date = aggregated_data[0]["date"]
        end_date = aggregated_data[-1]["date"]

        while current_date < end_date:
            if current_date not in aggregated_data:
                if not self.has_date(aggregated_data, current_date):
                    dt = {"date": current_date, "totalNearmiss": 0,
                                            "totalVehicleNearCol":0,
                          "is_holiday":int(configs.is_off_day_day(current_date))}

                    aggregated_data.append(dt)
            current_date = self.convert_to_date(current_date) + timedelta(days=1)
            current_date = self.convert_to_str(current_date)
            print(current_date)
        sorted(aggregated_data, key=lambda x: x["date"])
        return aggregated_data

    def has_date(self, dates, current_date):
        for date in dates:
            if date["date"] == current_date:
                return True
        return False

    def get_next_day(self, date_obj):
        return date_obj + timedelta(days=1)

    def export_to_csv(self, dates, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["date", "totalNearmiss","totalVehicleNearCol","is_holiday"])
            writer.writeheader()
            writer.writerows(dates)

    def timestamp_to_date(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')

    # def get_13_digit_epoch(self, timestamp):
    #     dt_object = self.timestamp_to_date(timestamp)
    #     dt_object = self.convert_to_date(dt_object)
    #     return int(dt_object.timestamp() * 1000)

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
    reporter = Reporter(n)
    reporter.report()