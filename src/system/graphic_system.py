from system.window import Window
from system.viewport import Viewport
from graphic_objects.line import *
from tkinter import Canvas
from graphic_objects.wireframe import Wireframe
from system.transformation_handler import TransformationHandler


class GraphicSystem:

    def __init__(self, width: float, height: float, viewport_canvas: Canvas) -> None:
        self.display_file = []
        self.window = Window(0, 0, width, height)
        self.viewport = Viewport(0, 0, width, height)
        self.viewport_canvas = viewport_canvas
        self.transformation_handler = TransformationHandler()

    def viewport_transformation(self, point: Point) -> tuple[float, float]:
        xw, yw = point.x, point.y
        xvp = ((xw - self.window.x_min) / (self.window.x_max - self.window.x_min) *
               (self.viewport.x_max - self.viewport.x_min))
        yvp = ((1 - ((yw - self.window.y_min) / (self.window.y_max - self.window.y_min))) *
               (self.viewport.y_max - self.viewport.y_min))
        return xvp, yvp

    def draw_display_file(self) -> None:
        self.viewport_canvas.delete("all")
        for obj in self.display_file:
            points_list = obj.get_points()
            match len(points_list):
                case 1:
                    x, y = self.viewport_transformation(points_list[0])
                    self.viewport_canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=obj.color)
                case 2:
                    x1, y1 = self.viewport_transformation(points_list[0])
                    x2, y2 = self.viewport_transformation(points_list[1])
                    self.viewport_canvas.create_line(x1, y1, x2, y2, fill=obj.color)
                case default:
                    for i in range(len(points_list)-1):
                        x1, y1 = self.viewport_transformation(points_list[i])
                        x2, y2 = self.viewport_transformation(points_list[i+1])
                        self.viewport_canvas.create_line(x1, y1, x2, y2, fill=obj.color)
                    x1, y1 = self.viewport_transformation(points_list[len(points_list)-1])
                    x2, y2 = self.viewport_transformation(points_list[0])
                    self.viewport_canvas.create_line(x1, y1, x2, y2, fill=obj.color)
        self.viewport_canvas.update()

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
            x, y = self.transformation_handler.get_object_center(self.display_file[object_index])
        self.transformation_handler.add_rotation_matrix(x, y, angle)

    def remove_operation(self, operation_index: int):
        self.transformation_handler.remove_operation(operation_index)

    def transform(self, object_index: int):
        self.transformation_handler.transform(self.display_file[object_index])
        self.draw_display_file()

    def clear_transformation(self):
        self.transformation_handler.clear_transformation()