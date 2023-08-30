from graphic_objects.graphic_object import GraphicObject
from graphic_objects.point import Point


class Line(GraphicObject):
    def __init__(self, name: str, color: str, x1: float, y1: float, x2: float, y2: float) -> None:
        super().__init__(name, color)
        self.points = [Point(name+" point1", color, x1, y1), Point(name+" point2", color, x2, y2)]

    def get_points(self) -> list[Point]:
        return self.points
