# TODO: Consider whether vectors should be tuples, to enforce immutable size.
# Most likely dictionary. List also has merits.
# Particle IDs have to be 0-based integers: 0, 1, 2... to be in synch with Matplotlib
# and Mplcursors which take arrays of x, y, and z coords as zero-based. User clicks
# on point in plot, Mplcursors provides the point ID. That ID is used by the model
# to identify the particle to set as the rest-frame particle.


class Particle:
    def __init__(self, index, name, vector):
        self._index = index
        self._name = name
        self._four_vector = vector

    # @property
    # def id(self):
    #     return self._id

    # @property
    # def type(self):
    #     return self._type

    @property
    def four_vector(self):
        return self._four_vector

    @property
    def spacial_vectors_xyz(self):
        return self._four_vector[1:4]
