import numpy as np

from system.graphic_objects.object_3d import Object3d
from system.core.window import Window
from system.core.transformation_handler_3d import TransformationHandler3d
from utils.math_utils import MathUtils


class ParallelProjection:

    @staticmethod
    def project_object(obj: Object3d, window: Window) -> Object3d:
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
