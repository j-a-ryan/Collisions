import numpy as np
from model.collision import create_collision
from model.experiment import Experiment
from model.four_vector_matrix import GalileanTransformationMatrix, IdentityMatrix
from model.general_matrix import GeneralTransformationMatrix
from model.qcd_matrix import LightConeRapidityMatrix, LightConeRapidityMatrixConfigurationData
from model.transformation import galilean_coordinate_transformation_3, galilean_coordinate_transformation_3_vector


class ExperimentController():

    def __init__(self, view):
        self.view = view
        self.experiment = Experiment()

    def plot_current_experiment(self):
        self.experiment = Experiment()
        collision = create_collision([[1, 0, 0, 0], [1, 3, 4, 5], [1, 5, 3, 3]], 0)
        # collision = create_collision([[1, 0, 0, 0], [10, 1, 4, 1], [7, 1, 0, 5]], 0)
        # collision = create_collision([[10, 1, 4, 1], [7, 1, 0, 5]], 0)
        self.experiment.set_lab_collision(collision)
        self.view.plot_experiment_vectors(self.get_experiment_vectors())


    def set_up_config_data(self, vector_V, vector_Y, exp_2yT, return_vector_in_minkowski_form, convert_incoming_vector_to_lcc=True):
        matrix_configuration_data = LightConeRapidityMatrixConfigurationData()
        matrix_configuration_data.rest_frame_vector = vector_V
        matrix_configuration_data.vector_to_be_transformed = vector_Y
        matrix_configuration_data.convert_incoming_vector_to_lcc = convert_incoming_vector_to_lcc
        matrix_configuration_data.return_vector_in_minkowski_form = return_vector_in_minkowski_form
        matrix_configuration_data.exp_2yT = exp_2yT
        return matrix_configuration_data
    
    identity_transformation = False
    def plot_transformation(self, particle_id):
        experiment_collision = self.get_experiment_vectors()
        exp_vectors = experiment_collision.get_vectors()
        if particle_id == 1:
            vector_V = np.array(exp_vectors[1]).copy().tolist()
            vector_Y = np.array(exp_vectors[2]).copy().tolist()
        else: # It's 2 that we want for V
            vector_V = np.array(exp_vectors[2]).copy().tolist()
            vector_Y = np.array(exp_vectors[1]).copy().tolist()

        # matrix = None
        if self.identity_transformation:
            matrix = IdentityMatrix(None)
            particle_id = experiment_collision.get_id_of_origin_vector()
        else:
            matrix_configuration_data = self.set_up_config_data(vector_V, vector_Y, 2, False)
            matrix = LightConeRapidityMatrix(matrix_configuration_data)

        transformed_vectors = []
        
        for i in range(len(exp_vectors)):
            vec_copy = np.array(exp_vectors[i]).copy().tolist()
            if i > 0:
                transformed_vec = matrix.transform(vec_copy)
                transformed_vectors.append(transformed_vec)
            else:
                transformed_vectors.append(vec_copy) # append the origin vec (0,0,0) untransformed
            
        
        collision_transformed = create_collision(transformed_vectors, particle_id)        

        self.view.plot_transformed_experiment_vectors(collision_transformed, experiment_collision)
    
    def close_current_experiment(self):
        self.view.clear_experiment_plot(True)

    def get_experiment_vectors(self):
        return self.experiment.get_collision_vectors()
    
    def get_experiment_vectors_xyz(self):
        vectors = self.get_experiment_vectors().get_vectors()
        return vectors[-3:]


    
        
