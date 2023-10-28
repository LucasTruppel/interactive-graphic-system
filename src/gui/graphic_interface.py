from pathlib import Path
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd

from gui.transform_3d_popup import Transform3dPopup
from gui.transform_popup import TransformPopup
from gui.add_2d_shape_popup import Add2DShapePopup
from gui.add_3d_point_popup import Add3DPointPopup
from gui.add_3d_object_popup import Add3DObjectPopup
from gui.clipping_popup import ClippingPopup
from system.core.graphic_system import GraphicSystem
from gui.style import BG_COLOR
from gui.logger import Logger
from gui.custom_button import CustomButton
from gui.entry_with_placeholder import EntryWithPlaceholder


class GraphicInterface:

    def __init__(self) -> None:
        self.WIDTH = 1600
        self.HEIGHT = 900

        self.main_window = Tk()
        self.items_dimensions_list = []
        self.items_listbox = None
        self.console_text = None
        self.viewport_canvas = None
        self.graphic_system = None
        self.logger = None

        self.init_tkinter()

    def init_tkinter(self) -> None:
        self.configure_main_window()
        self.create_menubar()
        self.create_interface()
        self.main_window.update()
        self.graphic_system = GraphicSystem(self.viewport_canvas.winfo_width(), self.viewport_canvas.winfo_height(),
                                            self.viewport_canvas, self.logger)
        self.main_window.mainloop()

    def configure_main_window(self) -> None:
        self.main_window.title("Interactive Graphic System")
        self.main_window.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.main_window.resizable(False, False)
        self.main_window.configure(bg=BG_COLOR)

    def create_menubar(self) -> None:
        menubar = Menu(self.main_window)
        self.main_window.config(menu=menubar)
        filemenu = Menu(menubar, tearoff=False)
        filemenu.add_command(label="Import obj",
                             command=lambda: self.import_obj())
        filemenu.add_command(label="Export obj",
                             command=lambda: self.export_obj())
        menubar.add_cascade(label="File", menu=filemenu)

    def create_interface(self) -> None:
        left_frame = Frame(self.main_window)
        right_frame = Frame(self.main_window)

        console_frame = Frame(right_frame)
        console_text = Text(right_frame, height=self.HEIGHT *
                            0.2, width=50, wrap=WORD, state="disabled")
        self.logger = Logger(console_text)

        left_frame.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)
        self.create_objects_list_frame(left_frame)
        self.create_shape_manipulation_buttons_frame(left_frame)
        self.create_buttons_frame(left_frame)
        self.create_camera_controls_frame(left_frame)
        self.create_zoom_controls_frame(left_frame)
        self.create_window_rotation_frame(left_frame)
        self.create_clipping_controls_frame(left_frame)

        right_frame.pack(side=RIGHT, padx=10, pady=10, fill=BOTH, expand=True)
        self.create_viewport_frame(right_frame)
        console_frame.pack(fill=BOTH, expand=True)
        console_text.pack(side=BOTTOM, fill=BOTH)

    def create_viewport_frame(self, right_frame: Frame) -> None:
        viewport_margin = 15
        viewport_frame = Frame(
            right_frame, padx=viewport_margin, pady=viewport_margin)
        viewport_frame.pack(fill=BOTH, expand=True)

        viewport_width = int(self.WIDTH * 0.75) - 2 * viewport_margin
        viewport_height = self.HEIGHT * 0.8 - 2 * viewport_margin
        viewport_canvas = Canvas(
            viewport_frame, width=viewport_width, height=viewport_height, bg="#FFFFFF")
        viewport_canvas.pack(fill=BOTH, expand=True)
        self.viewport_canvas = viewport_canvas

    def create_objects_list_frame(self, parent_frame: Frame) -> None:
        items_frame = Frame(parent_frame)
        items_frame.pack(fill=BOTH, expand=True)

        self.items_listbox = Listbox(items_frame, selectmode=SINGLE)
        self.items_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        self.items_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.items_listbox.yview)

    def create_shape_manipulation_buttons_frame(self, parent_frame: Frame) -> None:
        manipulation_buttons_frame = Frame(
            parent_frame, padx=10, pady=10, relief="solid")
        manipulation_buttons_frame.pack()
        #  transform shape button
        transform_button = CustomButton(
            manipulation_buttons_frame, text="Transform Shape",
            command=lambda: self.transform(), button_type='default_button')
        transform_button.pack(side=LEFT)
        #  remove shape button
        remove_button = CustomButton(
            manipulation_buttons_frame, text="Remove Shape", command=self.remove_shape, button_type='red_button')
        remove_button.pack(side=LEFT)

    def create_buttons_frame(self, parent_frame: Frame) -> None:
        buttons_frame = Frame(parent_frame, padx=10,
                              pady=10, relief="solid")
        buttons_frame.pack()

        # add 2d shape button
        add_2d_shape_button = CustomButton(
            buttons_frame,
            text="Add 2D Shape",
            command=lambda: Add2DShapePopup(self.main_window, self.graphic_system, self.items_listbox,
                                            self.items_dimensions_list, self.logger), button_type='default_button'
        )
        add_2d_shape_button.pack(side=LEFT)

        # add 3d point button
        add_3d_point_button = CustomButton(
            buttons_frame, text="Add 3D Point",
            command=lambda: Add3DPointPopup(self.main_window, self.graphic_system, self.items_listbox,
                                            self.items_dimensions_list, self.logger), button_type='default_button')
        add_3d_point_button.pack(side=LEFT)

        # add 3d object button
        add_3d_object_button = CustomButton(
            buttons_frame, text="Add 3D Object",
            command=lambda: Add3DObjectPopup(self.main_window, self.graphic_system, self.items_listbox,
                                             self.items_dimensions_list, self.logger), button_type='default_button')
        add_3d_object_button.pack(side=LEFT)

    def create_camera_controls_frame(self, parent_frame: Frame) -> None:
        camera_controls_frame = Frame(
            parent_frame, padx=10, pady=10)
        camera_controls_frame.pack(ipadx=10, ipady=10)

        up_button = CustomButton(camera_controls_frame,
                                 text="⬆", command=self.move_up, button_type='default_button')
        down_button = CustomButton(camera_controls_frame,
                                   text="⬇️", command=self.move_down, button_type='default_button')
        left_button = CustomButton(camera_controls_frame,
                                   text="⬅️", command=self.move_left, button_type='default_button')
        right_button = CustomButton(camera_controls_frame,
                                    text="➡️", command=self.move_right, button_type='default_button')

        up_button.pack(side=TOP)
        down_button.pack(side=BOTTOM)
        left_button.pack(side=LEFT)
        right_button.pack(side=RIGHT)

    def create_zoom_controls_frame(self, parent_frame: Frame) -> None:
        zoom_controls_frame = Frame(
            parent_frame, padx=10, pady=10)
        zoom_controls_frame.pack()

        zoom_in_button = CustomButton(zoom_controls_frame,
                                      text="Zoom In", command=self.zoom_in, button_type='default_button')
        zoom_out_button = CustomButton(
            zoom_controls_frame, text="Zoom Out", command=self.zoom_out, button_type='default_button')

        zoom_in_button.pack(side=LEFT)
        zoom_out_button.pack(side=LEFT)

    def create_window_rotation_frame(self, parent_frame: Frame) -> None:
        rotation_controls_frame = Frame(
            parent_frame, padx=10, pady=10)
        rotation_controls_frame.pack(ipadx=10, ipady=10)

        angle_entry = EntryWithPlaceholder(
            rotation_controls_frame, "Rotation angle (degrees)")
        rotate_left_button = CustomButton(rotation_controls_frame, text="↪",
                                          command=lambda: self.rotate_window(False, False, angle_entry), button_type='default_button')
        rotate_right_button = CustomButton(rotation_controls_frame, text="↩",
                                           command=lambda: self.rotate_window(True, False, angle_entry), button_type='default_button')
        rotate_up_button = CustomButton(rotation_controls_frame, text="⤴",
                                        command=lambda: self.rotate_window(False, True, angle_entry), button_type='default_button')
        rotate_down_button = CustomButton(rotation_controls_frame, text="⤵",
                                          command=lambda: self.rotate_window(True, True, angle_entry), button_type='default_button')

        angle_entry.pack(pady=10)
        rotate_left_button.pack(side=LEFT)
        rotate_right_button.pack(side=RIGHT)
        rotate_up_button.pack(side=TOP)
        rotate_down_button.pack(side=BOTTOM)

    def create_clipping_controls_frame(self, parent_frame: Frame) -> None:
        clipping_controls_frame = Frame(
            parent_frame, padx=10, pady=10)
        clipping_controls_frame.pack()

        clipping_options_button = CustomButton(
            clipping_controls_frame, text="Clipping Options", button_type='default_button',
            command=lambda: ClippingPopup(self.main_window, self.graphic_system))
        clipping_options_button.pack(side=LEFT)

    def remove_shape(self) -> None:
        if len(self.items_listbox.curselection()) == 0:
            messagebox.showerror(parent=self.main_window,
                                 title="Remove Shape Error",
                                 message="Select a shape")
        else:
            pos = self.items_listbox.curselection()[0]
            self.items_listbox.delete(pos)
            self.items_dimensions_list.pop(pos)
            name = self.graphic_system.remove_shape(pos)
            self.logger.log(f'Shape "{name}" deleted.')

    def move_up(self) -> None:
        self.graphic_system.move_up()

    def move_down(self) -> None:
        self.graphic_system.move_down()

    def move_left(self) -> None:
        self.graphic_system.move_left()

    def move_right(self) -> None:
        self.graphic_system.move_right()

    def zoom_in(self) -> None:
        self.graphic_system.zoom_in()

    def zoom_out(self) -> None:
        self.graphic_system.zoom_out()

    def transform(self) -> None:
        if len(self.items_listbox.curselection()) == 0:
            messagebox.showerror(parent=self.main_window,
                                 title="Transform Shape",
                                 message="Select a shape")
        else:
            pos = self.items_listbox.curselection()[0]
            if self.items_dimensions_list[pos]:
                Transform3dPopup(self.main_window, self.graphic_system, pos)
            else:
                TransformPopup(self.main_window, self.graphic_system, pos)

    def rotate_window(self, is_clockwize: bool, is_horizontal: bool, angle_entry: EntryWithPlaceholder) -> None:
        if angle_entry.validate(True, False):
            angle = float(angle_entry.get())
        else:
            angle = 10
        self.graphic_system.rotate_window(-angle if is_clockwize else angle, is_horizontal)

    def import_obj(self) -> None:
        file_path = fd.askopenfilename(parent=self.main_window,
                                       defaultextension=".obj",
                                       initialdir=f"{Path.cwd()}/docs/obj_samples",
                                       title="Open file",
                                       filetypes=(("Object Files", "*.obj"), ("All files", '*.*')))
        if file_path != "" and file_path != ():
            objects_names = self.graphic_system.import_obj(file_path)
            for name in objects_names:
                self.items_listbox.insert("end", name)
            messagebox.showinfo(parent=self.main_window,
                                title="Open file",
                                message=f"Objects imported from {file_path}")

    def export_obj(self) -> None:
        file_path = fd.asksaveasfilename(parent=self.main_window,
                                         confirmoverwrite=False,
                                         defaultextension=".obj",
                                         initialdir=f"{Path.cwd()}/docs/obj_samples",
                                         title="Save file",
                                         filetypes=(("Object Files", "*.obj"), ("All files", '*.*')))
        if file_path != "" and file_path != ():
            self.graphic_system.export_obj(file_path)
            messagebox.showinfo(parent=self.main_window,
                                title="Save file",
                                message=f"World exported to {file_path}")
