import math
import numpy as np
from system.graphic_objects.graphic_object import GraphicObject
from system.graphic_objects.point import Point
from gui.widgets.logger import Logger
from utils.utils import format_point_list, get_object_center


class TransformationHandler:

    def __init__(self, logger: Logger) -> None:
        self.operations = []
        self.logger = logger
        
    def transform(self, graphic_object: GraphicObject) -> None:
        matrix = self.join_operations(self.operations)
        self.logger.log(f"Operation matrix for {graphic_object.name}: \n{matrix}")
        self.transform_object(graphic_object, matrix)
        self.operations = []

    def transform_object(self, graphic_object: GraphicObject, matrix: np.array) -> None:
        points_list = graphic_object.get_points()
        for point in points_list:
            old_point_matrix = np.array([point.x, point.y, 1])
            new_point_matrix = np.dot(old_point_matrix, matrix)
            point.x = new_point_matrix[0]
            point.y = new_point_matrix[1]
        self.logger.log(f"New {graphic_object.name} points: "
                        f"{format_point_list(list(map(Point.get_coordinates, points_list)))}.")

    def join_operations(self, matrix_list: list[np.array]) -> np.array:
        if len(matrix_list) == 1:
            return matrix_list[0]
        matrix = np.dot(matrix_list[0], matrix_list[1])
        for i in range(2, len(matrix_list)):
            matrix = np.dot(matrix, matrix_list[i])
        return matrix

    def add_translation_matrix(self, dx: float, dy: float) -> np.array:
        self.operations.append(np.array([[1, 0, 0],
                                         [0, 1, 0],
                                         [dx, dy, 1]]))

    def add_scaling_matrix(self, graphic_object: GraphicObject, sx: float, sy: float) -> np.array:
        xc, yc = get_object_center(graphic_object)
        self.operations.append(np.array([[sx, 0, 0],
                                         [0, sy, 0],
                                         [xc-xc*sx, yc-yc*sy, 1]]))

    def add_rotation_matrix(self, x: float, y: float, angle: float) -> np.array:
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))
        self.operations.append(np.array([[cos, sin, 0],
                                         [-1*sin, cos, 0],
                                         [x-cos*x+y*sin, y-cos*y-x*sin, 1]]))

    def remove_operation(self, pos: int) -> None:
        self.operations.pop(pos)

    def clear_transformation(self) -> None:
        self.operations = []
