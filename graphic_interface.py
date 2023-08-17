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

        # Coluna da esquerda
        left_frame = Frame(self.main_window)
        left_frame.pack(side=LEFT, padx=10, pady=10)

        # Coluna da direita
        right_frame = Frame(self.main_window)
        right_frame.pack(side=RIGHT, padx=10, pady=10,
                         fill='both', expand=True)

        self.create_left_frame(left_frame)
        self.create_right_frame(right_frame)

    def create_left_frame(self, parent_frame):
        log_button = Button(parent_frame, text="Log Something",
                            command=self.log_something)
        log_button.pack()

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

    def log_something(self):
        message = "Button pressed in the left column.\n"
        self.console_text.insert(END, message)

    def test(self):
        self.graphic_system.test()
        self.graphic_system.draw_display_file()
