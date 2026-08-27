import numpy as np

import config
from model import qcd_matrix, util
from model.qcd_matrix import (
    LightConeRapidityMatrix,
    LightConeRapidityMatrixConfigurationData,
)
from model.transformations import TransformationEquationSystem


class Transformation:
    """
    Encapsulates the abstraction notion of a transformation: the parameters and processes that are
    comprised it.
    """

    def __init__(self):
        pass


def solve_for_second_step_transformation_exp_2yT(vector_V, vector_Y, third_vector):
    equation_system = TransformationEquationSystem(vector_V, vector_Y, third_vector)
    return equation_system.find_exp_2yT_numerical_3(None)


def set_up_config_data(
    vector_V,
    vector_Y_for_calculated_V,
    vector_Y,
    argument_type,
    third_vector=None,
    boost_parameter_A=None,
    return_vector_in_minkowski_form=True,
    convert_incoming_vector_to_lcc=True,
):
    boost_default_set_message = None
    matrix_configuration_data = LightConeRapidityMatrixConfigurationData()
    matrix_configuration_data.exp_2yT = boost_parameter_A if boost_parameter_A else config.exp_2yT

    match argument_type:
        case util.V:
            matrix_configuration_data.rest_frame_vector = vector_V
        case util.V_PLUS_Y:
            matrix_configuration_data.rest_frame_vector = util.add_vectors(vector_V, vector_Y)
        case util.V_MINUS_Y:
            matrix_configuration_data.rest_frame_vector = util.subtract_vectors(vector_V, vector_Y_for_calculated_V)
            if boost_parameter_A is None:
                if third_vector is not None:  # Otherwise, leave exp_2yT at config default value. Not configured to use system of equations.
                    exp_2yT_found, boost_default_set_message = solve_for_second_step_transformation_exp_2yT(
                        matrix_configuration_data.rest_frame_vector, vector_Y, third_vector
                    )
                    matrix_configuration_data.exp_2yT = exp_2yT_found
                else:  # Use default value
                    matrix_configuration_data.exp_2yT = config.exp_2yT
        case _:
            raise ValueError(f"Unknown argument_type: {argument_type!r}")

    matrix_configuration_data.vector_to_be_transformed = vector_Y
    matrix_configuration_data.convert_incoming_vector_to_lcc = convert_incoming_vector_to_lcc
    matrix_configuration_data.return_vector_in_minkowski_form = return_vector_in_minkowski_form
    return matrix_configuration_data, boost_default_set_message


def handle_transformation(
    vector_V,
    vector_Y,
    V_particle_name,
    Y_particle_name,
    particle_names,
    experiment,
    argument_type,
    third_vector=None,
    boost_parameter_A=None,
):

    original_vectors = experiment.original_four_vectors
    failure_message = None
    match argument_type:
        case util.V:
            transformed_vectors, boost_parameter_A_used, _ = transform(
                vector_V, vector_Y, vector_Y, original_vectors, argument_type, boost_parameter_A=boost_parameter_A
            )
        case util.V_MINUS_Y:
            # This is a secondary transformation. First we must tranform by (V + Y, Y)
            boost_parameter_A_for_first_step_of_two = config.exp_2yT  # We need this to be 1, not what the slider may be sliding to.
            initial_transformed_vectors, _, _ = transform(  # Do not catch boost_parameter_A_used return! That would confound below.
                vector_V, vector_Y, vector_Y, original_vectors, util.V_PLUS_Y, boost_parameter_A=boost_parameter_A_for_first_step_of_two
            )

            # Set the transformed vectors in the experiment only for the convenience of being able to
            # get the V and Y vectors from there using the lookup. This collision will soon be overwritten
            # with the final one. Not numpy for this because using the pathway that comes from the GUI to the model.
            experiment.set_transformed_four_vectors(initial_transformed_vectors, particle_names)
            vector_V_prime = experiment.get_transformed_four_vector(V_particle_name).copy()  # These are numpy
            vector_Y_prime = experiment.get_transformed_four_vector(Y_particle_name).copy()
            # We use V' and Y for the next pair.
            transformed_vectors, boost_parameter_A_used, failure_message = transform(  # Now catch boost_parameter_A_used return.
                vector_V_prime,
                vector_Y_prime,
                vector_Y,
                initial_transformed_vectors,
                argument_type,
                third_vector=third_vector,
                boost_parameter_A=boost_parameter_A,
            )
        case util.V_PLUS_Y:
            transformed_vectors, boost_parameter_A_used, _ = transform(
                vector_V, vector_Y, vector_Y, original_vectors, argument_type, boost_parameter_A=boost_parameter_A
            )
        case _:
            raise ValueError(f"Unknown argument_type: {argument_type!r}")
    return transformed_vectors, boost_parameter_A_used, failure_message


