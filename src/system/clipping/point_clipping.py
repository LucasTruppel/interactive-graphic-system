from system.graphic_objects.point import Point


class PointClipping:

    @staticmethod
    def point_clipping(point) -> bool:
        if (-1 <= point.nx <= 1) and (-1 <= point.ny <= 1):
            return True
        return False

    @staticmethod
    def point_coordinates_clipping(x: float, y: float) -> bool:
        if (-1 <= x <= 1) and (-1 <= y <= 1):
            return True
        return False
