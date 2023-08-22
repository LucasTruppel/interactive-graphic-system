from tkinter import *
from tkinter import messagebox
from entry_with_placeholder import EntryWithPlaceholder
from graphic_system import GraphicSystem


class GraphicInterface:

    def __init__(self) -> None:
        self.WIDTH = 1600
        self.HEIGHT = 900

        self.main_window = Tk()
        self.items_listbox = None
        self.console_text = None
        self.init_tkinter()

    def init_tkinter(self) -> None:
        self.configure_main_window()
        self.create_interface()
        self.main_window.mainloop()

    def configure_main_window(self) -> None:
        self.main_window.title("Interactive Graphic System")
        self.main_window.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.main_window.resizable(False, False)
        self.main_window.configure(bg="white")

    def create_interface(self) -> None:
        left_frame = Frame(self.main_window)
        left_frame.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)

        self.create_objects_list_frame(left_frame)
        self.create_buttons_frame(left_frame)
        self.create_camera_controls_frame(left_frame)
        self.create_zoom_controls_frame(left_frame)

        right_frame = Frame(self.main_window)
        right_frame.pack(side=RIGHT, padx=10, pady=10, fill=BOTH, expand=True)

        viewport_margin = 15
        viewport_frame = Frame(
            right_frame, padx=viewport_margin, pady=viewport_margin)
        viewport_frame.pack(fill=BOTH, expand=True)

        viewport_width = int(self.WIDTH * 0.75) - 2 * viewport_margin
        viewport_height = self.HEIGHT * 0.8 - 2 * viewport_margin
        viewport_canvas = Canvas(
            viewport_frame, width=viewport_width, height=viewport_height, borderwidth=2, relief="solid")
        viewport_canvas.pack(fill=BOTH, expand=True)

        self.console_text = Text(right_frame, height=self.HEIGHT * 0.2,
                            width=50, wrap=WORD)
        self.console_text.pack(side=BOTTOM, fill=BOTH)

        self.graphic_system = GraphicSystem(
            viewport_width, viewport_height, viewport_canvas)

    def create_objects_list_frame(self, parent_frame: Frame) -> None:
        objects_list_frame = Frame(parent_frame)
        objects_list_frame.pack(fill=X)

        items_frame = Frame(objects_list_frame)
        items_frame.pack(fill=BOTH, expand=True)

        self.items_listbox = Listbox(items_frame, selectmode=SINGLE)
        self.items_listbox.pack(fill=BOTH, expand=True)

    def create_buttons_frame(self, parent_frame: Frame) -> None:
        buttons_frame = Frame(parent_frame, borderwidth=2,
                              relief=SOLID, padx=10, pady=10)
        buttons_frame.pack(fill=X, expand=True, anchor=N)

        add_shape_button = Button(
            buttons_frame, text="Add Shape", command=self.add_shape_popup)
        add_shape_button.pack(pady=2)

        remove_button = Button(
            buttons_frame, text="Remove Shape", command=self.remove_shape)
        remove_button.pack(pady=2)

    def create_camera_controls_frame(self, parent_frame: Frame) -> None:
        camera_controls_frame = Frame(
            parent_frame, borderwidth=2, relief=SOLID, padx=10, pady=10)
        camera_controls_frame.pack(ipadx=10, ipady=10)

        up_button = Button(camera_controls_frame,
                           text="⬆️", command=self.move_up)
        down_button = Button(camera_controls_frame,
                             text="⬇️", command=self.move_down)
        left_button = Button(camera_controls_frame,
                             text="⬅️", command=self.move_left)
        right_button = Button(camera_controls_frame,
                              text="➡️", command=self.move_right)

        up_button.grid(row=0, column=1, padx=5, pady=5, sticky=N,)
        down_button.grid(row=2, column=1, padx=5, pady=5, sticky=S)
        left_button.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        right_button.grid(row=1, column=2,  padx=5, pady=5, sticky=E)

    def create_zoom_controls_frame(self, parent_frame: Frame) -> None:
        zoom_controls_frame = Frame(
            parent_frame, borderwidth=2, relief=SOLID, padx=10, pady=10)
        zoom_controls_frame.pack(fill=X)

        zoom_in_button = Button(zoom_controls_frame,
                                text="Zoom In", command=self.zoom_in)
        zoom_out_button = Button(
            zoom_controls_frame, text="Zoom Out", command=self.zoom_out)

        zoom_in_button.pack(side=LEFT, padx=10)
        zoom_out_button.pack(side=RIGHT, padx=10)

    def add_shape_popup(self) -> None:
        popup_window = Toplevel(self.main_window)
        popup_window.title("Add Shape")
        popup_window.resizable(False, False)

        # Frame for the list of points
        points_frame = Frame(popup_window)
        points_frame.pack(fill=BOTH, padx=10, pady=10)

        points_listbox = Listbox(points_frame, selectmode=SINGLE)
        points_listbox.pack(fill=BOTH, expand=True)

        # Frame for entering coordinates and adding points
        entry_frame = Frame(popup_window)
        entry_frame.pack(fill=X, padx=10, pady=(0, 10))

        x_entry = EntryWithPlaceholder(entry_frame , "x")
        y_entry = EntryWithPlaceholder(entry_frame, "y")

        x_entry.pack(side=LEFT, padx=(0, 10))
        y_entry.pack(side=LEFT, padx=(0, 10))

        points_list = []
        add_button = Button(entry_frame, text="Add Point",
                            command=lambda: self.add_point(x_entry, y_entry, points_listbox, points_list))
        add_button.pack(side=LEFT, expand=True, fill='both')

        # Button to remove selected point
        remove_button = Button(
            popup_window, text="Remove Selected Point", width=25,command=lambda: self.remove_point(points_listbox, points_list))
        remove_button.pack(pady=(0, 10))

        name_entry = EntryWithPlaceholder(popup_window, "Name")
        name_entry.pack(padx=10, pady=(0, 10), fill=X)

        popup_buttons_frame = Frame(popup_window)
        popup_buttons_frame.pack(padx=10, pady=(0, 10), fill=X)

        cancel_button = Button(
            popup_buttons_frame, text="Cancel", width=25, command=popup_window.destroy)
        cancel_button.pack(side=LEFT, padx=(0,5), expand=True, fill="both")

        create_button = Button(
            popup_buttons_frame, text="Create Shape", width=25, command=lambda: self.create_shape(points_list, name_entry, popup_window))
        create_button.pack(side=LEFT, padx=(5,0), expand=True, fill="both")

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

    def remove_shape(self) -> None:
        if len(self.items_listbox.curselection()) == 0:
            messagebox.showerror("Remove Shape Error", "Select a shape")
        else:
            pos = self.items_listbox.curselection()[0]
            self.items_listbox.delete(pos)
            name = self.graphic_system.remove_shape(pos)
            self.log(f'Shape "{name}" deleted.')

    def create_shape(self, points_list: list[tuple[float, float]], name_entry: Entry, popup_window: Toplevel) -> None:
        name = name_entry.get()
        if len(points_list) > 0:
            if name != "":
                self.graphic_system.create_shape(points_list, name)
                popup_window.destroy()
                self.items_listbox.insert("end", name)
                self.log(f'Shape "{name}" created with points: {self.format_point_list(points_list)}.')
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
        self.console_text.insert("end", text + "\n")
        self.console_text.see("end")
