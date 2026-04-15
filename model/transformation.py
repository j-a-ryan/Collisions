import config
from model import util
from model import qcd_matrix
from model.particle import Particle
import numpy as np

from model.qcd_matrix import LightConeRapidityMatrix, LightConeRapidityMatrixConfigurationData



def galilean_coordinate_transform1(to_particle, from_particle):
    from_vector = from_particle.vector
    to_vector = to_particle.vector
    transformed_vector = [from_vector[0], to_vector[1] - from_vector[1],
                          to_vector[2] - from_vector[2], to_vector[3] - from_vector[3]]
    from_particle_transformed = Particle(
        from_particle.id, from_particle.type, transformed_vector, False)
    return from_particle_transformed

def galilean_coordinate_transform2(to_particle, from_particle):
    from_vector = from_particle.vector
    to_vector = to_particle.vector
    matrix = np.array([[1, 0, 0, 0],
              [0, 1 - from_vector[1] / to_vector[1], 0, 0],
              [0, 0, 1 - from_vector[2] / to_vector[2], 0],
              [0, 0, 0, 1 - from_vector[3] / to_vector[3]]])
    transformed_vector = from_vector @ matrix
    # transformed_vector = np.dot(from_vector, matrix)
    from_particle_transformed = Particle(from_particle.id, from_particle.type, transformed_vector, False)
    return from_particle_transformed

# Galilean transformation matrix for arbitray position vectors.Purely for fun/exercise, 
# not use in app. Assumes t != 0 and t0 = 0. 
def galilean_coordinate_transformation_3(to_vector, from_vector):
    matrix = np.array([[1, 0, 0, 0],
              [(from_vector[1] - to_vector[1]) / from_vector[0], 0, 0, 0],
              [from_vector[2] - to_vector[2] / from_vector[0], 0, 0, 0],
              [from_vector[3] - to_vector[3] / from_vector[0], 0, 0, 0]])
    transformed_vector = matrix @ from_vector
    # transformed_vector = np.dot(matrix, from_vector)
    return transformed_vector

def galilean_coordinate_transformation_4(to_vector, from_vector):
    transformed_vector = [from_vector[0], from_vector[1] - to_vector[1],
                          from_vector[2] - to_vector[2], from_vector[3] - to_vector[3]]
    return transformed_vector

def galilean_coordinate_transformation_3_vector(to_vector, from_vector):
    transformed_vector = [from_vector[0] - to_vector[0],
                          from_vector[1] - to_vector[1], from_vector[2] - to_vector[2]]
    return transformed_vector

def transform(particle, matrix):
    pass


def configure_matrix(from_particle):
    pass


def transform(to_particle, from_particle):
    matrix = configure_matrix(from_particle)
    return transform(from_particle, matrix)

def calculate_gamma(vector):
    return None

def configure_lorentz_transformation_matrix(particle):
    vector = particle.vector
    gamma = calculate_gamma(vector)
    # Calculate the velocities, betas
    matrix = np.array([[gamma, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]])
    
def set_up_config_data(vector_V, vector_Y_for_calculated_V, vector_Y, exp_2yT, argument_type, return_vector_in_minkowski_form=True, convert_incoming_vector_to_lcc=True):
        matrix_configuration_data = LightConeRapidityMatrixConfigurationData()

        match argument_type:
            case util.V:
                matrix_configuration_data.rest_frame_vector = vector_V
            case util.V_PLUS_Y:
                matrix_configuration_data.rest_frame_vector = util.add_vectors(vector_V, vector_Y)
            case util.V_MINUS_Y:
                matrix_configuration_data.rest_frame_vector = util.subtract_vectors(vector_V, vector_Y_for_calculated_V)

        matrix_configuration_data.vector_to_be_transformed = vector_Y
        matrix_configuration_data.convert_incoming_vector_to_lcc = convert_incoming_vector_to_lcc
        matrix_configuration_data.return_vector_in_minkowski_form = return_vector_in_minkowski_form
        matrix_configuration_data.exp_2yT = exp_2yT
        return matrix_configuration_data

def handle_transformation(vector_V, vector_Y, V_particle_name, Y_particle_name, particle_names, experiment, argument_type):
        
    original_vectors = experiment.get_original_four_vectors()
    
    match argument_type:
        case util.V:
            transformed_vectors = transform(vector_V, vector_Y, vector_Y, original_vectors, argument_type)
        case util.V_MINUS_Y:
            # This is a secondary transformation. First we must tranform by (V + Y, Y)
            initial_transformed_vectors = transform(vector_V, vector_Y, vector_Y, original_vectors, util.V_PLUS_Y)
            
            # Set the transformed vectors in the experiment only for the convenience of being able to
            # get the V and Y vectors from there using the lookup. This collision will soon be overwritten
            # with the final one.
            experiment.set_transformed_four_vectors(initial_transformed_vectors, particle_names) # Not numpy for this because using the pathway that comes from the GUI to the model.        
            vector_V_prime = experiment.get_transformed_four_vector(V_particle_name).copy() # These are numpy
            vector_Y_prime = experiment.get_transformed_four_vector(Y_particle_name).copy()
            # We use V' and Y for the next pair.
            transformed_vectors = transform(vector_V_prime, vector_Y_prime, vector_Y, initial_transformed_vectors, argument_type)
        case util.V_PLUS_Y:
            transformed_vectors = transform(vector_V, vector_Y, vector_Y, original_vectors, argument_type)
    
    return transformed_vectors

