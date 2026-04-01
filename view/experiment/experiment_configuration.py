from PySide6.QtWidgets import QComboBox, QGridLayout, QRadioButton, QSizePolicy, QMessageBox, QStyle, QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QPushButton, QDialog, QLabel
from PySide6.QtGui import Qt, QPixmap
import config
from controller.experiment_controller import ExperimentController
from view.experiment.validation import VectorValidation
from view.experiment.vector_components import VectorMemberField
from view.experiment.vectors import VectorsGrid

class ExperimentConfigurationForm(QDialog):

    def __init__(self, parent, max_vector_count):
        super().__init__(parent)
        self.setWindowTitle("Experiment Configuration")

        self.controller = parent.experiment_controller
        self.vectors_qvbox_layout = QVBoxLayout()
        self.vectors_qvbox_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Set up vectors grid, its header, its layout, and its parent layout.
        vectors_grid_layout = QGridLayout() # needed as instance var?
        self.vectors_grid = VectorsGrid(vectors_grid_layout, self)
        values_requirements = f"values {config.xyz_min} to {config.xyz_max}, {config.xyz_decimal_precision}-decimal precision:"
        header_label = QLabel("Enter four-vector: " + values_requirements) # Insert header and grid for vectors layout
        self.vectors_qvbox_layout.addWidget(header_label)
        self.insert_vectors_grid_layout(vectors_grid_layout) # Insert the grid layout into its parent.

        self.max_vector_count = max_vector_count
        self.add_row_button = QPushButton(f"Add New Row (max {config.max_num_vectors}:)")
        self.add_row_button.clicked.connect(lambda: self.add_new_row(True))
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

        self.check_button = QPushButton("Check Parameters")
        self.check_button.clicked.connect(self.check_parameters)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.save_button = QPushButton("Save")
        # self.save_button.clicked.connect(self.save)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        self.set_buttons_enabled_state(False)
        widgets_to_enable_disable = {"ADD_ROW": self.add_row_button, "SAVE": self.save_button, 
                                     "SUBMIT": self.submit_button, "CHECK": self.check_button}
        self.vectors_grid.set_widgets_to_enable_disable(widgets_to_enable_disable)
        
        self.row_count = 0
        self.add_new_row()

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

    def delete_grid_for_refresh(self):
        while self.vectors_grid_layout.count():
            item = self.vectors_grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.vectors_qvbox_layout.removeWidget(self.add_row_button)
        self.vectors_qvbox_layout.removeItem(self.vectors_grid_layout)
        
        self.vectors_grid_layout.deleteLater()
        del self.vectors_grid_layout

    def insert_vectors_grid_layout(self, vectors_grid_layout, remove_current=False):
        self.vectors_grid_layout = vectors_grid_layout
        self.vectors_qvbox_layout.addLayout(vectors_grid_layout)
        if remove_current:
            self.vectors_qvbox_layout.addWidget(self.add_row_button)
        self.update() # or more immediate repaint()

    def updated_vector_validation(self, vector_valid):
        self.set_buttons_enabled_state(vector_valid)

    def set_buttons_enabled_state(self, enabled):
        if enabled:
            if self.vectors_grid.grid_row_count < self.max_vector_count:
                self.add_row_button.setEnabled(True)
            else: # Just to be sure
                self.add_row_button.setEnabled(False)
            self.submit_button.setEnabled(True)
            self.check_button.setEnabled(True)
            self.save_button.setEnabled(True)
        else:
            self.add_row_button.setEnabled(False)
            self.submit_button.setEnabled(False)
            self.check_button.setEnabled(False)
            self.save_button.setEnabled(False)

    def add_new_row(self, set_focus=False):
        self.vectors_grid.add_vector_row(set_focus)

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
        # Send experiment configuration data to the controller
        # Get list of vectors, etc. and create payload dict.
        payload = {"vectors": self.vectors_grid.backing_vectors,
                   "metadata": {"vectors_header": VectorsGrid.header_row, 
                                "hi": "ho", "experiment_directory": ""}}
        self.controller.create_experiment(payload)
        self.done(1) # self.close() instead? See the plot2d form, same question
