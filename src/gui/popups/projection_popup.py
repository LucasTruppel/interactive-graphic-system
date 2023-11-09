from tkinter import *

from system.core.system_state import ProjectionState
from system.core.graphic_system import GraphicSystem
from gui.style import BG_COLOR, FG_COLOR
from gui.widgets.custom_button import CustomButton


class ProjectionPopup:
    def __init__(self, root, graphic_system: GraphicSystem) -> None:
        self.graphic_system = graphic_system
        self.projection_var = IntVar()
        self.popup_window = Toplevel(root)
        self.popup_window.attributes("-topmost", True)

        self.init_popup()

    def init_popup(self) -> None:
        self.configure_popup()
        self.create_popup()

    def configure_popup(self) -> None:
        self.popup_window.title("Projection")
        self.popup_window.resizable(False, False)
        self.popup_window.configure(bg=BG_COLOR)

    def create_popup(self) -> None:

        self.configure_var()

        # Projection Frame
        projection_frame = Frame(self.popup_window)
        projection_frame.pack(fill=X, padx=10, pady=10)

        projection_label = Label(
            projection_frame, text="Projection Type", bg=BG_COLOR, fg=FG_COLOR)
        projection_label.pack(padx=5, pady=5)

        parallel_radio_button = Radiobutton(
            projection_frame, text="Parallel Projection", bg=BG_COLOR, fg=FG_COLOR, variable=self.projection_var,
            value=ProjectionState.PARALLEL.value)
        parallel_radio_button.pack(padx=5, pady=5)

        perspective_radio_button = Radiobutton(
            projection_frame, text="Perspective Projection", bg=BG_COLOR, fg=FG_COLOR, variable=self.projection_var,
            value=ProjectionState.PERSPECTIVE.value)
        perspective_radio_button.pack(padx=5, pady=5)

        # Popup Buttons Frame
        popup_buttons_frame = Frame(self.popup_window)
        popup_buttons_frame.pack(fill=X, padx=5, pady=5, side=RIGHT)

        # Confirm button
        confirm_button = CustomButton(
            popup_buttons_frame, text="Confirm", button_type='default_button', command=self.configure_projection)
        confirm_button.pack(side=LEFT)

        # Cancel Button
        cancel_button = CustomButton(
            popup_buttons_frame, text="Cancel", command=self.popup_window.destroy, button_type='red_button')
        cancel_button.pack(side=LEFT)

    def configure_var(self) -> None:
        self.projection_var.set(self.graphic_system.projection_state.value)

    def configure_projection(self) -> None:
        self.graphic_system.configure_projection(self.projection_var.get())
        self.popup_window.destroy()
