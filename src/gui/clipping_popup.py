from tkinter import *

from system.core.system_state import PointClippingState, LineClippingState, PolygonClippingState
from system.core.graphic_system import GraphicSystem
from gui.style import BG_COLOR, FG_COLOR
from gui.custom_button import CustomButton


class ClippingPopup:
    def __init__(self, root, graphic_system: GraphicSystem) -> None:
        self.graphic_system = graphic_system
        self.point_clipping_var = IntVar()
        self.line_clipping_var = IntVar()
        self.polygon_clipping_var = IntVar()
        self.popup_window = Toplevel(root)
        self.popup_window.attributes("-topmost", True)

        self.init_popup()

    def init_popup(self) -> None:
        self.configure_popup()
        self.create_popup()

    def configure_popup(self) -> None:
        self.popup_window.title("Clipping")
        self.popup_window.resizable(False, False)
        self.popup_window.configure(bg=BG_COLOR)

    def create_popup(self) -> None:

        self.configure_vars()

        # Point Clipping Frame
        point_clipping_frame = Frame(self.popup_window)
        point_clipping_frame.pack(fill=X, padx=10, pady=10)

        point_clipping_label = Label(
            point_clipping_frame, text="Point Clipping", bg=BG_COLOR, fg=FG_COLOR)
        point_clipping_label.pack(padx=5, pady=5)

        point_enabled_radio_button = Radiobutton(
            point_clipping_frame, text="Enabled", bg=BG_COLOR, fg=FG_COLOR, variable=self.point_clipping_var,
            value=PointClippingState.ENABLED.value)
        point_enabled_radio_button.pack(padx=5, pady=5)

        point_disabled_radio_button = Radiobutton(
            point_clipping_frame, text="Disabled", bg=BG_COLOR, fg=FG_COLOR, variable=self.point_clipping_var,
            value=PointClippingState.DISABLED.value)
        point_disabled_radio_button.pack(padx=5, pady=5)

        # Line Clipping Frame
        line_clipping_frame = Frame(self.popup_window)
        line_clipping_frame.pack(fill=X, padx=10, pady=10)

        line_clipping_frame_label = Label(
            line_clipping_frame, text="Line Clipping", bg=BG_COLOR, fg=FG_COLOR)
        line_clipping_frame_label.pack(padx=5, pady=5)

        cohen_sutherland_radio_button = Radiobutton(
            line_clipping_frame, text="Cohen-Sutherland", bg=BG_COLOR, fg=FG_COLOR, variable=self.line_clipping_var,
            value=LineClippingState.COHEN_SUTHERLAND.value)
        cohen_sutherland_radio_button.pack(padx=5, pady=5)

        liang_barsky_radio_button = Radiobutton(
            line_clipping_frame, text="Liang-Barsky", bg=BG_COLOR, fg=FG_COLOR, variable=self.line_clipping_var,
            value=LineClippingState.LIANG_BARSKY.value)
        liang_barsky_radio_button.pack(padx=5, pady=5)

        line_disabled_radio_button = Radiobutton(
            line_clipping_frame, text="Disabled", bg=BG_COLOR, fg=FG_COLOR, variable=self.line_clipping_var,
            value=LineClippingState.DISABLED.value)
        line_disabled_radio_button.pack(padx=5, pady=5)

        # Polygon Clipping Frame
        polygon_clipping_frame = Frame(self.popup_window)
        polygon_clipping_frame.pack(fill=X, padx=10, pady=10)

        polygon_clipping_label = Label(
            polygon_clipping_frame, text="Polygon Clipping", bg=BG_COLOR, fg=FG_COLOR)
        polygon_clipping_label.pack(padx=5, pady=5)

        sutherland_hodgman_radio_button = Radiobutton(
            polygon_clipping_frame, text="Sutherland-Hodgman", bg=BG_COLOR, fg=FG_COLOR,
            variable=self.polygon_clipping_var, value=PolygonClippingState.SUTHERLAND_HODGMAN.value)
        sutherland_hodgman_radio_button.pack(padx=5, pady=5)

        polygon_disabled_radio_button = Radiobutton(
            polygon_clipping_frame, text="Disabled", bg=BG_COLOR, fg=FG_COLOR,
            variable=self.polygon_clipping_var, value=PolygonClippingState.DISABLED.value)
        polygon_disabled_radio_button.pack(padx=5, pady=5)

        # Popup Buttons Frame
        popup_buttons_frame = Frame(self.popup_window)
        popup_buttons_frame.pack(fill=X, padx=5, pady=5, side=RIGHT)

        # Confirm button
        confirm_button = CustomButton(
            popup_buttons_frame, text="Confirm", button_type='default_button', command=self.configure_clipping)
        confirm_button.pack(side=LEFT)

        # Cancel Button
        cancel_button = CustomButton(
            popup_buttons_frame, text="Cancel", command=self.popup_window.destroy, button_type='red_button')
        cancel_button.pack(side=LEFT)

    def configure_vars(self) -> None:
        self.point_clipping_var.set(self.graphic_system.point_clipping_state.value)
        self.line_clipping_var.set(self.graphic_system.line_clipping_state.value)
        self.polygon_clipping_var.set(self.graphic_system.polygon_clipping_state.value)

    def configure_clipping(self) -> None:
        self.graphic_system.configure_clipping(self.point_clipping_var.get(), self.line_clipping_var.get(),
                                               self.polygon_clipping_var.get())
        self.popup_window.destroy()
