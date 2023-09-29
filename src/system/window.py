import math
import numpy as np

from graphic_objects.graphic_object import GraphicObject
from graphic_objects.wireframe import Wireframe
from utils.utils import rotate_vector, angle_between_vector_and_y_axis, distance_between_points, get_object_center
from system.transformation_handler import TransformationHandler
from gui.logger import Logger


class Window(Wireframe):

    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float, logger: Logger) -> None:
        super().__init__("window", "#FFFFFF", False,
                         [(x_min, y_min), (x_min, y_max), (x_max, y_max), (x_max, y_min)])
        self.width = x_max - x_min
        self.height = y_max - y_min
        self.vector = np.array([0, 1])
        self.transformation_handler = TransformationHandler(logger)
        self.normalization_matrix = None
        self.nx_min = -1
        self.nx_max = 1
        self.ny_min = -1
        self.ny_max = 1

    def move_up(self) -> None:
        shift = 0.2 * self.height
        shift_vector = shift * self.vector
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_translation_matrix(float(shift_vector[0]), float(shift_vector[1]))
        self.transformation_handler.transform(self)

    def move_down(self) -> None:
        shift = 0.2 * self.height
        shift_vector = -1 * shift * self.vector
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_translation_matrix(float(shift_vector[0]), float(shift_vector[1]))
        self.transformation_handler.transform(self)

    def move_left(self) -> None:
        shift = 0.2 * self.height
        shift_vector = shift * rotate_vector(self.vector, 90)
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_translation_matrix(float(shift_vector[0]), float(shift_vector[1]))
        self.transformation_handler.transform(self)

    def move_right(self) -> None:
        shift = 0.2 * self.height
        shift_vector = shift * rotate_vector(self.vector, -90)
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_translation_matrix(float(shift_vector[0]), float(shift_vector[1]))
        self.transformation_handler.transform(self)

    def zoom_in(self) -> None:
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_scaling_matrix(self, 0.8, 0.8)
        self.transformation_handler.transform(self)
        self.width = distance_between_points(self.points[0], self.points[3])
        self.height = distance_between_points(self.points[0], self.points[1])

    def zoom_out(self) -> None:
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_scaling_matrix(self, 1.2, 1.2)
        self.transformation_handler.transform(self)
        self.width = distance_between_points(self.points[0], self.points[3])
        self.height = distance_between_points(self.points[0], self.points[1])

    def rotate(self, angle_degrees) -> None:
        self.transformation_handler.clear_transformation()
        wcx, wcy = get_object_center(self)
        self.transformation_handler.add_rotation_matrix(wcx, wcy, angle_degrees)
        self.transformation_handler.transform(self)
        self.vector = rotate_vector(self.vector, angle_degrees)

    def update_normalization_matrix(self) -> None:
        cx, cy = get_object_center(self)
        angle_degrees = -1 * angle_between_vector_and_y_axis(self.vector)
        cos = math.cos(math.radians(angle_degrees))
        sin = math.sin(math.radians(angle_degrees))
        sx = 1 / (self.width / 2)
        sy = 1 / (self.height / 2)
        self.normalization_matrix = np.array([[cos*sx, sin*sy, 0],
                                              [-1*sin*sx, cos*sy, 0],
                                              [sx*(cy*sin-cx*cos), -1*sy*(cx*sin+cy*cos), 1]])

    def update_normalized_coordinates(self, graphic_object: GraphicObject) -> None:
        points_list = graphic_object.get_points()
        for point in points_list:
            coordinates_matrix = np.array([point.x, point.y, 1])
            normalized_coordinates_matrix = np.dot(coordinates_matrix, self.normalization_matrix)
            point.nx = normalized_coordinates_matrix[0]
            point.ny = normalized_coordinates_matrix[1]
