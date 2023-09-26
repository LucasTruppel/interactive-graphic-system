from graphic_objects.graphic_object import GraphicObject
from graphic_objects.point import Point


class Wireframe(GraphicObject):
    def __init__(self, name: str, color: str, coordinates_list: list[tuple[float, float]]) -> None:
        super().__init__(name, color)
        self.fill = False
        self.points = []
        for i in range(len(coordinates_list)):
            x, y = coordinates_list[i]
            self.points.append(Point(f"{name}: point {i}", color, x, y))

    def get_points(self) -> list[Point]:
        return self.points
