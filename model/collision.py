from model.particle import Particle


class Collision():

    def __init__(self):
        self.particles = {}
        self.vectors = []

    def add_id_particle(self, id, particle):
        self.particles.update({id: particle})

    def add_id_type_vector(self, id, type, vector, is_rest):
        self.add_id_particle(id, Particle(id, type, vector, is_rest))
        self.vectors.append(vector) # or init the Collision with num vecs and use self.vectors[id] = vector

    def add_particle(self, particle):
        self.add(particle.id, particle)

    def clear(self):
        self.particles.clear()

    def get_particles(self):
        return self.particles

    def get(self, id):
        return self.particles[id]

    def num_particles(self):
        return len(self.particles)
    
    def set_id_of_origin_vector(self, id_of_origin_vector):
        self.id_of_origin_vector = id_of_origin_vector
    
    def get_id_of_origin_vector(self):
        return self.id_of_origin_vector

    def get_vectors(self):
        return self.vectors
    
def create_collision(vectors, id_of_origin_vector):
    collision = Collision()
    collision.set_id_of_origin_vector(id_of_origin_vector)
    for i in range(len(vectors)):
        is_origin = i == id_of_origin_vector
        if i == 0:
            collision.add_id_type_vector(i, 'L', vectors[i], is_origin)
        else:
            collision.add_id_type_vector(i, f"h{i}", vectors[i], is_origin)
    return collision

# def get_vectors(collision):
#     particles = collision.get_particles()
#     vectors = []
#     for particle in particles.values():
#         vectors.append(particle.get_vectorI())
#     return vectors
