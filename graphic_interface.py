from tkinter import *


class GraphicInterface:

    def __init__(self):
        self.WIDTH = 1200
        self.HEIGHT = 800

        self.main_window = Tk()
        self.init_tkinter()

    def init_tkinter(self):
        self.configure_main_window()
        self.main_window.mainloop()

    def configure_main_window(self):
        self.main_window.title("Interactive Graphic System")
        self.main_window.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.main_window.resizable(False, False)
        self.main_window.configure(bg="white")
