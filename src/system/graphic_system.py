from tkinter import Canvas

from system.window import Window
from system.viewport import Viewport
from graphic_objects.line import *
from graphic_objects.wireframe import Wireframe
from system.transformation_handler import TransformationHandler
from gui.logger import Logger
from obj_file.obj_transcriber import ObjTranscriber
from obj_file.obj_reader import ObjReader
from utils.utils import get_object_center
from clipping.point_clipping import PointClipping
from clipping.cohen_sutherland import CohenSutherland
from clipping.liang_barsky import LiangBarsky



class GraphicSystem:

    def __init__(self, width: float, height: float, viewport_canvas: Canvas, logger: Logger) -> None:
        self.display_file: list[GraphicObject] = []
        self.window = Window(0, 0, width - 20, height - 20, logger)
        self.viewport = Viewport(0, 0, width - 20, height - 20, viewport_canvas)
        self.viewport_canvas = viewport_canvas
        self.transformation_handler = TransformationHandler(logger)
        self.logger = logger

    def draw_display_file(self) -> None:
        self.window.update_normalization_matrix()
        self.viewport.clear()
        for obj in self.display_file:
            self.window.update_normalized_coordinates(obj)
            match len(obj.get_points()):
                case 1:
                    if PointClipping.point_clipping(obj):
                        self.viewport.draw_point(obj)
                case 2:
                    if LiangBarsky.line_clipping(obj):
                        self.viewport.draw_line(obj)
                case default:
                    self.viewport.draw_wireframe(obj)
        self.viewport.update()

    def move_up(self) -> None:
        self.window.move_up()
        self.draw_display_file()

    def move_down(self) -> None:
        self.window.move_down()
        self.draw_display_file()

    def move_left(self) -> None:
        self.window.move_left()
        self.draw_display_file()

    def move_right(self) -> None:
        self.window.move_right()
        self.draw_display_file()

    def zoom_in(self) -> None:
        self.window.zoom_in()
        self.draw_display_file()

    def zoom_out(self) -> None:
        self.window.zoom_out()
        self.draw_display_file()

    def create_shape(self, points_list: list[tuple[float, float]], name: str, color: str) -> None:
        match len(points_list):
            case 1:
                x, y = points_list[0]
                self.display_file.append(Point(name, color, x, y))
            case 2:
                x1, y1 = points_list[0]
                x2, y2 = points_list[1]
                self.display_file.append(Line(name, color, x1, y1, x2, y2))
            case default:
                self.display_file.append(Wireframe(name, color, points_list))
        self.draw_display_file()

    def remove_shape(self, pos: int) -> str:
        name = self.display_file[pos].name
        self.display_file.pop(pos)
        self.draw_display_file()
        return name

    def add_translation(self, dx: float, dy: float) -> None:
        self.transformation_handler.add_translation_matrix(dx, dy)

    def add_scaling(self, object_index: int, sx: float, sy: float) -> None:
        self.transformation_handler.add_scaling_matrix(self.display_file[object_index], sx, sy)

    def add_rotation(self, x: float, y: float, angle: float, rotation_type: str, object_index: int) -> None:
        if rotation_type == "object_center":
            x, y = get_object_center(self.display_file[object_index])
        self.transformation_handler.add_rotation_matrix(x, y, angle)

    def remove_operation(self, operation_index: int) -> None:
        self.transformation_handler.remove_operation(operation_index)

    def transform(self, object_index: int) -> None:
        self.transformation_handler.transform(self.display_file[object_index])
        self.draw_display_file()

    def clear_transformation(self) -> None:
        self.transformation_handler.clear_transformation()

    def rotate_window(self, angle: float) -> None:
        self.window.rotate(angle)
        self.draw_display_file()

    def import_obj(self, file_path: str) -> list[str]:
        obj_reader = ObjReader(file_path)
        new_objects_list = obj_reader.read(self.display_file, self.window)
        self.draw_display_file()
        return list(map(lambda graphic_object: graphic_object.name, new_objects_list))

    def export_obj(self, file_path: str) -> None:
        obj_transcriber = ObjTranscriber(file_path)
        obj_transcriber.transcribre(self.display_file, self.window)
