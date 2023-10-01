from system.graphic_objects.graphic_object import GraphicObject


class Point(GraphicObject):
    def __init__(self, name: str, color: str, x: float, y: float) -> None:
        super().__init__(name, color)
        self.x = x
        self.y = y
        self.nx = x
        self.ny = y

    def get_points(self) -> list['Point']:
        return [self]

    def get_coordinates(self) -> tuple[float, float]:
        return self.x, self.y
