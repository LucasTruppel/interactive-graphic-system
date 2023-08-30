from tkinter import Text


class Logger:

    def __init__(self, console_text: Text):
        self.console_text = console_text

    def log(self, text: str) -> None:
        self.console_text.configure(state="normal")
        self.console_text.insert("end", text + "\n")
        self.console_text.see("end")
        self.console_text.configure(state="disabled")
