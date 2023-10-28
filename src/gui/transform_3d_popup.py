from tkinter import *
from tkinter import messagebox

from gui.entry_with_placeholder import EntryWithPlaceholder
from system.core.graphic_system import GraphicSystem
from gui.style import BG_COLOR, FG_COLOR
from gui.custom_button import CustomButton


class Transform3dPopup:

    def __init__(self, root, graphic_system: GraphicSystem, object_index: int) -> None:
        self.graphic_system = graphic_system
        self.object_index = object_index
        self.selected_rotation = StringVar()
        self.operation_listbox = None
        self.popup_window = Toplevel(root)
        self.popup_window.attributes("-topmost", True)
        self.init_popup()

    def init_popup(self) -> None:
        self.graphic_system.clear_transformation(True)
        self.configure_popup()
        main_popup_frame = Frame(self.popup_window)
        main_popup_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.create_right_column(main_popup_frame)
        self.create_left_column(main_popup_frame)

    def configure_popup(self) -> None:
        self.popup_window.title("Transform Shape")
        self.popup_window.resizable(False, False)
        self.popup_window.configure(bg=BG_COLOR)

    def create_right_column(self, main_popup_frame) -> None:
        right_column_frame = Frame(main_popup_frame)
        right_column_frame.pack(side=RIGHT, fill=BOTH,
                                expand=True, padx=5, pady=5)
        right_column_frame.configure(bg=BG_COLOR)

        # Operation list
        operation_list_frame = Frame(right_column_frame)
        operation_list_frame.pack(
            fill=BOTH, expand=True, padx=5, pady=5)
        operation_list_frame.configure(bg=BG_COLOR)

        self.operation_listbox = Listbox(
            operation_list_frame, selectmode=SINGLE, width=50)
        self.operation_listbox.pack(side=LEFT, fill=BOTH, expand=True)

        # Remove operation button
        remove_operation_button = CustomButton(
            right_column_frame, text="Remove Operation",
            command=lambda: self.remove_operation(), button_type='red_button')
        remove_operation_button.pack()

    def create_left_column(self, main_popup_frame) -> None:
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
        dz_entry = EntryWithPlaceholder(translation_entry_frame, "Dz")
        dx_entry.pack(side=LEFT, padx=5)
        dy_entry.pack(side=LEFT, padx=5)
        dz_entry.pack(side=LEFT, padx=5)

        add_translation_button = CustomButton(
            translation_frame, text="Add Translation",
            command=lambda: self.add_translation(dx_entry, dy_entry, dz_entry))
        add_translation_button.pack(padx=5, pady=5)

        # Scaling
        scaling_frame = Frame(left_column_frame)
        scaling_frame.pack(fill=X, padx=5, pady=5)
        scaling_frame.configure(bg=BG_COLOR)

        scaling_label = Label(scaling_frame, text="Scaling")
        scaling_label.pack(padx=5)
        scaling_label.configure(bg=BG_COLOR, fg=FG_COLOR)

        scaling_entry_frame = Frame(scaling_frame)
        scaling_entry_frame.pack(fill=X, expand=True, padx=5, pady=5)
        scaling_entry_frame.configure(bg=BG_COLOR)

        sx_entry = EntryWithPlaceholder(scaling_entry_frame, "Sx")
        sy_entry = EntryWithPlaceholder(scaling_entry_frame, "Sy")
        sz_entry = EntryWithPlaceholder(scaling_entry_frame, "Sz")
        sx_entry.pack(side=LEFT, padx=5)
        sy_entry.pack(side=LEFT, padx=5)
        sz_entry.pack(side=LEFT, padx=5)

        add_scaling_button = CustomButton(scaling_frame, text="Add Scaling",
                                          command=lambda: self.add_scaling(sx_entry, sy_entry, sz_entry))
        add_scaling_button.pack(padx=5, pady=5)

        # Rotation
        rotation_frame = Frame(left_column_frame)
        rotation_frame.pack(fill=X, padx=5, pady=5)
        rotation_frame.configure(bg=BG_COLOR)

        rotation_label = Label(rotation_frame, text="Rotation")
        rotation_label.pack(padx=5, pady=5)
        rotation_label.configure(bg=BG_COLOR, fg=FG_COLOR)

        angle_entry = EntryWithPlaceholder(rotation_frame, "Angle")
        angle_entry.pack(padx=5, pady=5)

        rotation_radio_frame = Frame(rotation_frame)
        rotation_radio_frame.pack(fill=X, expand=True, padx=5, pady=5)
        rotation_radio_frame.configure(bg=BG_COLOR)

        self.selected_rotation.set("object_center")

        world_center_radio_button = Radiobutton(
            rotation_radio_frame, text="X Axis", variable=self.selected_rotation, value="x_axis")
        world_center_radio_button.pack(padx=5, pady=5)
        world_center_radio_button = Radiobutton(
            rotation_radio_frame, text="Y Axis", variable=self.selected_rotation, value="y_axis")
        world_center_radio_button.pack(padx=5, pady=5)
        world_center_radio_button = Radiobutton(
            rotation_radio_frame, text="Z Axis", variable=self.selected_rotation, value="z_axis")
        world_center_radio_button.pack(padx=5, pady=5)
        object_center_radio_button = Radiobutton(
            rotation_radio_frame, text="Object Center Axis", variable=self.selected_rotation, value="object_center")
        object_center_radio_button.pack(padx=5, pady=5)
        arbitrary_point_radio_button = Radiobutton(
            rotation_radio_frame, text="Arbitrary Axis", variable=self.selected_rotation, value="arbitrary_axis")
        arbitrary_point_radio_button.pack(padx=5, pady=5)

        rotation_entry_frame1 = Frame(rotation_frame)
        rotation_entry_frame1.pack(fill=X, expand=True, padx=5, pady=5)
        rotation_entry_frame1.configure(bg=BG_COLOR)

        x1_entry = EntryWithPlaceholder(rotation_entry_frame1, "x1")
        y1_entry = EntryWithPlaceholder(rotation_entry_frame1, "y1")
        z1_entry = EntryWithPlaceholder(rotation_entry_frame1, "z1")
        x1_entry.pack(side=LEFT, padx=5, pady=5)
        y1_entry.pack(side=LEFT, padx=5, pady=5)
        z1_entry.pack(side=LEFT, padx=5, pady=5)

        rotation_entry_frame2 = Frame(rotation_frame)
        rotation_entry_frame2.pack(fill=X, expand=True, padx=5, pady=5)
        rotation_entry_frame2.configure(bg=BG_COLOR)

        x2_entry = EntryWithPlaceholder(rotation_entry_frame2, "x2")
        y2_entry = EntryWithPlaceholder(rotation_entry_frame2, "y2")
        z2_entry = EntryWithPlaceholder(rotation_entry_frame2, "z2")
        x2_entry.pack(side=LEFT, padx=5, pady=5)
        y2_entry.pack(side=LEFT, padx=5, pady=5)
        z2_entry.pack(side=LEFT, padx=5, pady=5)

        add_rotation_button = CustomButton(rotation_frame, text="Add Rotation",
                                           command=lambda: self.add_rotation(x1_entry, y1_entry, z1_entry,
                                                                             x2_entry, y2_entry, z2_entry,
                                                                             angle_entry))
        add_rotation_button.pack(padx=5, pady=5)

        # Bottom ok and cancel buttons frame

        popup_buttons_frame = Frame(self.popup_window)
        popup_buttons_frame.pack(padx=5, pady=5, fill=X, side=RIGHT)
        popup_buttons_frame.configure(bg=BG_COLOR)

        tramsform_button = CustomButton(
            popup_buttons_frame, text="Transform",
            command=lambda: self.transform_shape(self.operation_listbox.size(), self.popup_window), button_type='default_button')
        tramsform_button.pack(side=LEFT)

        cancel_button = CustomButton(
            popup_buttons_frame, text="Cancel", command=lambda: self.cancel_transformation(self.popup_window), button_type='red_button')
        cancel_button.pack(side=LEFT)

    def add_translation(self, dx_entry: EntryWithPlaceholder, dy_entry: EntryWithPlaceholder,
                        dz_entry: EntryWithPlaceholder) -> None:
        try:
            dx = float(dx_entry.get())
            dy = float(dy_entry.get())
            dz = float(dy_entry.get())
            self.graphic_system.add_translation(dx, dy, dz)
            self.operation_listbox.insert(
                "end", f"Translation Dx:{dx:g} Dy:{dy:g} Dz:{dz:g}")
            dx_entry.clear()
            dy_entry.clear()
            dz_entry.clear()
        except ValueError as e:
            if dx_entry.get() == "" or dy_entry.get() == "" or dz_entry.get() == "":
                messagebox.showerror(parent=self.popup_window,
                                     title="Add Translation Error",
                                     message="Values must be specified")
            else:
                messagebox.showerror(parent=self.popup_window,
                                     title="Add Translation Error",
                                     message="Invalid character")

    def add_scaling(self, sx_entry: EntryWithPlaceholder, sy_entry: EntryWithPlaceholder,
                    sz_entry: EntryWithPlaceholder) -> None:
        try:
            sx = float(sx_entry.get())
            sy = float(sy_entry.get())
            sz = float(sy_entry.get())
            self.graphic_system.add_scaling(self.object_index, sx, sy, sz)
            self.operation_listbox.insert(
                "end", f"Scaling Sx:{sx:g} Sy:{sy:g} Sz:{sz:g}")
            sx_entry.clear()
            sy_entry.clear()
            sz_entry.clear()
        except ValueError as e:
            if sx_entry.get() == "" or sy_entry.get() == "" or sz_entry.get() == "":
                messagebox.showerror(parent=self.popup_window,
                                     title="Add Scaling Error",
                                     message="Values must be specified")
            else:
                messagebox.showerror(parent=self.popup_window,
                                     title="Add Scaling Error",
                                     message="Invalid character")

    def add_rotation(self,
                     x1_entry: EntryWithPlaceholder, y1_entry: EntryWithPlaceholder, z1_entry: EntryWithPlaceholder,
                     x2_entry: EntryWithPlaceholder, y2_entry: EntryWithPlaceholder, z2_entry: EntryWithPlaceholder,
                     angle_entry: EntryWithPlaceholder) -> None:
        if not (angle_entry.validate(True)):
            return
        angle = float(angle_entry.get())
        rotation_type = self.selected_rotation.get()
        if rotation_type == "arbitrary_axis":
            self.add_arbitrary_axis_rotation(x1_entry, y1_entry, z1_entry, x2_entry, y2_entry, z2_entry, angle)
        else:
            self.operation_listbox.insert("end",
                                          f"Rotation {rotation_type.replace('_', ' ')} angle:{angle:g}")
            self.graphic_system.add_rotation3d(angle, rotation_type, self.object_index)
        angle_entry.clear()

    def add_arbitrary_axis_rotation(self,
                                    x1_entry: EntryWithPlaceholder, y1_entry: EntryWithPlaceholder,
                                    z1_entry: EntryWithPlaceholder,
                                    x2_entry: EntryWithPlaceholder, y2_entry: EntryWithPlaceholder,
                                    z2_entry: EntryWithPlaceholder,
                                    angle: float) -> None:
        if not (x1_entry.validate(True) and y1_entry.validate(True) and z1_entry.validate(True) and
                x2_entry.validate(True) and y2_entry.validate(True) and z2_entry.validate(True)):
            return
        x1, y1, z1 = float(x1_entry.get()), float(y1_entry.get()), float(z1_entry.get())
        x2, y2, z2 = float(x2_entry.get()), float(y2_entry.get()), float(z2_entry.get())
        x1_entry.clear()
        y1_entry.clear()
        z1_entry.clear()
        x2_entry.clear()
        y2_entry.clear()
        z2_entry.clear()
        self.operation_listbox.insert(
            "end", f"Arbitrary Rotation x1:{x1:g} y1:{y1:g} z1:{z1:g} x2:{x2:g} y2:{y2:g} z2:{z2:g} angle:{angle:g}")
        self.graphic_system.add_arbitrary_rotation3d(angle, x1, y1, z1, x2, y2, z2)

    def remove_operation(self) -> None:
        if len(self.operation_listbox.curselection()) == 0:
            messagebox.showerror(parent=self.popup_window,
                                 title="Remove Operation Error",
                                 message="Select an operation")
        else:
            pos = self.operation_listbox.curselection()[0]
            self.operation_listbox.delete(pos)
            self.graphic_system.remove_operation(pos)

    def transform_shape(self, operations_amount: int, popup_window: Toplevel) -> None:
        if operations_amount > 0:
            self.graphic_system.transform(self.object_index)
            popup_window.destroy()
        else:
            messagebox.showerror(parent=self.popup_window,
                                 title="Transform Error",
                                 message="At least one operation is needed")

    def cancel_transformation(self, popup_window: Toplevel) -> None:
        self.graphic_system.clear_transformation(True)
        popup_window.destroy()
