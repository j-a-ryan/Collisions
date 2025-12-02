from model.particle import Particle
import numpy as np

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
    from_particle_transformed = Particle(
        from_particle.id, from_particle.type, transformed_vector, False)
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