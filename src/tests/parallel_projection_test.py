from system.core.window import Window
from system.graphic_objects.object_3d import Object3d
from system.core.parallel_projection import ParallelProjection

a = [(0, 0, 0), (0, 0, 1)]

window = Window(0, 0, 800, 600)
objc = Object3d("", "#000000", a)
obj = ParallelProjection.project_object(objc, window)
print(obj.get_points()[1].get_coordinates())
