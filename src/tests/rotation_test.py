from system.core.transformation_handler_3d import TransformationHandler3d
from system.graphic_objects.object_3d import Object3d


points = [(1, 1, 1),
          (1, 1, -1),
          (1, -1, 1),
          (1, -1, -1),
          (-1, 1, 1),
          (-1, 1, -1),
          (-1, -1, 1),
          (-1, -1, -1)]
# points = [(3, 2, 4), (3, 6, 6), (-2, 3, 3), (-3, -5, -3), (-5, 10, 37)]

for i in range(len(points)):
    a = [(0, 0, 0), points[i]]
    objc = Object3d("", "#000000", a)
    th = TransformationHandler3d(None)

    th.add_arbitrary_rotation_matrix(objc, 45)
    th.transform(objc)

    point = objc.get_points()[1]
    print(point.x, point.y, point.z)
    print(round(point.x), round(point.y), round(point.z))
    print(points[i][0], points[i][1], points[i][2])
    print((round(point.x), round(point.y), round(point.z)) == (points[i][0], points[i][1], points[i][2]))
    print()
