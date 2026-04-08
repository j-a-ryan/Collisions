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
        self._particle_indices_picked_for_transformation = []

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
            four_vec = [float(j) for j in vec[:4]]
            names.append(vec[4])
            pre_treated_vectors.append(four_vec)

        return pre_treated_vectors, names
    
    def _extract_metadata(self, experiment_configuration_data):
        return experiment_configuration_data["metadata"] # Perhaps more logic needed in future.
        
    def create_experiment(self, experiment_configuration_data):
        
        experiment_vectors, names = self._extract_vectors(experiment_configuration_data)
        experiment_metadata = self._extract_metadata(experiment_configuration_data)   
        self.experiment = Experiment(experiment_vectors, names, experiment_metadata)

    def plot_current_experiment(self, extra_circles=None):
        self.view.plot_experiment_vectors(self.experiment.get_collision(), extra_circles)
    
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
    
    def plot_transformation(self, V_Y_particle_names, argument_type):
        V_particle_name = V_Y_particle_names[0]
        Y_particle_name = V_Y_particle_names[1]
        V_Y_particle_names.clear() # TODO: Probably not nec, just a copy.
        original_vectors = self.experiment.get_original_four_vectors()
        vector_V = self.experiment.get_original_four_vector(V_particle_name).copy() # These are numpy
        vector_Y = self.experiment.get_original_four_vector(Y_particle_name).copy()
        names = self.experiment.get_particle_names()

        match argument_type:
            case TransformationController.V:
                transformed_vectors = self.transform(vector_V, vector_Y, original_vectors, argument_type)
            case TransformationController.V_MINUS_Y:
                transformed_vectors = self.transform(vector_V, vector_Y, original_vectors, TransformationController.V_PLUS_Y)
                
                # Set the transformed vectors in the experiment only for the convenience of being able to
                # get the V and Y vectors from there using the lookup. This collision will soon be overwritten
                # with the final one.
                self.experiment.set_transformed_four_vectors(transformed_vectors, names) # Not numpy for this because using the pathway that comes from the GUI to the model.        
                vector_V_prime = self.experiment.get_transformed_four_vector(V_particle_name).copy() # These are numpy
                
                # We use V' and Y for the next pair.
                transformed_vectors = self.transform(vector_V_prime, vector_Y, original_vectors, argument_type)
            case TransformationController.V_PLUS_Y:
                transformed_vectors = self.transform(vector_V, vector_Y, original_vectors, argument_type)
        
        self.experiment.set_transformed_four_vectors(transformed_vectors, names) # Not numpy for this because using the pathway that comes from the GUI to the model.  
        self.view.plot_transformed_experiment_vectors(self.experiment.get_transformed_collision(), self.experiment.get_collision())

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
    
    def close_current_experiment(self):
        self.view.clear_experiment_plot(True)

    def get_experiment_vectors(self):
        return self.experiment.get_collision_vectors()
    
    def get_experiment_vectors_xyz(self):
        vectors = self.get_experiment_vectors().get_vectors()
        return vectors[-3:]
