from system.graphic_objects.graphic_object import GraphicObject
from system.graphic_objects.point import Point


class Line(GraphicObject):
    def __init__(self, name: str, color: str, x1: float, y1: float, x2: float, y2: float,
                 nx1=float("inf"), ny1=float("inf"), nx2=float("inf"), ny2=float("inf")) -> None:
        super().__init__(name, color)
        self.points = [Point(name+" point1", color, x1, y1, nx1, ny1),
                       Point(name+" point2", color, x2, y2, nx2, ny2)]

    @classmethod
    def line_from_points(cls, name: str, color: str, point1: Point, point2: Point) -> 'Line':
        return Line(name, color, point1.x, point1.y, point2.x, point2.y, point1.nx, point1.ny, point2.nx, point2.ny)

    def get_points(self) -> list[Point]:
        return self.points
