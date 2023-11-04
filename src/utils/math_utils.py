import math
import numpy as np

from system.graphic_objects.point_3d import Point3d


class MathUtils:

    @staticmethod
    def angle_between_vector_and_xy_plane(vector1: np.array) -> float:
        vector_yz_projection = np.array([0, vector1[1], vector1[2]])
        if np.all(vector_yz_projection == 0):
            return 0
        y_axis = np.array([0, 1, 0])
        angle = MathUtils.angle_between_vectors(vector_yz_projection, y_axis)
        return angle if vector1[2] <= 0 else 360 - angle

    @staticmethod
    def angle_between_vector_and_yz_plane(vector1: np.array) -> float:
        vector_xz_projection = np.array([vector1[0], 0, vector1[2]])
        if np.all(vector_xz_projection == 0):
            return 0
        z_axis = np.array([0, 0, 1])
        angle = MathUtils.angle_between_vectors(vector_xz_projection, z_axis)
        return angle if vector1[0] <= 0 else 360 - angle

    @staticmethod
    def angle_between_vector_and_xz_plane(vector1: np.array) -> float:
        vector_xy_projection = np.array([vector1[0], vector1[1], 0])
        if np.all(vector_xy_projection == 0):
            return 0
        y_axis = np.array([0, 1, 0])
        angle = MathUtils.angle_between_vectors(vector_xy_projection, y_axis)
        return angle if vector1[0] >= 0 else 360 - angle

    @staticmethod
    def angle_between_vector_and_y_axis(vector1: np.array) -> float:
        vector = np.array([vector1[0], vector1[1], 0])
        y_axis = np.array([0, 1, 0])
        angle = MathUtils.angle_between_vectors(vector, y_axis)
        return angle if vector1[0] >= 0 else 360 - angle

    @staticmethod
    def angle_between_vector_and_z_axis(vector: np.array) -> float:
        z_axis = np.array([0, 0, 1])
        angle = MathUtils.angle_between_vectors(vector, z_axis)
        return angle if vector[1] >= 0 else 360 - angle

    @staticmethod
    def angle_between_vectors(vector1: np.array, vector2: np.array) -> float:
        dot_product = np.dot(vector1, vector2)
        magnitude_vector1 = np.linalg.norm(vector1)
        magnitude_vector2 = np.linalg.norm(vector2)
        cosine_theta = dot_product / (magnitude_vector1 * magnitude_vector2)
        angle_degrees = np.degrees(np.arccos(cosine_theta))
        return float(angle_degrees)

    @staticmethod
    def rotate_vector_x_axis(vector: np.array, angle_degrees: float) -> np.array:
        angle_radians = np.deg2rad(angle_degrees)
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(angle_radians), -np.sin(angle_radians)],
            [0, np.sin(angle_radians), np.cos(angle_radians)]
        ])
        rotated_vector = np.dot(rotation_matrix, vector)
        return rotated_vector

    @staticmethod
    def rotate_vector_around_y_axis(vector: np.array, angle_degrees: float) -> np.array:
        angle_radians = np.deg2rad(angle_degrees)
        rotation_matrix = np.array([
            [np.cos(angle_radians), 0, np.sin(angle_radians)],
            [0, 1, 0],
            [-np.sin(angle_radians), 0, np.cos(angle_radians)]
        ])
        rotated_vector = np.dot(rotation_matrix, vector)
        return rotated_vector

    @staticmethod
    def rotate_vector_around_z_axis(vector: np.array, angle_degrees: float) -> np.array:
        angle_radians = np.deg2rad(angle_degrees)
        rotation_matrix = np.array([
            [np.cos(angle_radians), -np.sin(angle_radians), 0],
            [np.sin(angle_radians), np.cos(angle_radians), 0],
            [0, 0, 1]
        ])
        rotated_vector = np.dot(rotation_matrix, vector)
        return rotated_vector

    @staticmethod
    def calculate_unit_vector(vector):
        vector = np.array(vector)
        magnitude = np.linalg.norm(vector)
        if magnitude == 0:
            raise ValueError("Cannot calculate the unit vector of a zero-length vector.")
        unit_vector = vector / magnitude
        return unit_vector

    @staticmethod
    def get_middle_point(point1, point2) -> tuple[float, float, float]:
        return (point2.x + point1.x) / 2, (point2.y + point1.y) / 2, (point2.z + point1.z) / 2

    @staticmethod
    def distance_between_points_3d(point1: Point3d, point2: Point3d) -> float:
        return math.sqrt((point2.x - point1.x) ** 2 +
                         (point2.y - point1.y) ** 2 +
                         (point2.z - point1.z) ** 2)
