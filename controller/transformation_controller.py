

class TransformationController():

    V = "V"
    V_PLUS_Y = "V_plus_Y"
    V_MINUS_Y = "V_minus_Y"

    def __init__(self):
        pass

    def handle_transformation(self, vector_V, vector_Y, original_vectors, argument_type):
        match argument_type:
            case TransformationController.V:
                transformed_vectors = self.transform(vector_V, vector_Y, original_vectors, argument_type)
            case TransformationController.V_MINUS_Y:
                transformed_vectors = self.transform(vector_V, vector_Y, original_vectors, TransformationController.V_PLUS_Y)
                
                # Set the transformed vectors in the experiment only for the convenience of being able to
                # get the V and Y vectors from there using the lookup. This collision will soon be overwritten
                # with the final one.
                self.experiment.set_transformed_four_vectors(transformed_vectors, names) # Not numpy for this because using the pathway that comes from the GUI to the model.        
                vector_V_prime = self.experiment.get_transformed_four_vector(V_particle_name).copy() # These are numpy
                
                # We use V' and Y for the next pair.
                transformed_vectors = self.transform(vector_V_prime, vector_Y, original_vectors, argument_type)
            case TransformationController.V_PLUS_Y:
                transformed_vectors = self.transform(vector_V, vector_Y, original_vectors, argument_type)
        
        self.experiment.set_transformed_four_vectors(transformed_vectors, names) # Not numpy for this because using the pathway that comes from the GUI to the model.  
