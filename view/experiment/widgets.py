import sys

from PySide6.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel, QMessageBox, QPushButton, QStyle, QTextEdit, QVBoxLayout
from PySide6.QtGui import QIcon, Qt

import config
from controller.transformation_controller import TransformationController
from model import util
from view.controls_view import slider
from view.plot_view.widgets import create_argument_type_checkboxes

class DeleteVectorRowButton(QPushButton):

    def __init__(self, parent_form_style):
        super().__init__()
        self.parent_form_style = parent_form_style
        self.setStyleSheet("border: none;")
        self.disabled_icon = QIcon()
        self.delete_icon = self.parent_form_style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical) #SP_BrowserStop
    
    # Make button visible and enabled.
    def activate(self):
        self.setIcon(self.delete_icon)
        self.setEnabled(True)
    
    # Make butten just a spacer. N.B.: spacer and invisible don't work.
    def deactivate(self):
        self.setIcon(self.disabled_icon)
        self.setEnabled(False) # In effect, a spacer. Spacer and blank widget didn't work

    @staticmethod # Currently just activating. May need deactivation in future.
    def check_button_states(grid_layout):
        # Row 0 is header. Get row 1's button, which is in col 7.
        first_row_delete_button = grid_layout.itemAtPosition(1, 7).widget() # This should never throw exception.
        if grid_layout.rowCount() > 2:
            first_row_delete_button.activate() # We were deactivating her (first row of several). Decided not needed
        else:
            first_row_delete_button.activate()

class VectorIssueCheck(QDialog):
    
    def __init__(self, experiment_controller, vectors): # These vectors are the VectorsGrid's backing_vectors member
        super().__init__()
        self.setWindowTitle("Check Vectors for Issues")
        self.setFixedSize(240, 400)
        # vectors = [[1,0.000001,0.00,0.000001,"k1"], [1,5,3,3,"k2"]]
        raw_four_vectors = [vec_raw[:4] for vec_raw in vectors]
        self.vectors = []
        for vec in raw_four_vectors:
            self.vectors.append([float(j) for j in vec[:4]])
        self.names = [vec[4] for vec in vectors]

        self.experiment = experiment_controller.create_experiment(self.vectors, self.names)
        self.transformation_controller = TransformationController(experiment_controller)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        vectors_label = QLabel("Select V and Y")
        vectors_label_font = QLabel().font()
        vectors_label_font.setItalic(True)
        vectors_label_font.setPointSize(12)
        vectors_label.setFont(vectors_label_font)
        layout.addWidget(vectors_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        combobox_grid_layout = QGridLayout()
        V_label = QLabel("V")
        combobox_grid_layout.addWidget(V_label, 0, 0, alignment=(Qt.AlignCenter | Qt.AlignTop))
        Y_label = QLabel("Y")
        combobox_grid_layout.addWidget(Y_label, 0, 1, alignment=(Qt.AlignCenter | Qt.AlignTop))
        self.V_combo_box = self._set_up_combo_box()
        self.Y_combo_box = self._set_up_combo_box()
        self.default_combobox_stylesheet = self.Y_combo_box.styleSheet()
        combobox_grid_layout.addWidget(self.V_combo_box, 1, 0)
        combobox_grid_layout.addWidget(self.Y_combo_box, 1, 1)
        layout.addLayout(combobox_grid_layout)

        layout.addSpacing(25)
        
        create_argument_type_checkboxes(self, layout)

        self.check_button = QPushButton("Run Check")
        self.check_button.setEnabled(False)
        self.check_button.clicked.connect(self.submit)
        layout.addWidget(self.check_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.results_text_area = QTextEdit()
        self.results_text_area.setReadOnly(True)  # Make it look/behave like a label
        
        layout.addWidget(self.results_text_area)

        self.submit_cancel_button_box = QDialogButtonBox(QDialogButtonBox.Close)
        self.submit_cancel_button_box.rejected.connect(self.reject)
        layout.addWidget(self.submit_cancel_button_box, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)

    def _set_up_combo_box(self):
        box = QComboBox()
        box.activated.connect(self.combo_box_changed)
        for name in self.names:
            box.addItem(name)
        box.setEditable(True)
        box.lineEdit().setReadOnly(True)
        box.setMinimumContentsLength(6)
        box.setCurrentIndex(-1)
        return box

    def submit(self):
        self.results_text_area.clear()

        V_particle_name = self.V_combo_box.currentText()
        Y_particle_name = self.Y_combo_box.currentText()
        vector_V = self.experiment.get_original_four_vector(V_particle_name)
        vector_Y = self.experiment.get_original_four_vector(Y_particle_name)
        V_plus_Y = self.V_plus_Y_argument_type_checkbox.isChecked()
        V_minus_Y = self.post_transformation_checkbox.isChecked()
        argument_type = util.get_config_argument(V_plus_Y, V_minus_Y)
        results, transformation_type = self.transformation_controller.validate_vectors(vector_V, vector_Y, argument_type, V_particle_name, Y_particle_name, self.experiment, self.names)

        if results:
            self.results_text_area.setAlignment(Qt.AlignLeft)
            self.results_text_area.append("Problems found for " + transformation_type + ":")
            for line in results:
                self.results_text_area.append("\u2022 " + line)
        else:
            self.results_text_area.append("No issues found.")
            self.results_text_area.setAlignment(Qt.AlignCenter)

    def combo_box_changed(self):

        V_text = self.V_combo_box.currentText()
        Y_text = self.Y_combo_box.currentText()
        valid_selection_pair = False
        if V_text and Y_text:
            if V_text != Y_text:
                self.V_combo_box.setStyleSheet(self.default_combobox_stylesheet)
                self.Y_combo_box.setStyleSheet(self.default_combobox_stylesheet)
                valid_selection_pair = True
            else:
                self.V_combo_box.setStyleSheet(config.combo_box_invalid_stylesheet)
                self.Y_combo_box.setStyleSheet(config.combo_box_invalid_stylesheet)
        self.check_button.setEnabled(valid_selection_pair)

    def two_step_transformation_check(self):
        if self.V_plus_Y_argument_type_checkbox.isChecked():
            self.post_transformation_checkbox.setEnabled(True)
        else:
            self.post_transformation_checkbox.setChecked(False)
            self.post_transformation_checkbox.setEnabled(False)

def get_slider_transformation_issue_popup(argument_type, axis=None, value=None):
    msg = QMessageBox()
    msg.setWindowTitle("Transformation Problem")
    msg.setIcon(QMessageBox.Icon.Warning) 
    msg.setText(f"Transformation error")
    
    if not axis and not value:
        msg.setInformativeText(f"Transformation of type {argument_type} on this vector set " +\
                        "will leads to an error, such as division by zero. You can run the " +\
                        "vector check to address this issue.")
    else: # Assumes value and axis are not none.
        axis_name = slider.VectorSlider.lookup_0123_txyz[str(axis)]
        msg.setInformativeText(f"Transformation type {argument_type} with {axis_name} = {value} leads to an error, " +\
                            "such as division by zero.")
    font = msg.font()
    font.setPointSize(11)
    msg.setFont(font)
    return msg
        