from model.collision import Collision


class Experiment():
    def __init__(self):
        pass

    def set_lab_collision(self, lab_collision):
        self.lab_collision = lab_collision

    def get_collision_vectors(self):
        return self.lab_collision

    def end(self):
        self.lab_collision.clear()