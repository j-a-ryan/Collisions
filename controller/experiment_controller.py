import numpy as np
from model.collision import create_collision
from model.experiment import Experiment
from model.four_vector_matrix import GalileanTransformationMatrix, IdentityMatrix
from model.general_matrix import GeneralTransformationMatrix
from model.transformation import galilean_coordinate_transformation_3, galilean_coordinate_transformation_3_vector


class ExperimentController():

    def __init__(self, view):
        self.view = view
        self.experiment = Experiment()

    def plot_current_experiment(self):
        self.experiment = Experiment()
        collision = create_collision([[1, 0, 0, 0], [1, 3, 4, 5], [1, 5, 3, 3]], 0)
        self.experiment.set_lab_collision(collision)
        # self.experiment.set_lab_collision([[0, 0, 0], [3, 4, 5], [5, 3, 3]])
        self.view.plot_experiment_vectors(self.get_experiment_vectors())

    identity_transformation = True
    def plot_transformation(self, particle_id):
        experiment_collision = self.get_experiment_vectors()
        matrix = None
        if self.identity_transformation:
            matrix = IdentityMatrix(None)
            particle_id = experiment_collision.get_id_of_origin_vector()
        else:
            matrix = GalileanTransformationMatrix()
            # matrix = GeneralTransformationMatrix()

        transformed_vectors = []
        exp_vectors = experiment_collision.get_vectors()
        for vec in exp_vectors:
            vec_copy = np.array(vec).copy().tolist()
            # transf_vector = galilean_coordinate_transformation_3_vector()
            transformed_vec = matrix.transform(vec_copy)
            transformed_vectors.append(transformed_vec)
        
        collision_transformed = create_collision(transformed_vectors, particle_id)        

        self.view.plot_transformed_experiment_vectors(collision_transformed, experiment_collision)
    
    def close_current_experiment(self):
        self.view.clear_experiment_plot(True)

    def get_experiment_vectors(self):
        return self.experiment.get_collision_vectors()
    
    def get_experiment_vectors_xyz(self):
        vectors = self.get_experiment_vectors().get_vectors()
        return vectors[-3:]


    
        
