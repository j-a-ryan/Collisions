from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class AbstractTransformationPopup(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

    def argument_types_checkboxes_group_clicked(self):
        pass

    def two_step_transformation_check(self):
        pass

    def create_argument_type_checkboxes(self, vbox_layout):

        config_args_label = QLabel("Configuration arguments")
        config_args_label_font = QLabel().font()
        config_args_label_font.setItalic(True)
        config_args_label_font.setPointSize(12)
        config_args_label.setFont(config_args_label_font)
        self.argument_types_checkboxes_group = QButtonGroup()
        self.argument_types_checkboxes_group.setExclusive(True)
        self.V_Y_argument_type_checkbox = QCheckBox("(V, Y)")
        self.V_Y_argument_type_checkbox.setChecked(True)
        self.V_plus_Y_argument_type_checkbox = QCheckBox("(V + Y, Y)")
        self.V_plus_Y_argument_type_checkbox.checkStateChanged.connect(self.two_step_transformation_check)

        self.argument_types_checkboxes_group.addButton(self.V_Y_argument_type_checkbox)
        self.argument_types_checkboxes_group.addButton(self.V_plus_Y_argument_type_checkbox)
        self.argument_types_checkboxes_group.buttonClicked.connect(self.argument_types_checkboxes_group_clicked)

        vbox_layout.addWidget(config_args_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        vbox_layout.addWidget(self.V_Y_argument_type_checkbox)
        hbox_arguments = QHBoxLayout()
        hbox_arguments.setSpacing(0)
        hbox_arguments.addWidget(self.V_plus_Y_argument_type_checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
        self.post_transformation_checkbox = QCheckBox("(V' - Y', Y)")
        self.post_transformation_checkbox.setEnabled(False)
        arrow_label = QLabel("\u2192")
        arrow_label_font = arrow_label.font()
        # arrow_label_font.setItalic(True)
        arrow_label_font.setPointSize(16)
        arrow_label.setFont(arrow_label_font)
        hbox_arguments.addWidget(arrow_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        hbox_arguments.addWidget(self.post_transformation_checkbox, alignment=Qt.AlignmentFlag.AlignRight)
        vbox_layout.addLayout(hbox_arguments)


class ConfigureTransformationPopup(AbstractTransformationPopup):
    def __init__(self, indices_of_v_y_pair, all_particle_names, parent=None):
        super().__init__(parent)

        # Basics
        # self.resize(300, 200)
        self.setWindowTitle("Configure Transformation")
        self.original_first_particle = all_particle_names[indices_of_v_y_pair[0]]
        self.original_second_particle = all_particle_names[indices_of_v_y_pair[1]]

        self.transformation_config = {}
        self.transformation_config["V"] = self.original_first_particle  # TODO: Need static final constants
        self.transformation_config["Y"] = self.original_second_particle

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        vectors_label = QLabel("Vectors")
        vectors_label_font = QLabel().font()
        vectors_label_font.setItalic(True)
        vectors_label_font.setPointSize(12)
        vectors_label.setFont(vectors_label_font)
        layout.addWidget(vectors_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.pairing_text_base_case = "V=" + self.original_first_particle + "  Y=" + self.original_second_particle
        self.pairing_text_switched = "V=" + self.original_second_particle + "  Y=" + self.original_first_particle
        self.vector_pair_label = QLabel(self.pairing_text_base_case)
        self.vector_pair_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
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

        self.create_argument_type_checkboxes(layout)

        # layout.addLayout(self.arg_type_checkboxes)

        self.submit_cancel_button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.submit_cancel_button_box.accepted.connect(self.accept)
        self.submit_cancel_button_box.rejected.connect(self.reject)
        layout.addWidget(self.submit_cancel_button_box, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)

    def on_reversed(self):  # Swap the V, Y names in the GUI label and in the config dictionary.
        if self.vector_pair_label.text() == self.pairing_text_base_case:
            self.vector_pair_label.setText(self.pairing_text_switched)
            self.transformation_config["V"] = self.original_second_particle
            self.transformation_config["Y"] = self.original_first_particle
        else:  # It's not currently base case, so change it to base case.
            self.vector_pair_label.setText(self.pairing_text_base_case)
            self.transformation_config["V"] = self.original_first_particle  # TODO: Need static final constants for these terms
            self.transformation_config["Y"] = self.original_second_particle

    def accept(self):
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
