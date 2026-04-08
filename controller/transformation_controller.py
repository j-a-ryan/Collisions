

import numpy as np

from model.qcd_matrix import LightConeRapidityMatrix, LightConeRapidityMatrixConfigurationData


class TransformationController():

    V = "V"
    V_PLUS_Y = "V_plus_Y"
    V_MINUS_Y = "V_minus_Y"

    def __init__(self):
        pass

    def handle_transformation(self, vector_V, vector_Y, V_particle_name, particle_names, experiment, argument_type):
        
        original_vectors = experiment.get_original_four_vectors()
        
        match argument_type:
            case TransformationController.V:
                transformed_vectors = self.transform(vector_V, vector_Y, original_vectors, argument_type)
            case TransformationController.V_MINUS_Y:
                transformed_vectors = self.transform(vector_V, vector_Y, original_vectors, TransformationController.V_PLUS_Y)
                
                # Set the transformed vectors in the experiment only for the convenience of being able to
                # get the V and Y vectors from there using the lookup. This collision will soon be overwritten
                # with the final one.
                experiment.set_transformed_four_vectors(transformed_vectors, particle_names) # Not numpy for this because using the pathway that comes from the GUI to the model.        
                vector_V_prime = experiment.get_transformed_four_vector(V_particle_name).copy() # These are numpy
                
                # We use V' and Y for the next pair.
                transformed_vectors = self.transform(vector_V_prime, vector_Y, original_vectors, argument_type)
            case TransformationController.V_PLUS_Y:
                transformed_vectors = self.transform(vector_V, vector_Y, original_vectors, argument_type)
        return transformed_vectors

    def transform(self, vector_V, vector_Y, vectors, argument_type):
    
        matrix_configuration_data = self.set_up_config_data(vector_V, vector_Y, 2, argument_type)
        matrix = LightConeRapidityMatrix(matrix_configuration_data)

        transformed_vectors_temp = []
        
        for i in range(len(vectors)):
            vec_copy = vectors[i].copy() # Just to be sure no changes are made to original.
            transformed_vec = matrix.transform(vec_copy)
            transformed_vectors_temp.append(transformed_vec.tolist())

        transformed_vectors = np.array(transformed_vectors_temp)
        return transformed_vectors
    
    def set_up_config_data(self, vector_V, vector_Y, exp_2yT, argument_type, return_vector_in_minkowski_form=True, convert_incoming_vector_to_lcc=True):
        matrix_configuration_data = LightConeRapidityMatrixConfigurationData()

        match argument_type:
            case TransformationController.V:
                matrix_configuration_data.rest_frame_vector = vector_V
            case TransformationController.V_PLUS_Y:
                matrix_configuration_data.rest_frame_vector = [x + y for x, y in zip(vector_V, vector_Y)] # Sum the vectors
            case TransformationController.V_MINUS_Y:
                matrix_configuration_data.rest_frame_vector = [x - y for x, y in zip(vector_V, vector_Y)] # Sum the vectors
    
        matrix_configuration_data.vector_to_be_transformed = vector_Y
        matrix_configuration_data.convert_incoming_vector_to_lcc = convert_incoming_vector_to_lcc
        matrix_configuration_data.return_vector_in_minkowski_form = return_vector_in_minkowski_form
        matrix_configuration_data.exp_2yT = exp_2yT
        return matrix_configuration_data
