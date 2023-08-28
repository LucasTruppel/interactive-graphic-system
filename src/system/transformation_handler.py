import math
import numpy as np
from graphic_objects.graphic_object import GraphicObject


class TransformationHandler:

    def __init__(self):
        self.operations = []
        
    def transform(self, graphic_object: GraphicObject) -> None:
        matrix = self.join_operations(self.operations)
        self.transform_object(graphic_object, matrix)
        self.operations = []

    def transform_object(self, graphic_object: GraphicObject, matrix: np.array) -> None:
        points_list = graphic_object.get_points()
        for point in points_list:
            point_matrix = np.array([point.x, point.y, 1])
            new_point_matrix = np.dot(point_matrix, matrix)
            point.x = new_point_matrix[0]
            point.y = new_point_matrix[1]

    def join_operations(self, matrix_list: list[np.array]) -> np.array:
        if len(matrix_list) == 1:
            return matrix_list[0]
        matrix = np.dot(matrix_list[0], matrix_list[1])
        for i in range(2, len(matrix_list)):
            matrix = np.dot(matrix, matrix_list[i])
        return matrix

    def add_translation_matrix(self, dx: float, dy: float) -> np.array:
        self.operations.append(np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]]))

    def add_scaling_matrix(self, graphic_object: GraphicObject, sx: float, sy: float) -> np.array:
        xc, yc = self.get_object_center(graphic_object)
        self.operations.append(np.array([[sx, 0, 0], [0, sy, 0], [xc-xc*sx, yc-yc*sy, 1]]))

    def add_rotation_matrix(self, x: float, y: float, angle: float) -> np.array:
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))
        self.operations.append(np.array([[cos, -1*sin, 0], [sin, cos, 0], [x-cos*x-y*sin, y-cos*y+x*sin, 1]]))

    def remove_operation(self, pos: int):
        self.operations.pop(pos)

    def get_object_center(self, graphic_object: GraphicObject) -> tuple[float, float]:
        points_list = graphic_object.get_points()
        x_sum = 0
        y_sum = 0
        for point in points_list:
            x_sum += point.x
            y_sum += point.y
        n = len(points_list)
        return x_sum/n, y_sum/n