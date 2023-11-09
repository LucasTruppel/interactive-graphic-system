from gui.style import BG_COLOR
import tkinter as tk

class CustomFrame(tk.Frame):
  def __init__(self, master):
    super().__init__(master, bg=BG_COLOR)
