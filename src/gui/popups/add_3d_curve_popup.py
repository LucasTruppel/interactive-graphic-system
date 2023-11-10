from tkinter import *
from tkinter import messagebox, colorchooser
from tkinter import ttk

from gui.widgets.text_with_placeholder import TextWithPlaceholder
from gui.widgets.entry_with_placeholder import EntryWithPlaceholder
from system.core.graphic_system import GraphicSystem
from system.graphic_objects.graphic_object import GraphicObjectType
from gui.style import BG_COLOR
from gui.widgets.logger import Logger
from gui.widgets.custom_button import CustomButton


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
        self.combobox = None
        self.type_var = None
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

        self.type_var = StringVar()
        self.combobox = ttk.Combobox(
            name_and_color_frame, textvariable=self.type_var, state="readonly")
        self.combobox["values"] = (GraphicObjectType.BEZIER_CURVE_3D, GraphicObjectType.B_SPLINE_CURVE_3D)
        self.combobox.bind("<<ComboboxSelected>>", lambda x: self.clear(matrices_listbox))
        self.combobox.current(0)
        self.combobox.pack(side=LEFT, padx=5)

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

    def add_curve(self, matrix_entry: TextWithPlaceholder, matrices_listbox: Listbox) -> None:
        if self.type_var.get() == GraphicObjectType.B_SPLINE_CURVE_3D and len(self.matrices) > 0:
            messagebox.showerror(parent=self.popup_window,
                                 title="Error",
                                 message=f"B spline curve must have only one matrix.")
            return
        if not (matrix_entry.validate()):
            return
        if self.type_var.get() == GraphicObjectType.BEZIER_CURVE_3D:
            coords, valid = self.parse_bezier_string(matrix_entry.get_value())
        else:
            coords, valid = self.parse_bspline_string(matrix_entry.get_value())
        if not valid:
            messagebox.showerror(parent=self.popup_window,
                                 title="Error",
                                 message=f"Invalid {self.type_var.get()} matrix string. The matrix string must follow this example:\n"
                                         f"(x_11,y_11,z_11),(x_12,y_12,z_12),...;(x_21,y_21,z_21),(x_22,y_22,z_22),"
                                         f"...;...(x_ij,y_ij,z_ij)")
            return
        self.matrices.append(coords)
        self.last_matrix += 1
        matrices_listbox.insert("end",
                                f"Matrix {self.last_matrix}:    "
                                f"First point: {coords[0][0]}    Last point: {coords[-1][-1]}")
        matrix_entry.clear()

    def parse_bezier_string(self, matrix_str: str) -> tuple[list, bool]:
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
                new_line = []
                for coord_str in line:
                    values = coord_str.strip("()").split(",")
                    coords_tuple = tuple(float(value) for value in values)
                    new_line.append(coords_tuple)
                coords.append(new_line)
            return coords, True
        except Exception:
            return [], False

    def parse_bspline_string(self, matrix_str: str) -> tuple[list, bool]:
        try:
            coords = []
            matrix_str = matrix_str.strip()
            lines = matrix_str.split(";")
            size = len(lines)
            if size < 4 or size > 20:
                return [], False
            for line in lines:
                line = line.split("),")
                if len(line) != size:
                    return [], False
                new_line = []
                for coord_str in line:
                    values = coord_str.strip("()").split(",")
                    coords_tuple = tuple(float(value) for value in values)
                    new_line.append(coords_tuple)
                coords.append(new_line)
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
        curve_type = self.type_var.get()
        self.graphic_system.create_shape(
            self.matrices, name, color_entry.get(), False, curve_type)
        popup_window.destroy()
        self.items_listbox.insert(
            "end", f"{curve_type}: {name}")
        self.items_dimensions_list.append(True)
        self.logger.log(
            f'Shape "{name}" created.')

    def clear(self, matrices_listbox: Listbox) -> None:
        matrices_listbox.delete("0", "end")
        self.matrices = []
