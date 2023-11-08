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


class Add3DCurvePopup:

    def __init__(self, root, graphic_system: GraphicSystem, items_listbox: Listbox, items_dimensions_list: list[bool],
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
        popup_window.title("Add Shape")
        popup_window.resizable(False, False)
        popup_window.configure(bg=BG_COLOR)

    def create_popup(self, popup_window) -> None:
        points_frame = Frame(popup_window)
        points_frame.pack(fill=BOTH, padx=10, pady=10)

        points_listbox = Listbox(points_frame, selectmode=SINGLE)
        points_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = Scrollbar(points_frame)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        points_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=points_listbox.yview)

        matrix_frame = Frame(popup_window, height=200, width=200)
        matrix_frame.pack(fill=BOTH, padx=10, pady=10, side=TOP, expand=True)

        matrix_entry = EntryWithPlaceholder(matrix_frame, "Matrix")
        matrix_entry.pack(side=TOP, padx=10, expand=True, fill=BOTH)

        matrix_buttons_frame = Frame(popup_window)
        matrix_buttons_frame.pack(fill=X, padx=10, pady=10)
        matrix_buttons_frame.configure(bg=BG_COLOR)

        points_list = []
        add_button = CustomButton(matrix_buttons_frame, text="Add Curve",
                                  command=lambda: self.add_curve(matrix_entry, points_listbox, points_list), button_type='default_button')
        add_button.pack(side=LEFT)

        remove_button = CustomButton(
            matrix_buttons_frame, text="Remove Curve", command=lambda: self.remove_curve(points_listbox, points_list),
            button_type='red_button')
        remove_button.pack(side=LEFT)

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

        color_button = CustomButton(
            name_and_color_frame, text="Pick a color", button_type='default_button',
            command=lambda: self.pick_color(color_entry, color_canvas))
        color_button.pack(side=LEFT)

        popup_buttons_frame = Frame(popup_window)
        popup_buttons_frame.pack(padx=5, pady=5, fill=X, side=RIGHT)
        popup_buttons_frame.configure(bg=BG_COLOR)

        create_button = CustomButton(
            popup_buttons_frame, text="Create Shape", button_type='default_button',
            command=lambda: self.create_shape(points_list, name_entry, color_entry, popup_window))
        create_button.pack(side=LEFT)

        cancel_button = CustomButton(
            popup_buttons_frame, text="Cancel", command=popup_window.destroy, button_type='red_button')
        cancel_button.pack(side=LEFT)

    def add_curve(self,
                  matrix_entry: EntryWithPlaceholder, points_listbox: Listbox, points_list: list[tuple[float, float, float]]) -> None:
        if not (matrix_entry.validate(True)):
            return
        # TODO: extract points from matrix
        matrix_entry.clear()

    def remove_curve(self, points_listbox: Listbox, points_list: list[tuple[float, float]]) -> None:
        if len(points_listbox.curselection()) == 0:
            messagebox.showerror(parent=self.popup_window,
                                 title="Remove Line Error",
                                 message="Select a point")
        else:
            pos = points_listbox.curselection()[0]
            points_listbox.delete(pos)
            points_list.pop(pos)
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

    def create_shape(self, points_list: list[tuple[float, float]], name_entry: EntryWithPlaceholder, color_entry: Entry,
                     popup_window: Toplevel) -> None:
        if not name_entry.validate(False):
            return
        name = name_entry.get()
        self.graphic_system.create_shape(
            points_list, name, color_entry.get(), False, GraphicObjectType.CURVE_3D)
        popup_window.destroy()
        self.items_listbox.insert(
            "end", f"{GraphicObjectType.CURVE_3D}: {name}")
        self.items_dimensions_list.append(True)
        self.logger.log(
            f'Shape "{name}" created with points: {format_point_list(points_list)}.')
