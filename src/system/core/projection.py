import numpy as np

from system.graphic_objects.object_3d import Object3d
from system.core.window import Window
from system.core.transformation_handler_3d import TransformationHandler3d
from system.graphic_objects.point_3d import Point3d
from utils.math_utils import MathUtils


class Projection:

    @staticmethod
    def parallel_projection(obj: Object3d, window: Window) -> Object3d:
        transformation_handler = TransformationHandler3d(None)
        new_obj = obj.copy()

        rotation_vector = window.vpn
        angle_z = MathUtils.angle_between_vector_and_xz_plane(rotation_vector)
        angle_x = MathUtils.angle_between_vector_and_z_axis(
            MathUtils.rotate_vector_around_z_axis(rotation_vector, angle_z))

        transformation_handler.add_translation_matrix(-window.vrp.x, -window.vrp.y, -window.vrp.z)
        transformation_handler.add_matrix(TransformationHandler3d.get_z_rotation_matrix(angle_z))
        transformation_handler.add_matrix(TransformationHandler3d.get_x_rotation_matrix(angle_x))
        transformation_handler.transform(new_obj)

        return new_obj

    @staticmethod
    def perspective_projection(obj: Object3d, window: Window) -> Object3d:
        transformation_handler = TransformationHandler3d(None)
        new_obj = obj.copy()

        cop = Projection.__get_cop(window, 250)
        rotation_vector = window.vpn
        angle_z = MathUtils.angle_between_vector_and_xz_plane(rotation_vector)
        angle_x = MathUtils.angle_between_vector_and_z_axis(
            MathUtils.rotate_vector_around_z_axis(rotation_vector, angle_z))
        d = MathUtils.distance_between_points_3d(cop, window.vrp)

        transformation_handler.add_translation_matrix(-cop.x, -cop.y, -cop.z)
        transformation_handler.add_matrix(TransformationHandler3d.get_z_rotation_matrix(angle_z))
        transformation_handler.add_matrix(TransformationHandler3d.get_x_rotation_matrix(angle_x))
        transformation_handler.transform(new_obj)

        for point in new_obj.get_points():
            point.x = (d * point.x) / point.z
            point.y = (d * point.y) / point.z

        return new_obj

    @staticmethod
    def __get_cop(window: Window, cop_distance: float) -> Point3d:
        direction_vector = -1 * MathUtils.calculate_unit_vector(window.vpn)
        shift_vector = cop_distance * direction_vector
        x = window.vrp.x + shift_vector[0]
        y = window.vrp.y + shift_vector[1]
        z = window.vrp.z + shift_vector[2]
        return Point3d("cop", "#FFFFFF", x, y, z)
