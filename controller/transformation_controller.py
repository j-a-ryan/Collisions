from model import transformation


class TransformationController:

    def __init__(self, experiment_controller):
        self.experiment_controller = experiment_controller

    def handle_transformation(
        self,
        vector_V,
        vector_Y,
        V_particle_name,
        Y_particle_name,
        particle_names,
        experiment,
        argument_type,
        third_vector=None,
    ):
        transformed_vectors, failure_message = transformation.handle_transformation(
            vector_V,
            vector_Y,
            V_particle_name,
            Y_particle_name,
            particle_names,
            experiment,
            argument_type,
            third_vector,
        )
        if not failure_message:
            experiment.set_transformation(
                [V_particle_name, Y_particle_name], argument_type, transformed_vectors, particle_names
            )  # Not numpy for this because using the pathway that comes from the GUI to the model.
        return failure_message

    def validate_vectors(
        self,
        vector_V,
        vector_Y,
        argument_type,
        V_particle_name=None,
        Y_particle_name=None,
        experiment=None,
        particle_names=None,
        third_vector=None,
    ):
        return transformation.validate_vectors(
            vector_V, vector_Y, argument_type, V_particle_name, Y_particle_name, experiment, particle_names
        )

    def transformation_exists(self, experiment):
        return experiment.has_transformation()

    """
    Assumes transformation exists. Call transformation_exists() first.
    """

    def retransform_experiment_vectors(self, vector_V, vector_Y, V_particle_name, Y_particle_name, names, experiment):
        transformation_type = experiment.get_transformation_type()
        failure_mesage = self.handle_transformation(
            vector_V, vector_Y, V_particle_name, Y_particle_name, names, experiment, transformation_type
        )
        return failure_mesage
