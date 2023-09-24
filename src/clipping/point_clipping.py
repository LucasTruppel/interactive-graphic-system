from graphic_objects.point import Point


class PointClipping:

    @staticmethod
    def point_clipping(point: Point) -> bool:
        if (-1 <= point.nx <= 1) and (-1 <= point.ny <= 1):
            return True
        return False
