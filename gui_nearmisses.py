import tkinter as tk
from tkinter import Label, Entry, Button
import controller_nearmisses
import threading


class Application:
    def __init__(self):
        
        self.windows_controls_frame = None
        self.collision_controls_frame = None
        self.vehicle_controls_frame = None
        
        self.controller = controller_nearmisses.NearmissController(self)
        root = tk.Tk()
        root.title("FMLL")
        root.geometry("2200x1000")

        self.buttons_container = tk.Frame(root, background="grey")
        self.buttons_container.pack(side=tk.TOP)

        self.window_controls_parent = tk.Frame(root)
        self.window_controls_parent.pack(side=tk.TOP)


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

        self.status_label = Label(self.buttons_container, text="", bd=2, relief=tk.SOLID)

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

    def show_windows(self, all_windows, nm_windows, vc_windows):
        self.status_label.config(text=f"Done")
        self.status_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.show_window_controls(all_windows)
        self.show_nearmiss_controls(nm_windows)
        self.show_vehicle_controls(vc_windows)

    def show_window_controls(self, all_windows):
        if len(all_windows) == 0:
            return
        Label(self.window_controls_parent, text=f"Total windows: {len(all_windows)}").pack(side=tk.LEFT, padx=5, pady=5)
        self.window_controls_frame = tk.Frame(self.window_controls_parent)
        self.window_controls_frame.pack(side=tk.LEFT, padx=5, pady=5)
        Label(self.window_controls_frame, text="Window#:").pack(side=tk.LEFT, padx=5, pady=5)
        options = []

        for i,nm in enumerate(all_windows):
            options.append(nm['windowId'])
        self.selected_window_id = tk.StringVar(value=f"1")
        self.window_number_entry = tk.OptionMenu(self.window_controls_frame, self.selected_window_id, *options)
        self.window_number_entry.pack(side=tk.LEFT, padx=5, pady=5)
        show_collision_button = Button(
            self.window_controls_frame, text="Show window",command=lambda:self.controller.plot_window(int(self.selected_window_id.get())))
        show_collision_button.pack(side=tk.LEFT, padx=5, pady=5)

    def show_nearmiss_controls(self, nms):
        if len(nms) == 0:
            return
        Label(self.window_controls_parent, text=f"Total near miss: {len(nms)}").pack(side=tk.LEFT, padx=5, pady=5)
        self.collision_controls_frame = tk.Frame(self.window_controls_parent)
        self.collision_controls_frame.pack(side=tk.LEFT, padx=5, pady=5)
        Label(self.collision_controls_frame, text="Near miss#:").pack(side=tk.LEFT, padx=5, pady=5)
        options = {}

        for i,nm in enumerate(nms):
            options[f"{i+1} ({nm['windowId']})"] = nm['windowId']
        displays = list(options.keys())
        self.selected_id = tk.StringVar(value=f"{1} ({nms[0]['windowId']})")
        self.collision_number_entry = tk.OptionMenu(self.collision_controls_frame, self.selected_id, *displays)
        self.collision_number_entry.pack(side=tk.LEFT, padx=5, pady=5)
        show_collision_button = Button(
            self.collision_controls_frame, text="Show near miss",command=lambda:self.controller.plot_window(int(options[self.selected_id.get()])))
        show_collision_button.pack(side=tk.LEFT, padx=5, pady=5)

    def show_vehicle_controls(self, vehicle_windows):
        if len(vehicle_windows) == 0:
            return
        Label(self.window_controls_parent, text=f"Total near vehicle collision: {len(vehicle_windows)}").pack(side=tk.LEFT, padx=5, pady=5)
        self.vehicle_controls_frame = tk.Frame(self.window_controls_parent)
        self.vehicle_controls_frame.pack(side=tk.LEFT, padx=5, pady=5)
        Label(self.vehicle_controls_frame, text="Near vehicle collision#:").pack(side=tk.LEFT, padx=5, pady=5)
        options = {}

        for i,nm in enumerate(vehicle_windows):
            options[f"{i+1} ({nm['windowId']})"] = nm['windowId']
        displays = list(options.keys())
        self.selected_vehicle_windiow_id = tk.StringVar(value=f"{1} ({vehicle_windows[0]['windowId']})")
        self.vehicle_number_entry = tk.OptionMenu(self.vehicle_controls_frame, self.selected_vehicle_windiow_id, *displays)
        self.vehicle_number_entry.pack(side=tk.LEFT, padx=5, pady=5)
        show_collision_button = Button(
            self.vehicle_controls_frame, text="Show near vehicle collision",command=lambda:self.controller.plot_window(int(options[self.selected_vehicle_windiow_id.get()])))
        show_collision_button.pack(side=tk.LEFT, padx=5, pady=5)

    def show_loading(self):
        self.status_label.config(text=f"Processing ...")
        self.status_label.pack(side=tk.LEFT, padx=5, pady=5)

    def reset_window_controls(self):
        if self.windows_controls_frame is not None:
            self.windows_controls_frame.destroy()
            self.windows_controls_frame = None

        if self.collision_controls_frame is not None:
            self.collision_controls_frame.destroy()
            self.collision_controls_frame = None

        if self.vehicle_controls_frame is not None:
            self.vehicle_controls_frame.destroy()
            self.vehicle_controls_frame = None

    def button_clicked(self):
        self.reset_window_controls()
        threading.Thread(target=lambda: self.controller.plot(
            int(self.from_entry.get()),
            int(self.to_entry.get()),
            int(self.tw_entry.get()),
            self.netId_entry.get()
        )).start()


if __name__ == '__main__':
    app = Application()