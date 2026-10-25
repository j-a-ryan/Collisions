from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

import config
from view.experiment.vectors import VectorsGrid
from view.experiment.vectors_layout import VectorsFramedLayout
from view.experiment.widgets import VectorIssueCheck
from view.widgets import show_confirmation_popup


class ExperimentConfigurationForm(QDialog):
    def __init__(self, parent, max_vector_count, vector_data=None):
        super().__init__(parent)
        self.setWindowTitle("Experiment Configuration")
        self.resize(550, 150)
        self.view = parent
        self.experiment_controller = parent.experiment_controller

        self.vectors_grid_frame = VectorsFramedLayout(self)
        self.vectors_grid_frame.buttons_enabled_changed.connect(
            self.set_buttons_enabled_state
        )

        self.max_vector_count = max_vector_count
        self.add_row_button = QPushButton(f"Add New Row (max {config.max_num_vectors})")
        self.add_row_button.clicked.connect(
            lambda: self.vectors_grid_frame.initialize_grid_rows(True)
        )

        self.grid_hbox_layout = QHBoxLayout()
        self.grid_hbox_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.grid_hbox_layout.addWidget(self.vectors_grid_frame)

        self.check_button = QPushButton("Check Parameters")
        self.check_button.setToolTip(
            "Checks for issues in vector set,\nsuch as division by zero."
        )
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
        widgets_to_enable_disable = {
            "ADD_ROW": self.add_row_button,
            "SAVE": self.save_button,
            "SUBMIT": self.submit_button,
            "CHECK": self.check_button,
        }
        self.vectors_grid_frame.set_widgets_to_enable_disable(widgets_to_enable_disable)

        self.row_count = 0  # TODO: Refactor into the vectors object itself.
        self.vectors_grid_frame.initialize_grid_rows(False, vector_data)

        self.submit_buttons_layout = QGridLayout()
        self.submit_buttons_layout.addWidget(self.add_row_button, 0, 2, 1, 4)
        self.submit_buttons_layout.setColumnStretch(1, 1)
        self.submit_buttons_layout.addWidget(self.check_button, 1, 2)
        self.submit_buttons_layout.addWidget(self.submit_button, 1, 3)
        self.submit_buttons_layout.addWidget(self.save_button, 1, 4)
        self.submit_buttons_layout.addWidget(self.cancel_button, 1, 5)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addLayout(self.grid_hbox_layout)
        self.main_layout.addLayout(self.submit_buttons_layout)
        self.setLayout(self.main_layout)

    def updated_vector_validation(self, vector_valid):
        self.set_buttons_enabled_state(vector_valid)

    def set_buttons_enabled_state(self, enabled):
        if enabled:
            if self.vectors_grid_frame.grid_row_count < self.max_vector_count:
                self.add_row_button.setEnabled(True)
            else:  # Just to be sure
                self.add_row_button.setEnabled(False)
            self.submit_button.setEnabled(True)
            self.check_button.setEnabled(True)
            self.save_button.setEnabled(True)
        else:
            self.add_row_button.setEnabled(False)
            self.submit_button.setEnabled(False)
            self.check_button.setEnabled(False)
            self.save_button.setEnabled(False)

    def _create_payload(self, vectors, **kwargs):
        metadict = {"vectors_header": VectorsGrid.header_row}
        metadict.update(kwargs)
        return {"vectors": vectors, "metadata": metadict}

    def check_parameters(self):
        vector_issues_dialog = VectorIssueCheck(
            self.experiment_controller, self.vectors_grid_frame.backing_vectors
        )
        vector_issues_dialog.exec()

    def create_experiment(self):
        # Send experiment configuration data to the controller
        # Get list of vectors, etc. and create payload dict.
        payload = self._create_payload(self.vectors_grid_frame.backing_vectors)
        self.experiment_controller.configure_and_create_experiment(payload)

    def submit(self):
        self.create_experiment()
        self.done(1)  # self.close() instead? See the plot2d form, same question

    def save(self):
        self.create_experiment()
        self.experiment_controller.save_current_experiment()

    def cancel(self):
        if self.experiment_controller.experiment_exists():
            reply = show_confirmation_popup(
                self, "Confirm", "Stop working with this experiment?"
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.done(0)
            else:
                self.done(1)
        else:  # TODO: self.close() instead? See the plot2d form, same question
            self.done(0)
