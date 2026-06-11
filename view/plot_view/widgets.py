from PySide6.QtWidgets import QButtonGroup, QCheckBox, QDialog, QDialogButtonBox, QFrame, QHBoxLayout, QLabel, QProgressBar, QPushButton, QVBoxLayout
from PySide6.QtGui import Qt

import config
from PySide6.QtCore import QThread, Signal, Slot

class ConfigureTransformationPopup(QDialog):
    def __init__(self, indices, particle_names, parent=None):
        super().__init__(parent)
        self.transformation_config = {}
        
        # Basics
        # self.resize(300, 200)
        self.setWindowTitle("Configure Transformation")
        self.first_particle = particle_names[indices[0]]
        self.second_particle = particle_names[indices[1]]
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        vectors_label = QLabel("Vectors")
        vectors_label_font = QLabel().font()
        vectors_label_font.setItalic(True)
        vectors_label_font.setPointSize(12)
        vectors_label.setFont(vectors_label_font)
        layout.addWidget(vectors_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.pairing_text_base_case = "V=" + self.first_particle + "  Y=" + self.second_particle
        self.pairing_text_switched = "V=" + self.second_particle + "  Y=" + self.first_particle
        self.vector_pair_label = QLabel(self.pairing_text_base_case)
        self.vector_pair_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.vector_pair_label.setLineWidth(1)
        label_top_center_font = QLabel().font()
        label_top_center_font.setPointSize(16)
        self.vector_pair_label.setFont(label_top_center_font)
        
        V_Y_hbox = QHBoxLayout()
        V_Y_hbox.setSpacing(5)
        swap_button = QPushButton("Swap V \u2194 Y")
        swap_button.setFixedWidth(100)
        swap_button.clicked.connect(self.on_reversed)
        
        V_Y_hbox.addWidget(self.vector_pair_label)
        V_Y_hbox.addWidget(swap_button)
        V_Y_hbox.addStretch()
        layout.addLayout(V_Y_hbox)
        layout.addSpacing(25)

        create_argument_type_checkboxes(self, layout)

        # layout.addLayout(self.arg_type_checkboxes)

        self.submit_cancel_button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.submit_cancel_button_box.accepted.connect(self.accept)
        self.submit_cancel_button_box.rejected.connect(self.reject)
        layout.addWidget(self.submit_cancel_button_box, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)

    def on_reversed(self):
        if self.vector_pair_label.text() == self.pairing_text_base_case:
            self.vector_pair_label.setText(self.pairing_text_switched)
        else:
            self.vector_pair_label.setText(self.pairing_text_base_case)

    def accept(self):
        if self.vector_pair_label.text() == self.pairing_text_base_case:
            self.transformation_config["V"] = self.first_particle # TODO: Need static final constants for these terms
            self.transformation_config["Y"] = self.second_particle
        else:
            self.transformation_config["V"] = self.second_particle
            self.transformation_config["Y"] = self.first_particle
        self.transformation_config["VConfig"] = self.V_Y_argument_type_checkbox.isChecked()
        self.transformation_config["V+YConfig"] = self.V_plus_Y_argument_type_checkbox.isChecked()
        self.transformation_config["ApplyPostTransformationV'-Y'"] = self.post_transformation_checkbox.isChecked()
        
        super().accept()
    
    def two_step_transformation_check(self):
        if self.V_plus_Y_argument_type_checkbox.isChecked():
            self.post_transformation_checkbox.setEnabled(True)
        else:
            self.post_transformation_checkbox.setChecked(False)
            self.post_transformation_checkbox.setEnabled(False)

    def post_transformation_check(self):
        if self.post_transformation_checkbox.isChecked():
            # Show third-vector selection dropdown and make it a required field
            pass
        else:
            pass # Hide third-vector selection dropdown and make it not required field.

def create_argument_type_checkboxes(parent_form, parent_form_vbox_layout):

    config_args_label = QLabel("Configuration arguments")
    config_args_label_font = QLabel().font()
    config_args_label_font.setItalic(True)
    config_args_label_font.setPointSize(12)
    config_args_label.setFont(config_args_label_font)
    parent_form.argument_types_checkboxes_group = QButtonGroup()
    parent_form.argument_types_checkboxes_group.setExclusive(True)
    parent_form.V_Y_argument_type_checkbox = QCheckBox("(V, Y)")
    parent_form.V_Y_argument_type_checkbox.setChecked(True)
    parent_form.V_plus_Y_argument_type_checkbox = QCheckBox("(V + Y, Y)")
    parent_form.V_plus_Y_argument_type_checkbox.checkStateChanged.connect(parent_form.two_step_transformation_check)
    
    parent_form.argument_types_checkboxes_group.addButton(parent_form.V_Y_argument_type_checkbox)
    parent_form.argument_types_checkboxes_group.addButton(parent_form.V_plus_Y_argument_type_checkbox)
    
    parent_form_vbox_layout.addWidget(config_args_label, alignment=Qt.AlignmentFlag.AlignHCenter)
    
    parent_form_vbox_layout.addWidget(parent_form.V_Y_argument_type_checkbox)
    hbox_arguments = QHBoxLayout()
    hbox_arguments.setSpacing(0)
    hbox_arguments.addWidget(parent_form.V_plus_Y_argument_type_checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
    parent_form.post_transformation_checkbox = QCheckBox("(V' - Y', Y)")
    parent_form.post_transformation_checkbox.setEnabled(False)
    parent_form.post_transformation_checkbox.checkStateChanged.connect(parent_form.post_transformation_check)
    arrow_label = QLabel("\u2192")
    arrow_label_font = arrow_label.font()
    # arrow_label_font.setItalic(True)
    arrow_label_font.setPointSize(16)
    arrow_label.setFont(arrow_label_font)
    hbox_arguments.addWidget(arrow_label, alignment=Qt.AlignmentFlag.AlignHCenter)
    hbox_arguments.addWidget(parent_form.post_transformation_checkbox, alignment=Qt.AlignmentFlag.AlignRight)
    parent_form_vbox_layout.addLayout(hbox_arguments)

class WaitingPopup(QDialog):
    def __init__(self, parent, title="Please Wait", text="Please stand by.", additional_text=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 150)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        label = QLabel(text)
        larger_font = QLabel().font()
        larger_font.setPointSize(12)
        label.setFont(larger_font)
        layout.addWidget(label)
        if additional_text:
            layout.addWidget(QLabel(additional_text))
        # Initialize the Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {config.slider_accent_color};
                width: 20px;
            }}
        """)
        self.progress_bar.setMinimum(0)   # Default start point
        self.progress_bar.setMaximum(0) # Default end point
        self.progress_bar.setValue(0)     # Reset starting value
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    @Slot()
    def close_dialog(self):
        self.accept() 
