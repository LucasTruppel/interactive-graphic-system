import numpy as np

from system.graphic_objects.graphic_object import GraphicObject3d
from system.graphic_objects.point_3d import Point3d


class BSpline3d(GraphicObject3d):

    def __init__(self, name: str, color: str, points: list, define_points: bool = True) -> None:
        super().__init__(name, color)
        self.points = []
        self.Mbs = (1 / 6) * np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
        self.Mbst = np.transpose(self.Mbs)
        self.delta = 0.25
        self.delta2 = self.delta * self.delta
        self.delta3 = self.delta2 * self.delta
        self.n = int(1 / self.delta) + 1
        self.E = np.array([
            [0,             0,             0,          1],
            [self.delta3,   self.delta2,   self.delta, 0],
            [6*self.delta3, 2*self.delta2, 0,          0],
            [6*self.delta3, 0,             0,          0]
        ])
        self.Et = np.transpose(self.E)

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
        return BSpline3d(self.name, self.color, points, False)

    def __define_points(self, coordinates_list: list[list[tuple[float, float, float]]]) -> None:
        size = len(coordinates_list)
        for m in range(size - 3):
            for n in range(size - 3):
                gbsx, gbsy, gbsz = np.zeros((4, 4)), np.zeros((4, 4)), np.zeros((4, 4))
                for i in range(4):
                    for j in range(4):
                        coords = coordinates_list[m + i][n + j]
                        gbsx[i][j] = coords[0]
                        gbsy[i][j] = coords[1]
                        gbsz[i][j] = coords[2]
                self.__calculate_curve(gbsx, gbsy, gbsz)

    def __calculate_curve(self, gbsx: np.array, gbsy: np.array, gbsz: np.array) -> None:
        DDx, DDy, DDz = self.__get_initial_matrices(gbsx, gbsy, gbsz)
        for t in range(self.n):
            self.__define_points_segment(DDx[0][0], DDx[0][1], DDx[0][2], DDx[0][3],
                                         DDy[0][0], DDy[0][1], DDy[0][2], DDy[0][3],
                                         DDz[0][0], DDz[0][1], DDz[0][2], DDz[0][3])
            self.__update_matrices(DDx, DDy, DDz)

        DDx, DDy, DDz = self.__get_initial_matrices(gbsx, gbsy, gbsz)
        DDx, DDy, DDz = np.transpose(DDx), np.transpose(DDy), np.transpose(DDz)
        for s in range(self.n):
            self.__define_points_segment(DDx[0][0], DDx[0][1], DDx[0][2], DDx[0][3],
                                         DDy[0][0], DDy[0][1], DDy[0][2], DDy[0][3],
                                         DDz[0][0], DDz[0][1], DDz[0][2], DDz[0][3])
            self.__update_matrices(DDx, DDy, DDz)

    def __get_initial_matrices(self, gbsx: np.array, gbsy: np.array, gbsz: np.array) \
            -> tuple[np.array, np.array, np.array]:
        Cx = np.dot(np.dot(self.Mbs, gbsx), self.Mbst)
        DDx = np.dot(np.dot(self.E, Cx), self.Et)
        Cy = np.dot(np.dot(self.Mbs, gbsy), self.Mbst)
        DDy = np.dot(np.dot(self.E, Cy), self.Et)
        Cz = np.dot(np.dot(self.Mbs, gbsz), self.Mbst)
        DDz = np.dot(np.dot(self.E, Cz), self.Et)
        return DDx, DDy, DDz

    def __define_points_segment(self, x: float, dx: float, d2x: float, d3x: float,
                                y: float, dy: float, d2y: float, d3y: float,
                                z: float, dz: float, d2z: float, d3z: float) -> None:
        self.points.append(Point3d(f"point {0}", "#000000", x, y, z))
        for i in range(1, self.n):
            x = x + dx
            dx = dx + d2x
            d2x = d2x + d3x
            y = y + dy
            dy = dy + d2y
            d2y = d2y + d3y
            z = z + dz
            dz = dz + d2z
            d2z = d2z + d3z
            self.points.append(Point3d(f"point {i}", "#000000", x, y, z))

    def __update_matrices(self, ddx: np.array, ddy: np.array, ddz: np.array) -> np.array:
        for i in range(len(ddx)-1):
            for j in range(len(ddx)):
                ddx[i][j] = ddx[i][j] + ddx[i + 1][j]
                ddy[i][j] = ddy[i][j] + ddy[i + 1][j]
                ddz[i][j] = ddz[i][j] + ddz[i + 1][j]
