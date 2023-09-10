from pathlib import Path

from graphic_objects.graphic_object import GraphicObject
from graphic_objects.point import Point
from system.window import Window
from utils.utils import get_object_center


class ObjTranscriber:

    def __init__(self, file_path: str) -> None:
        self.obg_file_path = file_path
        self.vertices_string = ""
        self.obj_string = f"mtllib {Path(file_path).name[:-4]}.mtl\n"
        self.mtl_string = ""
        self.vertices_amount = 0
        self.colors_amount = 0

    def transcribre(self, object_list: list[GraphicObject], window: Window) -> None:
        self.__transcribe_window(window)
        for graphic_object in object_list:
            self.__transcribre_object(graphic_object)
        self.__write_file()

    def __transcribe_window(self, window: Window) -> None:
        wcx, wcy = get_object_center(window)
        self.vertices_amount += 2
        self.vertices_string += f"v {wcx} {wcy} 0.0\n"
        self.vertices_string += f"v {window.width} {window.height} 0.0\n"
        self.obj_string += "o window\n"
        self.obj_string += f"w {self.vertices_amount-1} {self.vertices_amount}\n"

    def __transcribre_object(self, graphic_object: GraphicObject) -> None:
        point_list = graphic_object.get_points()
        for point in point_list:
            self.vertices_amount += 1
            self.vertices_string += f"v {point.x} {point.y} 0.0\n"
        self.obj_string += f"o {graphic_object.name}\n"
        self.__write_color(graphic_object.color)
        self.__write_vertices(point_list)

    def __write_color(self, color: str) -> None:
        self.colors_amount += 1
        self.mtl_string += f"newmtl color{self.colors_amount}\n"
        color = color[1:]
        red = int(color[:2], 16) / 255
        green = int(color[2:4], 16) / 255
        blue = int(color[4:], 16) / 255
        self.mtl_string += f"Kd {red} {green} {blue}\n"
        self.obj_string += f"usemtl color{self.colors_amount}\n"

    def __write_vertices(self, point_list: list[Point]) -> None:
        self.obj_string += "p " if len(point_list) == 1 else "l "
        for i in range(len(point_list) - 1, -1, -1):
            self.obj_string += f"{self.vertices_amount - i} "
        if len(point_list) > 2:
            self.obj_string += f"{self.vertices_amount - (len(point_list) - 1)} "
        self.obj_string += "\n"

    def __write_file(self) -> None:
        with open(self.obg_file_path, "w") as file:
            file.write(self.vertices_string + self.obj_string)
        with open(self.obg_file_path.replace(".obj", ".mtl"), "w") as file:
            file.write(self.mtl_string)
