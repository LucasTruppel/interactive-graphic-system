from window import Window
from viewport import Viewport
from line import *
from tkinter import Canvas, BOTH
from wireframe import Wireframe
import numpy as np


class GraphicSystem:

    def __init__(self, width: float, height: float, viewport_canvas: Canvas) -> None:
        self.display_file = []
        self.window = Window(0, 0, width, height)
        self.viewport = Viewport(0, 0, width, height)
        self.viewport_canvas = viewport_canvas

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
                    self.viewport_canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
                case 2:
                    x1, y1 = self.viewport_transformation(points_list[0])
                    x2, y2 = self.viewport_transformation(points_list[1])
                    self.viewport_canvas.create_line(x1, y1, x2, y2)
                case default:
                    for i in range(len(points_list)-1):
                        x1, y1 = self.viewport_transformation(points_list[i])
                        x2, y2 = self.viewport_transformation(points_list[i+1])
                        self.viewport_canvas.create_line(x1, y1, x2, y2)
                    x1, y1 = self.viewport_transformation(points_list[len(points_list)-1])
                    x2, y2 = self.viewport_transformation(points_list[0])
                    self.viewport_canvas.create_line(x1, y1, x2, y2)
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

    def create_shape(self, points_list: list[tuple[float, float]], name: str) -> None:
        match len(points_list):
            case 1:
                x, y = points_list[0]
                self.display_file.append(Point(name, x, y))
            case 2:
                x1, y1 = points_list[0]
                x2, y2 = points_list[1]
                self.display_file.append(Line(name, x1, y1, x2, y2))
            case default:
                self.display_file.append(Wireframe(name, points_list))
        self.draw_display_file()

    def remove_shape(self, pos: int) -> str:
        name = self.display_file[pos].name
        self.display_file.pop(pos)
        self.draw_display_file()
        return name

    def transform(self, graphic_object: GraphicObject, matrix: np.array):
        points_list = graphic_object.get_points()
        for point in points_list:
            point_matrix = np.array([point.x, point.y, 1])
            new_point_matrix = np.dot(point_matrix, matrix)
            point.x = new_point_matrix[0]
            point.y = new_point_matrix[1]
        self.draw_display_file()

    def get_translation_matrix(self, dx: float, dy: float):
        return np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

    def get_object_center(self, graphic_object: GraphicObject):
        points_list = graphic_object.get_points()
        x_sum = 0
        y_sum = 0
        for point in points_list:
            x_sum += point.x
            y_sum += point.y
        n = len(points_list)
        return x_sum/n, y_sum/n

    def get_scaling_matrix(self, graphic_object: GraphicObject, sx: float, sy: float):
        xc, yc = self.get_object_center(graphic_object)
        return np.array([[sx, 0, 0], [0, sy, 0], [xc-xc*sx, yc-yc*sy, 0]])

    def test(self, pos: int):
        self.transform(self.display_file[pos], self.get_scaling_matrix(self.display_file[pos], 2, 2))
