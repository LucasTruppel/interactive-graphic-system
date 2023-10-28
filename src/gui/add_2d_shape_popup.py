from tkinter import *
from tkinter import messagebox, colorchooser
from tkinter import ttk
from gui.entry_with_placeholder import EntryWithPlaceholder
from system.core.graphic_system import GraphicSystem
from system.graphic_objects.graphic_object import GraphicObjectType
from gui.style import BG_COLOR
from gui.logger import Logger
from utils.utils import format_point_list
from gui.custom_button import CustomButton


class Add2DShapePopup:

    option_1 = (GraphicObjectType.POINT,)
    option_2 = (GraphicObjectType.LINE,)
    option_3 = (GraphicObjectType.POLYGON,
                GraphicObjectType.BEZIER_CURVE, GraphicObjectType.B_SPLINE_CURVE)

    def __init__(self, root, graphic_system: GraphicSystem, items_listbox: Listbox, items_dimensions_list: list[bool],
                 logger: Logger) -> None:
        self.graphic_system = graphic_system
        self.items_listbox = items_listbox
        self.items_dimensions_list = items_dimensions_list
        self.logger = logger
        self.popup_window = Toplevel(root)
        self.popup_window.attributes("-topmost", True)
        self.type_var = None
        self.combobox = None
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
        add_button = CustomButton(entry_frame, text="Add Point",
                                  command=lambda: self.add_point(x_entry, y_entry, points_listbox, points_list), button_type='default_button')
        add_button.pack(side=LEFT)

        # CustomButton to remove selected point
        remove_button = CustomButton(
            entry_frame, text="Remove Selected Point", command=lambda: self.remove_point(points_listbox, points_list), button_type='red_button')
        remove_button.pack(side=LEFT)

        # Name entry and pick color button frame
        name_and_color_frame = Frame(popup_window)
        name_and_color_frame.pack(padx=10, pady=(0, 10), fill=X)
        name_and_color_frame.configure(bg=BG_COLOR)

        name_entry = EntryWithPlaceholder(name_and_color_frame, "Name")
        name_entry.pack(side=LEFT, fill=X, expand=True)

        color_entry = Entry()
        color_entry.insert(0, "#000000")
        color_canvas = Canvas(name_and_color_frame, width=30,
                              height=20, bg=color_entry.get())
        color_canvas.pack(side=LEFT, padx=5)

        fill = BooleanVar()
        fill_shape_checkbox = Checkbutton(
            name_and_color_frame, text="Fill Shape", variable=fill)
        fill_shape_checkbox.pack(side=LEFT, padx=5)

        self.type_var = StringVar()
        self.combobox = ttk.Combobox(
            name_and_color_frame, textvariable=self.type_var, state="readonly")
        self.combobox["values"] = self.option_1
        self.combobox.current(0)
        self.combobox.pack(side=LEFT, padx=5)

        color_button = CustomButton(
            name_and_color_frame, text="Pick a color", button_type='default_button',
            command=lambda: self.pick_color(color_entry, color_canvas))
        color_button.pack(side=LEFT)

        # Add shape window confirm and cancel buttons frame
        popup_buttons_frame = Frame(popup_window)
        popup_buttons_frame.pack(padx=5, pady=5, fill=X, side=RIGHT)
        popup_buttons_frame.configure(bg=BG_COLOR)

        create_button = CustomButton(
            popup_buttons_frame, text="Create Shape", button_type='default_button',
            command=lambda: self.create_shape(points_list, name_entry, color_entry, fill.get(), self.type_var.get(),
                                              popup_window))
        create_button.pack(side=LEFT)

        cancel_button = CustomButton(
            popup_buttons_frame, text="Cancel", command=popup_window.destroy, button_type='red_button')
        cancel_button.pack(side=LEFT)

    def add_point(self, x_entry: EntryWithPlaceholder, y_entry: EntryWithPlaceholder, points_listbox: Listbox,
                  points_list: list[tuple[float, float]]) -> None:
        try:
            x = float(x_entry.get())
            y = float(y_entry.get())
            points_list.append((x, y))
            points_listbox.insert("end", f"({x:g}, {y:g})")
            x_entry.clear()
            y_entry.clear()
            if len(points_list) == 0 or len(points_list) == 1:
                self.combobox["values"] = self.option_1
                self.combobox.current(0)
            elif len(points_list) == 2:
                self.combobox["values"] = self.option_2
                self.combobox.current(0)
            elif len(points_list) == 3:
                self.combobox["values"] = self.option_3
                self.combobox.current(0)
        except ValueError:
            if x_entry.get() == "" or y_entry.get() == "":
                messagebox.showerror(parent=self.popup_window,
                                     title="Add Point Error",
                                     message="Point must be specified")
            else:
                messagebox.showerror(parent=self.popup_window,
                                     title="Add Point Error",
                                     message="Invalid character")

    def remove_point(self, points_listbox: Listbox, points_list: list[tuple[float, float]]) -> None:
        if len(points_listbox.curselection()) == 0:
            messagebox.showerror(parent=self.popup_window,
                                 title="Remove Point Error",
                                 message="Select a point")
        else:
            pos = points_listbox.curselection()[0]
            points_listbox.delete(pos)
            points_list.pop(pos)
            if len(points_list) == 1:
                self.combobox["values"] = self.option_1
                self.combobox.current(0)
            elif len(points_list) == 2:
                self.combobox["values"] = self.option_2
                self.combobox.current(0)

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

    def create_shape(self, points_list: list[tuple[float, float]], name_entry: Entry, color_entry: Entry, fill: bool,
                     object_type: str, popup_window: Toplevel) -> None:
        name = name_entry.get()
        if len(points_list) <= 0:
            messagebox.showerror(parent=self.popup_window, title="Create Shape Error",
                                 message="At least one point is needed")
            return
        if name == "" or name == "Name":
            messagebox.showerror(parent=self.popup_window, title="Create Shape Error",
                                 message="Shape name must be specified")
            return
        if (object_type == GraphicObjectType.BEZIER_CURVE
                and not ((len(points_list) >= 4) and ((len(points_list) - 4) % 3 == 0))):
            messagebox.showerror(parent=self.popup_window, title="Create Shape Error",
                                 message="Bezier Curve must have a point amount (a) that follows:\n "
                                         "a = 4 + 3n  |  n = 0, 1, 2, ...")
            return
        if object_type == GraphicObjectType.B_SPLINE_CURVE and len(points_list) < 4:
            messagebox.showerror(parent=self.popup_window, title="Create Shape Error",
                                 message="B-Spline Curve must have at least 4 points")
            return
        self.graphic_system.create_shape(
            points_list, name, color_entry.get(), fill, object_type)
        popup_window.destroy()
        self.items_listbox.insert("end", f"{object_type}: {name}")
        self.items_dimensions_list.append(False)
        self.logger.log(
            f'Shape "{name}" created with points: {format_point_list(points_list)}.')
