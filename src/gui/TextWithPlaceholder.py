import tkinter as tk
from tkinter import messagebox

from gui.style import BG_COLOR, FG_COLOR


class TextWithPlaceholder(tk.Text):
    def __init__(self, root, placeholder: str, **kwargs) -> None:
        super().__init__(root, **kwargs)

        self.root = root
        self.placeholder = placeholder
        self.default_fg_color = self["fg"]

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)
        self.put_placeholder()

    def put_placeholder(self) -> None:
        self.insert("1.0", self.placeholder)
        self["fg"] = "grey"

    def focus_in(self, *args) -> None:
        if self["fg"] == "grey":
            self.delete("1.0", "end")
            self["fg"] = self.default_fg_color

    def focus_out(self, *args) -> None:
        if self.get_value() == "":
            self.put_placeholder()

    def clear(self) -> None:
        self.delete("1.0", tk.END)
        self.root.focus_set()
        self.put_placeholder()

    def validate(self, show_message: bool = True) -> bool:
        if self.get_value() == "" or self.get_value() == self.placeholder:
            if show_message:
                messagebox.showerror(parent=self.root,
                                     title="Error",
                                     message=f"Field {self.placeholder} must be specified")
            return False
        return True

    def get_value(self) -> str:
        return self.get("1.0", "end-1c")
