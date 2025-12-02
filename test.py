from model.transformation import galilean_coordinate_transform1, galilean_coordinate_transform2, galilean_coordinate_transformation_3, galilean_coordinate_transformation_3_vector, galilean_coordinate_transformation_4
import numpy as np

from_vector = [1, 0, 0, 0]
to_vector = [1, 1, 1, 1]

print("These should be the same:")
print(galilean_coordinate_transformation_3(to_vector, from_vector))
print(galilean_coordinate_transformation_4(to_vector, from_vector))
# print(galilean_coordinate_transform1(to_vector, from_vector))
# print(galilean_coordinate_transform2(to_vector, from_vector))

tup = (2, 3, 4)
print(np.array(tup))
print(np.array(tup) @ np.array(tup))

print(galilean_coordinate_transformation_4([1, 1, 2, 3], [1, 1, 2, 3]))

print("Do our vectors:")
v1 = [3, 4, 5]
v2 = [5, 3, 3]
print(galilean_coordinate_transformation_3_vector(v1, v2))