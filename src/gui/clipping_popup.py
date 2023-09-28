from tkinter import *
from tkinter import messagebox

from gui.entry_with_placeholder import EntryWithPlaceholder
from system.graphic_system import GraphicSystem
from gui.style import BG_COLOR, FG_COLOR
from gui.custom_button import CustomButton


class ClippingPopup:
    def __init__(self, root, graphic_system: GraphicSystem) -> None:
        self.graphic_system = graphic_system
        self.popup_window = Toplevel(root)
        self.popup_window.attributes("-topmost", True)
        self.init_popup(self.popup_window)

    def init_popup(self, popup_window) -> None:
        self.configure_popup(popup_window)
        self.create_popup(popup_window)

    def configure_popup(self, popup_window) -> None:
        popup_window.title("Clipping")
        popup_window.resizable(False, False)
        popup_window.configure(bg=BG_COLOR)

    def create_popup(self, popup_window) -> None:

        # Point Clipping Frame
        point_clipping_frame = Frame(popup_window)
        point_clipping_frame.pack(fill=X, padx=10, pady=10)

        point_clipping_label = Label(
            point_clipping_frame, text="Point Clipping", bg=BG_COLOR, fg=FG_COLOR)
        point_clipping_label.pack(padx=5, pady=5)

        point_enabled_radio_button = Radiobutton(
            point_clipping_frame, text="Enabled", value=1, bg=BG_COLOR, fg=FG_COLOR)
        point_enabled_radio_button.pack(padx=5, pady=5)

        point_disabled_radio_button = Radiobutton(
            point_clipping_frame, text="Disabled", value=0, bg=BG_COLOR, fg=FG_COLOR)
        point_disabled_radio_button.pack(padx=5, pady=5)

        # Line Clipping Frame
        line_clipping_frame = Frame(popup_window)
        line_clipping_frame.pack(fill=X, padx=10, pady=10)

        line_clipping_frame_label = Label(
            line_clipping_frame, text="Line Clipping", bg=BG_COLOR, fg=FG_COLOR)
        line_clipping_frame_label.pack(padx=5, pady=5)

        cohen_sutherland_radio_button = Radiobutton(
            line_clipping_frame, text="Cohen-Sutherland", value=1, bg=BG_COLOR, fg=FG_COLOR)
        cohen_sutherland_radio_button.pack(padx=5, pady=5)

        liang_barsky_radio_button = Radiobutton(
            line_clipping_frame, text="Liang-Barsky", value=0, bg=BG_COLOR, fg=FG_COLOR)
        liang_barsky_radio_button.pack(padx=5, pady=5)

        line_disabled_radio_button = Radiobutton(
            line_clipping_frame, text="Disabled", value=0, bg=BG_COLOR, fg=FG_COLOR)
        line_disabled_radio_button.pack(padx=5, pady=5)

        # Polygon Clipping Frame
        polygon_clipping_frame = Frame(popup_window)
        polygon_clipping_frame.pack(fill=X, padx=10, pady=10)

        polygon_clipping_label = Label(
            polygon_clipping_frame, text="Polygon Clipping", bg=BG_COLOR, fg=FG_COLOR)
        polygon_clipping_label.pack(padx=5, pady=5)

        sutherland_hodgman_radio_button = Radiobutton(
            polygon_clipping_frame, text="Sutherland-Hodgman", value=1, bg=BG_COLOR, fg=FG_COLOR)
        sutherland_hodgman_radio_button.pack(padx=5, pady=5)

        polygon_disabled_radio_button = Radiobutton(
            polygon_clipping_frame, text="Disabled", value=0, bg=BG_COLOR, fg=FG_COLOR)
        polygon_disabled_radio_button.pack(padx=5, pady=5)

        # Popup Buttons Frame
        popup_buttons_frame = Frame(popup_window)
        popup_buttons_frame.pack(fill=X, padx=5, pady=5, side=RIGHT)

        # Confirm button
        confirm_button = CustomButton(
            popup_buttons_frame, text="Confirm", button_type='default_button')
        confirm_button.pack(side=LEFT)

        # Cancel Button
        cancel_button = CustomButton(
            popup_buttons_frame, text="Cancel", command=popup_window.destroy, button_type='red_button')
        cancel_button.pack(side=LEFT)
