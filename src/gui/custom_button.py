import tkinter as tk
from gui.style import BG_COLOR, FG_COLOR, REMOVE_COLOR


class CustomButton(tk.Button):
    def __init__(self, parent, text, command=None, button_type=None):
        if button_type == 'default_button':
            super().__init__(parent, text=text, command=command,
                             background=BG_COLOR, foreground=FG_COLOR, relief='raised')
        if button_type == 'red_button':
            super().__init__(parent, text=text, command=command,
                             background=REMOVE_COLOR, foreground='white', relief='raised')
        else:
            super().__init__(parent, text=text, command=command,
                             background=BG_COLOR, foreground=FG_COLOR, relief='raised')
        self.ipadx = 10  # Set a constant value for ipadx
        self.ipady = 10  # Set a constant value for ipady
        self.padx = 5  # Set a constant value for padding x
        self.pady = 5  # Set a constant value for padding y

    def pack(self, **kwargs):
        kwargs['ipadx'] = self.ipadx
        kwargs['ipady'] = self.ipady
        kwargs['padx'] = self.padx
        kwargs['pady'] = self.pady
        super().pack(**kwargs)
