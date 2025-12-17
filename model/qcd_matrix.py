

import math
from model.four_vector_matrix import FourVectorTransformationMatrix, MatrixConfigurationData
from model.util import convert_light_cone_coordinates_to_minkowski_form, convert_minkowski_to_light_cone_coordinates

"""
This matrix is used by QCD physicists at Old Dominion University. It may fairly standard or somewhat
idiosyncratic to ODU physicists. It is fraught with layers of arithmetical calculations and variables
wrapping variables. These aren't difficult calculations but the code is not easy to read. Developers 
wishing to make any surgical changes will probably want to consult the document of the matrix in the 
dev docs folder. Note that this matrix is custom-made for the vector it is meant to transform, unlike a
general boost matrix.

Usage: The matrix is configured with the new rest-frame vector and a vector to be tansformed to that frame.
After setting the data in a LightConeRapidityMatrixConfigurationData object, the user should call
calculate_calculated_values() on it before passing it in to a LightConeRapidityMatrix constructor. (TODO: Perhaps
that constructor should call that method in the parent class.) The LightConeRapidityMatrixConfigurationData object
can be reused for transforming another vector (such as the new rest-frame vector itself) by setting that data value
set_vector_to_be_transformed() and ensuring that calculate_calculated_values() is called again when creating a new
transormation matrix.

The subclass of MatrixConfigurationData here uses dotting for its pecular variables.
"""

class LightConeRapidityMatrix(FourVectorTransformationMatrix):
    def __init__(self, matrix_configuration_data: MatrixConfigurationData):
        super().__init__(matrix_configuration_data)

    def _set_member_values(self, matrix_configuration_data: MatrixConfigurationData):
        delta = matrix_configuration_data.delta
        R_plus = matrix_configuration_data.R_plus
        R_minus = matrix_configuration_data.R_minus
        rest_frame_vector_xyz = matrix_configuration_data.rest_frame_vector_xyz_magnitude
        rest_frame_vector_xz = matrix_configuration_data.rest_frame_vector_xz_magnitude
        rest_frame_vector_x = matrix_configuration_data.rest_frame_vector[1]
        rest_frame_vector_y = matrix_configuration_data.rest_frame_vector[2]
        rest_frame_vector_z = matrix_configuration_data.rest_frame_vector[3]
        f = matrix_configuration_data.f
        f_hat = matrix_configuration_data.f_hat

        self.m00 = 0.5 * math.exp(delta) * R_plus
        self.m01 = 0.5 * math.exp(delta) * R_minus
        self.m02 = math.exp(delta) * rest_frame_vector_x / (math.sqrt(2) * rest_frame_vector_xyz)
        self.m03 = math.exp(delta) * rest_frame_vector_y / (math.sqrt(2) * rest_frame_vector_xyz)
        self.m10 = 0.5 * math.exp(-delta) * R_minus
        self.m11 = 0.5 * math.exp(-delta) * R_plus
        self.m12 = -math.exp(-delta) * rest_frame_vector_x / (math.sqrt(2) * rest_frame_vector_xyz)
        self.m13 = -math.exp(-delta) * rest_frame_vector_y / (math.sqrt(2) * rest_frame_vector_xyz)
        self.m20 = -((rest_frame_vector_x / (math.sqrt(2) * rest_frame_vector_xz)) * f) - (f_hat * rest_frame_vector_y * rest_frame_vector_z / (math.sqrt(2) * rest_frame_vector_xyz * rest_frame_vector_xz))
        self.m21 = -self.m20 # (rest_frame_vector_x / (math.sqrt(2) * rest_frame_vector_xz) * f) + (f_hat * rest_frame_vector_y * rest_frame_vector_z / (math.sqrt(2) * rest_frame_vector_xyz * rest_frame_vector_xz))
        self.m22 = ((rest_frame_vector_z / rest_frame_vector_xz) * f) - (f_hat * rest_frame_vector_y * rest_frame_vector_z / (rest_frame_vector_xyz * rest_frame_vector_xz))
        self.m23 = f_hat * rest_frame_vector_xz / rest_frame_vector_xyz
        self.m30 = ((rest_frame_vector_x / (math.sqrt(2) * rest_frame_vector_xz)) * f_hat) - (f * rest_frame_vector_y * rest_frame_vector_z / (math.sqrt(2) * rest_frame_vector_xyz * rest_frame_vector_xz))
        self.m31 = -(rest_frame_vector_x / (math.sqrt(2) * rest_frame_vector_xz) * f_hat) + (f * rest_frame_vector_y * rest_frame_vector_z / (math.sqrt(2) * rest_frame_vector_xyz * rest_frame_vector_xz))
        self.m32 = -((rest_frame_vector_z / rest_frame_vector_xz) * f_hat) - (f * rest_frame_vector_y * rest_frame_vector_z / (rest_frame_vector_xyz * rest_frame_vector_xz))
        self.m33 = f * rest_frame_vector_xz / rest_frame_vector_xyz



