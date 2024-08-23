import tkinter as tk
from tkinter import Label, Entry, Button
import controller_nearmisses
import threading


class Application:
    def __init__(self):
        self.collision_controls_frame = None
        self.controller = controller_nearmisses.NearmissController(self)
        root = tk.Tk()
        root.title("FMLL")
        root.geometry("2200x1000")

        self.buttons_container = tk.Frame(root, background="grey")
        self.buttons_container.pack(side=tk.TOP)

        self.collision_controls_frame_parent = tk.Frame(root)
        self.collision_controls_frame_parent.pack(side=tk.TOP)


        self.canvas_container = tk.Frame(root, background="blue")
        self.canvas_container.pack(side=tk.TOP)

        Label(self.buttons_container, text="From:").pack(side=tk.LEFT, padx=5, pady=5)
        self.from_entry = Entry(self.buttons_container)
        self.from_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.from_entry.insert(0, '1716854905922')

        Label(self.buttons_container, text="To:").pack(side=tk.LEFT, padx=5, pady=5)
        self.to_entry = Entry(self.buttons_container)
        self.to_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.to_entry.insert(0, '1723432920411')

        Label(self.buttons_container, text="NetId:").pack(side=tk.LEFT, padx=5, pady=5)
        self.netId_entry = Entry(self.buttons_container)
        self.netId_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.netId_entry.insert(0, 'CM99V122139007597')

        Label(self.buttons_container, text="Time window (milliseconds):").pack(side=tk.LEFT, padx=5, pady=5)
        self.tw_entry = Entry(self.buttons_container)
        self.tw_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.tw_entry.insert(0, '1000')

        self.nm_label = Label(self.buttons_container, text="", bd=2, relief=tk.SOLID)

        plot_button = Button(
            self.buttons_container, text="Count",command=self.button_clicked)
        plot_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.canvas = tk.Canvas(self.canvas_container, width=1920, height=1080, bg="white", bd=10, relief=tk.SOLID)
        h_scrollbar = tk.Scrollbar(self.canvas_container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        v_scrollbar = tk.Scrollbar(self.canvas_container, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.pack(side=tk.LEFT)

        self.canvas.config(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        self.canvas.config(scrollregion=(0, 0, 1920, 1080))

        root.mainloop()


    def show_nearmisses(self, nm):
        self.nm_label.config(text=f"Near miss: {nm}")
        self.nm_label.pack(side=tk.LEFT, padx=5, pady=5)
        if nm > 0:
            self.show_collision_controls()

    def show_collision_controls(self):
        self.collision_controls_frame = tk.Frame(self.collision_controls_frame_parent)
        self.collision_controls_frame.pack(side=tk.LEFT, padx=5, pady=5)
        Label(self.collision_controls_frame, text="Near miss#:").pack(side=tk.LEFT, padx=5, pady=5)
        self.collision_number_entry = Entry(self.collision_controls_frame)
        self.collision_number_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.collision_number_entry.insert(0, '1')
        show_collision_button = Button(
            self.collision_controls_frame, text="Show",command=lambda:self.controller.plot_near_miss(int(self.collision_number_entry.get())))
        show_collision_button.pack(side=tk.LEFT, padx=5, pady=5)

    def show_loading(self):
        self.nm_label.config(text=f"Processing ...")
        self.nm_label.pack(side=tk.LEFT, padx=5, pady=5)

    def button_clicked(self):
        if self.collision_controls_frame is not None:
            self.collision_controls_frame.destroy()
            self.collision_controls_frame = None
        threading.Thread(target=lambda: self.controller.plot(
            int(self.from_entry.get()),
            int(self.to_entry.get()),
            int(self.tw_entry.get()),
            self.netId_entry.get()
        )).start()


if __name__ == '__main__':
    app = Application()