import tkinter as tk
from shapely.geometry import Polygon, Point


def check_point_in_polygon():
    canvas.delete('all')

    polygon_coords = [(100, 100), (300, 100), (350, 200), (250, 300), (150, 250)]
    point_coords = (200, 150)

    canvas.create_polygon(polygon_coords, outline='black', fill='blue', stipple='gray12')
    canvas.create_oval(point_coords[0] - 5, point_coords[1] - 5, point_coords[0] + 5, point_coords[1] + 5, fill='red')

    polygon = Polygon(polygon_coords)
    point = Point(point_coords)

    if polygon.contains(point):
        result_label.config(text="Point is inside the polygon")
    else:
        result_label.config(text="Point is outside the polygon")


root = tk.Tk()
root.title("Polygon and Point Detection")
root.geometry("600x400")

canvas = tk.Canvas(root, width=600, height=300)
canvas.pack()

result_label = tk.Label(root, text="")
result_label.pack()

check_point_in_polygon()

root.mainloop()
