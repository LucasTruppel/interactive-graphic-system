from system.graphic_objects.graphic_object import GraphicObject3d


class Point3d(GraphicObject3d):
    def __init__(self, name: str, color: str, x: float, y: float, z: float,
                 nx=float("inf"), ny=float("inf"), nz=float("inf")) -> None:
        super().__init__(name, color)
        self.x = x
        self.y = y
        self.z = z
        self.nx = nx if nx != float("inf") else x
        self.ny = ny if ny != float("inf") else y
        self.nz = nz if nz != float("inf") else z

    def __repr__(self):
        return str((self.x, self.y, self.z))

    def __str__(self):
        return str((self.x, self.y, self.z))

    def get_points(self) -> list['Point3d']:
        return [self]

    def get_coordinates(self) -> tuple[float, float, float]:
        return self.x, self.y, self.z

    def copy(self):
        return Point3d(self.name, self.color, self.x, self.y, self.z, self.nx, self.ny, self.nz)
