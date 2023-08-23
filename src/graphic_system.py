from window import Window
from viewport import Viewport
from line import *
from tkinter import Canvas, BOTH
from wireframe import Wireframe


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
            if len(points_list) > 1:
                for i in range(len(points_list)-1):
                    x1, y1 = self.viewport_transformation(points_list[i])
                    x2, y2 = self.viewport_transformation(points_list[i+1])
                    self.viewport_canvas.create_line(x1, y1, x2, y2)
            else:
                x, y = self.viewport_transformation(points_list[0])
                self.viewport_canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")
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
