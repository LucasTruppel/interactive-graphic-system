from window import Window
from viewport import Viewport
from line import *
from tkinter import Canvas, BOTH
from wireframe import Wireframe


class GraphicSystem:

    def __init__(self, width: int, height: int, viewport_canvas: Canvas):
        self.display_file = []
        self.window = Window(0, 0, width, height)
        self.viewport = Viewport(0, 0, width, height)
        self.viewport_canvas = viewport_canvas

    def viewport_transformation(self, point: Point):
        xw, yw = point.x, point.y
        xvp = ((xw - self.window.x_min) / (self.window.x_max - self.window.x_min) *
               (self.viewport.x_max - self.viewport.x_min))
        yvp = ((1 - ((yw - self.window.y_min) / (self.window.y_max - self.window.y_min))) *
               (self.viewport.y_max - self.viewport.y_min))
        return xvp, yvp

    def draw_display_file(self):
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
        self.viewport_canvas.pack(fill=BOTH, expand=1)

    def test(self):
        line = Line("linha1", 600, 0, 600, 600)
        self.display_file.append(line)
        wireframe = Wireframe("wireframe1", [(100, 100), (400, 0), (400, 400), (0, 400)])
        self.display_file.append(wireframe)
        point = Point("point1", 700, 700)
        self.display_file.append(point)
