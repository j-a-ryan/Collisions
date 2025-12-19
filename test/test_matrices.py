import math
import unittest

import numpy as np
import numpy.testing as npt
from model.four_vector_matrix import GalileanTransformationMatrix, IdentityMatrix, MatrixConfigurationData
from model.general_matrix import GeneralTransformationMatrix
from model.qcd_matrix import LightConeRapidityMatrix, LightConeRapidityMatrixConfigurationData
from model.util import convert_minkowski_to_light_cone_coordinates
from test.util import check_vectors_equal
# python -m unittest discover tests
# or just
# python -m unittest

class TestIdentityMatrix(unittest.TestCase):
    def test_basic_case(self):
        matrix = IdentityMatrix(None)
        vector = [7, 3, 6, 11]
        transformed_vector = matrix.transform(vector)
        self.assertTrue(check_vectors_equal(vector, transformed_vector))

class TestGalileanTransformationMatrix(unittest.TestCase):
    def test_same_location(self):
        matrix_configuration_data = MatrixConfigurationData()
        matrix_configuration_data.rest_frame_vector = [7, 3, 6, 11]
        matrix = GalileanTransformationMatrix(matrix_configuration_data)
        vector = [7, 3, 6, 11]
        correctly_transformed_vector = [7, 0, 0, 0]
        transformed_vector = matrix.transform(vector)
        self.assertTrue(np.array_equal(np.array(correctly_transformed_vector), np.array(transformed_vector)))
    
    def test_basic_case(self):
        matrix_configuration_data = MatrixConfigurationData()
        matrix_configuration_data.rest_frame_vector = [7, 4, 1, 11]
        matrix = GalileanTransformationMatrix(matrix_configuration_data)
        vector = [7, 3, 6, 6]
        correctly_transformed_vector = [7, -1, 5, -5]
        transformed_vector = matrix.transform(vector)
        self.assertTrue(np.array_equal(np.array(correctly_transformed_vector), np.array(transformed_vector)))
        
# class TestGeneralTransformationMatrix(unittest.TestCase):
#     def test_same_location(self):
#         matrix_configuration_data = MatrixConfigurationData()
#         matrix_configuration_data.rest_frame_vector = [10, 3, 1, 1]
#         matrix = GeneralTransformationMatrix(matrix_configuration_data)
#         vector = [10, 2, 1, 0]
#         correctly_transformed_vector = [10, 0, 0, 0]
#         transformed_vector = matrix.transform(vector)
#         print(transformed_vector)
#         self.assertTrue(np.array_equal(np.array(correctly_transformed_vector), np.array(transformed_vector)))

