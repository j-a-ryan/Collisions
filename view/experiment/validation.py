class VectorValidation():

    def __init__(self, vectors_grid):
        self.vectors_grid = vectors_grid
        self.fields = []

    def add_widget(self, widget):
        self.widgets_to_enable_disable.append(widget)

    def add_fields(self, *fields):
        self.fields.extend(fields)

    def remove_field(self, field):
        if field in self.fields: # Shouldn't be necessary, but error if not in list
            self.fields.remove(field)

    def update_fields_list(self, updated_list):
        self.fields.clear()
        self.add_fields(updated_list)

    def field_updated(self, validly):
        if not validly:
            self.vectors_grid.set_widgets_enabled_states(False)
        else:
            self.run_validation()    

    # Check each field. If all are valid, tell the vectors object
    # to update its backing grid and ensure widgets' enabled state is
    # correct.
    def run_validation(self, backing_grid_update_prudent=True):
        all_valid = True
        for field in self.fields:
            if not field.currently_valid:
                all_valid = False
                break
        
        if all_valid:
            if backing_grid_update_prudent:
                self.vectors_grid.update_backing_grid() 
        self.vectors_grid.set_widgets_enabled_states(all_valid)

def check_higher_order_validity():
    pass # # TODO: Do higher-level validation, division by zero, etc.