import math
import numpy as np

from system.graphic_objects.graphic_object import GraphicObject
from system.graphic_objects.object_3d import Object3d
from system.graphic_objects.point_3d import Point3d
from utils.math_utils import MathUtils
from utils.utils import (rotate_vector, angle_between_vector_and_y_axis, distance_between_points, get_object_center,
                         get_object_center_3d)
from system.core.transformation_handler_3d import TransformationHandler3d
from gui.logger import Logger


class Window(Object3d):

    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float) -> None:
        super().__init__("window", "#FFFFFF",
                         [(x_min, y_min, 0), (x_min, y_max, 0), (x_max, y_max, 0), (x_max, y_min, 0)])
        self.width = x_max - x_min
        self.height = y_max - y_min
        self.vpn = np.array([0, 0, 1])
        self.vector = np.array([0, 1])
        self.transformation_handler = TransformationHandler3d(None)
        self.normalization_matrix = None
        self.horizontal_rotation_axis = True
        xc, yc, zc = get_object_center_3d(self)
        self.vrp = Point3d("window_center", "#FFFFFF", xc, yc, zc)

    def move_up(self) -> None:
        shift = 0.2 * self.height
        shift_vector = shift * self.vpn
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_translation_matrix(float(shift_vector[0]), float(shift_vector[1]),
                                                           float(shift_vector[2]))
        self.transformation_handler.transform(self)
        self.update_vrp()

    def move_down(self) -> None:
        shift = 0.2 * self.height
        shift_vector = -1 * shift * self.vpn
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_translation_matrix(float(shift_vector[0]), float(shift_vector[1]),
                                                           float(shift_vector[2]))
        self.transformation_handler.transform(self)
        self.update_vrp()

    def move_left(self) -> None:
        shift = 0.2 * self.height
        shift_vector = shift * self.__get_side_movement_vector()
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_translation_matrix(float(shift_vector[0]), float(shift_vector[1]),
                                                           float(shift_vector[2]))
        self.transformation_handler.transform(self)
        self.update_vrp()

    def move_right(self) -> None:
        shift = 0.2 * self.height
        shift_vector = shift * self.__get_side_movement_vector(True)
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_translation_matrix(float(shift_vector[0]), float(shift_vector[1]),
                                                           float(shift_vector[2]))
        self.transformation_handler.transform(self)
        self.update_vrp()

    def zoom_in(self) -> None:
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_scaling_matrix(self, 0.8, 0.8, 0.8)
        self.transformation_handler.transform(self)
        self.width = MathUtils.distance_between_points_3d(self.points[0], self.points[3])
        self.height = MathUtils.distance_between_points_3d(self.points[0], self.points[1])

    def zoom_out(self) -> None:
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_scaling_matrix(self, 1.2, 1.2, 1.2)
        self.transformation_handler.transform(self)
        self.width = MathUtils.distance_between_points_3d(self.points[0], self.points[3])
        self.height = MathUtils.distance_between_points_3d(self.points[0], self.points[1])

    def rotate(self, angle_degrees: float, is_horizontal=True) -> None:
        xc, yc, zc = get_object_center_3d(self)
        self.transformation_handler.clear_transformation()
        self.horizontal_rotation_axis = is_horizontal
        rotation_matrix = self.transformation_handler.add_rotation_matrix(self, angle_degrees)
        self.transformation_handler.transform(self)
        self.update_vpn(xc, yc, zc, rotation_matrix)

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

    def __get_side_movement_vector(self, is_right=False) -> np.array:
        point1 = self.points[3] if is_right else self.points[0]
        point2 = self.points[2] if is_right else self.points[1]
        xlmp, ylmp, zlmp = MathUtils.get_middle_point(point1, point2)
        xc, yc, zc = get_object_center_3d(self)
        vector = np.array([xlmp - xc, ylmp - yc, zlmp - zc])
        return MathUtils.calculate_unit_vector(vector)

    def get_rotation_axis_point(self) -> tuple[float, float, float]:
        x, y, z = get_object_center_3d(self)
        return x, y, z

    def get_rotation_vector(self) -> np.array:
        if self.horizontal_rotation_axis:
            x, y, z = MathUtils.get_middle_point(self.points[3], self.points[2])
        else:
            x, y, z = MathUtils.get_middle_point(self.points[1], self.points[2])
        x, y, z = self.points[0].get_coordinates()
        xc, yc, zc = get_object_center_3d(self)
        return np.array([x - xc, y - yc, z - zc])

    def update_vrp(self):
        x, y, z = get_object_center_3d(self)
        self.vrp = Point3d("window_center", "#FFFFFF", x, y, z)

    def update_vpn(self, xc, yc, zc, rotation_matrix):
        self.transformation_handler.clear_transformation()
        vector = Object3d("vector", "#FFFFFF",
                          [(xc, yc, zc),
                           (xc + float(self.vpn[0]), float(yc + self.vpn[1]), float(zc + self.vpn[2]))])
        self.transformation_handler.add_matrix(rotation_matrix)
        self.transformation_handler.transform(vector)
        points = vector.get_points()
        x, y, z = points[1].x - points[0].x, points[1].y - points[0].y, points[1].z - points[0].z
        self.vpn = MathUtils.calculate_unit_vector(np.array([x, y, z]))
