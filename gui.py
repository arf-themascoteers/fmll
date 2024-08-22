import tkinter as tk
from tkinter import Label, Entry, Button
import controller

root = tk.Tk()
root.title("FMLL")
root.geometry("2200x1300")

c1 = tk.Frame(root, background="grey")
c1.place(relwidth=1, relheight=0.1, x=0, y=0)

c2 = tk.Frame(root)
c2.place(relwidth=1, relheight=0.9, x=0, rely=0.1)

Label(c1, text="From:").pack(side=tk.LEFT, padx=5, pady=5)
from_entry = Entry(c1)
from_entry.pack(side=tk.LEFT, padx=5, pady=5)
from_entry.insert(0, '1718845200000')

Label(c1, text="To:").pack(side=tk.LEFT, padx=5, pady=5)
to_entry = Entry(c1)
to_entry.pack(side=tk.LEFT, padx=5, pady=5)
to_entry.insert(0, '1718845300000')

plot_button = Button(c1, text="Plot", command=controller.plot)
plot_button.pack(side=tk.LEFT, padx=5, pady=5)

root.mainloop()