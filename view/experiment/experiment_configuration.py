import csv

from PySide6.QtWidgets import QGridLayout, QMessageBox, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QDialog, QLabel
from PySide6.QtGui import Qt, QPixmap
import config
from view.experiment.vectors import VectorsGrid
from view.experiment.widgets import VectorIssueCheck

class ExperimentConfigurationForm(QDialog):

    def __init__(self, parent, max_vector_count, vector_data=None):
        super().__init__(parent)
        self.setWindowTitle("Experiment Configuration")
        self.resize(550, 150)
        self.view = parent
        self.experiment_controller = parent.experiment_controller
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
        self.add_row_button.clicked.connect(lambda: self.initialize_grid_rows(True))

        self.grid_hbox_layout = QHBoxLayout()
        self.grid_hbox_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)        
        # self.qhbox_layout_1.addLayout(self.experiment_type_qhbox_layout)
        # self.qhbox_layout_1.addLayout(self.vectors_qvbox_layout)
        self.grid_hbox_layout.addWidget(self.vectors_grid_frame)

        self.refresh_button = QPushButton("Refresh Grid")
        self.refresh_button.setVisible(False)
        self.refresh_button.setToolTip("Refreshes grid values when graph\nhas been altered manually.")
        self.refresh_button.clicked.connect(self.refresh_grid)

        self.check_button = QPushButton("Check Parameters")
        self.check_button.setToolTip("Checks for issues in vector set,\nsuch as division by zero.")
        self.check_button.clicked.connect(self.check_parameters)
        self.submit_button = QPushButton("Submit")
        self.submit_button.setToolTip("Graph the vector set.")
        self.submit_button.clicked.connect(self.submit)
        self.save_button = QPushButton("Save")
        self.save_button.setToolTip("Save the vector set as a local CSV file.")
        self.save_button.clicked.connect(self.save)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel)

        self.set_buttons_enabled_state(False)
        widgets_to_enable_disable = {"ADD_ROW": self.add_row_button, "SAVE": self.save_button, 
                                     "SUBMIT": self.submit_button, "CHECK": self.check_button}
        self.vectors_grid.set_widgets_to_enable_disable(widgets_to_enable_disable)
        
        self.row_count = 0 # TODO: Refactor into the vectors object itself.
        self.initialize_grid_rows(False, vector_data)

        self.submit_buttons_layout = QGridLayout()
        # self.submit_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.submit_buttons_layout.addWidget(self.add_row_button, 0, 2, 1, 4)
        self.submit_buttons_layout.setColumnStretch(1, 1)
        self.submit_buttons_layout.addWidget(self.refresh_button, 1, 0)
        self.submit_buttons_layout.addWidget(self.check_button, 1, 2)
        self.submit_buttons_layout.addWidget(self.submit_button, 1, 3)
        self.submit_buttons_layout.addWidget(self.save_button, 1, 4)
        self.submit_buttons_layout.addWidget(self.cancel_button, 1, 5)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addLayout(self.grid_hbox_layout)
        self.main_layout.addLayout(self.submit_buttons_layout)
        self.setLayout(self.main_layout)

    def delete_grid_for_refresh(self):
        while self.vectors_grid_layout.count():
            item = self.vectors_grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.vectors_qvbox_layout.removeItem(self.vectors_grid_layout)
        
        self.vectors_grid_layout.deleteLater()
        del self.vectors_grid_layout

    def insert_vectors_grid_layout(self, vectors_grid_layout, remove_current=False):
        self.vectors_grid_layout = vectors_grid_layout
        self.vectors_qvbox_layout.addLayout(vectors_grid_layout)
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

    def initialize_grid_rows(self, set_focus=False, grid_data=None):
        if grid_data:
            self.vectors_grid.add_vector_rows(grid_data)
            self.vectors_grid.refresh_grid()
        else:
            self.vectors_grid.add_vector_row(set_focus) # Add empty row

    def _create_payload(self, vectors, **kwargs):
        metadict = {"vectors_header": VectorsGrid.header_row}
        metadict.update(kwargs)
        return {"vectors": vectors, "metadata": metadict}
    
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

    def refresh_grid(self):
        pass

    def check_parameters(self):
        vector_issues_dialog = VectorIssueCheck(self.experiment_controller, self.vectors_grid.backing_vectors)
        vector_issues_dialog.exec()

    def create_experiment(self):
        # Send experiment configuration data to the controller
        # Get list of vectors, etc. and create payload dict.
        payload = self._create_payload(self.vectors_grid.backing_vectors)
        self.experiment_controller.configure_and_create_experiment(payload)
        
    def submit(self):
        self.create_experiment()
        self.done(1) # self.close() instead? See the plot2d form, same question

    def save(self):
        msg = QMessageBox()
        msg.setWindowTitle("Save Experiment")
        msg.setText("This will save the vectors and delete\n" +\
                    "any current transformation of them that\n" +\
                    "you may currently have. Proceed?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Ok)
        result = msg.exec()
        if result == QMessageBox.Ok:
            self.create_experiment()
            self.experiment_controller.save_current_experiment()

    def cancel(self):
        self.done(1) # TODO: self.close() instead? See the plot2d form, same question
