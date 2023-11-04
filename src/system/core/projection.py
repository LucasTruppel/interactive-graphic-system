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
    def perspective_projection(obj: Object3d, window: Window, cop: Point3d) -> Object3d:
        transformation_handler = TransformationHandler3d(None)
        new_obj = obj.copy()

        rotation_vector = window.vpn
        angle_z = MathUtils.angle_between_vector_and_xz_plane(rotation_vector)
        angle_x = MathUtils.angle_between_vector_and_z_axis(
            MathUtils.rotate_vector_around_z_axis(rotation_vector, angle_z))
        d = MathUtils.distance_between_points_3d(cop, window.vrp)
        M = [[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 1/d, 0]]

        transformation_handler.add_translation_matrix(-cop.x, -cop.y, -cop.z)
        transformation_handler.add_matrix(TransformationHandler3d.get_z_rotation_matrix(angle_z))
        transformation_handler.add_matrix(TransformationHandler3d.get_x_rotation_matrix(angle_x))
        transformation_handler.add_matrix(M)
        transformation_handler.transform(new_obj)

        return new_obj

