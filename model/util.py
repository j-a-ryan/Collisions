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


"""
Takes Numpy arrays or Python lists, appends column to end of list.
"""


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


def calculate_m_2(vector):  # return minkowski_dot(vector, vector)
    return minkowski_dot(vector, vector)


def minkowski_dot(v1, v2):
    return v1[0] * v2[0] - v1[1] * v2[1] - v1[2] * v2[2] - v1[3] * v2[3]


def calculate_t_from_m_2_and_xyz(m_2, x, y, z):
    return math.sqrt(m_2 + x**2 + y**2 + z**2)


def calculate_m2_slider_limits(x, y, z):
    # ceil avoids rounding error pushing t2 < 0 in calculate_t_from_m_2_and_xyz's sqrt.
    m2_min = math.ceil(-(x**2 + y**2 + z**2))
    m2_max = config.t_max**2 + m2_min
    return m2_min, m2_max
