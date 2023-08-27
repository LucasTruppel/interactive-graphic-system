from graphic_object import GraphicObject
from point import Point


class Wireframe(GraphicObject):
    def __init__(self, name: str, coordinates_list: list[tuple[float, float]]) -> None:
        super().__init__(name)
        self.points = []
        for i in range(len(coordinates_list)):
            x, y = coordinates_list[i]
            self.points.append(Point(f"{name}: point {i}", x, y))

    def get_points(self) -> list[Point]:
        return self.points

