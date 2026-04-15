import numpy as np

from controller.transformation_controller import TransformationController
from model.experiment import Experiment
from model.transformation import galilean_coordinate_transformation_3, galilean_coordinate_transformation_3_vector

class ExperimentController():

    def __init__(self, view):
        self.view = view
        self.experiment = None
        self._particle_indices_picked_for_transformation = []
        self.transformation_controller = TransformationController(None)

    def set_controls_controller(self, controller):
        self.controls_controller = controller

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
        metadata = None
        if "metadata" in experiment_configuration_data:
            metadata = experiment_configuration_data["metadata"]
        return metadata
        
    def configure_and_create_experiment(self, experiment_configuration_data):
        experiment_vectors, names = self._extract_vectors(experiment_configuration_data)
        experiment_metadata = self._extract_metadata(experiment_configuration_data)
        self.experiment = self.create_experiment(experiment_vectors, names, experiment_metadata)

    def create_experiment(self, experiment_vectors, names, experiment_metadata=None):
        return Experiment(experiment_vectors, names, experiment_metadata)

    def plot_current_experiment(self, extra_circles=None, initial_plot=False):
        self.view.plot_experiment_vectors(self.experiment.get_collision(), extra_circles)

        if initial_plot:
            # Now tell the view to set up controls appropriate to the vector set
            self.controls_controller.set_up_controls(self.view, self.experiment)

    def save_current_experiment(self):
        if self.experiment:
            self.view.save_experiment(self.experiment.get_original_vectors())

    def unpack_vector_arguments(self, V_Y_particle_names):
        V_particle_name = V_Y_particle_names[0]
        Y_particle_name = V_Y_particle_names[1]
        vector_V = self.get_vector(V_particle_name).copy() # These are numpy
        vector_Y = self.get_vector(Y_particle_name).copy()
        names = self.experiment.get_particle_names()
        return V_particle_name, Y_particle_name, vector_V, vector_Y, names
    
    def transformation_exists(self):
        return self.transformation_controller.transformation_exists(self.experiment)

    def get_current_transformation_arguments(self):
        V_Y_particle_names = self.experiment.get_transformation_particle_pair_names()
        argument_type = self.experiment.get_transformation_type() # TODO: Pick one or the other of these names
        return V_Y_particle_names, argument_type
    
    def pre_check_transformation_update(self):
        V_Y_particle_names, argument_type = self.get_current_transformation_arguments()
        return self.pre_check_transformation(V_Y_particle_names, argument_type)
    
    def pre_check_transformation(self, V_Y_particle_names, argument_type):
        V_particle_name, Y_particle_name, vector_V, vector_Y, names = self.unpack_vector_arguments(V_Y_particle_names)
        results, transformation_type = self.transformation_controller.validate_vectors(vector_V, vector_Y, argument_type, V_particle_name, Y_particle_name, self.experiment, names)
        return results, transformation_type
    
    def plot_transformation(self, V_Y_particle_names, argument_type):
        V_particle_name, Y_particle_name, vector_V, vector_Y, names = self.unpack_vector_arguments(V_Y_particle_names)
        self.transformation_controller.handle_transformation(vector_V, vector_Y, V_particle_name, Y_particle_name, names, self.experiment, argument_type)
        self.view.plot_transformed_experiment_vectors(self.experiment.get_transformed_collision(), self.experiment.get_collision())

    def refresh_transformation(self):
        V_Y_particle_names, argument_type = self.get_current_transformation_arguments()
        self.plot_transformation(V_Y_particle_names, argument_type)

    def close_current_experiment(self):
        self.view.clear_experiment_plot(True)
        self.view.clear_controls_layout()
        self.view.delete_experiment()

    def get_vector(self, vector_name):
        return self.experiment.get_original_four_vector(vector_name)
