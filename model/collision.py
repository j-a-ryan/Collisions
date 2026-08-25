import numpy as np

import config
from model.particle import Particle


class Collision:

    tolerance = config.zero_rounding_tolerance

    def __init__(self, vectors, names):  # Vector includes name element [t, x, y, z, name]
        self.particles = {}  # We keep the particles but...
        self.vectors: np.ndarray | None = np.array(vectors)
        self.names = names
        for i in range(
            len(vectors)
        ):  # TODO: We need a dictionary or similar to be promoted from here to Vectors itself, so that we don't depend on order of names corresponding to order of vectors.
            self.create_particle(i, self.names[i], self.vectors[i])

    def create_particle(self, index, name, vector):
        self.particles.update({name: Particle(index, name, vector)})

    def clear(self):
        self.particles.clear()
        self.vectors = None

    def get_four_vector(self, name):
        return self.particles[name].four_vector

    def get_vectors_column(self, col_num, round_near_zeros_to_zero=True):  # Matplotlib needs the xs, the ys and the zs separately
        assert self.vectors is not None
        arr = np.array(self.vectors[:, col_num])  # copy array
        if round_near_zeros_to_zero:
            arr[np.abs(arr) < self.tolerance] = 0
        return arr

    def get_vectors_spatial_columns(self):
        xyz = {}
        xyz["x"] = self.get_vectors_column(1)
        xyz["y"] = self.get_vectors_column(2)
        xyz["z"] = self.get_vectors_column(3)
        return xyz

    def get_spatial_vectors_xyz(self, round_near_zeros_to_zero=True):
        """
        Copy the x, y, z values into fresh array. Presumed to be for
        plotting, the near-zeros (e.g. 1e-16) should be rounded to zero
        so that the 1e-16 doesn't show up at top of Matplotlib plot
        """
        assert self.vectors is not None
        np_arr = self.vectors
        spatial_vectors_to_return = spatial_vectors = np_arr[:, 1:].tolist()

        if round_near_zeros_to_zero:
            tolerance = 1e-5  # Could be made a parameter of the method
            np_arr = np.array(spatial_vectors)
            np_arr[np.abs(np_arr) < tolerance] = 0
            spatial_vectors_to_return = np_arr

        return spatial_vectors_to_return
