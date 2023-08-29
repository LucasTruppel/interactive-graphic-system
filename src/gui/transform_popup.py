from tkinter import *
from tkinter import messagebox
from gui.entry_with_placeholder import EntryWithPlaceholder
from system.graphic_system import GraphicSystem


class TransformPopup:

    def __init__(self, root, graphic_system: GraphicSystem, object_index: int):
        self.graphic_system = graphic_system
        self.object_index = object_index
        self.selected_rotation = StringVar()
        self.operation_listbox = None
        popup_window = Toplevel(root)
        self.init_popup(popup_window)

    def init_popup(self, popup_window):
        self.configure_popup(popup_window)
        main_popup_frame = Frame(popup_window)
        main_popup_frame.pack(fill=BOTH, expand=True)
        self.create_right_column(main_popup_frame)
        self.create_left_column(main_popup_frame, popup_window)

    def configure_popup(self, popup_window):
        popup_window.title("Transform Shape")
        popup_window.resizable(False, False)
        popup_window.configure(bg="#333333")

    def create_right_column(self, main_popup_frame):
        right_column_frame = Frame(main_popup_frame)
        right_column_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        right_column_frame.configure(bg="#333333")

        # Operation list
        operation_list_frame = Frame(right_column_frame)
        operation_list_frame.pack(fill=X, padx=10, pady=(10, 0))
        operation_list_frame.configure(bg="#333333")

        self.operation_listbox = Listbox(operation_list_frame, selectmode=SINGLE)
        self.operation_listbox.pack(side=LEFT, fill=BOTH, expand=True)

        # Remove operation button
        remove_operation_button = Button(
            right_column_frame, text="Remove Operation", width=25,
            command=lambda: self.remove_operation())
        remove_operation_button.pack(padx=10, pady=(10, 0))

    def create_left_column(self, main_popup_frame, popup_window):
        # Left Column
        left_column_frame = Frame(main_popup_frame)
        left_column_frame.pack(side=LEFT, fill=BOTH, expand=True)
        left_column_frame.configure(bg="#333333")

        # Translation
        translation_frame = Frame(left_column_frame)
        translation_frame.pack(fill=X, padx=10, pady=(10, 0))
        translation_frame.configure(bg="#333333")

        translation_label = Label(translation_frame, text="Translation")
        translation_label.pack(side=LEFT, padx=(0, 10))
        translation_label.configure(bg="#333333", fg="white")

        translation_entry_frame = Frame(translation_frame)
        translation_entry_frame.pack(side=LEFT, fill=X, expand=True)
        translation_entry_frame.configure(bg="#333333")

        dx_entry = EntryWithPlaceholder(translation_entry_frame, "Dx")
        dy_entry = EntryWithPlaceholder(translation_entry_frame, "Dy")
        dx_entry.pack(side=LEFT, padx=(0, 10))
        dy_entry.pack(side=LEFT, padx=(0, 10))

        add_translation_button = Button(
            translation_frame, text="Add Translation",
            command=lambda: self.add_translation(dx_entry, dy_entry))
        add_translation_button.pack(side=LEFT, padx=(0, 10))

        # Scaling
        scaling_frame = Frame(left_column_frame)
        scaling_frame.pack(fill=X, padx=10, pady=(10, 0))
        scaling_frame.configure(bg="#333333")

        scaling_label = Label(scaling_frame, text="Scaling")
        scaling_label.pack(side=LEFT, padx=(0, 10))
        scaling_label.configure(bg="#333333", fg="white")

        scaling_entry_frame = Frame(scaling_frame)
        scaling_entry_frame.pack(side=LEFT, fill=X, expand=True)
        scaling_entry_frame.configure(bg="#333333")

        sx_entry = EntryWithPlaceholder(scaling_entry_frame, "x")
        sy_entry = EntryWithPlaceholder(scaling_entry_frame, "y")
        sx_entry.pack(side=LEFT, padx=(0, 10))
        sy_entry.pack(side=LEFT, padx=(0, 10))

        add_scaling_button = Button(scaling_frame, text="Add Scaling",
                                    command=lambda: self.add_scaling(sx_entry, sy_entry))
        add_scaling_button.pack(side=LEFT, padx=(0, 10))

        # Rotation
        rotation_frame = Frame(left_column_frame)
        rotation_frame.pack(fill=X, padx=10, pady=(10, 0))
        rotation_frame.configure(bg="#333333")

        rotation_label = Label(rotation_frame, text="Rotation")
        rotation_label.pack(side=LEFT, padx=(0, 10))
        rotation_label.configure(bg="#333333", fg="white")

        rotation_radio_frame = Frame(rotation_frame)
        rotation_radio_frame.pack(side=LEFT, fill=X, expand=True)
        rotation_radio_frame.configure(bg="#333333")

        self.selected_rotation.set("object_center")

        world_center_radio_button = Radiobutton(
            rotation_radio_frame, text="World Center", variable=self.selected_rotation, value="world_center")
        world_center_radio_button.pack(side=LEFT, padx=(0, 10))
        object_center_radio_button = Radiobutton(
            rotation_radio_frame, text="Object Center", variable=self.selected_rotation, value="object_center")
        object_center_radio_button.pack(side=LEFT, padx=(0, 10))
        arbitrary_point_radio_button = Radiobutton(
            rotation_radio_frame, text="Arbitrary Point", variable=self.selected_rotation, value="arbitrary_point")
        arbitrary_point_radio_button.pack(side=LEFT, padx=(0, 10))

        rotation_entry_frame = Frame(rotation_frame)
        rotation_entry_frame.pack(side=LEFT, fill=X, expand=True)
        rotation_entry_frame.configure(bg="#333333")

        x_entry = EntryWithPlaceholder(rotation_entry_frame, "x")
        y_entry = EntryWithPlaceholder(rotation_entry_frame, "y")
        x_entry.pack(side=LEFT, padx=(0, 10))
        y_entry.pack(side=LEFT, padx=(0, 10))

        add_rotation_button = Button(rotation_frame, text="Add Rotation",
                                     command=lambda: self.add_rotation(x_entry, y_entry))
        add_rotation_button.pack(side=LEFT, padx=(0, 10))

        # Bottom ok and cancel buttons frame

        popup_buttons_frame = Frame(popup_window)
        popup_buttons_frame.pack(padx=10, pady=(0, 10), fill=X)
        popup_buttons_frame.configure(bg="#333333")

        tramsform_button = Button(
            popup_buttons_frame, text="Transform", width=25,
            command=lambda: self.transform_shape(self.operation_listbox.size(), popup_window))
        tramsform_button.pack(side=LEFT, padx=(5, 0), expand=True, fill="both")

        cancel_button = Button(
            popup_buttons_frame, text="Cancel", width=25, command=lambda: self.cancel_transformation(popup_window))
        cancel_button.pack(side=LEFT, padx=(0, 5), expand=True, fill="both")

    def add_translation(self, dx_entry: EntryWithPlaceholder, dy_entry: EntryWithPlaceholder):
        try:
            dx = float(dx_entry.get())
            dy = float(dy_entry.get())
            self.graphic_system.add_translation(dx, dy)
            self.operation_listbox.insert("end", f"Translation Dx:{dx:g} Dy:{dy:g}")
            dx_entry.clear()
            dy_entry.clear()
        except ValueError as e:
            if dx_entry.get() == "" or dy_entry.get() == "":
                messagebox.showerror(
                    "Add Translation Error", "Values must be specified")
            else:
                messagebox.showerror("Add Translation Error", "Invalid character")

    def add_scaling(self, sx_entry: EntryWithPlaceholder, sy_entry: EntryWithPlaceholder):
        try:
            sx = float(sx_entry.get())
            sy = float(sy_entry.get())
            self.graphic_system.add_scaling(self.object_index, sx, sy)
            self.operation_listbox.insert("end", f"Scaling Sx:{sx:g} Sy:{sy:g}")
            sx_entry.clear()
            sy_entry.clear()
        except ValueError as e:
            if sx_entry.get() == "" or sy_entry.get() == "":
                messagebox.showerror(
                    "Add Scaling Error", "Values must be specified")
            else:
                messagebox.showerror("Add Scaling Error", "Invalid character")

    def add_rotation(self, x_entry: EntryWithPlaceholder, y_entry: EntryWithPlaceholder):
        rotation_type = self.selected_rotation.get()
        if rotation_type == "arbitrary_point":
            try:
                x = float(x_entry.get())
                y = float(y_entry.get())
                self.graphic_system.add_rotation(x, y, 30, rotation_type, self.object_index)
                self.operation_listbox.insert("end", f"Rotation x:{x:g} y:{y:g}")
                x_entry.clear()
                y_entry.clear()
            except ValueError as e:
                if x_entry.get() == "" or y_entry.get() == "":
                    messagebox.showerror(
                        "Add Rotation Error", "Values must be specified")
                else:
                    messagebox.showerror("Add Rotation Error", "Invalid character")
        else:
            self.operation_listbox.insert("end", f"Rotation: {rotation_type.replace('_',' ')}")
            self.graphic_system.add_rotation(0, 0, 30, rotation_type, self.object_index)

    def remove_operation(self):
        if len(self.operation_listbox.curselection()) == 0:
            messagebox.showerror("Remove Operation Error", "Select an operation")
        else:
            pos = self.operation_listbox.curselection()[0]
            self.operation_listbox.delete(pos)
            self.graphic_system.remove_operation(pos)

    def transform_shape(self, operations_amount: int, popup_window: Toplevel):
        if operations_amount > 0:
            self.graphic_system.transform(self.object_index)
            popup_window.destroy()
        else:
            messagebox.showerror("Transform Error", "At least one operation is needed")

    def cancel_transformation(self, popup_window: Toplevel):
        self.graphic_system.clear_transformation()
        popup_window.destroy()
