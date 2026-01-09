class VectorValidation():

    def __init__(self, *widgets):
        self.widgets = widgets
        self. fields = []

    def add_widget(self, widget):
        self.widgets.append(widget)

    def add_field(self, *fields):
        self.fields.extend(fields)

    def field_updated(self, validly):
        if not validly:
            self.set_widgets_enabled_states(False)
        else:
            # Check each field. If all are valid, enable all widgets
            all_valid = True
            for field in self.fields:
                if not field.currently_valid:
                    all_valid = False
                    break
            # TODO: Do higher-level validation, division by zero, etc.
            if all_valid:
                self.set_widgets_enabled_states(True)

    def set_widgets_enabled_states(self, enabled):
        for widget in self.widgets:
            widget.setEnabled(enabled)