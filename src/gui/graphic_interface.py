from tkinter import *
from tkinter import messagebox, colorchooser
from gui.entry_with_placeholder import EntryWithPlaceholder
from system.graphic_system import GraphicSystem


class GraphicInterface:

    def __init__(self) -> None:
        self.WIDTH = 1600
        self.HEIGHT = 900

        self.main_window = Tk()
        self.items_listbox = None
        self.console_text = None
        self.graphic_system = None

        self.init_tkinter()

    def init_tkinter(self) -> None:
        self.configure_main_window()
        self.create_interface()
        self.main_window.mainloop()

    def configure_main_window(self) -> None:
        self.main_window.title("Interactive Graphic System")
        self.main_window.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.main_window.resizable(False, False)
        self.main_window.configure(bg="#333333")

    def create_interface(self) -> None:
        left_frame = Frame(self.main_window)
        left_frame.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)

        self.create_objects_list_frame(left_frame)
        self.create_buttons_frame(left_frame)
        self.create_camera_controls_frame(left_frame)
        self.create_zoom_controls_frame(left_frame)

        right_frame = Frame(self.main_window)
        right_frame.pack(side=RIGHT, padx=10, pady=10, fill=BOTH, expand=True)

        self.create_viewport_frame(right_frame)
        self.create_console_frame(right_frame)

    def create_console_frame(self, right_frame: Frame) -> None:
        console_frame = Frame(right_frame)
        console_frame.pack(fill=BOTH, expand=True)
        self.console_text = Text(right_frame, height=self.HEIGHT * 0.2,
                                 width=50, wrap=WORD, state="disabled")
        self.console_text.pack(side=BOTTOM, fill=BOTH)

    def create_viewport_frame(self, right_frame: Frame) -> None:
        viewport_margin = 15
        viewport_frame = Frame(
            right_frame, padx=viewport_margin, pady=viewport_margin)
        viewport_frame.pack(fill=BOTH, expand=True)

        viewport_width = int(self.WIDTH * 0.75) - 2 * viewport_margin
        viewport_height = self.HEIGHT * 0.8 - 2 * viewport_margin
        viewport_canvas = Canvas(
            viewport_frame, width=viewport_width, height=viewport_height, borderwidth=2, relief="solid")
        viewport_canvas.pack(fill=BOTH, expand=True)

        self.graphic_system = GraphicSystem(
            viewport_width, viewport_height, viewport_canvas)

    def create_objects_list_frame(self, parent_frame: Frame) -> None:
        items_frame = Frame(parent_frame)
        items_frame.pack(fill=BOTH, expand=True)

        self.items_listbox = Listbox(items_frame, selectmode=SINGLE)
        self.items_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        self.items_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.items_listbox.yview)

    def create_buttons_frame(self, parent_frame: Frame) -> None:
        buttons_frame = Frame(parent_frame, padx=10,
                              pady=10, borderwidth=2, relief="solid")
        buttons_frame.pack()

        add_shape_button = Button(
            buttons_frame, text="Add Shape", command=self.add_shape_popup)
        add_shape_button.pack(padx=5, pady=5, side=LEFT, ipadx=5, ipady=5)

        transform_button = Button(
            buttons_frame, text="Transform Shape",
            command=lambda: self.transform())
        transform_button.pack(padx=5, pady=5, side=LEFT, ipadx=5, ipady=5)

        remove_button = Button(
            buttons_frame, text="Remove Shape", command=self.remove_shape, background="#C95052", fg="white")
        remove_button.pack(padx=5, pady=5, side=LEFT, ipadx=5, ipady=5)

    def create_camera_controls_frame(self, parent_frame: Frame) -> None:
        camera_controls_frame = Frame(
            parent_frame, padx=10, pady=10)
        camera_controls_frame.pack(ipadx=10, ipady=10)

        up_button = Button(camera_controls_frame,
                           text="⬆", command=self.move_up)
        down_button = Button(camera_controls_frame,
                             text="⬇️", command=self.move_down)
        left_button = Button(camera_controls_frame,
                             text="⬅️", command=self.move_left)
        right_button = Button(camera_controls_frame,
                              text="➡️", command=self.move_right)

        button_padding = 5

        up_button.pack(side=TOP, padx=button_padding, pady=button_padding,
                       ipadx=button_padding, ipady=button_padding)
        down_button.pack(side=BOTTOM, padx=button_padding,
                         pady=button_padding, ipadx=button_padding, ipady=button_padding)
        left_button.pack(side=LEFT, padx=button_padding, pady=button_padding,
                         ipadx=button_padding, ipady=button_padding)
        right_button.pack(side=RIGHT, padx=button_padding,
                          pady=button_padding, ipadx=button_padding, ipady=button_padding)

    def create_zoom_controls_frame(self, parent_frame: Frame) -> None:
        zoom_controls_frame = Frame(
            parent_frame, padx=10, pady=10)
        zoom_controls_frame.pack()

        zoom_in_button = Button(zoom_controls_frame,
                                text="Zoom In", command=self.zoom_in)
        zoom_out_button = Button(
            zoom_controls_frame, text="Zoom Out", command=self.zoom_out)

        zoom_in_button.pack(padx=5, pady=5, side=LEFT, ipadx=5, ipady=5)
        zoom_out_button.pack(padx=5, pady=5, side=LEFT, ipadx=5, ipady=5)

    def add_shape_popup(self) -> None:
        popup_window = Toplevel(self.main_window)
        popup_window.title("Add Shape")
        popup_window.resizable(False, False)
        popup_window.configure(bg="#333333")

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
        entry_frame.configure(bg="#333333")

        x_entry = EntryWithPlaceholder(entry_frame, "x")
        y_entry = EntryWithPlaceholder(entry_frame, "y")

        x_entry.pack(side=LEFT, padx=(0, 10))
        y_entry.pack(side=LEFT, padx=(0, 10))

        points_list = []
        add_button = Button(entry_frame, text="Add Point",
                            command=lambda: self.add_point(x_entry, y_entry, points_listbox, points_list))
        add_button.pack(side=LEFT, expand=True, fill='both')

        # Button to remove selected point
        remove_button = Button(
            popup_window, text="Remove Selected Point", width=25, command=lambda: self.remove_point(points_listbox, points_list))
        remove_button.pack(pady=(0, 10))

        # Name entry and pick color button frame
        name_and_color_frame = Frame(popup_window)
        name_and_color_frame.pack(padx=10, pady=(0, 10), fill=X)
        name_and_color_frame.configure(bg="#333333")

        name_entry = EntryWithPlaceholder(name_and_color_frame, "Name")
        name_entry.pack(side=LEFT, padx=10, pady=(0, 10), fill=X, expand=True)

        color_entry = Entry()
        color_entry.insert(0, "#000000")
        color_button = Button(name_and_color_frame, text="Pick a color", command=lambda: self.pick_color(color_entry))
        color_button.pack(side=RIGHT, padx=10, pady=(0, 10), fill=X)

        popup_buttons_frame = Frame(popup_window)
        popup_buttons_frame.pack(padx=10, pady=(0, 10), fill=X)
        popup_buttons_frame.configure(bg="#333333")

        create_button = Button(
            popup_buttons_frame, text="Create Shape", width=25, command=lambda: self.create_shape(points_list, name_entry, color_entry, popup_window))
        create_button.pack(side=LEFT, padx=(5, 0), expand=True, fill="both")

        cancel_button = Button(
            popup_buttons_frame, text="Cancel", width=25, command=popup_window.destroy)
        cancel_button.pack(side=LEFT, padx=(0, 5), expand=True, fill="both")

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

    def pick_color(self, color_entry: Entry):
        new_color = colorchooser.askcolor()[1]
        if new_color is not None:
            color = new_color
        else:
            color = color_entry.get()
        color_entry.delete(0, END)
        color_entry.insert(0, color)

    def remove_shape(self) -> None:
        if len(self.items_listbox.curselection()) == 0:
            messagebox.showerror("Remove Shape Error", "Select a shape")
        else:
            pos = self.items_listbox.curselection()[0]
            self.items_listbox.delete(pos)
            name = self.graphic_system.remove_shape(pos)
            self.log(f'Shape "{name}" deleted.')

    def create_shape(self, points_list: list[tuple[float, float]], name_entry: Entry, color_entry: Entry,
                     popup_window: Toplevel) -> None:
        name = name_entry.get()
        if len(points_list) > 0:
            if name != "" and name != "Name":
                self.graphic_system.create_shape(points_list, name, color_entry.get())
                popup_window.destroy()
                self.items_listbox.insert("end", name)
                self.log(
                    f'Shape "{name}" created with points: {self.format_point_list(points_list)}.')
            else:
                messagebox.showerror("Create Shape Error",
                                     "Shape name must be specified")
        else:
            messagebox.showerror("Create Shape Error",
                                 "At least one point is needed")

    def format_point_list(self, points_list: list[tuple[float, float]]) -> str:
        return (str(points_list)
                .replace("[", "")
                .replace("]", "")
                .replace(".0,", ",")
                .replace(".0)", ")"))

    def move_up(self) -> None:
        self.graphic_system.move_up()

    def move_down(self) -> None:
        self.graphic_system.move_down()

    def move_left(self) -> None:
        self.graphic_system.move_left()

    def move_right(self) -> None:
        self.graphic_system.move_right()

    def zoom_in(self) -> None:
        self.graphic_system.zoom_in()

    def zoom_out(self) -> None:
        self.graphic_system.zoom_out()

    def log(self, text: str) -> None:
        self.console_text.configure(state="normal")
        self.console_text.insert("end", text + "\n")
        self.console_text.see("end")
        self.console_text.configure(state="disabled")

    def transform(self):
        if len(self.items_listbox.curselection()) == 0:
            messagebox.showerror("Transform Shape", "Select a shape")
        else:
            pos = self.items_listbox.curselection()[0]
            self.transform_popup(pos)

    def transform_popup(self, object_index: int):
        popup_window = Toplevel(self.main_window)
        popup_window.title("Transform Shape")
        popup_window.resizable(False, False)
        popup_window.configure(bg="#333333")

        # Top frame
        main_popup_frame = Frame(popup_window)
        main_popup_frame.pack(fill=BOTH, expand=True)

        # Right Column
        right_column_frame = Frame(main_popup_frame)
        right_column_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        right_column_frame.configure(bg="#333333")

        # Operation list
        operation_list_frame = Frame(right_column_frame)
        operation_list_frame.pack(fill=X, padx=10, pady=(10, 0))
        operation_list_frame.configure(bg="#333333")

        operation_listbox = Listbox(operation_list_frame, selectmode=SINGLE)
        operation_listbox.pack(side=LEFT, fill=BOTH, expand=True)

        # Remove operation button
        remove_operation_button = Button(
            right_column_frame, text="Remove Operation", width=25, command=lambda: self.remove_operation(operation_listbox))
        remove_operation_button.pack(padx=10, pady=(10, 0))

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
            translation_frame, text="Add Translation", command=lambda: self.add_translation(dx_entry, dy_entry, operation_listbox))
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
                                    command=lambda: self.add_scaling(object_index, sx_entry, sy_entry,
                                                                     operation_listbox))
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

        self.selected_rotation = StringVar()
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
                                     command=lambda: self.add_rotation(object_index, x_entry, y_entry, operation_listbox))
        add_rotation_button.pack(side=LEFT, padx=(0, 10))

        # Bottom ok and cancel buttons frame

        popup_buttons_frame = Frame(popup_window)
        popup_buttons_frame.pack(padx=10, pady=(0, 10), fill=X)
        popup_buttons_frame.configure(bg="#333333")

        tramsform_button = Button(
            popup_buttons_frame, text="Transform", width=25, command=lambda: self.transform_shape(operation_listbox.size() ,object_index, popup_window))
        tramsform_button.pack(side=LEFT, padx=(5, 0), expand=True, fill="both")

        cancel_button = Button(
            popup_buttons_frame, text="Cancel", width=25, command=lambda: self.cancel_transformation(popup_window))
        cancel_button.pack(side=LEFT, padx=(0, 5), expand=True, fill="both")

    def add_translation(self, dx_entry: EntryWithPlaceholder, dy_entry: EntryWithPlaceholder, operation_listbox: Listbox):
        try:
            dx = float(dx_entry.get())
            dy = float(dy_entry.get())
            self.graphic_system.add_translation(dx, dy)
            operation_listbox.insert("end", f"Translation Dx:{dx:g} Dy:{dy:g}")
            dx_entry.clear()
            dy_entry.clear()
        except ValueError as e:
            if dx_entry.get() == "" or dy_entry.get() == "":
                messagebox.showerror(
                    "Add Translation Error", "Values must be specified")
            else:
                messagebox.showerror("Add Translation Error", "Invalid character")

    def add_scaling(self, object_index: int, sx_entry: EntryWithPlaceholder, sy_entry: EntryWithPlaceholder, operation_listbox: Listbox):
        try:
            sx = float(sx_entry.get())
            sy = float(sy_entry.get())
            self.graphic_system.add_scaling(object_index, sx, sy)
            operation_listbox.insert("end", f"Scaling Sx:{sx:g} Sy:{sy:g}")
            sx_entry.clear()
            sy_entry.clear()
        except ValueError as e:
            if sx_entry.get() == "" or sy_entry.get() == "":
                messagebox.showerror(
                    "Add Scaling Error", "Values must be specified")
            else:
                messagebox.showerror("Add Scaling Error", "Invalid character")

    def add_rotation(self, object_index: int, x_entry: EntryWithPlaceholder, y_entry: EntryWithPlaceholder,
                     operation_listbox: Listbox):
        rotation_type = self.selected_rotation.get()
        if rotation_type == "arbitrary_point":
            try:
                x = float(x_entry.get())
                y = float(y_entry.get())
                self.graphic_system.add_rotation(x, y, 30, rotation_type, object_index)
                operation_listbox.insert("end", f"Rotation x:{x:g} y:{y:g}")
                x_entry.clear()
                y_entry.clear()
            except ValueError as e:
                if x_entry.get() == "" or y_entry.get() == "":
                    messagebox.showerror(
                        "Add Rotation Error", "Values must be specified")
                else:
                    messagebox.showerror("Add Rotation Error", "Invalid character")
        else:
            operation_listbox.insert("end", f"Rotation: {rotation_type.replace('_',' ')}")
            self.graphic_system.add_rotation(0, 0, 30, rotation_type, object_index)

    def remove_operation(self, operation_listbox: Listbox):
        if len(operation_listbox.curselection()) == 0:
            messagebox.showerror("Remove Operation Error", "Select an operation")
        else:
            pos = operation_listbox.curselection()[0]
            operation_listbox.delete(pos)
            self.graphic_system.remove_operation(pos)

    def transform_shape(self, operations_amount: int, object_index: int, popup_window: Toplevel):
        if operations_amount > 0:
            self.graphic_system.transform(object_index)
            popup_window.destroy()
        else:
            messagebox.showerror("Transform Error", "At least one operation is needed")

    def cancel_transformation(self, popup_window: Toplevel):
        self.graphic_system.clear_transformation()
        popup_window.destroy()
