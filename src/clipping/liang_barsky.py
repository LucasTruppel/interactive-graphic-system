from graphic_objects.line import Line
from graphic_objects.point import Point


class LiangBarsky:

    @staticmethod
    def line_clipping(line: Line) -> bool:
        point1, point2 = line.get_points()
        p = [-1 * (point2.nx - point1.nx), point2.nx - point1.nx, -1 * (point2.ny - point1.ny), point2.ny - point1.ny]
        q = [point1.nx - (-1), 1 - point1.nx, point1.ny - (-1), 1 - point1.ny]

        for i in range(4):
            if p[i] == 0 and q[i] < 0:
                return False

        r = [0, 0, 0, 0]
        negative = [0]
        positive = [1]
        if p[0] != 0:
            r[0] = q[0] / p[0]
            r[1] = q[1] / p[1]
            negative.append(r[0] if p[0] < 0 else r[1])
            positive.append(r[1] if p[0] < 0 else r[0])
        if p[2] != 0:
            r[2] = q[2] / p[2]
            r[3] = q[3] / p[3]
            negative.append(r[2] if p[2] < 0 else r[3])
            positive.append(r[3] if p[2] < 0 else r[2])

        c = [max(negative), min(positive)]
        if c[0] > c[1]:
            return False

        x, y = point1.nx, point1.ny
        point1.nx, point1.ny = x + c[0] * p[1], y + c[0] * p[3]
        point2.nx, point2.ny = x + c[1] * p[1], y + c[1] * p[3]
        return True
