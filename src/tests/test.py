from system.graphic_objects.b_spline_3d import BSpline3d


curve_coord = [[(0, 0, 0), (33, 50, 0), (66, 50, 0), (100, 0, 0)],
               [(0, 0, 33), (33, 50, 33), (66, 50, 33), (100, 0, 33)],
               [(0, 0, 66), (33, 50, 66), (66, 50, 66), (100, 0, 66)],
               [(0, 0, 100), (33, 50, 100), (66, 50, 100), (100, 0, 100)]]
bs = BSpline3d("", "", curve_coord, 4)
print(bs.points)
