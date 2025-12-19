from PySide6.QtWidgets import QComboBox, QGridLayout, QRadioButton, QSizePolicy, QMessageBox, QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QPushButton, QDialog, QLabel
from PySide6.QtGui import Qt, QPixmap
class ExperimentConfigurationForm(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Experiment Configuration")
        self.vectors_qvbox_layout = QVBoxLayout()
        self.vectors_qvbox_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.grid_layout = QGridLayout()
        header_label = QLabel("Enter four-vector:")
        t_label = QLabel("t")
        x_label = QLabel("X")
        y_label = QLabel("Y")
        z_label = QLabel("Z")
        pt_label = QLabel("Particle Type")
        speed_label = QLabel("Speed")
        self.grid_layout.addWidget(t_label, 0, 1, alignment=(Qt.AlignCenter | Qt.AlignTop))
        self.grid_layout.addWidget(x_label, 0, 2, alignment=(Qt.AlignCenter | Qt.AlignTop))
        self.grid_layout.addWidget(y_label, 0, 3, alignment=(Qt.AlignCenter | Qt.AlignTop))
        self.grid_layout.addWidget(z_label, 0, 4, alignment=(Qt.AlignCenter | Qt.AlignTop))
        self.grid_layout.addWidget(pt_label, 0, 5, alignment=(Qt.AlignCenter | Qt.AlignTop))
        self.grid_layout.addWidget(speed_label, 0, 6, alignment=(Qt.AlignCenter | Qt.AlignTop))
        self.vectors_qvbox_layout.addWidget(header_label)
        self.vectors_qvbox_layout.addLayout(self.grid_layout)

        self.add_row_button = QPushButton("Add Row (max 4)")
        # self.add_row_button.setCheckable(False) TODO: why is button dark until pressed and then always bright? Fix
        self.add_row_button.clicked.connect(self.add_new_row)
        self.vectors_qvbox_layout.addWidget(self.add_row_button)

        self.experiment_type_qhbox_layout = QVBoxLayout()
        self.experiment_type_qhbox_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.experiment_type_frame = QFrame()
        self.experiment_type_frame.setFrameShape(QFrame.StyledPanel)
        self.experiment_type_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.exp_type_qhbox = QHBoxLayout(self.experiment_type_frame)
        self.exp_type_qhbox.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.field_radio_layout = QVBoxLayout()
        self.field_label = QLabel("Physics Field:")
        self.field_radio_layout.addWidget(self.field_label)
        self.radio1 = QRadioButton("General")
        self.radio2 = QRadioButton("Nuclear")
        self.radio3 = QRadioButton("Particle")
        self.radio4 = QRadioButton("QCD")
        self.field_radio_layout.addWidget(self.radio1)
        self.field_radio_layout.addWidget(self.radio2)
        self.field_radio_layout.addWidget(self.radio3)
        self.field_radio_layout.addWidget(self.radio4)
        self.radio1.setChecked(True)
        self.exp_type_qhbox.addLayout(self.field_radio_layout)

        self.experiment_type_combo_box_label = QLabel("Experiment Type:")
        self.experiment_type_combo_box = QComboBox()
        self.experiment_type_combo_box.setEditable(False)
        self.experiment_type_combo_box.addItem("e⁺e⁻")
        self.experiment_type_combo_box.addItem("p-p")
        self.experiment_type_combo_box.addItem("Heavy ion")
        self.experiment_type_combo_box.addItem("e-p/e-A")
        self.experiment_type_combo_box.setMinimumContentsLength(5)
        self.experiment_type_combo_box.setCurrentIndex(-1)
        self.combo_box_qvbox_layout_exp_type_units = QVBoxLayout()
        self.combo_box_qvbox_layout_exp_type_units.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.combo_box_qvbox_layout_exp_type_units.addWidget(self.experiment_type_combo_box_label)
        self.combo_box_qvbox_layout_exp_type_units.addWidget(self.experiment_type_combo_box)
        self.combo_box_qvbox_layout_exp_type_units.addStretch()
        self.combo_box_qvbox_layout_exp_type_units2 = QVBoxLayout()
        self.combo_box_qvbox_layout_exp_type_units2.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.vector_units_combo_box_label = QLabel("Units:")
        self.vector_units_combo_box = QComboBox()
        self.vector_units_combo_box.setEditable(False)
        self.vector_units_combo_box.addItem("m")
        self.vector_units_combo_box.addItem("ss")
        self.combo_box_qvbox_layout_exp_type_units2.addWidget(self.vector_units_combo_box_label)
        self.combo_box_qvbox_layout_exp_type_units2.addWidget(self.vector_units_combo_box)
        self.combo_box_qvbox_layout_exp_type_units_both = QVBoxLayout()
        self.combo_box_qvbox_layout_exp_type_units_both.addLayout(self.combo_box_qvbox_layout_exp_type_units)
        self.combo_box_qvbox_layout_exp_type_units_both.addLayout(self.combo_box_qvbox_layout_exp_type_units2)
        
        self.matrix_type_combo_box_label = QLabel("Transformation Matrix:")
        self.matrix_type_combo_box = QComboBox()
        self.matrix_type_combo_box.setEditable(False)
        self.matrix_type_combo_box.addItem("Galilean")
        self.matrix_type_combo_box.addItem("General Boost")
        self.matrix_type_combo_box.addItem("Momentum-Realignment Boost")
        self.matrix_type_combo_box.addItem("Identity Matrix (for app testing)")
        self.matrix_type_combo_box.setMinimumContentsLength(5)
        self.matrix_type_combo_box.setCurrentIndex(-1)
        self.matrix_type_combo_box_qvbox_layout = QVBoxLayout()
        self.matrix_type_combo_box_qvbox_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.matrix_type_combo_box_qvbox_layout.addWidget(self.matrix_type_combo_box_label)
        self.matrix_type_combo_box_qvbox_layout.addWidget(self.matrix_type_combo_box)
        self.matrix_view_button = QPushButton("View Matrix")
        self.matrix_view_button.clicked.connect(self.view_matrix)
        self.matrix_type_combo_box_qvbox_layout.addWidget(self.matrix_view_button)
        
        self.vector_type_combo_box_label = QLabel("Four-Vector Type:")
        self.vector_type_combo_box = QComboBox()
        self.vector_type_combo_box.setEditable(False)
        self.vector_type_combo_box.addItem("Location")
        self.vector_type_combo_box.addItem("Velocity")
        self.vector_type_combo_box.addItem("Momentum")
        self.vector_type_combo_box.addItem("Energy-Momentum")
        self.matrix_type_combo_box_qvbox_layout.addWidget(self.vector_type_combo_box_label)
        self.matrix_type_combo_box_qvbox_layout.addWidget(self.vector_type_combo_box)

        self.exp_type_qhbox.addLayout(self.combo_box_qvbox_layout_exp_type_units_both)
        self.exp_type_qhbox.addLayout(self.matrix_type_combo_box_qvbox_layout)

        self.experiment_type_qhbox_layout.addWidget(self.experiment_type_frame)

        self.qhbox_layout_1 = QHBoxLayout()
        self.qhbox_layout_1.setAlignment(Qt.AlignmentFlag.AlignLeft)        
        self.qhbox_layout_1.addLayout(self.experiment_type_qhbox_layout)
        self.qhbox_layout_1.addLayout(self.vectors_qvbox_layout)

        self.row_count = 0
        self.add_new_row()
        
        self.check_button = QPushButton("Check Parameters")
        self.check_button.clicked.connect(self.check_parameters)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.save_button = QPushButton("Save")
        # self.save_button.clicked.connect(self.save)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        self.submit_buttons_layout = QHBoxLayout()
        self.submit_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.submit_buttons_layout.addWidget(self.check_button)
        self.submit_buttons_layout.addWidget(self.submit_button)
        self.submit_buttons_layout.addWidget(self.save_button)
        self.submit_buttons_layout.addWidget(self.cancel_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addLayout(self.qhbox_layout_1)
        self.main_layout.addLayout(self.submit_buttons_layout)
        self.setLayout(self.main_layout)

    def add_new_row(self):
        self.row_count += 1
        label = QLabel(f"{self.row_count}:")
        time_field = QLineEdit()
        x_field = QLineEdit()
        y_field = QLineEdit()
        z_field = QLineEdit()
        self.grid_layout.addWidget(label, self.row_count, 0, alignment=Qt.AlignTop)
        self.grid_layout.addWidget(time_field, self.row_count, 1, alignment=Qt.AlignTop)
        self.grid_layout.addWidget(x_field, self.row_count, 2, alignment=Qt.AlignTop)
        self.grid_layout.addWidget(y_field, self.row_count, 3, alignment=Qt.AlignTop)
        self.grid_layout.addWidget(z_field, self.row_count, 4, alignment=Qt.AlignTop)
        particle_combo_box = QComboBox()
        particle_combo_box.setEditable(True)
        particle_combo_box.addItem("e+")
        particle_combo_box.addItem("π")
        particle_combo_box.addItem("p")
        particle_combo_box.setMinimumContentsLength(6)
        particle_combo_box.setCurrentIndex(-1)
        self.grid_layout.addWidget(particle_combo_box, self.row_count, 5)
        speed_field = QLineEdit()
        self.grid_layout.addWidget(speed_field, self.row_count, 6, alignment=Qt.AlignTop)

    matrix_view_lookup = {"General Boost": "resources/GeneralBoost.png", "Momentum-Realignment Boost": "resources/LCC-RapidityBoost.png"}
        
    def view_matrix(self):
        msg_box = QMessageBox(self)

        selected_matrix_name = self.matrix_type_combo_box.currentText()
        if selected_matrix_name is not None and selected_matrix_name != "":
            msg_box.setWindowTitle(selected_matrix_name + " matrix")
            if selected_matrix_name in self.matrix_view_lookup:
                file = self.matrix_view_lookup[selected_matrix_name]
                pixmap = QPixmap(file)
                pixmap = pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                msg_box.setIconPixmap(pixmap)
            else:
                msg_box.setText("Image of " + selected_matrix_name)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()


    def check_parameters(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Parameter Check")
        msg.setText("No conflicts detected")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        
    def submit(self):
        self.done(1) # self.close() instead? See the plot2d form, same question
