import tkinter as tk
from tkinter import Label, Entry, Button
import sqlite3
from shapely.geometry import Point, Polygon


def is_near_miss(start, end):
    conn = sqlite3.connect('path_data.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT x, y, channelId FROM path 
        WHERE timestamp BETWEEN ? AND ?
    ''', (start, end))
    rows = cur.fetchall()
    conn.close()
    for x, y, channelId in rows:
        p = Point(x, y)
        if not polygon.contains(p):
            return False
    return True

conn = sqlite3.connect('path_data.db')
cur = conn.cursor()
cur.execute('''
SELECT CAST(timestamp / 1000 AS INTEGER) AS timestamp_div_1000, networkId
FROM path
WHERE channelid IN (0, 1)
GROUP BY timestamp_div_1000, networkId
HAVING COUNT(DISTINCT channelid) = 2;

''')

rows = cur.fetchall()
conn.close()

vertices = [(553, 271), (644, 304), (1008, 206), (890, 210)]
polygon = Polygon(vertices)
for timestamp_div_1000,nid in rows:
    start = timestamp_div_1000*1000
    end = start + 999
    if is_near_miss(start, end):
        print(start)



