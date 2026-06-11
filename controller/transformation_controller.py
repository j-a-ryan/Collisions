

import numpy as np

import config
from model import transformation, util
from model.qcd_matrix import LightConeRapidityMatrix, LightConeRapidityMatrixConfigurationData


class TransformationController():

    def __init__(self, experiment_controller):
        self.experiment_controller = experiment_controller

    def handle_transformation(self, vector_V, vector_Y, V_particle_name, Y_particle_name, particle_names, experiment, argument_type, third_vector=None):
        transformed_vectors = transformation.handle_transformation(vector_V, vector_Y, V_particle_name, Y_particle_name, particle_names, experiment, argument_type, third_vector)
        experiment.set_transformation([V_particle_name, Y_particle_name], argument_type, transformed_vectors, particle_names) # Not numpy for this because using the pathway that comes from the GUI to the model.

    # def set_up_config_data(self, vector_V, vector_Y, exp_2yT, argument_type, return_vector_in_minkowski_form=True, convert_incoming_vector_to_lcc=True):
    #     return transformation.set_up_config_data(vector_V, vector_Y, exp_2yT, argument_type, return_vector_in_minkowski_form, convert_incoming_vector_to_lcc)
    
    def validate_vectors(self, vector_V, vector_Y, argument_type, V_particle_name=None, Y_particle_name=None, experiment=None, particle_names=None):
        return transformation.validate_vectors(vector_V, vector_Y, argument_type, V_particle_name, Y_particle_name, experiment, particle_names)

    def transformation_exists(self, experiment):
        return experiment.has_transformation()
    
    '''
    Assumes transformation exists. Call transformation_exists() first.
    '''
    def retransform_experiment_vectors(self, vector_V, vector_Y, V_particle_name, Y_particle_name, names, experiment):
        transformation_type = experiment.get_transformation_type()
        self.handle_transformation(vector_V, vector_Y, V_particle_name, Y_particle_name, names, experiment, transformation_type)

        
