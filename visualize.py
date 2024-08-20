import tkinter as tk
from tkinter import Label, Entry, Button
import sqlite3


def plot_data():
    canvas.delete("all")
    from_timestamp = int(from_entry.get())
    to_timestamp = int(to_entry.get())

    conn = sqlite3.connect('path_data.db')
    cur = conn.cursor()

    cur.execute('''
        SELECT x, y, channelId FROM path 
        WHERE timestamp BETWEEN ? AND ?
    ''', (from_timestamp, to_timestamp))

    rows = cur.fetchall()
    conn.close()

    canvas.delete("all")

    for x, y, channelId in rows:
        color = 'red' if channelId == 0 else 'green' if channelId == 1 else 'blue' if channelId == 2 else 'black'
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outline=color)

    canvas.create_polygon([553, 271, 644, 304, 1008, 206, 890, 210], outline='yellow', fill='', width=2)

root = tk.Tk()
root.title("Data Plotter")
root.geometry("2200x1300")

canvas = tk.Canvas(root, width=1920, height=1080, bg="white")
canvas.place(x=0, y=0)

Label(root, text="From:").place(x=10, y=10)
from_entry = Entry(root)
from_entry.place(x=70, y=10)
from_entry.insert(0, '1718845200000')

Label(root, text="To:").place(x=250, y=10)
to_entry = Entry(root)
to_entry.place(x=300, y=10)
to_entry.insert(0, '1718865200000')

plot_button = Button(root, text="Plot", command=plot_data)
plot_button.place(x=500, y=10)

root.mainloop()
