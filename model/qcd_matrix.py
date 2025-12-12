

import math
from model.four_vector_matrix import FourVectorTransformationMatrix, MatrixConfigurationData

"""
This matrix is used by QCD physicists at Old Dominion University. It may fairly standard or somewhat
idiosyncratic to ODU physicists. It is fraught with layers of arithmetical calculations and variables
wrapping variables. These aren't difficult calculations but the code is not easy to read. Developers 
wishing to make any surgical changes will probably want to consult the document of the matrix in the 
dev docs folder.

The subclass of MatrixConfigurationData here uses dotting for its pecular variables.
"""

class LightConeRapidityMatrix(FourVectorTransformationMatrix):
    def __init__(self, matrix_configuration_data: MatrixConfigurationData):
        super().__init__(matrix_configuration_data)

    def _set_member_values(self, matrix_configuration_data: MatrixConfigurationData):
        delta = matrix_configuration_data.delta
        R_plus = matrix_configuration_data.R_plus
        R_minus = matrix_configuration_data.R_minus
        rest_frame_vector_xyz = self.rest_frame_vector_xyz_magnitude
        rest_frame_vector_xz = self.rest_frame_vector_xz_magnitude
        rest_frame_vector_x = matrix_configuration_data.get_rest_frame_vector()[1]
        rest_frame_vector_y = matrix_configuration_data.get_rest_frame_vector()[2]
        rest_frame_vector_z = matrix_configuration_data.get_rest_frame_vector()[3]
        f = matrix_configuration_data.f
        f_hat = matrix_configuration_data.f_hat

        self.m00 = 0.5 * math.exp(delta) * R_plus
        self.m01 = 0.5 * math.exp(delta) * R_minus
        self.m02 = math.exp(delta) * rest_frame_vector_x / (math.sqrt(2) * rest_frame_vector_xyz)
        self.m03 = math.exp(delta) * rest_frame_vector_y / (math.sqrt(2) * rest_frame_vector_xyz)
        self.m10 = 0.5 * math.exp(-delta) * R_plus
        self.m11 = 0.5 * math.exp(-delta) * R_minus
        self.m12 = -math.exp(-delta) * rest_frame_vector_x / (math.sqrt(2) * rest_frame_vector_xyz)
        self.m13 = -math.exp(-delta) * rest_frame_vector_y / (math.sqrt(2) * rest_frame_vector_xyz)
        self.m20 = -((rest_frame_vector_x / (math.sqrt(2) * rest_frame_vector_xz)) * f) - (f_hat * rest_frame_vector_y * rest_frame_vector_z / (math.sqrt(2) * rest_frame_vector_xyz * rest_frame_vector_xz))
        self.m21 = (rest_frame_vector_x / (math.sqrt(2) * rest_frame_vector_xz) * f) + (f_hat * rest_frame_vector_y * rest_frame_vector_z / (math.sqrt(2) * rest_frame_vector_xyz * rest_frame_vector_xz))
        self.m22 = ((rest_frame_vector_z / rest_frame_vector_xz) * f) - (f_hat * rest_frame_vector_y * rest_frame_vector_z / (rest_frame_vector_xyz * rest_frame_vector_xz))
        self.m23 = f_hat * rest_frame_vector_xz / rest_frame_vector_xyz
        self.m30 = ((rest_frame_vector_x / (math.sqrt(2) * rest_frame_vector_xz)) * f_hat) - (f * rest_frame_vector_y * rest_frame_vector_z / (math.sqrt(2) * rest_frame_vector_xyz * rest_frame_vector_xz))
        self.m31 = -(rest_frame_vector_x / (math.sqrt(2) * rest_frame_vector_xz) * f_hat) + (f * rest_frame_vector_y * rest_frame_vector_z / (math.sqrt(2) * rest_frame_vector_xyz * rest_frame_vector_xz))
        self.m32 = -((rest_frame_vector_z / rest_frame_vector_xz) * f_hat) - (f * rest_frame_vector_y * rest_frame_vector_z / (rest_frame_vector_xyz * rest_frame_vector_xz))
        self.m33 = f * rest_frame_vector_xz / rest_frame_vector_xyz


class LightConeRapidityMatrixConfigurationData(MatrixConfigurationData):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_rest_frame_vector(self, rest_frame_vector):
        MatrixConfigurationData.set_rest_frame_vector(rest_frame_vector=rest_frame_vector)
        self.rest_frame_vector_xyz_magnitude = math.sqrt(math.pow(rest_frame_vector[1], 2),
                                                         math.pow(rest_frame_vector[2], 2),
                                                         math.pow(rest_frame_vector[3], 2))
        self.rest_frame_vector_xz_magnitude = math.sqrt(math.pow(rest_frame_vector[1], 2),
                                                        math.pow(rest_frame_vector[3], 2))

        self.exp_2yr = abs((rest_frame_vector[0] + self.rest_frame_vector_xyz_magnitude) /
                           (rest_frame_vector[0] - self.rest_frame_vector_xyz_magnitude))

        self.R_plus = 1 + (rest_frame_vector[3] / self.rest_frame_vector_xyz_magnitude)
        self.R_minus = 1 - (rest_frame_vector[3] / self.rest_frame_vector_xyz_magnitude)

    def set_exp_2yT(self, exp_2yT):
        """
        This is the boost value, a.k.a "A". It is set by fiat, for instance to 10, not calculated as an 
        exponential of 2yT.

        :param exp_2yT: The boost value, such that V+ = AV−.
        """
        self.exp_2yT = exp_2yT

    def get_exp_2yT(self):
        return self.exp_2yT

    def get_exp_2yr(self):
        return self.exp_2yTr

    def calculate_calculated_values(self):
        self.YLx = (self.rest_frame_vector[3] * self.vector_to_be_transformed[1] - self.rest_frame_vector[1]
                    * self.vector_to_be_transformed[2]) / self.rest_frame_vector_xz_magnitude

        self.YLy = (math.pow(self.rest_frame_vector[1], 2) * self.vector_to_be_transformed[2] - self.rest_frame_vector[1] * self.rest_frame_vector[2] * self.vector_to_be_transformed[1] +
                    self.rest_frame_vector[3] * (self.rest_frame_vector[3] * self.vector_to_be_transformed[2] - self.rest_frame_vector[2] * self.vector_to_be_transformed[3])) / (self.rest_frame_vector_xz_magnitude * self.rest_frame_vector_xyz_magnitude)

        self.f = (self.YLx / self.YLy) / math.sqrt(1 + math.pow((self.YLx / self.YLy), 2))
        self.f_hat = math.sqrt(1 - math.pow(self.f, 2))
        self.delta = (math.log(self.exp_2yT) / 2) - (math.log(self.exp_2yr) / 2)