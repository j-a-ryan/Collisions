from model.collision import create_collision
from model.experiment import Experiment
from model.transformation import galilean_coordinate_transformation_3, galilean_coordinate_transformation_3_vector


class ExperimentController():

    def __init__(self, view):
        self.view = view
        self.experiment = Experiment()

    def plot_current_experiment(self):
        print("plot_current_experiment")
        self.experiment = Experiment()
        collision = create_collision([[0, 0, 0], [3, 4, 5], [5, 3, 3]], 0)
        self.experiment.set_lab_collision(collision)
        # self.experiment.set_lab_collision([[0, 0, 0], [3, 4, 5], [5, 3, 3]])
        self.view.plot_experiment_vectors(self.get_experiment_vectors())

    def plot_transformation(self, particle_id):

        # transformed_vectors = []
        # for vec in self.get_experiment_vectors():
        #     transf_vector = galilean_coordinate_transformation_3_vector()


        self.view.plot_transformed_experiment_vectors(self.get_experiment_vectors())
    
    def close_current_experiment(self):
        self.view.clear_experiment_plot()
    
    def get_experiment_vectors(self):
        vectors = self.experiment.get_collision_vectors()
        return vectors

    
        
