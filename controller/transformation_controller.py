

import numpy as np

import config
from model import transformation, util
from model.qcd_matrix import LightConeRapidityMatrix, LightConeRapidityMatrixConfigurationData


class TransformationController():

    def __init__(self):
        pass

    def handle_transformation(self, vector_V, vector_Y, V_particle_name, Y_particle_name, particle_names, experiment, argument_type):
        return transformation.handle_transformation(vector_V, vector_Y, V_particle_name, Y_particle_name, particle_names, experiment, argument_type)
    
    def set_up_config_data(self, vector_V, vector_Y, exp_2yT, argument_type, return_vector_in_minkowski_form=True, convert_incoming_vector_to_lcc=True):
        return transformation.set_up_config_data(vector_V, vector_Y, exp_2yT, argument_type, return_vector_in_minkowski_form, convert_incoming_vector_to_lcc)
    
    def validate_vectors(self, vector_V, argument_type):
        return transformation.validate_vectors(vector_V, argument_type)


        
