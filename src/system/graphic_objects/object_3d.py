import numpy as np

from system.graphic_objects.graphic_object import GraphicObject
from system.graphic_objects.point_3d import Point3d
from utils.utils import get_object_center_3d


class Object3d(GraphicObject):
    def __init__(self, name: str, color: str, coordinates_list: list[tuple[float, float, float]]) -> None:
        super().__init__(name, color)
        self.points = []
        for i in range(len(coordinates_list)):
            x, y, z = coordinates_list[i]
            self.points.append(Point3d(f"{name}: point {i}", color, x, y, z))

    def __repr__(self):
        return self.points

    def __str__(self):
        return str(self.points)

    def get_points(self) -> list[Point3d]:
        return self.points

    def get_rotation_axis_point(self) -> tuple[float, float, float]:
        point = self.points[0]
        return point.x, point.y, point.z

    def get_rotation_vector(self) -> np.array:
        x, y, z = self.points[0].get_coordinates()
        xc, yc, zc = get_object_center_3d(self)
        return np.array([xc - x, yc - y, zc - z])
