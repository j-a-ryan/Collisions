import numpy as np

from model.collision import Collision


class Experiment:
    """
    Encapsulates the collision: vectors, particles, and
    any metadata (name of experiment, filepath, etc.)
    """

    def __init__(self, vectors, names, metadata=None):
        # self.original_vectors = vectors # FINAL, do not transform TODO: Needed? delete
        self.metadata = metadata

        # TODO: These are a transformation. Make a transformation class
        self.transformed_collision = None  # Just as a reminder
        self.collision = Collision(vectors, names)
        self.V_Y_particle_names = None
        self.argument_type = None
        self.boost_parameter_A = None

    def get_original_vectors(self):
        names = self.particle_names
        vectors = []
        for name in names:
            vec_temp = self.get_original_four_vector(name)
            vectors.append(np.append(vec_temp, name))
        return vectors

    @property
    def original_four_vectors(self):
        return self.collision.vectors

    def get_original_four_vector(self, name):
        return self.collision.get_four_vector(name)

    @property
    def has_transformation(self):
        return self.transformed_collision is not None

    def clear_transformation(self):
        if self.has_transformation:
            del self.transformed_collision
            self.transformed_collision = None
            self.argument_type = None
            self.V_Y_particle_names = None
            self.boost_parameter_A = None

    def set_transformation(self, V_Y_particle_names, argument_type, transformed_vectors, names):
        self.set_transformed_four_vectors(transformed_vectors, names)
        self._record_transformation_arguments(V_Y_particle_names, argument_type)

    def _record_transformation_arguments(
        self, V_Y_particle_names, argument_type
    ):  # TODO These could be in the Collision object but it doesn't matter. Only one transformed Collision per experiment.
        self.V_Y_particle_names = V_Y_particle_names
        self.argument_type = argument_type

    def set_transformed_four_vectors(self, transformed_vectors, names):
        self.transformed_collision = Collision(transformed_vectors, names)

    def get_transformed_four_vector(self, name):
        assert self.transformed_collision is not None
        return self.transformed_collision.get_four_vector(name)

    @property
    def particle_names(self):
        return self.collision.names
