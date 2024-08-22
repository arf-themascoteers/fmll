import sqlite3


def plot(f,t,n):
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
