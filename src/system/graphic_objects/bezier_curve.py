import numpy as np

from system.graphic_objects.graphic_object import GraphicObject
from system.graphic_objects.point import Point


class BezierCurve(GraphicObject):

    def __init__(self, name: str, color: str, coordinates_list: list[tuple[float, float]]) -> None:
        super().__init__(name, color)
        self.points = []
        self.Mb = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])

        self.__define_points(coordinates_list)

    def get_points(self) -> list[Point]:
        return self.points

    def __define_points(self, coordinates_list: list[tuple[float, float]]) -> None:
        pace = 0.05
        for i in range(0, len(coordinates_list), 3):
            if i + 3 > len(coordinates_list) - 1:
                break
            Gbx = np.array([coordinates_list[i][0], coordinates_list[i + 1][0], coordinates_list[i + 2][0],
                            coordinates_list[i + 3][0]])
            Gby = np.array([coordinates_list[i][1], coordinates_list[i + 1][1], coordinates_list[i + 2][1],
                            coordinates_list[i + 3][1]])
            for t in np.arange(0, 1 + pace, pace):
                T = np.array([t ** 3, t ** 2, t, 1])
                TMb = np.dot(T, self.Mb)
                x = float(np.dot(TMb, Gbx))
                y = float(np.dot(TMb, Gby))
                self.points.append(Point(f"point i:{i} t:{t}", self.color, x, y))
