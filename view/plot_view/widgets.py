import sys

from PySide6.QtWidgets import QApplication, QCheckBox, QDialog, QDialogButtonBox, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from PySide6.QtGui import Qt


class ConfigureTransformationPopup(QDialog):
    def __init__(self, indices, particle_names, parent=None):
        super().__init__(parent)
        self.transformation_config = {}
        
        # Basics
        self.resize(300, 200)
        self.setWindowTitle("Configure Transformation")
        self.first_particle = particle_names[indices[0]]
        self.second_particle = particle_names[indices[1]]
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        hbox_top = QHBoxLayout()
        self.pairing_text_base_case = "V=" + self.first_particle + "   Y=" + self.second_particle
        self.pairing_text_switched = "V=" + self.second_particle + "   Y=" + self.first_particle
        self.vector_pair_label = QLabel(self.pairing_text_base_case)
        label_top_center_font = QLabel().font()
        label_top_center_font.setPointSize(22)
        self.vector_pair_label.setFont(label_top_center_font)
        layout.addWidget(self.vector_pair_label, alignment=Qt.AlignCenter)
        
        # The top widgets
        before_transformation_label = QLabel("1. Pre-Transformation:")
        before_transformation_label_font = QLabel().font()
        before_transformation_label_font.setPointSize(12)
        before_transformation_label.setFont(before_transformation_label_font)
        layout.addWidget(before_transformation_label, alignment=Qt.AlignLeft)
        top_vbox = QVBoxLayout()
        top_vbox.setSpacing(0)
        swap_button = QPushButton("Swap V \u2194 Y")
        swap_button.setFixedWidth(100)
        swap_button.clicked.connect(self.on_reversed)
        top_vbox.addWidget(swap_button)
        self.rotate_checkbox = QCheckBox("Rotate system \u2192 (V + Y) || z axis")
        top_vbox.addWidget(self.rotate_checkbox)
        hbox_top.addLayout(top_vbox)
        layout.addLayout(hbox_top)
        
        h_line = QFrame()
        h_line.setFrameShape(QFrame.Shape.HLine)
        h_line.setFrameShadow(QFrame.Shadow.Plain)
        layout.addWidget(h_line)

        transformation_label = QLabel("2. Transformation")
        transformation_label_font = QLabel().font()
        transformation_label_font.setPointSize(12)
        transformation_label.setFont(before_transformation_label_font)
        layout.addWidget(transformation_label, alignment=Qt.AlignLeft)
        self.transformation_checkbox = QCheckBox("Configure and apply transformation matrix")
        self.transformation_checkbox.setChecked(True)
        layout.addWidget(self.transformation_checkbox)

        h_line2 = QFrame()
        h_line2.setFrameShape(QFrame.Shape.HLine)
        h_line2.setFrameShadow(QFrame.Shadow.Plain)
        layout.addWidget(h_line2)
        
        post_transformation_label = QLabel("3. Post-Transformation:")
        post_transformation_label_font = QLabel().font()
        post_transformation_label_font.setPointSize(12)
        post_transformation_label.setFont(post_transformation_label_font)
        layout.addWidget(post_transformation_label, alignment=Qt.AlignLeft)
        self.post_transformation_checkbox = QCheckBox("Additional Transformation")
        layout.addWidget(self.post_transformation_checkbox)

        self.submit_cancel_button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.submit_cancel_button_box.accepted.connect(self.accept)
        self.submit_cancel_button_box.rejected.connect(self.reject)
        layout.addWidget(self.submit_cancel_button_box)
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
        self.transformation_config["RotateV+Ytoz"] = self.rotate_checkbox.isChecked()
        self.transformation_config["ApplyTransformationMatrix"] = self.transformation_checkbox.isChecked()
        self.transformation_config["ApplyPostTransformation"] = self.post_transformation_checkbox.isChecked()
        
        super().accept()

    def on_reversed(self):
        if self.vector_pair_label.text() == self.pairing_text_base_case:
            self.vector_pair_label.setText(self.pairing_text_switched)
        else:
            self.vector_pair_label.setText(self.pairing_text_base_case)
            
# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     main_dialog = ConfigureTransformationPopup([0, 1], ["k2", "k1"])
#     if main_dialog.exec() == QDialog.Accepted:
#         print("User okayed")
#     else:
#         print("User cancelled.")

#     sys.exit(app.exec())