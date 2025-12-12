

from abc import ABC, abstractmethod
import math
import numpy as np

class MatrixConfigurationData():
    """
    Convenience class that wraps a dictionary of data to be
    used in configuring transformation matrices. Data includes
    scalars, vectors, etc. All values are strictly optional, 
    as different matrix types require different data. Some values
    will probably always be present, however, such as rest_frame_vector.
    The class offers getters and setters as convenient reminder to 
    developers of which variables are likely to be needed. Subclasses
    more likely will use a we-are-all-adults-here dot strategy for
    their peculiar variables.

    User can set idiosyncratic values, using set_value() or directly by dot, 
    most likely in a subclass. If a new value is likely to be used again, a
    setter and getter for it might be added, instead.
    """
    def __init__(self, **kwargs):
        self.data_dict = {}
        for key, val in kwargs.items():
            self.set_value(key, val)

    def calculate_calculated_values(self):
        """
        To be overridden and implemented by any class requiring
        calculated values to be calculated only after ensuring
        that multiple values required for the calculation have been
        set. Fire this method after setting the appropriate values.
        
        """
        pass

    def set_value(self, key, value):
        """
        For setting custom/user-defined values that aren't 
        already presented by any of the class's setter
        methods. User may instead create getter/setter for any
        such value if it is likely to be commonly used. Subclassing
        this class is a similar option.
        
        :param key: Custom value's name/key.
        :param value: The custom value
        """
        self.data_dict[key] = value

    def set_rest_frame_vector(self, rest_frame_vector):
        """
        Set the vector of the particle to whose rest frame
        transformation is to be done.
        
        :param rest_frame_vector: The vector of the particle to whose rest frame
        transformation is to be done
        """
        self.data_dict["rest_frame_vector"] = rest_frame_vector
    
    def get_rest_frame_vector(self):
        return self.data_dict["rest_frame_vector"]
    
    def set_velocity_of_rest_frame(self, velocity_of_rest_frame):
        """
        The rest frame to which we are transforming other vectors 
        has this velocity relative to the frame in which the vectors 
        to be transformed have their values.
        
        :param velocity_of_rest_frame: velocity of the rest frame to which
        transformations will be made
        """
        self.velocity_of_rest_frame = velocity_of_rest_frame
    
    def get_velocity_of_rest_frame(self):
        return self.velocity_of_rest_frame
    
    def set_vector_to_be_transformed(self, vector_to_be_transformed):
        """
        Set the vector that will be transformed.
        
        :param rest_frame_vector: The vector of the particle to whose rest frame
        transformation is to be done
        """
        self.data_dict["vector_to_be_transformed"] = vector_to_be_transformed
    
    def get_vector_to_be_transformed(self):
        return self.data_dict["vector_to_be_transformed"]


class FourVectorTransformationMatrix(ABC):
    
    def __init__(self, matrix_configuration_data: MatrixConfigurationData):
        self.initialize_parameters_to_default()
        self.set_up_matrix(matrix_configuration_data=matrix_configuration_data)

    def initialize_parameters_to_default(self):
        """
        Initializes matrix member parameters to those of an identity matrix. Sets
        gamma and beta to 1, 0.
        
        """
        self.gamma = 1
        self.beta = 0
        self.beta_squared = 0
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

    # def transform(self, matrix_configuration_data: MatrixConfigurationData, vector_to_be_transformed):
    #     """
    #     Sets up matrix and applies it to the vector_to_be_transformed. For use
    #     in cases in which matrix is to be set up especially for the matrix to be
    #     transformed and then discarded, rather than reused on other vectors to be 
    #     transformed. For the latter situation, users should call  
        
    #     :param matrix_configuration_data: Description
    #     :type matrix_configuration_data: MatrixConfigurationData
    #     :param vector_to_be_transformed: Description
    #     """ DELETE ME
    #     self.set_up_matrix(matrix_configuration_data)
    #     return self.transform_vector(four_vector=vector_to_be_transformed)
    
    def set_up_matrix(self, matrix_configuration_data: MatrixConfigurationData):
        self._set_member_values(matrix_configuration_data)
        self._compile_matrix()

    # To be implemented by child classes. Child classes simply calling pass will
    # have an identity matrix by default. See Google idea and stackoverflow idea below
    @abstractmethod  
    def _set_member_values(self, matrix_configuration_data: MatrixConfigurationData):
        pass
    
    # Sets the matrix up with its member values.
    def _compile_matrix(self):
        self.matrix = np.array([[self.m00, self.m01, self.m02, self.m03],
                                [self.m10, self.m11, self.m12, self.m13],
                                [self.m20, self.m21, self.m22, self.m23],
                                [self.m30, self.m31, self.m32, self.m33]])
    
    # To be called by other methods in this class, in particular transform(),
    # which is the public method.
    def transform(self, four_vector):
        return self.matrix @ four_vector
    

class IdentityMatrix(FourVectorTransformationMatrix):
    def __init__(self, matrix_configuration_data: MatrixConfigurationData):
        super().__init__(matrix_configuration_data)

    def _set_member_values(self, matrix_configuration_data: MatrixConfigurationData):
        pass # Do no calculations, leave the default values, which are identity matrix.

class GalileanTransformationMatrix(FourVectorTransformationMatrix):
    def __init__(self, matrix_configuration_data: MatrixConfigurationData):
        super().__init__(matrix_configuration_data)

    def _set_member_values(self, matrix_configuration_data: MatrixConfigurationData):
        rest_frame_vector = matrix_configuration_data.get_rest_frame_vector()
        self.m10 = -rest_frame_vector[1] / rest_frame_vector[0]
        self.m20 = -rest_frame_vector[2] / rest_frame_vector[0]
        self.m30 = -rest_frame_vector[3] / rest_frame_vector[0]



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