class LightConeRapidityMatrixConfigurationData(MatrixConfigurationData):
    def __init__(self):
        super().__init__()

        """
        LCC vectors and Minkowski-form vectors may be used for incoming arguments and the
        transformed vectors returned. Default to Minkowski. The matrix assumes LCC, so the
        any Minkowski-form arguments are converted to LCC coordinates before transformation
        """

        # Initialize non-calculated values
        self.convert_incoming_vector_to_lcc = True
        self.return_vector_in_minkowski_form = True
        self.vector_pretreatment_function = convert_minkowski_to_light_cone_coordinates
        self.vector_posttreatment_function = convert_light_cone_coordinates_to_minkowski_form

        """
        This is the boost value, a.k.a "A". It is set by fiat, for instance to 10, not calculated as an 
        exponential of 2yT. The boost value, such that V+ = AV−.
        """
        self.exp_2yT = None
        
    def calculate_calculated_values(self):
        super().calculate_calculated_values()
        self.rest_frame_vector_xyz_magnitude = math.sqrt(math.pow(self.rest_frame_vector[1], 2) +
                                                         math.pow(self.rest_frame_vector[2], 2) +
                                                         math.pow(self.rest_frame_vector[3], 2))
        self.rest_frame_vector_xz_magnitude = math.sqrt(math.pow(self.rest_frame_vector[1], 2) +
                                                        math.pow(self.rest_frame_vector[3], 2))

        self.exp_2yr = abs((self.rest_frame_vector[0] + self.rest_frame_vector_xyz_magnitude) /
                           (self.rest_frame_vector[0] - self.rest_frame_vector_xyz_magnitude))

        self.R_plus = 1 + (self.rest_frame_vector[3] / self.rest_frame_vector_xyz_magnitude)
        self.R_minus = 1 - (self.rest_frame_vector[3] / self.rest_frame_vector_xyz_magnitude)
        self.YLx = (self.rest_frame_vector[3] * self.vector_to_be_transformed[1] - self.rest_frame_vector[1]
                    * self.vector_to_be_transformed[3]) / self.rest_frame_vector_xz_magnitude

        self.YLy = (math.pow(self.rest_frame_vector[1], 2) * self.vector_to_be_transformed[2] - self.rest_frame_vector[1] * self.rest_frame_vector[2] * self.vector_to_be_transformed[1] +
                    self.rest_frame_vector[3] * (self.rest_frame_vector[3] * self.vector_to_be_transformed[2] - self.rest_frame_vector[2] * self.vector_to_be_transformed[3])) / (self.rest_frame_vector_xz_magnitude * self.rest_frame_vector_xyz_magnitude)

        self.f = (self.YLx / self.YLy) / math.sqrt(1 + math.pow(self.YLx / self.YLy, 2))
        self.f_hat = math.sqrt(1 - math.pow(self.f, 2))
        self.delta = (math.log(self.exp_2yT) / 2) - (math.log(self.exp_2yr) / 2)

        # In the unlikely event user has turned off the normal conversions, for instance
        # for unit testing, we eliminate them here (or put them back in if the user has turned 
        # them back on.):
        if self.convert_incoming_vector_to_lcc is False:
            self.vector_pretreatment_function = lambda vector: vector
        else:
            self.vector_pretreatment_function = convert_minkowski_to_light_cone_coordinates
        if self.return_vector_in_minkowski_form is False:
            self.vector_posttreatment_function = lambda vector: vector
        else:
            self.vector_posttreatment_function = convert_light_cone_coordinates_to_minkowski_form
        
