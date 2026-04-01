from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QColor, QDoubleValidator, QFontInfo, QPalette
from PySide6.QtCore import Qt
import config

class VectorMemberField(QLineEdit):
    def __init__(self, form_validation, already_validated=False, *args, **kwargs):
        super(VectorMemberField, self).__init__(*args, **kwargs)
        self.setFixedHeight(16) # default was too tall
        current_font = self.font()
        # font_info = QFontInfo(current_font)
        # point_size = font_info.pointSize()
        # print(point_size)
        current_font.setPointSize(11) # Sets the font size to 16 points
        self.setFont(current_font) 
        self.setStyleSheet("QLineEdit:focus { color: black; background-color: PaleTurquoise; }")
        self.default_background_color = None
        self.default_font_color = None
        self.default_style_string = None
        self.currently_valid = already_validated
        self.form_validation = form_validation
        self.validator = QDoubleValidator(config.xyz_min, config.xyz_max, config.xyz_decimal_precision, notation=QDoubleValidator.StandardNotation)
        self.setValidator(self.validator)

        self.textEdited.connect(self.new_text) # Perhaps textEdited might be enough here.
        self.latest_text = None # TODO: Needed anymore?

    def new_text(self, text, run_form_validation=True):
        
        if self.default_background_color is None: #line_edit.setStyleSheet("color: white; background-color: black;")
            self.default_background_color = self.palette().color(QPalette.ColorRole.Base).name()
            self.default_font_color = self.palette().color(QPalette.ColorGroup.Current, QPalette.ColorRole.Text).name()
            self.default_style_string = "QLineEdit { color: " + self.default_font_color + "; background-color: " + self.default_background_color + "; } QLineEdit:focus { color: black; background-color: PaleTurquoise; }"
        if self.hasAcceptableInput():
            self.setStyleSheet(self.default_style_string)           
            self.latest_text = text
            self.currently_valid = True
            if run_form_validation:
                self.form_validation.field_updated(True)
        else:
            self.currently_valid = False
            style_string = "QLineEdit { color: red; background-color: LightYellow; } QLineEdit:focus { color: red; background-color: PaleTurquoise; }"
            self.setStyleSheet(style_string)
            if run_form_validation:
                self.form_validation.field_updated(False)
