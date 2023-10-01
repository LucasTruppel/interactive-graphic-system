from pathlib import Path
import numpy as np

from system.graphic_objects.graphic_object import GraphicObject
from system.core.window import Window
from system.graphic_objects.point import Point
from system.graphic_objects.line import Line
from system.graphic_objects.wireframe import Wireframe


class ObjReader:

    def __init__(self, file_path: str) -> None:
        self.obj_file_path = file_path
        self.vertices = []
        self.new_objects = []
        self.colors = {}
        self.current_color = ""
        self.current_object = ""

    def read(self, object_list: list[GraphicObject], window: Window) -> list[GraphicObject]:
        with open(self.obj_file_path, "r") as file:
            for line in file:
                line = line.split()
                match line[0]:
                    case "v":
                        self.vertices.append((float(line[1]), float(line[2])))
                    case "mtllib":
                        self.__read_mtl_file(line[1])
                    case "o":
                        self.current_object = line[1]
                    case "w":
                        self.__update_window(int(line[1]), int(line[2]), window)
                    case "usemtl":
                        self.current_color = self.colors[line[1]]
                    case "p":
                        x, y = self.vertices[int(line[1])-1]
                        point = Point(self.current_object, self.current_color, x, y)
                        object_list.append(point)
                        self.new_objects.append(point)
                    case "l":
                        self.__create_object(object_list, line)
        return self.new_objects

    def __read_mtl_file(self, mtl_file_name: str) -> None:
        with open(self.obj_file_path.replace(Path(self.obj_file_path).name, mtl_file_name), "r") as file:
            for line in file:
                line = line.split()
                match line[0]:
                    case "newmtl":
                        self.current_color = line[1]
                        self.colors[line[1]] = "#000000"
                    case "Kd":
                        red = format(int(float(line[1]) * 255), "02x")
                        green = format(int(float(line[2]) * 255), "02x")
                        blue = format(int(float(line[3]) * 255), "02x")
                        color = "#" + red + green + blue
                        self.colors[self.current_color] = color

    def __update_window(self, vertice_center: int, vertice_size: int, window: Window) -> None:
        wcx, wcy = self.vertices[vertice_center-1]
        window.width, window.height = self.vertices[vertice_size-1]
        x_min = wcx - window.width / 2
        y_min = wcy - window.height / 2
        x_max = wcx + window.width / 2
        y_max = wcy + window.height / 2
        window.points[0].x, window.points[0].y = x_min, y_min
        window.points[1].x, window.points[1].y = x_min, y_max
        window.points[2].x, window.points[2].y = x_max, y_max
        window.points[3].x, window.points[3].y = x_max, y_min
        window.vector = np.array([0, 1])
        window.transformation_handler.clear_transformation()

    def __create_object(self, object_list: list[GraphicObject], line: list) -> None:
        point_list = []
        for i in range(1, len(line)):
            point_list.append(self.vertices[int(line[i])-1])
        if len(point_list) == 2:
            x1, y1 = point_list[0]
            x2, y2 = point_list[1]
            new_object = Line(self.current_object, self.current_color, x1, y1, x2, y2)
        else:
            point_list.pop()
            new_object = Wireframe(self.current_object, self.current_color, False, point_list)
        object_list.append(new_object)
        self.new_objects.append(new_object)
