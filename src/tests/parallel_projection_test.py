from system.core.window import Window
from system.graphic_objects.object_3d import Object3d
from system.core.projection import Projection

a = [(0, 0, 0), (0, 0, 1)]

window = Window(800, 600, None)
objc = Object3d("", "#000000", a)
obj = Projection.parallel_projection(objc, window)
print(obj.get_points()[1].get_coordinates())
