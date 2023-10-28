import math
import numpy as np
from system.graphic_objects.object_3d import Object3d
from gui.logger import Logger
from utils.utils import get_object_center_3d
from utils.math_utils import MathUtils


class TransformationHandler3d:

    def __init__(self, logger: Logger) -> None:
        self.operations = []
        self.logger = logger

    def transform(self, graphic_object: Object3d) -> None:
        matrix = self.__join_operations(self.operations)
        self.__transform_object(graphic_object, matrix)
        self.operations = []

    def __transform_object(self, graphic_object: Object3d, matrix: np.array) -> None:
        points_list = graphic_object.get_points()
        for point in points_list:
            old_point_matrix = np.array([point.x, point.y, point.z, 1])
            new_point_matrix = np.dot(old_point_matrix, matrix)
            point.x = new_point_matrix[0]
            point.y = new_point_matrix[1]
            point.z = new_point_matrix[2]

    def __join_operations(self, matrix_list: list[np.array]) -> np.array:
        if len(matrix_list) == 1:
            return matrix_list[0]
        matrix = np.dot(matrix_list[0], matrix_list[1])
        for i in range(2, len(matrix_list)):
            matrix = np.dot(matrix, matrix_list[i])
        return matrix

    def add_translation_matrix(self, dx: float, dy: float, dz: float) -> np.array:
        self.operations.append(TransformationHandler3d.get_translation_matrix(dx, dy, dz))

    def add_scaling_matrix(self, graphic_object: Object3d, sx: float, sy: float, sz: float) -> np.array:
        xc, yc, zc = get_object_center_3d(graphic_object)
        op = [TransformationHandler3d.get_translation_matrix(-xc, -yc, -zc),
              TransformationHandler3d.get_scaling_matrix(sx, sy, sz),
              TransformationHandler3d.get_translation_matrix(xc, yc, zc)]
        self.operations.append(self.__join_operations(op))

    def add_arbitrary_rotation_matrix(self, obj: Object3d, angle: float) -> np.array:
        x, y, z = obj.get_rotation_axis_point()
        rotation_vector = obj.get_rotation_vector()
        angle_x = MathUtils.angle_between_vector_and_xy_plane(rotation_vector)
        angle_z = MathUtils.angle_between_vector_and_y_axis(MathUtils.rotate_vector_x_axis(rotation_vector, angle_x))

        op = [TransformationHandler3d.get_translation_matrix(-x, -y, -z),
              TransformationHandler3d.get_x_rotation_matrix(angle_x),
              TransformationHandler3d.get_z_rotation_matrix(angle_z),
              TransformationHandler3d.get_y_rotation_matrix(angle),
              TransformationHandler3d.get_z_rotation_matrix(-angle_z),
              TransformationHandler3d.get_x_rotation_matrix(-angle_x),
              TransformationHandler3d.get_translation_matrix(x, y, z)]
        matrix = self.__join_operations(op)
        self.operations.append(matrix)
        return matrix

    def add_x_rotation_matrix(self, angle: float) -> None:
        self.operations.append(TransformationHandler3d.get_x_rotation_matrix(angle))

    def add_y_rotation_matrix(self, angle: float) -> None:
        self.operations.append(TransformationHandler3d.get_y_rotation_matrix(angle))

    def add_z_rotation_matrix(self, angle: float) -> None:
        self.operations.append(TransformationHandler3d.get_z_rotation_matrix(angle))

    def add_matrix(self, matrix: np.array):
        self.operations.append(matrix)

    def remove_operation(self, pos: int) -> None:
        self.operations.pop(pos)

    def clear_transformation(self) -> None:
        self.operations = []

    @staticmethod
    def get_x_rotation_matrix(angle: float) -> np.array:
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))
        return np.array([[1, 0, 0, 0],
                         [0, cos, sin, 0],
                         [0, -sin, cos, 0],
                         [0, 0, 0, 1]])

    @staticmethod
    def get_y_rotation_matrix(angle: float) -> np.array:
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))
        return np.array([[cos, 0, -sin, 0],
                         [0, 1, 0, 0],
                         [sin, 0, cos, 0],
                         [0, 0, 0, 1]])

    @staticmethod
    def get_z_rotation_matrix(angle: float) -> np.array:
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))
        return np.array([[cos, sin, 0, 0],
                         [-sin, cos, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])

    @staticmethod
    def get_translation_matrix(dx: float, dy: float, dz: float) -> np.array:
        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [dx, dy, dz, 1]])

    @staticmethod
    def get_scaling_matrix(sx: float, sy: float, sz: float) -> np.array:
        return np.array([[sx, 0, 0, 0],
                         [0, sy, 0, 0],
                         [0, 0, sz, 0],
                         [0, 0, 0, 1]])
