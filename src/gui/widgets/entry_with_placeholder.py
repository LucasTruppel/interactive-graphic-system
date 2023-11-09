import tkinter as tk
from tkinter import messagebox

from gui.style import BG_COLOR, FG_COLOR


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, root, placeholder: str, **kwargs) -> None:
        super().__init__(root, **kwargs)

        self.root = root
        self.placeholder = placeholder
        self.default_fg_color = self["fg"]

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)
        self.put_placeholder()

    def put_placeholder(self) -> None:
        self.insert(0, self.placeholder)
        self["fg"] = "grey"

    def focus_in(self, *args) -> None:
        if self["fg"] == "grey":
            self.delete("0", "end")
            self["fg"] = self.default_fg_color

    def focus_out(self, *args) -> None:
        if self.get() == "":
            self.put_placeholder()

    def clear(self) -> None:
        self.delete(0, tk.END)
        self.root.focus_set()
        self.put_placeholder()

    def validate(self, is_number: bool, show_message: bool = True) -> bool:
        if self.get() == "" or self.get() == self.placeholder:
            if show_message:
                messagebox.showerror(parent=self.root,
                                     title="Error",
                                     message=f"Field {self.placeholder} must be specified")
            return False
        if is_number:
            try:
                float(self.get())
            except ValueError:
                if show_message:
                    messagebox.showerror(parent=self.root,
                                         title="Error",
                                         message=f"Invalid character for {self.placeholder}.")
                return False
        return True
