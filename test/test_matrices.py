import math
import unittest

import numpy as np
from model.four_vector_matrix import GalileanTransformationMatrix, IdentityMatrix, MatrixConfigurationData
from model.general_matrix import GeneralTransformationMatrix
from model.qcd_matrix import LightConeRapidityMatrix
# python -m unittest discover tests
# or just
# python -m unittest

def check_vectors_equal(vector_a, vector_b):
    return np.array_equal(np.array(vector_a), np.array(vector_b))

class TestIdentityMatrix(unittest.TestCase):
    def test_basic_case(self):
        matrix = IdentityMatrix(None)
        vector = [7, 3, 6, 11]
        transformed_vector = matrix.transform(vector)
        self.assertTrue(check_vectors_equal(vector, transformed_vector))

# class TestGalileanTransformationMatrix(unittest.TestCase):
#     def test_same_location(self):
#         matrix_configuration_data = MatrixConfigurationData()
#         matrix_configuration_data.set_rest_frame_vector([7, 3, 6, 11])
#         matrix = GalileanTransformationMatrix(matrix_configuration_data)
#         vector = [7, 3, 6, 11]
#         correctly_transformed_vector = [7, 0, 0, 0]
#         transformed_vector = matrix.transform(vector)
#         self.assertTrue(np.array_equal(np.array(correctly_transformed_vector), np.array(transformed_vector)))
    
#     def test_basic_case(self):
#         matrix_configuration_data = MatrixConfigurationData()
#         matrix_configuration_data.set_rest_frame_vector([7, 4, 1, 11])
#         matrix = GalileanTransformationMatrix(matrix_configuration_data)
#         vector = [7, 3, 6, 6]
#         correctly_transformed_vector = [7, -1, 5, -5]
#         transformed_vector = matrix.transform(vector)
#         self.assertTrue(np.array_equal(np.array(correctly_transformed_vector), np.array(transformed_vector)))
        
# class TestGeneralTransformationMatrix(unittest.TestCase):
#     def test_same_location(self):
#         matrix_configuration_data = MatrixConfigurationData()
#         matrix_configuration_data.set_rest_frame_vector([10, 3, 1, 1])
#         matrix = GeneralTransformationMatrix(matrix_configuration_data)
#         vector = [10, 2, 1, 0]
#         correctly_transformed_vector = [10, 0, 0, 0]
#         transformed_vector = matrix.transform(vector)
#         print(transformed_vector)
#         self.assertTrue(np.array_equal(np.array(correctly_transformed_vector), np.array(transformed_vector)))

# class TestLightConeRapidityMatrix(unittest.TestCase):
    # def test_basic_case(self):
    #     A = 2
    #     matrix = LightConeRapidityMatrix(None)
    #     matrix = LightConeRapidityMatrix()
    #     vector_V = [10, 1, 4, 1] # This will be rest frame.
    #     vector_Y = [7, 1, 0, 5]
    #     correctly_transformed_vector_V = [3 * math.sqrt(41)/2, 0, 0, math.sqrt(41)/2] #
    #     correctly_transformed_vector_Y = [1, 0, 0, 0]
    #     transformed_vector_V = matrix.transform(vector_V)
    #     transformed_vector_Y = matrix.transform(vector_Y)
    #     # self.assertTrue(np.array_equal(np.array(vector), np.array(transformed_vector)))
    #     self.fail()
    
    # def test_basic_case_2(self):
    #     matrix = LightConeRapidityMatrix(None)
    #     matrix = LightConeRapidityMatrix()
    #     vector = [7, 3, 6, 11]
    #     # correctly_transformed_vector = [?, ?, ?, ?]
    #     transformed_vector = matrix.transform(vector)
    #     # self.assertTrue(np.array_equal(np.array(vector), np.array(transformed_vector)))
    #     self.fail()
    
    # def test_basic_case_3(self):
    #     matrix = LightConeRapidityMatrix(None)
    #     vector = [7, 3, 6, 11]
    #     correctly_transformed_vector = []
    #     transformed_vector = matrix.transform(vector)
    #     # self.assertTrue(np.array_equal(np.array(vector), np.array(transformed_vector)))
    #     self.fail()


if __name__ == '__main__':
    unittest.main()
