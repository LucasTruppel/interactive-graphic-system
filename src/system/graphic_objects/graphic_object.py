from abc import ABC, abstractmethod


class GraphicObject(ABC):

    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color
        self.is_3d = False

    @abstractmethod
    def get_points(self) -> list['Point']:
        pass


class GraphicObject3d(GraphicObject, ABC):

    def __init__(self, name: str, color: str) -> None:
        super().__init__(name, color)
        self.is_3d = True

    @abstractmethod
    def get_points(self) -> list['Point3d']:
        pass


class GraphicObjectType:
    POINT = "Point"
    LINE = "Line"
    POLYGON = "Polygon"
    BEZIER_CURVE = "Bezier Curve"
    B_SPLINE_CURVE = "B-Spline Curve"
    POINT_3D = "3d Point"
    OBJECT_3D = "3d Object"
    BEZIER_CURVE_3D = "3d Bezier Curve"
