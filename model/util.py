

# TODO: Make configurable to use any VT of the three possible
# VT values. Currently VT = (Vx, Vy)
import math

import numpy as np

import config

V = "(V, Y)"
V_PLUS_Y = "(V + Y, Y)"
V_MINUS_Y = "(V' - Y', Y)"

def get_config_argument(V_plus_Y, V_minus_Y):
    argument_type = V
    if V_plus_Y:
        if V_minus_Y:
            argument_type = V_MINUS_Y
        else:
            argument_type = V_PLUS_Y
    return argument_type

'''
Takes Numpy arrays or Python lists, appends column to end of list.
'''
def append_column_to_2d_array(two_d_array, column):
    np.append(np.array(two_d_array), np.array(column), axis=1)

def convert_minkowski_to_light_cone_coordinates(vector):
    return np.array([(vector[0] + vector[3]) / config.sqrt2, (vector[0] - vector[3]) / config.sqrt2, vector[1], vector[2]])

def convert_light_cone_coordinates_to_minkowski_form(vector):
    return np.array([(vector[0] + vector[1]) * config.sqrt2 / 2, vector[2], vector[3], (vector[0] - vector[1]) * config.sqrt2 / 2])

def calculate_four_vector_xyz_magnitude(four_vector):
    return math.sqrt(math.pow(four_vector[1], 2) + math.pow(four_vector[2], 2) + math.pow(four_vector[3], 2))

def calculate_four_vector_xz_magnitude(four_vector):
    return math.sqrt(math.pow(four_vector[1], 2) + math.pow(four_vector[3], 2))

def calculate_difference_t_minus_xyz_magnitude(four_vector):
    return four_vector[0] - calculate_four_vector_xyz_magnitude(four_vector)

def add_vectors(vector_1, vector_2):
    return [x + y for x, y in zip(vector_1, vector_2)]

def subtract_vectors(vector_1, vector_2):
    return [x - y for x, y in zip(vector_1, vector_2)]