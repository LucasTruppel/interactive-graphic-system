from system.graphic_objects.line import Line
from system.graphic_objects.point import Point


class CohenSutherland:

    TOP = 0b1000
    BOTTOM = 0b0100
    RIGHT = 0b0010
    LEFT = 0b0001
    CENTER = 0b0000

    @staticmethod
    def line_clipping(line: Line) -> bool:
        point1, point2 = line.get_points()
        point1_code = CohenSutherland.__define_region_code(point1)
        point2_code = CohenSutherland.__define_region_code(point2)
        if point1_code == CohenSutherland.CENTER and point2_code == CohenSutherland.CENTER:
            return True
        elif (point1_code & point2_code) != CohenSutherland.CENTER:
            return False
        else:
            if point2.nx != point1.nx:
                m = (point2.ny - point1.ny) / (point2.nx - point1.nx)
            else:
                m = float('inf')
            found_intersection1, found_intersection2 = False, False
            if point1_code != CohenSutherland.CENTER:
                found_intersection1, x1, y1 = CohenSutherland.__define_inteserction(m, point1_code, point1)
                if found_intersection1:
                    point1.nx, point1.ny = x1, y1
            if point2_code != CohenSutherland.CENTER:
                found_intersection2, x2, y2 = CohenSutherland.__define_inteserction(m, point2_code, point2)
                if found_intersection2:
                    point2.nx, point2.ny = x2, y2
            return found_intersection1 or found_intersection2

    @staticmethod
    def __define_region_code(point: Point) -> int:
        region_code = CohenSutherland.CENTER
        if point.ny > 1:
            region_code |= CohenSutherland.TOP
        elif point.ny < -1:
            region_code |= CohenSutherland.BOTTOM
        if point.nx > 1:
            region_code |= CohenSutherland.RIGHT
        elif point.nx < -1:
            region_code |= CohenSutherland.LEFT
        return region_code

    @staticmethod
    def __define_inteserction(m: int, point_code: int, point: Point) -> bool:
        if point_code & CohenSutherland.TOP:
            found, x, y = CohenSutherland.__intersection_top(m, point)
            if found:
                return found, x, y
        elif point_code & CohenSutherland.BOTTOM:
            found, x, y = CohenSutherland.__intersection_bottom(m, point)
            if found:
                return found, x, y
        if point_code & CohenSutherland.RIGHT:
            found, x, y = CohenSutherland.__intersection_right(m, point)
            if found:
                return found, x, y
        elif point_code & CohenSutherland.LEFT:
            found, x, y = CohenSutherland.__intersection_left(m, point)
            if found:
                return found, x, y
        return False, 0, 0

    @staticmethod
    def __intersection_top(m: int, point: Point) -> tuple[bool, int, int]:
        if m == float('inf'):
            x = point.nx
        else:
            x = point.nx + 1/m * (1 - point.ny)
        intersection_found = -1 <= x <= 1
        return intersection_found, x, 1

    @staticmethod
    def __intersection_bottom(m: int, point: Point) -> tuple[bool, int, int]:
        if m == float('inf'):
            x = point.nx
        else:
            x = point.nx + 1/m * (-1 - point.ny)
        intersection_found = -1 <= x <= 1
        return intersection_found, x, -1

    @staticmethod
    def __intersection_right(m: int, point: Point) -> tuple[bool, int, int]:
        y = m * (1 - point.nx) + point.ny
        intersection_found = -1 <= y <= 1
        return intersection_found, 1, y

    @staticmethod
    def __intersection_left(m: int, point: Point) -> tuple[bool, int, int]:
        y = m * (-1 - point.nx) + point.ny
        intersection_found = -1 <= y <= 1
        return intersection_found, -1, y
