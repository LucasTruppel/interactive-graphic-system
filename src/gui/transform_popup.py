from tkinter import *
from tkinter import messagebox
from gui.entry_with_placeholder import EntryWithPlaceholder
from system.graphic_system import GraphicSystem
from gui.style import BG_COLOR, FG_COLOR


class TransformPopup:

    def __init__(self, root, graphic_system: GraphicSystem, object_index: int) -> None:
        self.graphic_system = graphic_system
        self.object_index = object_index
        self.selected_rotation = StringVar()
        self.operation_listbox = None
        popup_window = Toplevel(root)
        self.init_popup(popup_window)

    def init_popup(self, popup_window) -> None:
        self.graphic_system.clear_transformation()
        self.configure_popup(popup_window)
        main_popup_frame = Frame(popup_window)
        main_popup_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.create_right_column(main_popup_frame)
        self.create_left_column(main_popup_frame, popup_window)

    def configure_popup(self, popup_window) -> None:
        popup_window.title("Transform Shape")
        popup_window.resizable(False, False)
        popup_window.configure(bg=BG_COLOR)

    def create_right_column(self, main_popup_frame) -> None:
        right_column_frame = Frame(main_popup_frame)
        right_column_frame.pack(side=RIGHT, fill=BOTH,
                                expand=True, padx=5, pady=5)
        right_column_frame.configure(bg=BG_COLOR)

        # Operation list
        operation_list_frame = Frame(right_column_frame)
        operation_list_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        operation_list_frame.configure(bg=BG_COLOR)

        self.operation_listbox = Listbox(
            operation_list_frame, selectmode=SINGLE)
        self.operation_listbox.pack(side=LEFT, fill=BOTH, expand=True)

        # Remove operation button
        remove_operation_button = Button(
            right_column_frame, text="Remove Operation", width=25,
            command=lambda: self.remove_operation())
        remove_operation_button.pack(padx=10, pady=(10, 0))

    def create_left_column(self, main_popup_frame, popup_window) -> None:
        # Left Column
        left_column_frame = Frame(main_popup_frame)
        left_column_frame.pack(side=LEFT, fill=BOTH,
                               expand=True, padx=5, pady=5)
        left_column_frame.configure(bg=BG_COLOR)

        # Translation
        translation_frame = Frame(left_column_frame)
        translation_frame.pack(fill=X, padx=5, pady=5)
        translation_frame.configure(bg=BG_COLOR)

        translation_label = Label(translation_frame, text="Translation")
        translation_label.pack(padx=5, pady=5)
        translation_label.configure(bg=BG_COLOR, fg=FG_COLOR)

        translation_entry_frame = Frame(translation_frame)
        translation_entry_frame.pack(fill=X, expand=True, padx=5, pady=5)
        translation_entry_frame.configure(bg=BG_COLOR)

        dx_entry = EntryWithPlaceholder(translation_entry_frame, "Dx")
        dy_entry = EntryWithPlaceholder(translation_entry_frame, "Dy")
        dx_entry.pack(side=LEFT, padx=(0, 10))
        dy_entry.pack(side=LEFT, padx=(0, 10))

        add_translation_button = Button(
            translation_frame, text="Add Translation",
            command=lambda: self.add_translation(dx_entry, dy_entry))
        add_translation_button.pack(padx=5, pady=5)

        # Scaling
        scaling_frame = Frame(left_column_frame)
        scaling_frame.pack(fill=X, padx=5, pady=5)
        scaling_frame.configure(bg=BG_COLOR)

        scaling_label = Label(scaling_frame, text="Scaling")
        scaling_label.pack(padx=(0, 10))
        scaling_label.configure(bg=BG_COLOR, fg=FG_COLOR)

        scaling_entry_frame = Frame(scaling_frame)
        scaling_entry_frame.pack(fill=X, expand=True, padx=5, pady=5)
        scaling_entry_frame.configure(bg=BG_COLOR)

        sx_entry = EntryWithPlaceholder(scaling_entry_frame, "Sx")
        sy_entry = EntryWithPlaceholder(scaling_entry_frame, "Sy")
        sx_entry.pack(side=LEFT, padx=(0, 10))
        sy_entry.pack(side=LEFT, padx=(0, 10))

        add_scaling_button = Button(scaling_frame, text="Add Scaling",
                                    command=lambda: self.add_scaling(sx_entry, sy_entry))
        add_scaling_button.pack(padx=5, pady=5)

        # Rotation
        rotation_frame = Frame(left_column_frame)
        rotation_frame.pack(fill=X, padx=5, pady=5)
        rotation_frame.configure(bg=BG_COLOR)

        rotation_label = Label(rotation_frame, text="Rotation")
        rotation_label.pack(padx=5, pady=5)
        rotation_label.configure(bg=BG_COLOR, fg=FG_COLOR)

        rotation_radio_frame = Frame(rotation_frame)
        rotation_radio_frame.pack(fill=X, expand=True, padx=5, pady=5)
        rotation_radio_frame.configure(bg=BG_COLOR)

        self.selected_rotation.set("object_center")

        world_center_radio_button = Radiobutton(
            rotation_radio_frame, text="World Center", variable=self.selected_rotation, value="world_center")
        world_center_radio_button.pack(padx=5, pady=5)
        object_center_radio_button = Radiobutton(
            rotation_radio_frame, text="Object Center", variable=self.selected_rotation, value="object_center")
        object_center_radio_button.pack(padx=5, pady=5)
        arbitrary_point_radio_button = Radiobutton(
            rotation_radio_frame, text="Arbitrary Point", variable=self.selected_rotation, value="arbitrary_point")
        arbitrary_point_radio_button.pack(padx=5, pady=5)

        rotation_entry_frame = Frame(rotation_frame)
        rotation_entry_frame.pack(fill=X, expand=True, padx=5, pady=5)
        rotation_entry_frame.configure(bg=BG_COLOR)

        x_entry = EntryWithPlaceholder(rotation_entry_frame, "x")
        y_entry = EntryWithPlaceholder(rotation_entry_frame, "y")
        x_entry.pack(side=LEFT, padx=5, pady=5)
        y_entry.pack(side=LEFT, padx=5, pady=5)

        angle_entry = EntryWithPlaceholder(rotation_frame, "Angle")
        angle_entry.pack(padx=5, pady=5)

        add_rotation_button = Button(rotation_frame, text="Add Rotation",
                                     command=lambda: self.add_rotation(x_entry, y_entry, angle_entry))
        add_rotation_button.pack(padx=5, pady=5)

        # Bottom ok and cancel buttons frame

        popup_buttons_frame = Frame(popup_window)
        popup_buttons_frame.pack(padx=5, pady=5, fill=X)
        popup_buttons_frame.configure(bg=BG_COLOR)

        tramsform_button = Button(
            popup_buttons_frame, text="Transform", width=25,
            command=lambda: self.transform_shape(self.operation_listbox.size(), popup_window))
        tramsform_button.pack(side=LEFT, padx=5, pady=5,
                              expand=True, fill="both")

        cancel_button = Button(
            popup_buttons_frame, text="Cancel", width=25, command=lambda: self.cancel_transformation(popup_window))
        cancel_button.pack(side=LEFT, padx=5, pady=5,
                           expand=True, fill="both")

    def add_translation(self, dx_entry: EntryWithPlaceholder, dy_entry: EntryWithPlaceholder) -> None:
        try:
            dx = float(dx_entry.get())
            dy = float(dy_entry.get())
            self.graphic_system.add_translation(dx, dy)
            self.operation_listbox.insert(
                "end", f"Translation Dx:{dx:g} Dy:{dy:g}")
            dx_entry.clear()
            dy_entry.clear()
        except ValueError as e:
            if dx_entry.get() == "" or dy_entry.get() == "":
                messagebox.showerror(
                    "Add Translation Error", "Values must be specified")
            else:
                messagebox.showerror(
                    "Add Translation Error", "Invalid character")

    def add_scaling(self, sx_entry: EntryWithPlaceholder, sy_entry: EntryWithPlaceholder) -> None:
        try:
            sx = float(sx_entry.get())
            sy = float(sy_entry.get())
            self.graphic_system.add_scaling(self.object_index, sx, sy)
            self.operation_listbox.insert(
                "end", f"Scaling Sx:{sx:g} Sy:{sy:g}")
            sx_entry.clear()
            sy_entry.clear()
        except ValueError as e:
            if sx_entry.get() == "" or sy_entry.get() == "":
                messagebox.showerror(
                    "Add Scaling Error", "Values must be specified")
            else:
                messagebox.showerror("Add Scaling Error", "Invalid character")

    def add_rotation(self, x_entry: EntryWithPlaceholder, y_entry: EntryWithPlaceholder,
                     angle_entry: EntryWithPlaceholder) -> None:
        rotation_type = self.selected_rotation.get()
        if not (angle_entry.validate(True)):
            return
        angle = float(angle_entry.get())
        if rotation_type == "arbitrary_point":
            if not (x_entry.validate(True) and y_entry.validate(True)):
                return
            x = float(x_entry.get())
            y = float(y_entry.get())
            x_entry.clear()
            y_entry.clear()
            self.operation_listbox.insert("end", f"Rotation x:{x:g} y:{y:g} angle:{angle:g}")
        else:
            x = 0
            y = 0
            self.operation_listbox.insert("end",
                                          f"Rotation {rotation_type.replace('_', ' ')} angle:{angle:g}")
        angle_entry.clear()
        self.graphic_system.add_rotation(x, y, angle, rotation_type, self.object_index)

    def remove_operation(self) -> None:
        if len(self.operation_listbox.curselection()) == 0:
            messagebox.showerror("Remove Operation Error",
                                 "Select an operation")
        else:
            pos = self.operation_listbox.curselection()[0]
            self.operation_listbox.delete(pos)
            self.graphic_system.remove_operation(pos)

    def transform_shape(self, operations_amount: int, popup_window: Toplevel) -> None:
        if operations_amount > 0:
            self.graphic_system.transform(self.object_index)
            popup_window.destroy()
        else:
            messagebox.showerror(
                "Transform Error", "At least one operation is needed")

    def cancel_transformation(self, popup_window: Toplevel) -> None:
        self.graphic_system.clear_transformation()
        popup_window.destroy()
