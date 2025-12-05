

from abc import ABC, abstractmethod
import math
import numpy as np


class FourVectorTransformationMatrix(ABC):
    def __init__(self):
        self.gamma = 1
        self.beta = 0
        self.beta_x = 0
        self.beta_y = 0
        self.beta_z = 0
        self.m00 = 1
        self.m01 = 0
        self.m02 = 0
        self.m03 = 0
        self.m10 = 0
        self.m11 = 1
        self.m12 = 0
        self.m13 = 0
        self.m20 = 0
        self.m21 = 0
        self.m22 = 1
        self.m23 = 0
        self.m30 = 0
        self.m31 = 0
        self.m32 = 0
        self.m33 = 1

    def transform(self, four_vector, velocity_of_four_vector_frame, function, additional_data=None):
        self.set_member_values(four_vector, velocity_of_four_vector_frame, function, additional_data=None)
        self.configure_matrix()
        return self._transform_four_vector(four_vector=four_vector)

    # Is this flexible enough for both velocity and momentum? Will a lambda arg help?
    # May need to dedicate this class to momentum. (dict params -> func lambda might work, 
    # where dict and func were appropriate for the particular case) See Google idea below
    # and especially stackoverflow idea.
    @abstractmethod  
    def set_member_values(self, four_vector, velocity_of_four_vector_frame, function, additional_data=None):
        pass

    # Call this after setting all the mxx members of the matrix to their
    # correct values.
    def configure_matrix(self):
        self.matrix = np.array([[self.m00, self.m01, self.m02, self.m03],
                                [self.m10, self.m11, self.m12, self.m13],
                                [self.m20, self.m21, self.m22, self.m23],
                                [self.m30, self.m31, self.m32, self.m33]])
    
    # To be called by other methods in this class, in particular transform(),
    # which is the public method.
    def _transform_four_vector(self, four_vector):
        return self.matrix @ four_vector
    

class IdentityMatrix(FourVectorTransformationMatrix):
    def __init__(self):
        super().__init__()

    def set_member_values(self, four_vector, velocity_of_four_vector_frame, function, additional_data=None):
        pass # Do no calculations, leave the default values, which are identity matrix.

class GalileanTransformationMatrix(FourVectorTransformationMatrix):
    def __init__(self):
        super().__init__()

    def set_member_values(self, four_vector, velocity_of_four_vector_frame, function, additional_data=None):
        pass # TODO: galilean sets here

# Three matrices: 1. General (Jackson 11.98) 2. Four velocity transformation
# 3. Four momentum transformation
class GeneralTransformationMatrix(FourVectorTransformationMatrix):
    def __init__(self):
        super().__init__()

    def set_member_values(self, four_vector, velocity_of_four_vector_frame, function, additional_data=None):
        # Calculate gamma

        # Calculate the three components of beta: beta_x, beta_y, beta_z

        # Calculate the members of the matrix, using gamma, beta
        self.m00 = self.gamma
        self.m01 = -self.gamma * self.beta_x
        self.m02 = -self.gamma * self.beta_y
        self.m03 = -self.gamma * self.beta_z
        self.m10 = -self.gamma * self.beta_x
        self.m11 = 1 + (self.gamma - 1) * math.pow(self.beta_x, 2)/math.pow(self.beta, 2)
        self.m12 = 1 + (self.gamma - 1) * self.beta_x * self.beta_y/math.pow(self.beta, 2)
        self.m13 = 1 + (self.gamma - 1) * self.beta_x * self.beta_z/math.pow(self.beta, 2)
        self.m20 = -self.gamma * self.beta_y
        self.m21 = 1 + (self.gamma - 1) * self.beta_x * self.beta_y/math.pow(self.beta, 2)
        self.m22 = 1 + (self.gamma - 1) * math.pow(self.beta_y, 2)/math.pow(self.beta, 2)
        self.m23 = 1 + (self.gamma - 1) * self.beta_y * self.beta_z/math.pow(self.beta, 2)
        self.m30 = -self.gamma * self.beta_z
        self.m31 = 1 + (self.gamma - 1) * self.beta_x * self.beta_z/math.pow(self.beta, 2)
        self.m32 = 1 + (self.gamma - 1) * self.beta_y * self.beta_z/math.pow(self.beta, 2)
        self.m33 = 1 + (self.gamma - 1) * math.pow(self.beta_z, 2)/math.pow(self.beta, 2)
    
# Four velocity Lorentz transformation matrix
class FourVelocityMatrix(FourVectorTransformationMatrix):
    def __init__(self):
        super().__init__()


class FourMomentumMatrix(FourVectorTransformationMatrix):
    def __init__(self):
        super().__init__()

###################################################
# # Google AI's lambda idea:
# class MyClass:
#     def process_data(self, data_list, operation_func):
#         """
#         Processes a list of data using a provided function.

#         Args:
#             data_list (list): The list of data to process.
#             operation_func (callable): A function (often a lambda) to apply to each item.

#         Returns:
#             list: A new list with the processed data.
#         """
#         processed_results = []
#         for item in data_list:
#             processed_results.append(operation_func(item))
#         return processed_results

# # Create an instance of MyClass
# my_instance = MyClass()

# # Example 1: Using a lambda to double each number in a list
# numbers = [1, 2, 3, 4, 5]
# doubled_numbers = my_instance.process_data(numbers, lambda x: x * 2)
# print(f"Doubled numbers: {doubled_numbers}")

# # Example 2: Using a lambda to convert strings to uppercase
# words = ["hello", "world", "python"]
# uppercased_words = my_instance.process_data(words, lambda s: s.upper())
# print(f"Uppercased words: {uppercased_words}")

# # Example 3: Using a lambda with multiple arguments (if the operation_func expects them)
# # In this case, process_data would need to be adapted to handle multiple arguments
# # For simplicity, this example shows a single-argument lambda.

# # Stackoverflow idea:
# # Source - https://stackoverflow.com/q
# # Posted by Salvador Dali, modified by community. See post 'Timeline' for change history
# # Retrieved 2025-12-02, License - CC BY-SA 3.0

# def iterator(function, x, n=4):
#     x = float(x)
#     arr = []
#     for i in range(n + 1):
#         arr.append(x)
#         x = function(x)

#     return arr

# def funcM(x):
#     return x / 4 + 12
