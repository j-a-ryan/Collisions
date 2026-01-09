from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt

class VectorMemberField(QLineEdit):
    def __init__(self, form_validation, *args, **kwargs):
        super(VectorMemberField, self).__init__(*args, **kwargs)
        self.currently_valid = False
        self.form_validation = form_validation
        # self.setMaxLength(10) # Not needed if decimal places limit suffices.
        # self.setPlaceholderText("-10 to 10, maximum four decimal places")
        self.validator = QDoubleValidator(-100, 100, 4, notation=QDoubleValidator.StandardNotation)
        self.setValidator(self.validator)
        self.textChanged.connect(self.new_text)
        # self.returnPressed.connect(self.check_validator) Not needed
        self.latest_text = None

    def new_text(self, text):
        if self.hasAcceptableInput():
            self.latest_text = text
            self.currently_valid = True
            self.form_validation.field_updated(True)
        else:
            self.currently_valid = False
            self.form_validation.field_updated(False)

    # def check_validator(self):
    #     try:
    #         if float(self.text()) > self.validator.top():
    #             self.setText(str(self.validator.top()))
    #         elif float(self.text()) < self.validator.bottom():
    #             self.setText(str(self.validator.bottom()))
    #     except:
    #         mssg = QMessageBox.about(self, "Error", "Input can only be a number")
    #         self.setText(self.latest_text)
# '''
    # # Override keyPressEvent to check input and send message if it's invalid.
    # Not needed
    # # '''  
    # def keyPressEvent(self, event):
    #     super().keyPressEvent(event)
    #     if event.key() == Qt.Key_Return and not self.hasAcceptableInput():
    #         print("Hey")
    #         # self.check_validator()
