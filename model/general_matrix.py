
import math
from model.four_vector_matrix import FourVectorTransformationMatrix, MatrixConfigurationData

# Three matrices: 1. General (Jackson 11.98) 2. Four velocity transformation
# 3. Four momentum transformation

class GeneralTransformationMatrix(FourVectorTransformationMatrix):
    def __init__(self, matrix_configuration_data: MatrixConfigurationData):
        super().__init__(matrix_configuration_data)
        self.set_up_matrix(matrix_configuration_data=matrix_configuration_data)

    def _set_member_values(self, matrix_configuration_data: MatrixConfigurationData):
        rest_frame_vector = matrix_configuration_data.rest_frame_vector
        # Calculate the three components of beta: beta_x, beta_y, beta_z
        self.beta_x = rest_frame_vector[1] / rest_frame_vector[0]
        self.beta_y = rest_frame_vector[2] / rest_frame_vector[0]
        self.beta_z = rest_frame_vector[3] / rest_frame_vector[0]
        self.beta_squared = math.pow(self.beta_x, 2) + math.pow(self.beta_y, 2) + math.pow(self.beta_z, 2)
        print("beta2 " + str(self.beta_squared))
        self.beta = math.sqrt(self.beta_squared) # Not used
        print("beta " + str(self.beta))
        # Calculate gamma
        self.gamma = 1 / math.sqrt(1 - self.beta_squared)
        print("gamma " + str(self.gamma))
        # Calculate the members of the matrix, using gamma, beta
        self.m00 = self.gamma
        self.m01 = -self.gamma * self.beta_x
        self.m02 = -self.gamma * self.beta_y
        self.m03 = -self.gamma * self.beta_z
        self.m10 = -self.gamma * self.beta_x
        self.m11 = 1 + ((self.gamma - 1) * math.pow(self.beta_x, 2) / self.beta_squared)
        self.m12 = 1 + ((self.gamma - 1) * self.beta_x * self.beta_y / self.beta_squared)
        self.m13 = 1 + ((self.gamma - 1) * self.beta_x * self.beta_z / self.beta_squared)
        self.m20 = -self.gamma * self.beta_y
        self.m21 = 1 + (self.gamma - 1) * self.beta_x * self.beta_y / self.beta_squared
        self.m22 = 1 + (self.gamma - 1) * math.pow(self.beta_y, 2) / self.beta_squared
        self.m23 = 1 + (self.gamma - 1) * self.beta_y * self.beta_z / self.beta_squared
        self.m30 = -self.gamma * self.beta_z
        self.m31 = 1 + (self.gamma - 1) * self.beta_x * self.beta_z / self.beta_squared
        self.m32 = 1 + (self.gamma - 1) * self.beta_y * self.beta_z / self.beta_squared
        self.m33 = 1 + (self.gamma - 1) * math.pow(self.beta_z, 2) / self.beta_squared
    
# Four velocity Lorentz transformation matrix
class FourVelocityMatrix(FourVectorTransformationMatrix):
    def __init__(self):
        super().__init__()


class FourMomentumMatrix(FourVectorTransformationMatrix):
    def __init__(self):
        super().__init__()