def transform(vector_V, vector_Y_for_calculated_V, vector_Y, vectors, argument_type, third_vector=None, boost_parameter_A=None):

    matrix_configuration_data, failure_message = set_up_config_data(
        vector_V, vector_Y_for_calculated_V, vector_Y, argument_type, third_vector=third_vector, boost_parameter_A=boost_parameter_A
    )
    matrix = LightConeRapidityMatrix(matrix_configuration_data)

    transformed_vectors_temp = []
    for i in range(len(vectors)):
        vec_copy = vectors[i].copy()  # Just to be sure no changes are made to original.
        transformed_vec = matrix.transform(vec_copy)
        transformed_vectors_temp.append(transformed_vec.tolist())

    transformed_vectors = np.array(transformed_vectors_temp)

    return transformed_vectors, matrix_configuration_data.exp_2yT, failure_message


def validate_vectors(
    vector_V,
    vector_Y,
    argument_type,
    V_particle_name=None,
    Y_particle_name=None,
    experiment=None,
    particle_names=None,
    third_vector=None,  # No way to pre-check V - Y with third vector known at the moment
):

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
        ret_val_errors = check_for_errors(vector_V_to_use_1, vector_Y_to_use)
        # transformation_type = util.V_PLUS_Y Works, but for clarity we moved this down to the two elses below.
        if not ret_val_errors:
            if argument_type == util.V_MINUS_Y:
                transformation_type = util.V_MINUS_Y
                assert experiment is not None

                # First we must make the V_PLUS_Y transformation; we now know that it won't cause exceptions.
                original_vectors = experiment.original_four_vectors
                # Yes, pass in vector_V, not vector_V_to_use. We will redundantly re-add V and Y. No big deal.
                transformed_vectors, _, _ = transform(vector_V, vector_Y, vector_Y, original_vectors, util.V_PLUS_Y)
                experiment.set_transformation([V_particle_name, Y_particle_name], argument_type, transformed_vectors, particle_names)
                vector_V_prime = experiment.get_transformed_four_vector(V_particle_name).copy()
                vector_Y_prime = experiment.get_transformed_four_vector(Y_particle_name).copy()
                # Now check the second transformation.
                vector_V_to_use = util.subtract_vectors(vector_V_prime, vector_Y_prime)
                ret_val = check_for_errors(vector_V_to_use, vector_Y_to_use)
            else:
                transformation_type = util.V_PLUS_Y
        else:
            ret_val = ret_val_errors
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
        invalidity_message1 = "Magnitude of V is ~0 (<" + config.zero_rounding_tolerance_string + ")"
    xz_magnitude_V = util.calculate_four_vector_xz_magnitude(vector_V_to_use)
    if xz_magnitude_V == 0:
        invalidity_message2 = "Magnitude of V in x-z plane is zero"
    elif abs(xz_magnitude_V) < config.zero_rounding_tolerance:
        invalidity_message2 = "Magnitude of V in x-z plane is ~0 (<" + config.zero_rounding_tolerance_string + ")"
    diff_t_minus_xyz = abs(util.calculate_difference_t_minus_xyz_magnitude(vector_V_to_use))
    if diff_t_minus_xyz == 0:
        invalidity_message3 = "The difference between the time component of V and the xyz magnitude of V is zero"
    elif abs(diff_t_minus_xyz) < config.zero_rounding_tolerance:
        invalidity_message3 = (
            "The difference between the time component of V and the xyz magnitude of V is ~0 (<"
            + config.zero_rounding_tolerance_string
            + ")"
        )
    numerator_of_YLy = qcd_matrix.calculate_numerator_of_YLy(vector_V_to_use, vector_Y_to_use)
    if numerator_of_YLy == 0:
        invalidity_message4 = "The value of YLy is zero"
    elif abs(numerator_of_YLy) < config.zero_rounding_tolerance:
        invalidity_message4 = "The value of YLy is ~0 (<" + config.zero_rounding_tolerance_string + ")"

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
