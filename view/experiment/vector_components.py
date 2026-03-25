from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt
import config

class VectorMemberField(QLineEdit):
    def __init__(self, form_validation, already_validated=False, *args, **kwargs):
        super(VectorMemberField, self).__init__(*args, **kwargs)
        self.currently_valid = already_validated
        self.form_validation = form_validation
        # self.setMaxLength(10) # Not needed if decimal places limit suffices.
        # self.setPlaceholderText("-10 to 10, maximum four decimal places")
        self.validator = QDoubleValidator(config.xyz_min, config.xyz_max, config.xyz_decimal_precision, notation=QDoubleValidator.StandardNotation)
        self.setValidator(self.validator)

        # textChanged() is emited whenever the contents of the widget changes whereas textEdited() is emited only when the user changes the text using mouse and keyboard (so it is not emitted when you call QLineEdit::setText())
        self.textEdited.connect(self.new_text) # Perhaps textEdited might be enough here.
        # self.returnPressed.connect(self.check_validator) Not needed
        self.latest_text = None # TODO: Needed anymore?

    def new_text(self, text, run_form_validation=True):
        if self.hasAcceptableInput():            
            self.latest_text = text
            self.currently_valid = True
            if run_form_validation:
                self.form_validation.field_updated(True)
        else:
            self.currently_valid = False
            if run_form_validation:
                self.form_validation.field_updated(False)
