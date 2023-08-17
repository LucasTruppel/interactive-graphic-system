from tkinter import *
from graphic_system import GraphicSystem


class GraphicInterface:

    def __init__(self):
        self.WIDTH = 1200
        self.HEIGHT = 800

        self.main_window = Tk()
        self.viewport_canvas = Canvas(self.main_window)
        self.graphic_system = GraphicSystem(self.WIDTH, self.HEIGHT, self.viewport_canvas)
        self.init_tkinter()

    def init_tkinter(self):
        self.configure_main_window()
        self.test()
        self.main_window.mainloop()

    def configure_main_window(self):
        self.main_window.title("Interactive Graphic System")
        self.main_window.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.main_window.resizable(False, False)
        self.main_window.configure(bg="white")

    def test(self):
        self.graphic_system.test()
        self.graphic_system.draw_display_file()