def transform_vector_set(vector_V, vector_Y, vectors, argument_type):
    match argument_type:
        case util.V:
            vector_Y_for_calculated_V = vector_Y
        case util.V_PLUS_Y:
            vector_Y_for_calculated_V = vector_Y
        case util.V_MINUS_Y:
            vector_Y_for_calculated_V = None #???
    return transform(vector_V, vector_Y_for_calculated_V, vector_Y, vectors, argument_type)

def transform(vector_V, vector_Y_for_calculated_V, vector_Y, vectors, argument_type):
    
        matrix_configuration_data = set_up_config_data(vector_V, vector_Y_for_calculated_V, vector_Y, config.exp_2yT, argument_type)
        matrix = LightConeRapidityMatrix(matrix_configuration_data)

        transformed_vectors_temp = []
        
        for i in range(len(vectors)):
            vec_copy = vectors[i].copy() # Just to be sure no changes are made to original.
            transformed_vec = matrix.transform(vec_copy)
            transformed_vectors_temp.append(transformed_vec.tolist())

        transformed_vectors = np.array(transformed_vectors_temp)
        return transformed_vectors

def validate_vectors(vector_V, vector_Y, argument_type, V_particle_name=None, Y_particle_name=None, experiment=None, particle_names=None):

        vector_V_to_use = None
        vector_Y_to_use = vector_Y
        ret_val = None
        transformation_type = None

        if argument_type == util.V:
            vector_V_to_use = vector_V
            transformation_type = util.V
            ret_val = check_for_errors(vector_V_to_use, vector_Y_to_use)
        else:
            vector_V_to_use_1 = util.add_vectors(vector_V, vector_Y)
            ret_val_1 = check_for_errors(vector_V_to_use_1, vector_Y_to_use)
            # transformation_type = util.V_PLUS_Y Works, but for clarity we moved this down to the two elses below.
            if not ret_val_1:
                if argument_type ==util.V_MINUS_Y:
                    transformation_type = util.V_MINUS_Y
                    
                    # First we must make the V_PLUS_Y transformation; we now know that it won't cause exceptions.
                    original_vectors = experiment.get_original_four_vectors()
                    transformed_vectors = transform(vector_V, vector_Y, vector_Y, original_vectors, util.V_PLUS_Y) # Yes, pass in vector_V, not vector_V_to_use. We will redundantly re-add V and Y. No big deal.
                    experiment.set_transformation([V_particle_name, Y_particle_name], argument_type, transformed_vectors, particle_names)
                    vector_V_prime = experiment.get_transformed_four_vector(V_particle_name).copy()
                    vector_Y_prime = experiment.get_transformed_four_vector(Y_particle_name).copy()
                    # Now check the second transformation.
                    vector_V_to_use = util.subtract_vectors(vector_V_prime, vector_Y_prime)
                    ret_val = check_for_errors(vector_V_to_use, vector_Y_to_use)
                else:
                    transformation_type = util.V_PLUS_Y
            else:
                ret_val = ret_val_1
                transformation_type = util.V_PLUS_Y
        
        return ret_val, transformation_type

def check_for_errors(vector_V_to_use, vector_Y_to_use):
    invalidity_message1 = None
    invalidity_message2 = None
    invalidity_message3 = None
    invalidity_message4 = None

    xyz_magnitude_V = util.calculate_four_vector_xyz_magnitude(vector_V_to_use)
    if xyz_magnitude_V == 0:
        invalidity_message1 = "Magnitude of V is zero"
    elif abs(xyz_magnitude_V) < config.zero_rounding_tolerance:
        invalidity_message1 = "Magnitude of V is ~0 (<" + config.zero_rounding_tolerance_string +")"
    xz_magnitude_V = util.calculate_four_vector_xz_magnitude(vector_V_to_use)
    if xz_magnitude_V == 0:
        invalidity_message2 = "Magnitude of V in x-z plane is zero"
    elif abs(xz_magnitude_V) < config.zero_rounding_tolerance:
        invalidity_message2 = "Magnitude of V in x-z plane is ~0 (<" + config.zero_rounding_tolerance_string +")"
    diff_t_minus_xyz = abs(util.calculate_difference_t_minus_xyz_magnitude(vector_V_to_use))
    if diff_t_minus_xyz == 0:
        invalidity_message3 = "The difference between the time component of V and the xyz magnitude of V is zero"
    elif abs(diff_t_minus_xyz) < config.zero_rounding_tolerance:
        invalidity_message3 = "The difference between the time component of V and the xyz magnitude of V is ~0 (<" + config.zero_rounding_tolerance_string +")"
    numerator_of_YLy = qcd_matrix.calculate_numerator_of_YLy(vector_V_to_use, vector_Y_to_use)
    if numerator_of_YLy == 0:
        invalidity_message4 = "The value of YLy is zero"
    elif abs(numerator_of_YLy) < config.zero_rounding_tolerance:
        invalidity_message4 = "The value of YLy is ~0 (<" + config.zero_rounding_tolerance_string +")"

    ret_val = []
    if invalidity_message1:
        ret_val.append(invalidity_message1)
    if invalidity_message2:
        ret_val.append(invalidity_message2)
    if invalidity_message3:
        ret_val.append(invalidity_message3)
    if invalidity_message4:
        ret_val.append(invalidity_message4)
    return ret_val