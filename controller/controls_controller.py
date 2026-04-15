

'''
Unfortunately but accurately named, serves the GUI's controls widgets,
the widgets that manipulate the graphed vectors.
'''
class ControlsController():

    def __init__(self, experiment_controller):
        self.experiment_controller = experiment_controller
        self.experiment_controller.set_controls_controller(self)

    def change_vector_member_value(self, vector_name, axis, new_value):
        # Get vector and member from exp controller. Update value. The reference should stick.
        vector = self.experiment_controller.get_vector(vector_name)
        vector[axis] = new_value # The vector has now been altered by the control.

        # Tell exp controller to re-transform the collision vectors
        # and redraw the transformation graph if there is any such.
        success = True
        transformation_type = None
        if self.experiment_controller.transformation_exists():
            results, transformation_type = self.experiment_controller.pre_check_transformation_update() # Ignore the transformation type return
            if results:
                # Send failure back to view, which should show a popup, stopping the thread.
                # User's closing the popup should cancel any update(s).
                success = False
            else:
                # Tell exp controller to redraw the graphs
                self.experiment_controller.plot_current_experiment()
                self.experiment_controller.refresh_transformation()
        else:
            # Tell exp controller to redraw the graph
            self.experiment_controller.plot_current_experiment()
        return success, transformation_type

    def set_up_controls(self, view, experiment):
        vectors_xyz = experiment.get_spatial_vectors() # np array
        names = experiment.get_particle_names()
        view.set_up_controls(names, vectors_xyz)