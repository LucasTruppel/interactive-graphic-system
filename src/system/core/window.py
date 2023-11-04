import math
import numpy as np

from gui.logger import Logger
from system.graphic_objects.graphic_object import GraphicObject
from system.graphic_objects.object_3d import Object3d
from system.graphic_objects.point_3d import Point3d
from utils.math_utils import MathUtils
from utils.utils import (rotate_vector, angle_between_vector_and_y_axis, distance_between_points, get_object_center,
                         get_object_center_3d)
from system.core.transformation_handler_3d import TransformationHandler3d


class Window(Object3d):

    def __init__(self, width: float, height: float, logger: Logger) -> None:
        x_min, y_min, x_max, y_max = -width/2, -height/2, width/2, height/2
        super().__init__("window", "#FFFFFF",
                         [(x_min, y_min, 0), (x_min, y_max, 0), (x_max, y_max, 0), (x_max, y_min, 0)])
        self.width = width
        self.height = height
        self.logger = logger
        self.vpn = np.array([0, 0, 1])
        self.vector = np.array([0, 1])
        self.transformation_handler = TransformationHandler3d(None)
        self.normalization_matrix = None
        self.horizontal_rotation_axis = True
        xc, yc, zc = get_object_center_3d(self)
        self.vrp = Point3d("window_center", "#FFFFFF", xc, yc, zc)
        self.__log(f"[Window Initialized] VRP:   x: {xc:.3f}  y: {yc:.3f}  z: {zc:.3f}")
        self.__log(f"[Window Initialized] VPN:   x: {self.vpn[0]:.3f}  y: {self.vpn[1]:.3f}  z: {self.vpn[2]:.3f}")
        self.__log(f"[Window Initialized] Points:   {self.__get_point_list_str()}")

    def move_front(self) -> None:
        shift = 0.2 * self.height
        shift_vector = shift * self.vpn
        self.__move(shift_vector, "front")

    def move_back(self) -> None:
        shift = 0.2 * self.height
        shift_vector = -1 * shift * self.vpn
        self.__move(shift_vector, "back")

    def move_left(self) -> None:
        shift = 0.2 * self.height
        shift_vector = shift * self.__get_side_movement_vector()
        self.__move(shift_vector, "left")

    def move_right(self) -> None:
        shift = 0.2 * self.height
        shift_vector = shift * self.__get_side_movement_vector(True)
        self.__move(shift_vector, "right")

    def __move(self, shift_vector: np.array, direction_str: str) -> None:
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_translation_matrix(float(shift_vector[0]), float(shift_vector[1]),
                                                           float(shift_vector[2]))
        self.transformation_handler.transform(self)
        self.__log(f"[Move {direction_str} window] Shift Vector: {shift_vector}")
        self.__log(f"[Move {direction_str} window] New window points: {self.__get_point_list_str()}")
        self.update_vrp(direction_str)

    def zoom_in(self) -> None:
        self.__zoom(0.8, 0.8, 0.8, "in")

    def zoom_out(self) -> None:
        self.__zoom(1.2, 1.2, 1.2, "out")

    def __zoom(self, sx: float, sy: float, sz: float, zoom_str: str) -> None:
        self.transformation_handler.clear_transformation()
        self.transformation_handler.add_scaling_matrix(self, sx, sy, sz)
        self.transformation_handler.transform(self)
        self.width = MathUtils.distance_between_points_3d(self.points[0], self.points[3])
        self.height = MathUtils.distance_between_points_3d(self.points[0], self.points[1])
        self.__log(f"[Zoom {zoom_str} window] New window points: {self.__get_point_list_str()}")

    def rotate(self, angle_degrees: float, is_horizontal: bool) -> None:
        xc, yc, zc = get_object_center_3d(self)
        self.transformation_handler.clear_transformation()
        self.horizontal_rotation_axis = is_horizontal
        rotation_matrix = self.transformation_handler.add_center_axis_rotation_matrix(self, angle_degrees)
        self.transformation_handler.transform(self)
        self.update_vpn(xc, yc, zc, rotation_matrix)
        self.__log(f"[Rotate window] New window points: {self.__get_point_list_str()}")

    def update_normalization_matrix(self) -> None:
        cx, cy = get_object_center(self)

        point1, point2 = self.points[0], self.points[1]
        v = np.array([point2.x - point1.x, point2.y - point1.y])
        vector = MathUtils.calculate_unit_vector(v)

        angle_degrees = -1 * angle_between_vector_and_y_axis(vector)
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
        xc, yc, zc = get_object_center_3d(self)
        return np.array([x - xc, y - yc, z - zc])

    def update_vrp(self, direction_str: str) -> None:
        x, y, z = get_object_center_3d(self)
        self.vrp = Point3d("window_center", "#FFFFFF", x, y, z)
        self.__log(f"[Move {direction_str} window] New VRP:   x: {x:.3f}  y: {y:.3f}  z: {z:.3f}")

    def update_vpn(self, xc: float, yc: float, zc: float, rotation_matrix: np.array) -> None:
        self.transformation_handler.clear_transformation()
        vector = Object3d("vector", "#FFFFFF",
                          [(xc, yc, zc),
                           (xc + float(self.vpn[0]), yc + float(self.vpn[1]), zc + float(self.vpn[2]))])
        self.transformation_handler.add_matrix(rotation_matrix)
        self.transformation_handler.transform(vector)
        points = vector.get_points()
        x, y, z = points[1].x - points[0].x, points[1].y - points[0].y, points[1].z - points[0].z
        self.vpn = MathUtils.calculate_unit_vector(np.array([x, y, z]))
        self.__log(f"[Rotate window] New VPN:   x: {self.vpn[0]:.3f}  y: {self.vpn[1]:.3f}  z: {self.vpn[2]:.3f}")

    def __log(self, text: str) -> None:
        if self.logger is not None:
            self.logger.log(text)

    def __get_point_list_str(self) -> str:
        list_str = "["
        for point in self.points:
            list_str += f"({point.x:.3f}, {point.y:.3f}, {point.z:.3f}), "
        return list_str[:-2] + "]"
