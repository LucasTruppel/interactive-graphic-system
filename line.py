from graphic_object import GraphicObject
from point import Point


class Line(GraphicObject):
    def __init__(self, name: str, x1: float, y1: float, x2: float, y2: float):
        super().__init__(name)
        self.points = [Point(name+" point1", x1,  y1), Point(name+" point2", x2, y2)]

    def get_points(self) -> list[Point]:
        return self.points

