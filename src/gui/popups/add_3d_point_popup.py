from tkinter import *
from tkinter import messagebox, colorchooser
from tkinter import ttk
from gui.widgets.entry_with_placeholder import EntryWithPlaceholder
from system.core.graphic_system import GraphicSystem
from system.graphic_objects.graphic_object import GraphicObjectType
from gui.style import BG_COLOR
from gui.widgets.logger import Logger
from utils.utils import format_point_list
from gui.widgets.custom_button import CustomButton


class Add3DPointPopup:

    def __init__(self, root, graphic_system: GraphicSystem, items_listbox: Listbox, items_dimensions_list,
                 logger: Logger) -> None:
        self.graphic_system = graphic_system
        self.items_listbox = items_listbox
        self.items_dimensions_list = items_dimensions_list
        self.logger = logger
        self.popup_window = Toplevel(root)
        self.popup_window.attributes("-topmost", True)
        self.init_popup(self.popup_window)

    def init_popup(self, popup_window) -> None:
        self.configure_popup(popup_window)
        self.create_popup(popup_window)

    def configure_popup(self, popup_window) -> None:
        popup_window.title("Add Point")
        popup_window.resizable(False, False)
        popup_window.configure(bg=BG_COLOR)

    def create_popup(self, popup_window) -> None:
        point_frame = Frame(popup_window)
        point_frame.pack(fill=BOTH, padx=10, pady=10)

        # Frame for entering coordinates and adding a point
        entry_frame = Frame(popup_window)
        entry_frame.pack(fill=X, padx=10, pady=10)
        entry_frame.configure(bg=BG_COLOR)

        # x entry
        x_entry = EntryWithPlaceholder(entry_frame, "x")
        x_entry.pack(side=LEFT, padx=10, expand=True)
        # y entry
        y_entry = EntryWithPlaceholder(entry_frame, "y")
        y_entry.pack(side=LEFT, padx=10, expand=True)
        # z entry
        z_entry = EntryWithPlaceholder(entry_frame, "z")
        z_entry.pack(side=LEFT, padx=10, expand=True)

        # Name entry and color picker frame
        name_and_color_frame = Frame(popup_window)
        name_and_color_frame.pack(fill=X, padx=10, pady=10)
        name_and_color_frame.configure(bg=BG_COLOR)

        # Name entry
        name_entry = EntryWithPlaceholder(name_and_color_frame, "Name")
        name_entry.pack(side=LEFT, fill=X, expand=True)

        # Color picker
        color_entry = Entry()
        color_entry.insert(0, "#000000")
        color_canvas = Canvas(name_and_color_frame, width=30,
                              height=20, bg=color_entry.get())
        color_canvas.pack(side=LEFT, padx=5)

        color_button = CustomButton(
            name_and_color_frame, text="Pick a color", button_type='default_button',
            command=lambda: self.pick_color(color_entry, color_canvas))
        color_button.pack(side=LEFT)

        # confirm point and cancel button
        popup_buttons_frame = Frame(popup_window)
        popup_buttons_frame.pack(padx=5, pady=5, fill=X, side=RIGHT)
        popup_buttons_frame.configure(bg=BG_COLOR)

        create_button = CustomButton(
            popup_buttons_frame, text="Create Point", button_type='default_button',
            command=lambda: self.create_3d_pointshape(x_entry, y_entry, z_entry, name_entry, color_entry, popup_window))
        create_button.pack(side=LEFT)

        cancel_button = CustomButton(
            popup_buttons_frame, text="Cancel", command=popup_window.destroy, button_type='red_button')
        cancel_button.pack(side=LEFT)

    def create_3d_pointshape(self, x_entry: EntryWithPlaceholder, y_entry: EntryWithPlaceholder,
                             z_entry: EntryWithPlaceholder, name_entry: EntryWithPlaceholder,
                             color_entry, popup_window: Toplevel):
        if not (x_entry.validate(True) and y_entry.validate(True) and z_entry.validate(True) and
                name_entry.validate(False)):
            return
        x, y, z = float(x_entry.get()), float(y_entry.get()), float(z_entry.get())
        self.graphic_system.create_shape([(x, y, z)], name_entry.get(), color_entry.get(), False,
                                         GraphicObjectType.POINT_3D)
        self.items_listbox.insert("end", f"{GraphicObjectType.POINT_3D}: {name_entry.get()}")
        self.items_dimensions_list.append(True)
        popup_window.destroy()
