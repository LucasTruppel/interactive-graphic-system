from tkinter import Canvas

import numpy as np

from system.core.window import Window
from system.core.viewport import Viewport
from system.graphic_objects.b_spline_3d import BSpline3d
from system.graphic_objects.bezier_curve_3d import BezierCurve3d
from system.graphic_objects.graphic_object import GraphicObjectType, GraphicObject3d
from system.graphic_objects.line import *
from system.graphic_objects.wireframe import Wireframe
from system.graphic_objects.bezier_curve import BezierCurve
from system.graphic_objects.b_spline import BSpline
from system.graphic_objects.point_3d import Point3d
from system.graphic_objects.object_3d import Object3d
from system.core.projection import Projection
from system.core.transformation_handler import TransformationHandler
from system.core.transformation_handler_3d import TransformationHandler3d
from gui.widgets.logger import Logger
from system.obj_file.obj_transcriber import ObjTranscriber
from system.obj_file.obj_reader import ObjReader
from utils.utils import get_object_center
from system.clipping.point_clipping import PointClipping
from system.clipping.cohen_sutherland import CohenSutherland
from system.clipping.liang_barsky import LiangBarsky
from system.clipping.sutherland_hodgman import SutherlandHodgman
from system.core.system_state import *


class GraphicSystem:

    def __init__(self, width: float, height: float, viewport_canvas: Canvas, logger: Logger) -> None:
        self.display_file: list[GraphicObject] = []
        self.window = Window(width - 20, height - 20, logger)
        self.viewport = Viewport(0, 0, width - 20, height - 20, viewport_canvas)
        self.viewport_canvas = viewport_canvas
        self.transformation_handler = TransformationHandler(logger)
        self.transformation_handler_3d = TransformationHandler3d(logger)
        self.logger = logger
        self.point_clipping_state = PointClippingState.ENABLED
        self.line_clipping_state = LineClippingState.COHEN_SUTHERLAND
        self.polygon_clipping_state = PolygonClippingState.SUTHERLAND_HODGMAN
        self.projection_state = ProjectionState.PERSPECTIVE
        self.cop = Point3d("cop", "#FFFFFF", 0, 0, -250)

        # self.test()

    def draw_display_file(self) -> None:
        self.window.update_normalization_matrix()
        self.viewport.clear()
        for obj in self.display_file:
            if obj.is_3d:
                obj, draw = self.project(obj)
                if not draw:
                    continue
            self.window.update_normalized_coordinates(obj)
            match obj.__class__.__name__:
                case Point.__name__:
                    self.draw_point(obj)
                case Line.__name__:
                    self.draw_line(obj)
                case Wireframe.__name__:
                    self.draw_wireframe(obj)
                case BezierCurve.__name__:
                    self.draw_curve(obj)
                case BSpline.__name__:
                    self.draw_curve(obj)
                case Point3d.__name__:
                    self.draw_point(obj)
                case Object3d.__name__:
                    self.draw_object3d(obj)
                case BezierCurve3d.__name__:
                    self.draw_curve3d(obj)
                case BSpline3d.__name__:
                    self.draw_curve3d(obj)
        self.viewport.update()

    def project(self, obj: GraphicObject3d) -> tuple[GraphicObject3d, bool]:
        if self.projection_state == ProjectionState.PARALLEL:
            return Projection.parallel_projection(obj, self.window), True
        else:
            new_obj = Projection.perspective_projection(obj, self.window)
            draw = True
            for point in new_obj.get_points():
                if point.z < 0:
                    draw = False
                    break
            return new_obj, draw

    def draw_point(self, obj: GraphicObject) -> None:
        if self.point_clipping_state == PointClippingState.ENABLED:
            if PointClipping.point_clipping(obj):
                self.viewport.draw_point(obj)
        else:
            self.viewport.draw_point(obj)

    def draw_line(self, obj: GraphicObject) -> None:
        if self.line_clipping_state == LineClippingState.COHEN_SUTHERLAND:
            if CohenSutherland.line_clipping(obj):
                self.viewport.draw_line(obj)
        elif self.line_clipping_state == LineClippingState.LIANG_BARSKY:
            if LiangBarsky.line_clipping(obj):
                self.viewport.draw_line(obj)
        else:
            self.viewport.draw_line(obj)

    def draw_wireframe(self, obj: GraphicObject) -> None:
        if self.polygon_clipping_state == PolygonClippingState.SUTHERLAND_HODGMAN:
            draw, new_obj = SutherlandHodgman.polygon_clipping(obj)
            if draw:
                self.viewport.draw_wireframe(new_obj)
        else:
            self.viewport.draw_wireframe(obj)

    def draw_curve(self, obj: GraphicObject) -> None:
        clipping_on = self.line_clipping_state != LineClippingState.DISABLED
        self.viewport.draw_curve(obj, clipping_on)

    def draw_object3d(self, obj: Object3d) -> None:
        clipping_on = self.line_clipping_state != LineClippingState.DISABLED
        self.viewport.draw_object3d(obj, clipping_on)

    def draw_curve3d(self, obj: Object3d) -> None:
        clipping_on = self.line_clipping_state != LineClippingState.DISABLED
        self.viewport.draw_curve3d(obj, clipping_on)

    def move_front(self) -> None:
        self.window.move_front()
        self.draw_display_file()

    def move_back(self) -> None:
        self.window.move_back()
        self.draw_display_file()

    def move_left(self) -> None:
        self.window.move_left()
        self.draw_display_file()

    def move_right(self) -> None:
        self.window.move_right()
        self.draw_display_file()

    def move_up(self) -> None:
        self.window.move_up()
        self.draw_display_file()

    def move_down(self) -> None:
        self.window.move_down()
        self.draw_display_file()

    def zoom_in(self) -> None:
        self.window.zoom_in()
        self.draw_display_file()

    def zoom_out(self) -> None:
        self.window.zoom_out()
        self.draw_display_file()

    def create_shape(self, points_list: list, name: str, color: str, fill: bool,
                     object_type: str) -> None:
        match object_type:
            case GraphicObjectType.POINT:
                x, y = points_list[0]
                self.display_file.append(Point(name, color, x, y))
            case GraphicObjectType.LINE:
                x1, y1 = points_list[0]
                x2, y2 = points_list[1]
                self.display_file.append(Line(name, color, x1, y1, x2, y2))
            case GraphicObjectType.POLYGON:
                self.display_file.append(Wireframe(name, color, fill, points_list))
            case GraphicObjectType.BEZIER_CURVE:
                self.display_file.append(BezierCurve(name, color, points_list))
            case GraphicObjectType.B_SPLINE_CURVE:
                self.display_file.append(BSpline(name, color, points_list))
            case GraphicObjectType.POINT_3D:
                x, y, z = points_list[0]
                self.display_file.append(Point3d(name, color, x, y, z))
            case GraphicObjectType.OBJECT_3D:
                self.display_file.append(Object3d(name, color, points_list))
            case GraphicObjectType.BEZIER_CURVE_3D:
                self.display_file.append(BezierCurve3d(name, color, points_list))
            case GraphicObjectType.B_SPLINE_CURVE_3D:
                self.display_file.append(BSpline3d(name, color, points_list[0]))

        self.draw_display_file()

    def remove_shape(self, pos: int) -> str:
        name = self.display_file[pos].name
        self.display_file.pop(pos)
        self.draw_display_file()
        return name

    def add_translation(self, dx: float, dy: float, dz=float("inf")) -> None:
        if dz == float("inf"):
            self.transformation_handler.add_translation_matrix(dx, dy)
        else:
            self.transformation_handler_3d.add_translation_matrix(dx, dy, dz)

    def add_scaling(self, object_index: int, sx: float, sy: float, sz=float("inf")) -> None:
        if sz == float("inf"):
            self.transformation_handler.add_scaling_matrix(self.display_file[object_index], sx, sy)
        else:
            self.transformation_handler_3d.add_scaling_matrix(self.display_file[object_index], sx, sy, sz)

    def add_rotation(self, x: float, y: float, angle: float, rotation_type: str, object_index: int) -> None:
        if rotation_type == "object_center":
            x, y = get_object_center(self.display_file[object_index])
        self.transformation_handler.add_rotation_matrix(x, y, angle)

    def add_rotation3d(self, angle: float, rotation_type: str, object_index: int) -> None:
        obj = self.display_file[object_index]
        if rotation_type == "x_axis":
            self.transformation_handler_3d.add_x_rotation_matrix(angle)
        elif rotation_type == "y_axis":
            self.transformation_handler_3d.add_y_rotation_matrix(angle)
        elif rotation_type == "z_axis":
            self.transformation_handler_3d.add_z_rotation_matrix(angle)
        else:
            self.transformation_handler_3d.add_center_axis_rotation_matrix(obj, angle)

    def add_arbitrary_rotation3d(self, angle: float, x1: float, y1: float, z1: float,
                                 x2: float, y2: float, z2: float):
        axis_vector = np.array([x2 - x1, y2 - y1, z2 - z1])
        self.transformation_handler_3d.add_arbitrary_axis_rotation_matrix(x1, y1, z1, axis_vector, angle)

    def remove_operation(self, operation_index: int, object_index: int) -> None:
        obj = self.display_file[object_index]
        if obj.is_3d:
            self.transformation_handler_3d.remove_operation(operation_index)
        else:
            self.transformation_handler.remove_operation(operation_index)
        self.draw_display_file()

    def transform(self, object_index: int) -> None:
        obj = self.display_file[object_index]
        if obj.is_3d:
            self.transformation_handler_3d.transform(obj)
        else:
            self.transformation_handler.transform(obj)
        self.draw_display_file()

    def clear_transformation(self, is_3d=False) -> None:
        if is_3d:
            self.transformation_handler_3d.clear_transformation()
        else:
            self.transformation_handler.clear_transformation()

    def rotate_window(self, angle: float, is_horizontal: bool) -> None:
        self.window.rotate(angle, is_horizontal)
        self.draw_display_file()

    def import_obj(self, file_path: str) -> list[str]:
        obj_reader = ObjReader(file_path)
        new_objects_list = obj_reader.read(self.display_file, self.window)
        self.draw_display_file()
        return list(map(lambda graphic_object: graphic_object.name, new_objects_list))

    def export_obj(self, file_path: str) -> None:
        obj_transcriber = ObjTranscriber(file_path)
        obj_transcriber.transcribre(self.display_file, self.window)

    def configure_clipping(self, point_clipping: int, line_clipping: int, polygon_clipping: int) -> None:
        self.point_clipping_state = PointClippingState(point_clipping)
        self.line_clipping_state = LineClippingState(line_clipping)
        self.polygon_clipping_state = PolygonClippingState(polygon_clipping)
        self.draw_display_file()

    def configure_projection(self, projection: int) -> None:
        self.projection_state = ProjectionState(projection)
        self.draw_display_file()

    def test(self):
        curve_coord = [[[(0, 0, 0), (33, 50, 0), (66, 50, 0), (100, 0, 0)],
                       [(0, 0, 33), (33, 50, 33), (66, 50, 33), (100, 0, 33)],
                       [(0, 0, 66), (33, 50, 66), (66, 50, 66), (100, 0, 66)],
                       [(0, 0, 100), (33, 50, 100), (66, 50, 100), (100, 0, 100)]]]
        curve_coord2 = \
            [[(0, 0, 0), (33, 50, 0), (66, 50, 0), (100, 100, 0), (133, 100, 0), (166, 50, 0), (200, 50, 0),
              (233, 0, 0)],
             [(0, 0, 33), (33, 50, 33), (66, 50, 33), (100, 100, 33), (133, 100, 33), (166, 50, 33), (200, 50, 33),
              (233, 0, 33)],
             [(0, 0, 66), (33, 50, 66), (66, 50, 66), (100, 100, 66), (133, 100, 66), (166, 50, 66), (200, 50, 66),
              (233, 0, 66)],
             [(0, 0, 100), (33, 50, 100), (66, 50, 100), (100, 100, 100), (133, 100, 100), (166, 50, 100),
              (200, 50, 100), (233, 0, 100)],
             [(0, 0, 133), (33, 50, 133), (66, 50, 133), (100, 100, 133), (133, 100, 133), (166, 50, 133),
              (200, 50, 133), (233, 0, 133)],
             [(0, 0, 166), (33, 50, 166), (66, 50, 166), (100, 100, 166), (133, 100, 166), (166, 50, 166),
              (200, 50, 166), (233, 0, 166)],
             [(0, 0, 200), (33, 50, 200), (66, 50, 200), (100, 100, 200), (133, 100, 200), (166, 50, 200),
              (200, 50, 200), (233, 0, 200)],
             [(0, 0, 233), (33, 50, 233), (66, 50, 233), (100, 100, 233), (133, 100, 233), (166, 50, 233),
              (200, 50, 233), (233, 0, 233)],
             ]
        cube_coords = [
            (0, 0, 0), (0, 100, 0),
            (0, 100, 0), (100, 100, 0),
            (100, 100, 0), (100, 0, 0),
            (100, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 100),
            (100, 0, 0), (100, 0, 100),
            (100, 100, 0), (100, 100, 100),
            (0, 100, 0), (0, 100, 100),
            (0, 0, 100), (0, 100, 100),
            (0, 100, 100), (100, 100, 100),
            (100, 100, 100), (100, 0, 100),
            (100, 0, 100), (0, 0, 100),
        ]
        x_axis_cords = [(0, 0, 0), (1000, 0, 0)]
        y_axis_cords = [(0, 0, 0), (0, 1000, 0)]
        z_axis_cords = [(0, 0, 0), (0, 0, 1000)]
        self.display_file.append(BSpline3d("", "#000000", curve_coord2))
        self.display_file.append(Object3d("", "#000000", cube_coords))
        self.display_file.append(BezierCurve3d("", "#000000", curve_coord))
        self.display_file.append(Object3d("", "#000000", x_axis_cords))
        self.display_file.append(Object3d("", "#000000", y_axis_cords))
        self.display_file.append(Object3d("", "#000000", z_axis_cords))
        self.display_file.append(Point3d("", "#000000", 1000, 1000, 0))
        self.draw_display_file()
