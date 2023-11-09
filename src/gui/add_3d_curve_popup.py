from tkinter import *
from tkinter import messagebox, colorchooser
from tkinter import ttk

from gui.TextWithPlaceholder import TextWithPlaceholder
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
        self.matrices = []
        self.last_matrix = 0
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

        matrices_listbox = Listbox(points_frame, selectmode=SINGLE)
        matrices_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = Scrollbar(points_frame)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        matrices_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=matrices_listbox.yview)

        matrix_frame = Frame(popup_window)
        matrix_frame.pack(fill=BOTH, padx=10, pady=10, side=TOP, expand=True)

        matrix_entry = TextWithPlaceholder(matrix_frame, "Matrix string", height=10, width=50)
        matrix_entry.pack(side=LEFT, padx=10, expand=True, fill=BOTH)

        add_button = CustomButton(matrix_frame, text="Add Curve",
                                  command=lambda: self.add_curve(matrix_entry, matrices_listbox), button_type='default_button')
        add_button.pack(side=LEFT)

        remove_button = CustomButton(
            matrix_frame, text="Remove Curve", command=lambda: self.remove_curve(matrices_listbox),
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
            command=lambda: self.create_shape(name_entry, color_entry, popup_window))
        create_button.pack(side=LEFT)

        cancel_button = CustomButton(
            popup_buttons_frame, text="Cancel", command=popup_window.destroy, button_type='red_button')
        cancel_button.pack(side=LEFT)

    def add_curve(self,
                  matrix_entry: TextWithPlaceholder, matrices_listbox: Listbox) -> None:
        if not (matrix_entry.validate()):
            return
        coords, valid = self.get_coords_from_string(matrix_entry.get_value())
        if not valid:
            messagebox.showerror(parent=self.popup_window,
                                 title="Error",
                                 message=f"Invaldid matrix string. The matrix must be 4x4 and the string must follow "
                                         f"this example:\n"
                                         f"(x_11,y_11,z_11),(x_12,y_12,z_12),...;(x_21,y_21,z_21),(x_22,y_22,z_22),"
                                         f"...;...(x_ij,y_ij,z_ij)")
            return
        self.matrices.append(coords)
        self.last_matrix += 1
        matrices_listbox.insert("end",
                                f"Matrix {self.last_matrix}:    "
                                f"First point: {coords[0]}    Last point: {coords[-1]}")
        matrix_entry.clear()

    def get_coords_from_string(self, matrix_str: str) -> tuple[list[tuple[float, float, float]], bool]:
        try:
            coords = []
            matrix_str = matrix_str.strip()
            lines = matrix_str.split(";")
            if len(lines) != 4:
                return [], False
            for line in lines:
                line = line.split("),")
                if len(line) != 4:
                    return [], False
                for coord_str in line:
                    values = coord_str.strip("()").split(",")
                    coords_tuple = tuple(float(value) for value in values)
                    coords.append(coords_tuple)
            return coords, True
        except Exception:
            return [], False

    def remove_curve(self, matrices_listbox: Listbox) -> None:
        if len(matrices_listbox.curselection()) == 0:
            messagebox.showerror(parent=self.popup_window,
                                 title="Remove Matrix Error",
                                 message="Select a matrix")
        else:
            pos = matrices_listbox.curselection()[0]
            matrices_listbox.delete(pos)
            self.matrices.pop(pos)

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

    def create_shape(self, name_entry: EntryWithPlaceholder, color_entry: Entry,
                     popup_window: Toplevel) -> None:
        if len(self.matrices) == 0:
            messagebox.showerror(parent=self.popup_window,
                                 title="Error",
                                 message="At least one matrix is neeeded")
            return
        if not name_entry.validate(False):
            return
        name = name_entry.get()
        points_list = []
        for matrix in self.matrices:
            points_list.extend(matrix)
        self.graphic_system.create_shape(
            points_list, name, color_entry.get(), False, GraphicObjectType.BEZIER_CURVE_3D)
        popup_window.destroy()
        self.items_listbox.insert(
            "end", f"{GraphicObjectType.BEZIER_CURVE_3D}: {name}")
        self.items_dimensions_list.append(True)
        self.logger.log(
            f'Shape "{name}" created with points: {format_point_list(points_list)}.')
