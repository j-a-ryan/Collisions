import numpy as np

# from model.experiment import Experiment
from controller.transformation_controller import TransformationController
from model.experiment import Experiment
from model.four_vector_matrix import GalileanTransformationMatrix, IdentityMatrix
from model.general_matrix import GeneralTransformationMatrix
from model.qcd_matrix import LightConeRapidityMatrix, LightConeRapidityMatrixConfigurationData
from model.transformation import galilean_coordinate_transformation_3, galilean_coordinate_transformation_3_vector
from model import util

class ExperimentController():

    def __init__(self, view):
        self.view = view
        self.experiment = None
        self._particle_indices_picked_for_transformation = []
        self.transformation_controller = TransformationController()

    @property
    def particle_indices_picked_for_transformation(self):
        return self._particle_indices_picked_for_transformation
    
    @particle_indices_picked_for_transformation.setter
    def particle_indices_picked_for_transformation(self, indices):
        self._particle_indices_picked_for_transformation = indices
    
    def _extract_vectors(self, experiment_configuration_data):

        # Basic treatment of the data from GUI data to data in form digestibly by model.
        # Numerical vector members: from string to float. Embellishment of particle-type 
        # strings.

        raw_vectors = experiment_configuration_data["vectors"]
        pre_treated_vectors = []
        names = []
        for vec in raw_vectors:
            pre_treated_vectors.append([float(j) for j in vec[:4]])
            names.append(vec[4])
            
        return pre_treated_vectors, names
    
    def _extract_metadata(self, experiment_configuration_data):
        return experiment_configuration_data["metadata"] # Perhaps more logic needed in future.
        
    def configure_and_create_experiment(self, experiment_configuration_data):
        
        experiment_vectors, names = self._extract_vectors(experiment_configuration_data)
        experiment_metadata = self._extract_metadata(experiment_configuration_data)
        self.experiment = self.create_experiment(experiment_vectors, names, experiment_metadata)

    def create_experiment(self, experiment_vectors, names, experiment_metadata=None):
        return Experiment(experiment_vectors, names, experiment_metadata)

    def plot_current_experiment(self, extra_circles=None):
        self.view.plot_experiment_vectors(self.experiment.get_collision(), extra_circles)

    def save_current_experiment(self):
        self.view.save_experiment(self.experiment.get_original_vectors())

    def _unpack_vector_arguments(self, V_Y_particle_names, argument_type):
        V_particle_name = V_Y_particle_names[0]
        Y_particle_name = V_Y_particle_names[1]
        vector_V = self.experiment.get_original_four_vector(V_particle_name).copy() # These are numpy
        vector_Y = self.experiment.get_original_four_vector(Y_particle_name).copy()
        names = self.experiment.get_particle_names()
        return V_particle_name, Y_particle_name, vector_V, vector_Y, names
    
    def pre_check_transformation(self, V_Y_particle_names, argument_type):
        V_particle_name, Y_particle_name, vector_V, vector_Y, names = self._unpack_vector_arguments(V_Y_particle_names, argument_type)
        results, transformation_type = self.transformation_controller.validate_vectors(vector_V, vector_Y, argument_type, V_particle_name, Y_particle_name, self.experiment, names)
        return results, transformation_type
    
    def plot_transformation(self, V_Y_particle_names, argument_type):
        V_particle_name, Y_particle_name, vector_V, vector_Y, names = self._unpack_vector_arguments(V_Y_particle_names, argument_type)
        transformed_vectors = self.transformation_controller.handle_transformation(vector_V, vector_Y, V_particle_name, Y_particle_name, names, self.experiment, argument_type)
        self.experiment.set_transformed_four_vectors(transformed_vectors, names) # Not numpy for this because using the pathway that comes from the GUI to the model.  
        self.view.plot_transformed_experiment_vectors(self.experiment.get_transformed_collision(), self.experiment.get_collision())
    
    def close_current_experiment(self):
        self.view.clear_experiment_plot(True)
        self.view.delete_experiment()
