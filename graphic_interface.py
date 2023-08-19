from tkinter import *
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
        left_frame.pack(side=LEFT, padx=10, pady=10)

        self.create_objects_list_frame(left_frame)
        self.create_buttons_frame(left_frame)
        self.create_camera_controls_frame(left_frame)
        self.create_zoom_controls_frame(left_frame)

        right_frame = Frame(self.main_window)
        right_frame.pack(side=RIGHT, padx=10, pady=10, fill=BOTH, expand=True)

        viewport_width = int(self.WIDTH * 0.75)
        viewport_height = self.HEIGHT // 2
        viewport_canvas = Canvas(
            right_frame, width=viewport_width, height=viewport_height)
        viewport_canvas.pack()

        console_text = Text(right_frame, height=5,
                            width=50, wrap=WORD)
        console_text.pack(side=BOTTOM, fill=BOTH)

        self.console_text = console_text
        self.graphic_system = GraphicSystem(
            viewport_width, viewport_height, viewport_canvas)

    def create_objects_list_frame(self, parent_frame):
        objects_list_frame = Frame(parent_frame)
        objects_list_frame.pack(fill=X)

        # Add your list of objects to the objects_list_frame

    def create_buttons_frame(self, parent_frame):
        buttons_frame = Frame(parent_frame, borderwidth=2,
                              relief="solid", highlightbackground="red")
        buttons_frame.pack(fill=X)

        add_shape_button = Button(
            buttons_frame, text="Add Shape", command=self.add_shape)
        add_shape_button.pack()

        remove_button = Button(
            buttons_frame, text="Remove Shape", command=self.remove_shape)
        remove_button.pack()

    def create_camera_controls_frame(self, parent_frame):
        camera_controls_frame = Frame(parent_frame)
        camera_controls_frame.pack(fill=X)

        up_button = Button(camera_controls_frame,
                           text="⬆️", command=self.move_up)
        down_button = Button(camera_controls_frame,
                             text="⬇️", command=self.move_down)
        left_button = Button(camera_controls_frame,
                             text="⬅️", command=self.move_left)
        right_button = Button(camera_controls_frame,
                              text="➡️", command=self.move_right)

        up_button.grid(row=0, column=1)
        down_button.grid(row=2, column=1)
        left_button.grid(row=1, column=0)
        right_button.grid(row=1, column=2)

    def create_zoom_controls_frame(self, parent_frame):
        zoom_controls_frame = Frame(parent_frame)
        zoom_controls_frame.pack(fill=X)

        zoom_in_button = Button(zoom_controls_frame,
                                text="Zoom In", command=self.zoom_in)
        zoom_out_button = Button(
            zoom_controls_frame, text="Zoom Out", command=self.zoom_out)

        zoom_in_button.pack(side=LEFT, padx=10)
        zoom_out_button.pack(side=RIGHT, padx=10)

    def open_popup(self):
        popup_window = Toplevel(self.main_window)
        popup_window.title("Popup Window")

        # You can add elements to the popup window here in the future

    def remove_shape(self):
        # Implement shape removal logic here
        pass

    def move_up(self):
        # Implement move up logic here
        pass

    def move_down(self):
        # Implement move down logic here
        pass

    def move_left(self):
        # Implement move left logic here
        pass

    def move_right(self):
        # Implement move right logic here
        pass

    def zoom_in(self):
        # Implement zoom in logic here
        pass

    def zoom_out(self):
        # Implement zoom out logic here
        pass

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
