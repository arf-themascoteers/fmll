import tkinter as tk
from tkinter import Label, Entry, Button
import controller

root = tk.Tk()
root.title("FMLL")
root.geometry("2200x1000")

c1 = tk.Frame(root, background="grey")
c1.pack(side=tk.TOP)

c2 = tk.Frame(root, background="blue")
c2.pack(side=tk.TOP)

Label(c1, text="From:").pack(side=tk.LEFT, padx=5, pady=5)
from_entry = Entry(c1)
from_entry.pack(side=tk.LEFT, padx=5, pady=5)
from_entry.insert(0, '1718845200000')

Label(c1, text="To:").pack(side=tk.LEFT, padx=5, pady=5)
to_entry = Entry(c1)
to_entry.pack(side=tk.LEFT, padx=5, pady=5)
to_entry.insert(0, '1718845300000')

Label(c1, text="NetId:").pack(side=tk.LEFT, padx=5, pady=5)
netId_entry = Entry(c1)
netId_entry.pack(side=tk.LEFT, padx=5, pady=5)
netId_entry.insert(0, 'CM99V122139007597')

plot_button = Button(
                        c1, text="Plot",
                        command=lambda: controller.plot(
                            int(from_entry.get()),
                            int(to_entry.get()),
                            netId_entry.get(),
                            canvas
                        )
                     )
plot_button.pack(side=tk.LEFT, padx=5, pady=5)

canvas = tk.Canvas(c2, width=1920, height=1080, bg="white", bd=10, relief=tk.SOLID)
h_scrollbar = tk.Scrollbar(c2, orient=tk.HORIZONTAL, command=canvas.xview)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

v_scrollbar = tk.Scrollbar(c2, orient=tk.VERTICAL, command=canvas.yview)
v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.pack(side=tk.LEFT)

canvas.config(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
canvas.config(scrollregion=(0, 0, 1920, 1080))

#canvas.create_line(0, 0, 1920, 1080, fill="black", width=5)

root.mainloop()
