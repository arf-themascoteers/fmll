import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=1920, height=1080, bg="white", bd=2, relief=tk.SOLID)

h_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

v_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.pack(side=tk.LEFT)

canvas.config(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
canvas.config(scrollregion=(0, 0, 1920, 1080))

canvas.create_line(0, 0, 1920, 1080, fill="black", width=5)

root.mainloop()
