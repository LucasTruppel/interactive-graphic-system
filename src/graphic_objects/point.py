from graphic_objects.graphic_object import GraphicObject


class Point(GraphicObject):
    def __init__(self, name: str, x: float, y: float) -> None:
        super().__init__(name)
        self.x = x
        self.y = y

    def get_points(self) -> list['Point']:
        return [self]
