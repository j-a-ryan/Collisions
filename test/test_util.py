import math
import unittest
import numpy as np
import numpy.testing as npt

from model.util import convert_minkowski_to_light_cone_coordinates, convert_light_cone_coordinates_to_minkowski_form

# class TestMinkowskiLCC(unittest.TestCase):

        
#     def test_lcc_to_minkowski(self):
#         lcc_vector = [math.sqrt(82), math.sqrt(20.5), 0, 0]
#         mink_vector = convert_light_cone_coordinates_to_minkowski_form(lcc_vector)
#         mink_vec_expected = [1.5 * math.sqrt(41), 0, 0, math.sqrt(41) / 2]
#         npt.assert_allclose(np.array(mink_vector), np.array(mink_vec_expected))

#     def test_minkowski_to_lcc(self):
#         mink_vec = [1.5 * math.sqrt(41), 0, 0, math.sqrt(41) / 2]
#         lcc_vector_expected = [math.sqrt(82), math.sqrt(20.5), 0, 0]
#         lcc_vector = convert_minkowski_to_light_cone_coordinates(mink_vec)
#         npt.assert_allclose(np.array(lcc_vector), np.array(lcc_vector_expected))

#     def test_minkowski_to_lcc_2(self):
#         mink_vec = [10, 1, 4, 1]
#         direct_from_func = convert_minkowski_to_light_cone_coordinates(mink_vec)
#         lcc_vec = [7.7781745930520225, 6.363961030678928, 1, 4]
#         npt.assert_allclose(np.array(direct_from_func), np.array(lcc_vec))