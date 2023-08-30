from tkinter import *
from tkinter import messagebox
from gui.transform_popup import TransformPopup
from gui.add_shape_popup import AddShapePopup
from system.graphic_system import GraphicSystem
from gui.style import BG_COLOR, FG_COLOR
from gui.logger import Logger


class GraphicInterface:

    def __init__(self) -> None:
        self.WIDTH = 1600
        self.HEIGHT = 900

        self.main_window = Tk()
        self.items_listbox = None
        self.console_text = None
        self.graphic_system = None
        self.logger = None

        self.init_tkinter()

    def init_tkinter(self) -> None:
        self.configure_main_window()
        self.create_interface()
        self.main_window.mainloop()

    def configure_main_window(self) -> None:
        self.main_window.title("Interactive Graphic System")
        self.main_window.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.main_window.resizable(False, False)
        self.main_window.configure(bg=BG_COLOR)

    def create_interface(self) -> None:
        left_frame = Frame(self.main_window)
        right_frame = Frame(self.main_window)

        console_frame = Frame(right_frame)
        console_text = Text(right_frame, height=self.HEIGHT * 0.2, width=50, wrap=WORD, state="disabled")
        self.logger = Logger(console_text)

        left_frame.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)
        self.create_objects_list_frame(left_frame)
        self.create_buttons_frame(left_frame)
        self.create_camera_controls_frame(left_frame)
        self.create_zoom_controls_frame(left_frame)

        right_frame.pack(side=RIGHT, padx=10, pady=10, fill=BOTH, expand=True)
        self.create_viewport_frame(right_frame)
        console_frame.pack(fill=BOTH, expand=True)
        console_text.pack(side=BOTTOM, fill=BOTH)

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
            viewport_width, viewport_height, viewport_canvas, self.logger)

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
                              pady=10, relief="solid")
        buttons_frame.pack()

        add_shape_button = Button(
            buttons_frame, text="Add Shape", command=lambda: AddShapePopup(self.main_window, self.graphic_system,
                                                                           self.items_listbox, self.logger))
        add_shape_button.pack(padx=5, pady=5, side=LEFT, ipadx=5, ipady=5)

        transform_button = Button(
            buttons_frame, text="Transform Shape",
            command=lambda: self.transform())
        transform_button.pack(padx=5, pady=5, side=LEFT, ipadx=5, ipady=5)

        remove_button = Button(
            buttons_frame, text="Remove Shape", command=self.remove_shape, background="#C95052", fg=FG_COLOR)
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

    def remove_shape(self) -> None:
        if len(self.items_listbox.curselection()) == 0:
            messagebox.showerror("Remove Shape Error", "Select a shape")
        else:
            pos = self.items_listbox.curselection()[0]
            self.items_listbox.delete(pos)
            name = self.graphic_system.remove_shape(pos)
            self.logger.log(f'Shape "{name}" deleted.')

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

    def transform(self):
        if len(self.items_listbox.curselection()) == 0:
            messagebox.showerror("Transform Shape", "Select a shape")
        else:
            pos = self.items_listbox.curselection()[0]
            TransformPopup(self.main_window, self.graphic_system, pos)
