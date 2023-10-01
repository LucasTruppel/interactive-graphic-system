import math
import numpy as np

from system.graphic_objects.point import Point
from system.graphic_objects.graphic_object import GraphicObject


def format_point_list(points_list: list[tuple[float, float]]) -> str:
    return (str(points_list)
            .replace("[", "")
            .replace("]", "")
            .replace(".0,", ",")
            .replace(".0)", ")"))


def get_object_center(graphic_object: GraphicObject) -> tuple[float, float]:
    points_list = graphic_object.get_points()
    x_sum = 0
    y_sum = 0
    for point in points_list:
        x_sum += point.x
        y_sum += point.y
    n = len(points_list)
    return x_sum/n, y_sum/n


def angle_between_vector_and_y_axis(vector1: np.array) -> float:
    y_axis = np.array([0, 1])
    dot_product = np.dot(vector1, y_axis)
    magnitude_vector1 = np.linalg.norm(vector1)
    magnitude_vector2 = np.linalg.norm(y_axis)
    cosine_theta = dot_product / (magnitude_vector1 * magnitude_vector2)
    angle_degrees = np.degrees(np.arccos(cosine_theta))
    if vector1[0] > 0:
        angle_degrees = 360 - angle_degrees
    return angle_degrees


def rotate_vector(vector: np.array, angle_degrees: float) -> np.array:
    cos = math.cos(math.radians(angle_degrees))
    sin = math.sin(math.radians(angle_degrees))
    x = vector[0] * cos - vector[1] * sin
    y = vector[0] * sin + vector[1] * cos
    return np.array([x, y])


def distance_between_points(point1: Point, point2: Point) -> float:
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)
