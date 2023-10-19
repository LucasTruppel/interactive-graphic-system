import numpy as np

from system.graphic_objects.graphic_object import GraphicObject
from system.graphic_objects.point import Point


class BSpline(GraphicObject):

    def __init__(self, name: str, color: str, coordinates_list: list[tuple[float, float]]) -> None:
        super().__init__(name, color)
        self.points = []
        self.Mbs = (1 / 6) * np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
        self.delta = 0.05
        self.delta2 = self.delta * self.delta
        self.delta3 = self.delta2 * self.delta

        self.__define_points(coordinates_list)

    def get_points(self) -> list[Point]:
        return self.points

    def __define_points(self, coordinates_list: list[tuple[float, float]]) -> None:
        for i in range(len(coordinates_list)):
            if i + 3 > len(coordinates_list) - 1:
                break
            ax, bx, cx, dx = self.__calculete_coefficients(coordinates_list[i][0], coordinates_list[i + 1][0],
                                                           coordinates_list[i + 2][0], coordinates_list[i + 3][0])
            ay, by, cy, dy = self.__calculete_coefficients(coordinates_list[i][1], coordinates_list[i + 1][1],
                                                           coordinates_list[i + 2][1], coordinates_list[i + 3][1])
            x, dx, d2x, d3x = self.__calculate_first_point(ax, bx, cx, dx)
            y, dy, d2y, d3y = self.__calculate_first_point(ay, by, cy, dy)
            self.__define_points_segment(x, dx, d2x, d3x, y, dy, d2y, d3y)

    def __calculete_coefficients(self, p1: float, p2: float, p3: float, p4: float) -> tuple[float, float, float, float]:
        Gbs = np.array([[p1], [p2], [p3], [p4]])
        C = np.dot(self.Mbs, Gbs)
        return float(C[0]), float(C[1]), float(C[2]), float(C[3])

    def __calculate_first_point(self, a: float, b: float, c: float, d: float) -> tuple[float, float, float, float]:
        f = d
        df = a * self.delta3 + b * self.delta2 + c * self.delta
        d2f = 6 * a * self.delta3 + 2 * b * self.delta2
        d3f = 6 * a * self.delta3
        return f, df, d2f, d3f

    def __define_points_segment(self, x: float, dx: float, d2x: float, d3x: float, y: float, dy: float, d2y: float,
                                d3y: float) -> None:
        i = 1
        self.points.append(Point(f"point {i}", "#000000", x, y))
        while i < (1 / self.delta):
            i += 1
            x = x + dx
            dx = dx + d2x
            d2x = d2x + d3x
            y = y + dy
            dy = dy + d2y
            d2y = d2y + d3y
            self.points.append(Point(f"point {i}", "#000000", x, y))
