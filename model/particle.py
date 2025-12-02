# TODO: Consider whether vectors should be tuples, to enforce immutable size.
# Most likely dictionary. List also has merits.
# Particle IDs have to be 0-based integers: 0, 1, 2... to be in synch with Matplotlib
# and Mplcursors which take arrays of x, y, and z coords as zero-based. User clicks
# on point in plot, Mplcursors provides the point ID. That ID is used by the model
# to identify the particle to set as the rest-frame particle.
class Particle():
    def __init__(self, id, type, vector, rest):
        self.id = id
        self.type = type
        self.vector = vector
        self.rest = rest

    def vector_len(self):
        return len(self.vector)
    
    def get_vector(self):
        return self.vector
    
