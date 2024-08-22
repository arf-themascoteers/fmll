import db_handler
import configs


def plot(f,t,n,canvas):
    canvas.delete("all")
    rows = db_handler.get_data_by_from_to_netId(f,t,n)

    for x, y, channelId, objectId in rows:
        color = 'red' if channelId == 0 else 'green' if channelId == 1 else 'blue' if channelId == 2 else 'black'
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outline=color)
    boundary = configs.get_boundary(n)
    canvas.create_polygon(boundary, outline='yellow', fill='', width=2)
