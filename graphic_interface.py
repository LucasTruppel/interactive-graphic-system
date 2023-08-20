from tkinter import *
from tkinter import messagebox
from graphic_system import GraphicSystem


class GraphicInterface:

    def __init__(self):
        self.WIDTH = 1600
        self.HEIGHT = 900

        self.main_window = Tk()
        # self.viewport_canvas = Canvas(self.main_window)
        # self.graphic_system = GraphicSystem(self.WIDTH, self.HEIGHT, self.viewport_canvas)
        self.init_tkinter()

    def init_tkinter(self):
        self.configure_main_window()
        self.create_interface()
        self.test()
        self.main_window.mainloop()

    def configure_main_window(self):
        self.main_window.title("Interactive Graphic System")
        self.main_window.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.main_window.resizable(False, False)
        self.main_window.configure(bg="white")

    def create_interface(self):
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

        console_text = Text(right_frame, height=self.HEIGHT * 0.2,
                            width=50, wrap=WORD)
        console_text.pack(side=BOTTOM, fill=BOTH)

        self.console_text = console_text
        self.graphic_system = GraphicSystem(
            viewport_width, viewport_height, viewport_canvas)

    def create_objects_list_frame(self, parent_frame):
        objects_list_frame = Frame(parent_frame)
        objects_list_frame.pack(fill=X)

        items_frame = Frame(objects_list_frame)
        items_frame.pack(fill=BOTH, expand=True)

        items_listbox = Listbox(items_frame, selectmode=SINGLE)
        items_listbox.pack(fill=BOTH, expand=True)

        # TODO substituir pelo codigo correto para pegar as formas ja desenhadas
        items = ["Shape 1", "Shape 2", "Shape 3"]
        for item in items:
            items_listbox.insert(END, item)

    def create_buttons_frame(self, parent_frame):
        buttons_frame = Frame(parent_frame, borderwidth=2,
                              relief=SOLID, padx=10, pady=10)
        buttons_frame.pack(fill=X, expand=True, anchor=N)

        add_shape_button = Button(
            buttons_frame, text="Add Shape", command=self.add_shape_popup)
        add_shape_button.pack(pady=2)

        remove_button = Button(
            buttons_frame, text="Remove Shape", command=self.remove_shape)
        remove_button.pack(pady=2)

    def create_camera_controls_frame(self, parent_frame):
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

    def create_zoom_controls_frame(self, parent_frame):
        zoom_controls_frame = Frame(
            parent_frame, borderwidth=2, relief=SOLID, padx=10, pady=10)
        zoom_controls_frame.pack(fill=X)

        zoom_in_button = Button(zoom_controls_frame,
                                text="Zoom In", command=self.zoom_in)
        zoom_out_button = Button(
            zoom_controls_frame, text="Zoom Out", command=self.zoom_out)

        zoom_in_button.pack(side=LEFT, padx=10)
        zoom_out_button.pack(side=RIGHT, padx=10)

    def add_shape_popup(self):
        popup_window = Toplevel(self.main_window)
        popup_window.title("Add Shape")

        # Frame for the list of points
        points_frame = Frame(popup_window)
        points_frame.pack(fill=BOTH, padx=10, pady=10)

        points_listbox = Listbox(points_frame, selectmode=SINGLE)
        points_listbox.pack(fill=BOTH, expand=True)

        # Frame for entering coordinates and adding points
        entry_frame = Frame(popup_window)
        entry_frame.pack(fill=X, padx=10, pady=(0, 10))

        x_entry = Entry(entry_frame)
        y_entry = Entry(entry_frame)

        x_entry.pack(side=LEFT, padx=(0, 10))
        y_entry.pack(side=LEFT, padx=(0, 10))

        points_list = []
        add_button = Button(entry_frame, text="Add Point",
                            command=lambda: self.add_point(x_entry, y_entry, points_listbox, points_list))
        add_button.pack(side=LEFT)

        # Button to remove selected point
        remove_button = Button(
            popup_window, text="Remove Selected Point", command=lambda: self.remove_point(points_listbox, points_list))
        remove_button.pack()

        create_button = Button(
            popup_window, text="Create Shape", command=lambda: self.create_shape(points_list, popup_window))
        create_button.pack()

    def add_point(self, x_entry, y_entry, points_listbox, points_list):
        try:
            x = float(x_entry.get())
            y = float(y_entry.get())
            if (x, y) not in points_list:
                points_list.append((x, y))
                points_listbox.insert("end", f"({x:g}, {y:g})")
            else:
                messagebox.showerror(
                    "Add Point Error", "Point already registered")
            x_entry.delete(0, END)
            y_entry.delete(0, END)
        except ValueError:
            if x_entry.get() == "" or y_entry.get() == "":
                messagebox.showerror(
                    "Add Point Error", "Point must be specified")
            else:
                messagebox.showerror("Add Point Error", "Invalid character")

    def remove_point(self, points_listbox, points_list):
        if len(points_listbox.curselection()) == 0:
            messagebox.showerror("Remove Point Error", "Select a point")
        else:
            pos = points_listbox.curselection()[0]
            points_listbox.delete(pos)
            points_list.pop(pos)

    def remove_shape(self):
        # Implement shape removal logic here
        pass

    def create_shape(self, points_list: list[tuple[float, float]], popup_window: Toplevel):
        if len(points_list) > 0:
            self.graphic_system.create_shape(points_list)
            popup_window.destroy()
        else:
            messagebox.showerror("Create Shape Error",
                                 "At least one point is needed")

    def move_up(self):
        self.graphic_system.move_up()

    def move_down(self):
        self.graphic_system.move_down()

    def move_left(self):
        self.graphic_system.move_left()

    def move_right(self):
        self.graphic_system.move_right()

    def zoom_in(self):
        self.graphic_system.zoom_in()

    def zoom_out(self):
        self.graphic_system.zoom_out()

    def create_left_frame(self, parent_frame):
        add_shape_button = Button(parent_frame, text="Add Shape",
                                  command=self.add_shape)
        add_shape_button.pack()

    def create_right_frame(self, parent_frame):
        viewport_width = int(self.WIDTH * 0.75)
        viewport_height = self.HEIGHT // 1.2

        viewport_canvas = Canvas(
            parent_frame, width=viewport_width, height=viewport_height)
        viewport_canvas.pack(fill='both', expand=True)

        console_text = Text(parent_frame, height=5, width=50)
        console_text.pack(fill='both', side="bottom")

        self.console_text = console_text
        self.graphic_system = GraphicSystem(
            viewport_width, viewport_height, viewport_canvas)

    def add_shape(self):
        # open popup window
        popup_window = Toplevel(self.main_window)
        popup_window.title("Popup Window")
        message = "Add shape button pressed\n"
        self.console_text.insert(END, message)

    def test(self):
        self.graphic_system.test()
        self.graphic_system.draw_display_file()
