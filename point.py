from graphic_object import GraphicObject


class Point(GraphicObject):
    def __init__(self, name: str, x: int, y: int):
        super().__init__(name)
        self.x = x
        self.y = y

    def get_points(self):
        return [self]
