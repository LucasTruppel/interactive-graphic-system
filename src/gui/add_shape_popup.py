from tkinter import *
from tkinter import messagebox, colorchooser
from gui.entry_with_placeholder import EntryWithPlaceholder
from gui.transform_popup import TransformPopup
from system.graphic_system import GraphicSystem
from gui.style import BG_COLOR, FG_COLOR
from gui.logger import Logger
from utils.utils import format_point_list


class AddShapePopup:

    def __init__(self, root, graphic_system: GraphicSystem, items_listbox: Listbox, logger: Logger) -> None:
        self.graphic_system = graphic_system
        self.items_listbox = items_listbox
        self.logger = logger
        self.popup_window = Toplevel(root)
        self.popup_window.attributes("-topmost", True)
        self.init_popup(self.popup_window)

    def init_popup(self, popup_window) -> None:
        self.configure_popup(popup_window)
        self.create_popup(popup_window)

    def configure_popup(self, popup_window) -> None:
        popup_window.title("Add Shape")
        popup_window.resizable(False, False)
        popup_window.configure(bg=BG_COLOR)

    def create_popup(self, popup_window) -> None:
        # Frame for the list of points
        points_frame = Frame(popup_window)
        points_frame.pack(fill=BOTH, padx=10, pady=10)

        points_listbox = Listbox(points_frame, selectmode=SINGLE)
        points_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = Scrollbar(points_frame)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        points_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=points_listbox.yview)

        # Frame for entering coordinates and adding points
        entry_frame = Frame(popup_window)
        entry_frame.pack(fill=X, padx=10, pady=(0, 10))
        entry_frame.configure(bg=BG_COLOR)

        x_entry = EntryWithPlaceholder(entry_frame, "x")
        y_entry = EntryWithPlaceholder(entry_frame, "y")

        x_entry.pack(side=LEFT, padx=(0, 10), expand=True)
        y_entry.pack(side=LEFT, padx=(0, 10), expand=True)

        points_list = []
        add_button = Button(entry_frame, text="Add Point", width=10,
                            command=lambda: self.add_point(x_entry, y_entry, points_listbox, points_list))
        add_button.pack(side=LEFT)

        # Button to remove selected point
        remove_button = Button(
            popup_window, text="Remove Selected Point", width=25, command=lambda: self.remove_point(points_listbox, points_list))
        remove_button.pack(pady=(0, 10))

        # Name entry and pick color button frame
        name_and_color_frame = Frame(popup_window)
        name_and_color_frame.pack(padx=10, pady=(0, 10), fill=X)
        name_and_color_frame.configure(bg=BG_COLOR)

        name_entry = EntryWithPlaceholder(name_and_color_frame, "Name")
        name_entry.pack(side=LEFT, fill=X, expand=True, padx=5)

        color_entry = Entry()
        color_entry.insert(0, "#000000")
        color_canvas = Canvas(name_and_color_frame, width=30,
                              height=30, bg=color_entry.get())
        color_canvas.pack(side=LEFT, padx=5)

        color_button = Button(name_and_color_frame, text="Pick a color", width=10,
                              command=lambda: self.pick_color(color_entry, color_canvas))
        color_button.pack(side=LEFT, padx=5, fill=X)

        # Add shape window confirm and cancel buttons frame
        popup_buttons_frame = Frame(popup_window)
        popup_buttons_frame.pack(padx=10, pady=(0, 10), fill=X)
        popup_buttons_frame.configure(bg=BG_COLOR)

        create_button = Button(
            popup_buttons_frame, text="Create Shape", width=25, command=lambda: self.create_shape(points_list, name_entry, color_entry, popup_window))
        create_button.pack(side=LEFT, padx=(0, 10), expand=True, fill="both")

        cancel_button = Button(
            popup_buttons_frame, text="Cancel", width=25, command=popup_window.destroy)
        cancel_button.pack(side=LEFT,  expand=True, fill="both")

    def add_point(self, x_entry: EntryWithPlaceholder, y_entry: EntryWithPlaceholder, points_listbox: Listbox,
                  points_list: list[tuple[float, float]]) -> None:
        try:
            x = float(x_entry.get())
            y = float(y_entry.get())
            if (x, y) not in points_list:
                points_list.append((x, y))
                points_listbox.insert("end", f"({x:g}, {y:g})")
            else:
                messagebox.showerror(
                    "Add Point Error", "Point already registered")
            x_entry.clear()
            y_entry.clear()
        except ValueError:
            if x_entry.get() == "" or y_entry.get() == "":
                messagebox.showerror(
                    "Add Point Error", "Point must be specified")
            else:
                messagebox.showerror("Add Point Error", "Invalid character")

    def remove_point(self, points_listbox: Listbox, points_list: list[tuple[float, float]]) -> None:
        if len(points_listbox.curselection()) == 0:
            messagebox.showerror("Remove Point Error", "Select a point")
        else:
            pos = points_listbox.curselection()[0]
            points_listbox.delete(pos)
            points_list.pop(pos)

    def pick_color(self, color_entry: Entry, color_canvas: Canvas) -> None:
        new_color = colorchooser.askcolor(parent=self.popup_window)[1]
        if new_color is not None:
            color = new_color
        else:
            color = color_entry.get()
        color_entry.delete(0, END)
        color_entry.insert(0, color)

        # Update the color of the canvas square
        color_canvas.configure(bg=color)

    def create_shape(self, points_list: list[tuple[float, float]], name_entry: Entry, color_entry: Entry,
                     popup_window: Toplevel) -> None:
        name = name_entry.get()
        if len(points_list) > 0:
            if name != "" and name != "Name":
                self.graphic_system.create_shape(
                    points_list, name, color_entry.get())
                popup_window.destroy()
                self.items_listbox.insert("end", name)
                self.logger.log(
                    f'Shape "{name}" created with points: {format_point_list(points_list)}.')
            else:
                messagebox.showerror("Create Shape Error",
                                     "Shape name must be specified")
        else:
            messagebox.showerror("Create Shape Error",
                                 "At least one point is needed")
