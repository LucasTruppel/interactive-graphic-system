import math
import numpy as np


class MathUtils:

    @staticmethod
    def angle_between_vector_and_xy_plane(vector1: np.array) -> float:
        vector_yz_projection = np.array([0, vector1[1], vector1[2]])
        y_axis = np.array([0, 1, 0])
        angle = MathUtils.angle_between_vectors(vector_yz_projection, y_axis)
        return angle if vector1[2] <= 0 else 360 - angle

    @staticmethod
    def angle_between_vector_and_y_axis(vector1: np.array) -> float:
        vector = np.array([vector1[0], vector1[1], 0])
        y_axis = np.array([0, 1, 0])
        angle = MathUtils.angle_between_vectors(vector, y_axis)
        return angle if vector1[0] >= 0 else 360 - angle

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
