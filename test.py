import tkinter as tk
from shapely.geometry import Polygon, Point
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def plot_shape():
    fig, ax = plt.subplots()

    polygon = Polygon([(1, 1), (5, 1), (4, 4), (2, 5)])
    point = Point(3, 3)

    x, y = polygon.exterior.xy
    ax.plot(x, y, color='blue')

    ax.plot(point.x, point.y, 'ro')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.draw()

root = tk.Tk()
root.title("Shapely Polygon and Point Plotter")

plot_button = tk.Button(root, text="Plot Polygon and Point", command=plot_shape)
plot_button.pack()

root.mainloop()
