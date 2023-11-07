import numpy as np

from system.graphic_objects.graphic_object import GraphicObject3d
from system.graphic_objects.point_3d import Point3d


class BezierCurve3d(GraphicObject3d):

    def __init__(self, name: str, color: str, points: list, define_points: bool = True) -> None:
        super().__init__(name, color)
        self.points = []
        self.Mb = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])
        self.Mbt = np.transpose(self.Mb)

        if define_points:
            self.__define_points(points)
        else:
            self.points = points

    def get_points(self) -> list[Point3d]:
        return self.points

    def copy(self):
        points = []
        for point in self.points:
            points.append(Point3d("", point.color, point.x, point.y, point.z))
        return BezierCurve3d(self.name, self.color, points, False)

    def __define_points(self, coordinates_list: list[tuple[float, float, float]]) -> None:
        pace = 0.1
        for k in range(0, len(coordinates_list), 16):
            if k + 15 > len(coordinates_list) - 1:
                break
            Gbx, Gby, Gbz = np.zeros((4, 4)), np.zeros((4, 4)), np.zeros((4, 4))
            for ik in range(4):
                for jk in range(4):
                    coordinate = coordinates_list[ik*4 + jk + k]
                    Gbx[ik][jk] = coordinate[0]
                    Gby[ik][jk] = coordinate[1]
                    Gbz[ik][jk] = coordinate[2]
            for s in np.arange(0, 1 + pace, pace):
                S = np.array([s ** 3, s ** 2, s, 1])
                last_point = None
                for t in np.arange(0, 1 + pace, pace):
                    Tt = np.array([[t ** 3], [t ** 2], [t], [1]])
                    SMb = np.dot(S, self.Mb)
                    MtbTt = np.dot(self.Mbt, Tt)
                    x = float(np.dot(np.dot(SMb, Gbx), MtbTt))
                    y = float(np.dot(np.dot(SMb, Gby), MtbTt))
                    z = float(np.dot(np.dot(SMb, Gbz), MtbTt))
                    new_point = Point3d(f"", self.color, x, y, z)
                    if last_point is not None:
                        self.points.append(last_point.copy())
                        self.points.append(new_point)
                    last_point = new_point