class TestLightConeRapidityMatrix(unittest.TestCase):

    def set_up_config_data(self, vector_V, vector_Y, exp_2yT, return_vector_in_minkowski_form, convert_incoming_vector_to_lcc=True):
        matrix_configuration_data = LightConeRapidityMatrixConfigurationData()
        matrix_configuration_data.rest_frame_vector = vector_V
        matrix_configuration_data.vector_to_be_transformed = vector_Y
        matrix_configuration_data.convert_incoming_vector_to_lcc = convert_incoming_vector_to_lcc
        matrix_configuration_data.return_vector_in_minkowski_form = return_vector_in_minkowski_form
        matrix_configuration_data.exp_2yT = exp_2yT
        return matrix_configuration_data
    
    def test_basic_case_minkowski_in_mink_out(self):
        # PASSES
        vector_V = [10, 1, 4, 1] # This will be rest frame?
        vector_Y = [7, 1, 0, 5]
        matrix_configuration_data = self.set_up_config_data(vector_V, vector_Y, 2, True)

        correctly_transformed_vector_V_minkowski = [3 * math.sqrt(41)/2, 0, 0, math.sqrt(41)/2]
        matrix = LightConeRapidityMatrix(matrix_configuration_data)
        transformed_vector_V_mink = matrix.transform(vector_V)
        npt.assert_allclose(np.array(transformed_vector_V_mink), np.array(correctly_transformed_vector_V_minkowski), atol=1e-07)

    def test_basic_case_minkowski_in_lcc_out_plus_reconfig_to_mink_out(self):
        # PASSES
        vector_V = [10, 1, 4, 1] # This will be rest frame?
        vector_Y = [7, 1, 0, 5]
        matrix_configuration_data = self.set_up_config_data(vector_V, vector_Y, 2, False)

        correctly_transformed_vector_V_lcc = [math.sqrt(82), math.sqrt(20.5), 0, 0]
        matrix = LightConeRapidityMatrix(matrix_configuration_data)
        transformed_vector_V_lcc = matrix.transform(vector_V)
        npt.assert_allclose(np.array(transformed_vector_V_lcc), np.array(correctly_transformed_vector_V_lcc), atol=1e-07)

        # Test the reuse of the config data object here, with its being reset to
        # return_vector_in_minkowski_form = True
        matrix_configuration_data.return_vector_in_minkowski_form = True
        matrix = LightConeRapidityMatrix(matrix_configuration_data)
        transformed_vector_V_mink = matrix.transform(vector_V)
        correctly_transformed_vector_V_minkowski = [3 * math.sqrt(41)/2, 0, 0, math.sqrt(41)/2]
        npt.assert_allclose(np.array(transformed_vector_V_mink), np.array(correctly_transformed_vector_V_minkowski), atol=1e-07)

    def test_basic_case_minkowski_Y_vec_lcc_out(self):
        vector_V = [10, 1, 4, 1]
        vector_Y = [7, 1, 0, 5]
        matrix_configuration_data = self.set_up_config_data(vector_V, vector_Y, 2, False)
        
        matrix = LightConeRapidityMatrix(matrix_configuration_data)
        transformed_vector_Y_lcc = matrix.transform(vector_Y)
        correctly_transformed_vector_Y_lcc = [math.sqrt((2169 - 704 * math.sqrt(2)) / 41), math.sqrt(2169 / 164 + 176 * math.sqrt(2) / 41), -2 * math.sqrt(6), 0]
        npt.assert_allclose(np.array(transformed_vector_Y_lcc), np.array(correctly_transformed_vector_Y_lcc), atol=1e-07)

        # Test Minkowski output via reconfiguration.
        matrix_configuration_data.return_vector_in_minkowski_form = True # Testing the setting back once again to True
        matrix = LightConeRapidityMatrix(matrix_configuration_data)
        transformed_vector_Y_mink = matrix.transform(vector_Y)
        correctly_transformed_vector_Y_mink = [(2 * math.sqrt(2169 - 704 * math.sqrt(2)) + math.sqrt(2169 + 704 * math.sqrt(2))) / (2 * math.sqrt(82)), -2 * math.sqrt(6), 0, math.sqrt((2169 - 704 * math.sqrt(2)) / 82) - 0.5 * math.sqrt((2169 + 704 * math.sqrt(2)) / 82)]
        npt.assert_allclose(np.array(transformed_vector_Y_mink), np.array(correctly_transformed_vector_Y_mink), atol=1e-07)

    def test_basic_case_minkowski_Y_vec_mink_out(self):
        vector_V = [10, 1, 4, 1] # This will be rest frame?
        vector_Y = [7, 1, 0, 5]
        matrix_configuration_data = self.set_up_config_data(vector_V, vector_Y, 2, True)
        
        matrix = LightConeRapidityMatrix(matrix_configuration_data)
        transformed_vector_Y_lcc = matrix.transform(vector_Y)
        correctly_transformed_vector_Y_mink = [(2 * math.sqrt(2169 - 704 * math.sqrt(2)) + math.sqrt(2169 + 704 * math.sqrt(2))) / (2 * math.sqrt(82)), -2 * math.sqrt(6), 0, math.sqrt((2169 - 704 * math.sqrt(2)) / 82) - 0.5 * math.sqrt((2169 + 704 * math.sqrt(2)) / 82)]
        npt.assert_allclose(np.array(transformed_vector_Y_lcc), np.array(correctly_transformed_vector_Y_mink), atol=1e-07)

    def test_basic_case_2_minkowski_in_lcc_out(self):
        
        vector_V = [11, 2, 14, 1] # This will be rest frame?
        vector_Y = [6, 1, 3, 5]
        matrix_configuration_data = self.set_up_config_data(vector_V, vector_Y, 2, False)

        correctly_transformed_vector_V_lcc = [4 * math.sqrt(5), -2 * math.sqrt(5), 0, 0]
        matrix = LightConeRapidityMatrix(matrix_configuration_data)
        transformed_vector_V_lcc = matrix.transform(vector_V)
        npt.assert_allclose(np.array(transformed_vector_V_lcc), np.array(correctly_transformed_vector_V_lcc), atol=1e-07)
    
    def test_basic_case_2_minkowski_in_mink_out(self):
        
        vector_V = [11, 2, 14, 1] 
        vector_Y = [6, 1, 3, 5]
        matrix_configuration_data = self.set_up_config_data(vector_V, vector_Y, 2, True)

        correctly_transformed_vector_V_mink = [math.sqrt(10), 0, 0, 3 * math.sqrt(10)]
        matrix = LightConeRapidityMatrix(matrix_configuration_data)
        transformed_vector_V_mink = matrix.transform(vector_V)
        npt.assert_allclose(np.array(transformed_vector_V_mink), np.array(correctly_transformed_vector_V_mink), atol=1e-07)

    def test_basic_case_3_minkowski_in_lcc_out(self):
        
        vector_V = [3, 1, 2, 16] # This will be rest frame?
        vector_Y = [3, 5, 2, 4]
        matrix_configuration_data = self.set_up_config_data(vector_V, vector_Y, 3, False)

        correctly_transformed_vector_V_lcc = [3 * math.sqrt(42), -math.sqrt(42), 0, 0]
        matrix = LightConeRapidityMatrix(matrix_configuration_data)
        transformed_vector_V_lcc = matrix.transform(vector_V)
        npt.assert_allclose(np.array(transformed_vector_V_lcc), np.array(correctly_transformed_vector_V_lcc), atol=1e-07)
    
    def test_basic_case_3_minkowski_in_mink_out(self):
        
        vector_V = [3, 1, 2, 16]
        vector_Y = [3, 5, 2, 4]
        matrix_configuration_data = self.set_up_config_data(vector_V, vector_Y, 3, True)

        correctly_transformed_vector_V_mink = [2 * math.sqrt(21), 0, 0, 4 * math.sqrt(21)]
        matrix = LightConeRapidityMatrix(matrix_configuration_data)
        transformed_vector_V_mink = matrix.transform(vector_V)
        npt.assert_allclose(np.array(transformed_vector_V_mink), np.array(correctly_transformed_vector_V_mink), atol=1e-07)


if __name__ == '__main__':
    unittest.main()
