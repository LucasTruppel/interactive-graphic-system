from graphic_objects.wireframe import Wireframe
from graphic_objects.point import Point


class SutherlandHodgman:

    @staticmethod
    def polygon_clipping(wireframe: Wireframe) -> Wireframe:
        points = [(point.nx, point.ny) for point in wireframe.get_points()]
        new_points = []
        for border in ["left", "top", "right", "bottom"]:
            for i in range(len(points)):
                point1 = points[i]
                point2 = points[(i + 1) % len(points)]
                point1_inside = SutherlandHodgman.is_inside(point1, border)
                point2_inside = SutherlandHodgman.is_inside(point2, border)
                if not point1_inside and point2_inside:
                    SutherlandHodgman.__out_in(point1, point2, border, new_points)
                elif point1_inside and point2_inside:
                    SutherlandHodgman.__in_in(point2, new_points)
                elif point1_inside and not point2_inside:
                    SutherlandHodgman.__in_out(point1, point2, border, new_points)
            points = new_points.copy()
            new_points = []
        if SutherlandHodgman.__is_window(points) or len(points) < 3:
            return False, None
        return True, Wireframe(wireframe.name, wireframe.color, wireframe.fill, points)

    @staticmethod
    def __out_in(point1: tuple[float, float], point2: tuple[float, float], border: str,
                 new_points: list[tuple[float, float]]) -> None:
        match border:
            case "left":
                found, x, y = SutherlandHodgman.__vertical_intersection(point1, point2, -1)
            case "top":
                found, x, y = SutherlandHodgman.__horizontal_intersection(point1, point2, 1)
            case "right":
                found, x, y = SutherlandHodgman.__vertical_intersection(point1, point2, 1)
            case default:
                found, x, y = SutherlandHodgman.__horizontal_intersection(point1, point2, -1)
        new_points.append((x, y))
        new_points.append(point2)

    @staticmethod
    def __in_in(point2: tuple[float, float], new_points: list[tuple[float, float]]) -> None:
        new_points.append(point2)

    @staticmethod
    def __in_out(point1: tuple[float, float], point2: tuple[float, float], border: str,
                 new_points: list[tuple[float, float]]) -> None:
        match border:
            case "left":
                found, x, y = SutherlandHodgman.__vertical_intersection(point1, point2, -1)
            case "top":
                found, x, y = SutherlandHodgman.__horizontal_intersection(point1, point2, 1)
            case "right":
                found, x, y = SutherlandHodgman.__vertical_intersection(point1, point2, 1)
            case default:
                found, x, y = SutherlandHodgman.__horizontal_intersection(point1, point2, -1)
        new_points.append((x, y))

    @staticmethod
    def __vertical_intersection(point1: tuple[float, float], point2: tuple[float, float], x: float) \
            -> tuple[bool, float, float]:
        m = SutherlandHodgman.__slope(point1, point2)
        if m == float("inf"):
            if point1[0] != x:
                return False, float("inf"), float("inf")
            return True, x, float("inf")
        y = m * (x - point1[0]) + point1[1]
        return True, x, y

    @staticmethod
    def __horizontal_intersection(point1: tuple[float, float], point2: tuple[float, float], y: float) \
            -> tuple[bool, float, float]:
        m = SutherlandHodgman.__slope(point1, point2)
        if m == float("inf"):
            return True, point1[0], y
        if m == 0:
            return False, float("inf"), float("inf")
        x = (1 / m) * (y - point1[1]) + point1[0]
        return True, x, y

    @staticmethod
    def __slope(point1: tuple[float, float], point2: tuple[float, float]) -> float:
        if point2[0] - point1[0] == 0:
            return float("inf")
        return (point2[1] - point1[1]) / (point2[0] - point1[0])

    @staticmethod
    def is_inside(point1: tuple[float, float], border: str) -> bool:
        match border:
            case "left":
                if point1[0] < -1:
                    return False
                return True
            case "top":
                if point1[1] > 1:
                    return False
                return True
            case "right":
                if point1[0] > 1:
                    return False
                return True
            case default:
                if point1[1] < -1:
                    return False
                return True

    @staticmethod
    def __is_window(points: list[tuple[float, float]]) -> bool:
        if len(points) != 4:
            return False
        for x, y in points:
            if abs(x) != 1 or abs(y) != 1:
                return False
        return True
