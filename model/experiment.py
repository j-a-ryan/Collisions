from model.collision import Collision


"""
Encapsulates the collision: vectors, particles, and
any metadata (name of experiment, filepath, etc.)
"""
class Experiment():

    def __init__(self, vectors, names, metadata):
        # self.original_vectors = vectors # FINAL, do not transform TODO: Needed? delete
        self.metadata = metadata
        self.transformed_collision = None # Just as a reminder
        self.collision = Collision(vectors, names)
    
    def get_collision(self):
        return self.collision

    def get_original_four_vectors(self):
        return self.collision.get_four_vectors()
    
    def get_original_four_vector(self, name):
        return self.collision.get_four_vector(name)

    def get_original_spatial_vectors(self):
        return self.collision.get_vectors_columns()
    
    def set_transformed_four_vectors(self, transformed_vectors, names):
        self.transformed_collision = Collision(transformed_vectors, names)

    def get_transformed_collision(self):
        return self.transformed_collision
    
    def get_transformed_spatial_vectors(self):
        return self.transformed_collision.get_vectors_columns()
    
    def get_particle_names(self):
        return self.collision.get_vectors_name_column()

    def end(self):
        self.lab_collision.clear()