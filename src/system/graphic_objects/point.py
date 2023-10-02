from system.graphic_objects.graphic_object import GraphicObject


class Point(GraphicObject):
    def __init__(self, name: str, color: str, x: float, y: float, nx=float("inf"), ny=float("inf")) -> None:
        super().__init__(name, color)
        self.x = x
        self.y = y
        self.nx = nx if nx != float("inf") else x
        self.ny = ny if ny != float("inf") else y

    def get_points(self) -> list['Point']:
        return [self]

    def get_coordinates(self) -> tuple[float, float]:
        return self.x, self.y
