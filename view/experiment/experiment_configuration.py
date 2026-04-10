from PySide6.QtWidgets import QGridLayout, QMessageBox, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QDialog, QLabel
from PySide6.QtGui import Qt, QPixmap
import config
from view.experiment.vectors import VectorsGrid
from view.experiment.widgets import VectorIssueCheck

class ExperimentConfigurationForm(QDialog):

    def __init__(self, parent, max_vector_count):
        super().__init__(parent)
        self.setWindowTitle("Experiment Configuration")
        self.resize(550, 150)
        self.controller = parent.experiment_controller
        self.vectors_grid_frame = QFrame()
        self.vectors_grid_frame.setFrameShape(QFrame.StyledPanel)
        self.vectors_qvbox_layout = QVBoxLayout(self.vectors_grid_frame)
        self.vectors_qvbox_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Set up vectors grid, its header, its layout, and its parent layout.
        
        vectors_grid_layout = QGridLayout()#self.vectors_grid_frame) # needed as instance var?
        self.vectors_grid = VectorsGrid(vectors_grid_layout, self)
        values_requirements = f"(Values {config.xyz_min} to {config.xyz_max}, {config.xyz_decimal_precision}-decimal precision)"
        header_label = QLabel("Enter four-vectors " + values_requirements) # Insert header and grid for vectors layout
        self.vectors_qvbox_layout.addWidget(header_label)
        self.insert_vectors_grid_layout(vectors_grid_layout) # Insert the grid layout into its parent.

        self.max_vector_count = max_vector_count
        self.add_row_button = QPushButton(f"Add New Row (max {config.max_num_vectors}:)")
        self.add_row_button.clicked.connect(lambda: self.add_new_row(True))

        self.qhbox_layout_1 = QHBoxLayout()
        self.qhbox_layout_1.setAlignment(Qt.AlignmentFlag.AlignLeft)        
        # self.qhbox_layout_1.addLayout(self.experiment_type_qhbox_layout)
        # self.qhbox_layout_1.addLayout(self.vectors_qvbox_layout)
        self.qhbox_layout_1.addWidget(self.vectors_grid_frame)

        self.check_button = QPushButton("Check Parameters")
        self.check_button.clicked.connect(self.check_parameters)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel)

        self.set_buttons_enabled_state(False)
        widgets_to_enable_disable = {"ADD_ROW": self.add_row_button, "SAVE": self.save_button, 
                                     "SUBMIT": self.submit_button, "CHECK": self.check_button}
        self.vectors_grid.set_widgets_to_enable_disable(widgets_to_enable_disable)
        
        self.row_count = 0
        self.add_new_row()

        self.submit_buttons_layout = QGridLayout()
        self.submit_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.submit_buttons_layout.addWidget(self.add_row_button, 0, 0, 1, 4)
        self.submit_buttons_layout.addWidget(self.check_button, 1, 0)
        self.submit_buttons_layout.addWidget(self.submit_button, 1, 1)
        self.submit_buttons_layout.addWidget(self.save_button, 1, 2)
        self.submit_buttons_layout.addWidget(self.cancel_button, 1, 3)

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
        # self.vectors_qvbox_layout.removeWidget(self.add_row_button)
        self.vectors_qvbox_layout.removeItem(self.vectors_grid_layout)
        
        self.vectors_grid_layout.deleteLater()
        del self.vectors_grid_layout

    def insert_vectors_grid_layout(self, vectors_grid_layout, remove_current=False):
        self.vectors_grid_layout = vectors_grid_layout
        self.vectors_qvbox_layout.addLayout(vectors_grid_layout)
        # if remove_current:
            # self.vectors_qvbox_layout.addWidget(self.add_row_button)
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

    # matrix_view_lookup = {"General Boost": "resources/GeneralBoost.png", "Momentum-Realignment Boost": "resources/LCC-RapidityBoost.png"}
        
    # def view_matrix(self):
    #     msg_box = QMessageBox(self)

    #     selected_matrix_name = self.matrix_type_combo_box.currentText()
    #     if selected_matrix_name is not None and selected_matrix_name != "":
    #         msg_box.setWindowTitle(selected_matrix_name + " matrix")
    #         if selected_matrix_name in self.matrix_view_lookup:
    #             file = self.matrix_view_lookup[selected_matrix_name]
    #             pixmap = QPixmap(file)
    #             pixmap = pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    #             msg_box.setIconPixmap(pixmap)
    #         else:
    #             msg_box.setText("Image of " + selected_matrix_name)
    #         msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    #         msg_box.exec()


    def check_parameters(self):
        vector_issues_dialog = VectorIssueCheck(self.controller, self.vectors_grid.backing_vectors)
        vector_issues_dialog.exec()
        
    def submit(self):
        # Send experiment configuration data to the controller
        # Get list of vectors, etc. and create payload dict.
        payload = {"vectors": self.vectors_grid.backing_vectors,
                   "metadata": {"vectors_header": VectorsGrid.header_row, 
                                "hi": "ho", "experiment_directory": ""}}
        self.controller.configure_and_create_experiment(payload)
        self.done(1) # self.close() instead? See the plot2d form, same question

    def save(self):
        pass

    def cancel(self):
        self.done(0) # TODO: self.close() instead? See the plot2d form, same question
