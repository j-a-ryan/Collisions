import sys

from PySide6.QtWidgets import QApplication, QButtonGroup, QCheckBox, QDialog, QDialogButtonBox, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from PySide6.QtGui import Qt


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
        
        vectors_label = QLabel("Vectors:")
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
        V_Y_hbox.setSpacing(0)
        swap_button = QPushButton("Swap V \u2194 Y")
        swap_button.setFixedWidth(100)
        swap_button.clicked.connect(self.on_reversed)
        
        V_Y_hbox.addWidget(self.vector_pair_label)
        V_Y_hbox.addWidget(swap_button)
        V_Y_hbox.addStretch()
        layout.addLayout(V_Y_hbox)

        config_args_label = QLabel("Configuration arguments:")
        config_args_label_font = QLabel().font()
        config_args_label_font.setItalic(True)
        config_args_label_font.setPointSize(12)
        config_args_label.setFont(config_args_label_font)
        self.rest_frame_checkboxes_group = QButtonGroup()
        self.rest_frame_checkboxes_group.setExclusive(True)
        self.V_rest_frame_checkbox = QCheckBox("(V, Y)")
        self.V_rest_frame_checkbox.setChecked(True)
        self.V_plus_Y_rest_frame_checkbox = QCheckBox("(V + Y, Y)")
        self.V_plus_Y_rest_frame_checkbox.checkStateChanged.connect(self.two_step_transformation_check)
        self.rest_frame_checkboxes_group.addButton(self.V_rest_frame_checkbox)
        self.rest_frame_checkboxes_group.addButton(self.V_plus_Y_rest_frame_checkbox)
        layout.addSpacing(15)
        layout.addWidget(config_args_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        
        layout.addWidget(self.V_rest_frame_checkbox)
        hbox_arguments = QHBoxLayout()
        hbox_arguments.setSpacing(0)
        hbox_arguments.addWidget(self.V_plus_Y_rest_frame_checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
        self.post_transformation_checkbox = QCheckBox("(V' - Y', Y)")
        self.post_transformation_checkbox.setEnabled(False)
        arrow_label = QLabel("\u2192")
        arrow_label_font = arrow_label.font()
        # arrow_label_font.setItalic(True)
        arrow_label_font.setPointSize(16)
        arrow_label.setFont(arrow_label_font)
        hbox_arguments.addWidget(arrow_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        hbox_arguments.addWidget(self.post_transformation_checkbox, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(hbox_arguments)
        layout.addWidget(self.post_transformation_checkbox)

        self.submit_cancel_button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.submit_cancel_button_box.accepted.connect(self.accept)
        self.submit_cancel_button_box.rejected.connect(self.reject)
        layout.addWidget(self.submit_cancel_button_box, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)

    def two_step_transformation_check(self):
        if self.V_plus_Y_rest_frame_checkbox.isChecked():
            self.post_transformation_checkbox.setEnabled(True)
        else:
            self.post_transformation_checkbox.setChecked(False)
            self.post_transformation_checkbox.setEnabled(False)

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
        self.transformation_config["RestFrameV+Y"] = self.V_plus_Y_rest_frame_checkbox.isChecked()
        self.transformation_config["ApplyPostTransformation"] = self.post_transformation_checkbox.isChecked()
        
        super().accept()

    def on_reversed(self):
        if self.vector_pair_label.text() == self.pairing_text_base_case:
            self.vector_pair_label.setText(self.pairing_text_switched)
        else:
            self.vector_pair_label.setText(self.pairing_text_base_case)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_dialog = ConfigureTransformationPopup([0, 1], ["k2", "k1"])
    if main_dialog.exec() == QDialog.Accepted:
        print("User okayed")
    else:
        print("User cancelled.")

    sys.exit(app.exec())