

# TODO: Make configurable to use any VT of the three possible
# VT values. Currently VT = (Vx, Vy)
import math

sqrt2 = math.sqrt(2)

def convert_minkowski_to_light_cone_coordinates(vector):
    return [(vector[0] + vector[3]) / sqrt2, (vector[0] - vector[3]) / sqrt2, vector[1], vector[2]]

def convert_light_cone_coordinates_to_minkowski_form(vector):
    return [(vector[0] + vector[1]) * sqrt2 / 2, vector[2], vector[3],  (vector[0] - vector[1]) * sqrt2 / 2]