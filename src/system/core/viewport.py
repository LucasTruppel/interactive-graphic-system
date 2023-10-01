from tkinter import Canvas
from system.graphic_objects.point import Point
from system.graphic_objects.line import Line
from system.graphic_objects.wireframe import Wireframe


class Viewport:
    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float, viewport_canvas: Canvas) -> None:
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.viewport_canvas = viewport_canvas
        self.draw_border()

    def viewport_transformation(self, point: Point) -> tuple[float, float]:
        xw, yw = point.nx, point.ny
        xvp = ((xw + 1) / 2 * (self.x_max - self.x_min)) + 10
        yvp = ((1 - ((yw + 1) / 2)) * (self.y_max - self.y_min)) + 10
        return xvp, yvp

    def clear(self) -> None:
        self.viewport_canvas.delete("all")

    def update(self) -> None:
        self.draw_border()
        self.viewport_canvas.update()

    def draw_border(self) -> None:
        self.viewport_canvas.create_line(self.x_min + 10, self.y_min + 10, self.x_min + 10, self.y_max + 10)
        self.viewport_canvas.create_line(self.x_min + 10, self.y_max + 10, self.x_max + 10, self.y_max + 10)
        self.viewport_canvas.create_line(self.x_max + 10, self.y_max + 10, self.x_max + 10, self.y_min + 10)
        self.viewport_canvas.create_line(self.x_max + 10, self.y_min + 10, self.x_min + 10, self.y_min + 10)

    def draw_point(self, point: Point) -> None:
        x, y = self.viewport_transformation(point.get_points()[0])
        self.viewport_canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=point.color)

    def draw_line(self, line: Line) -> None:
        points_list = line.get_points()
        x1, y1 = self.viewport_transformation(points_list[0])
        x2, y2 = self.viewport_transformation(points_list[1])
        self.viewport_canvas.create_line(x1, y1, x2, y2, fill=line.color)

    def draw_wireframe(self, wireframe: Wireframe) -> None:
        if not wireframe.fill:
            points_list = wireframe.get_points()
            for i in range(len(points_list) - 1):
                x1, y1 = self.viewport_transformation(points_list[i])
                x2, y2 = self.viewport_transformation(points_list[i + 1])
                self.viewport_canvas.create_line(x1, y1, x2, y2, fill=wireframe.color)
            x1, y1 = self.viewport_transformation(points_list[len(points_list) - 1])
            x2, y2 = self.viewport_transformation(points_list[0])
            self.viewport_canvas.create_line(x1, y1, x2, y2, fill=wireframe.color)
        else:
            coords = []
            for point in wireframe.get_points():
                x, y = self.viewport_transformation(point)
                coords.append(x)
                coords.append(y)
            self.viewport_canvas.create_polygon(coords, fill=wireframe.color)
