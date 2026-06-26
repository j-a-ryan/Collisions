from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)
from PySide6.QtGui import Qt

import config
from PySide6.QtCore import QThread, Signal, Slot

from view.common.widgets import create_particle_names_combo_box


class AbstractTransformationPopup(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

    def get_combobox_names(self, candidate_particle_names):
        return candidate_particle_names

    def update_submit_buttons_state(self, enabled):
        pass

    def argument_types_checkboxes_group_clicked(self):
        pass

    def post_transformation_check(self):
        if config.step_2_uses_system_of_equations:
            if self.post_transformation_checkbox.isChecked():
                if self.particle_names_combo_box.count() == 0:
                    pass
                else:
                    # Enable third-vector selection dropdown
                    self.particle_names_combo_box.setVisible(True)
                    self.particle_names_combo_box.setEnabled(True)
                    if self.particle_names_combo_box.count() > 1:
                        self.particle_names_combo_box.setCurrentIndex(-1)
                        self.update_submit_buttons_state(False)
                    else:
                        self.particle_names_combo_box.setCurrentIndex(0)
                        self.update_submit_buttons_state(True)
                    self.third_vector_label.setVisible(True)
                    # Disable Submit button

            else:
                # Enable submit button
                self.update_submit_buttons_state(True)
                # set combo box to -1
                self.particle_names_combo_box.setCurrentIndex(-1)
                # Disable combo box and ensure set to -1
                self.particle_names_combo_box.setEnabled(False)
                self.particle_names_combo_box.setVisible(False)
                self.third_vector_label.setVisible(False)

    def particle_names_combo_box_activated(self):
        if self.particle_names_combo_box.isEnabled():
            if self.particle_names_combo_box.currentIndex() == -1:
                self.update_submit_buttons_state(False)
            else:
                self.update_submit_buttons_state(True)

    def create_argument_type_checkboxes(self, vbox_layout, all_particle_names):

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
        self.post_transformation_checkbox.checkStateChanged.connect(self.post_transformation_check)
        arrow_label = QLabel("\u2192")
        arrow_label_font = arrow_label.font()
        # arrow_label_font.setItalic(True)
        arrow_label_font.setPointSize(16)
        arrow_label.setFont(arrow_label_font)
        hbox_arguments.addWidget(arrow_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        hbox_arguments.addWidget(self.post_transformation_checkbox, alignment=Qt.AlignmentFlag.AlignRight)
        vbox_layout.addLayout(hbox_arguments)

        hbox_third_vector = QHBoxLayout()
        # Remove the V, Y names from a copy of the list of names

        combobox_names = self.get_combobox_names(all_particle_names)

        self.particle_names_combo_box = create_particle_names_combo_box(combobox_names)
        self.particle_names_combo_box.setEnabled(False)
        size_policy = self.particle_names_combo_box.sizePolicy()
        # Tell the policy to keep the layout space even when hidden
        size_policy.setRetainSizeWhenHidden(True)
        self.particle_names_combo_box.setSizePolicy(size_policy)  # Yes, you have to reset this.

        self.particle_names_combo_box.setVisible(False)
        self.particle_names_combo_box.activated.connect(self.particle_names_combo_box_activated)

        if config.step_2_uses_system_of_equations:
            self.third_vector_label = QLabel("Select a third vector:")
            size_policy.setRetainSizeWhenHidden(True)
            self.third_vector_label.setVisible(False)
            # hbox_third_vector.setContentsMargins(0, 0, 0, 0)
            # hbox_third_vector.setSpacing(2)
            # parent_form.third_vector_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            hbox_third_vector.addStretch(1)
            hbox_third_vector.addWidget(self.third_vector_label, alignment=Qt.AlignmentFlag.AlignRight)
            hbox_third_vector.addWidget(self.particle_names_combo_box, alignment=Qt.AlignmentFlag.AlignRight)
            ttt = "Second step of two-step transformation requires a third vector."
            self.particle_names_combo_box.setToolTip(ttt)
            self.third_vector_label.setToolTip(ttt)
        vbox_layout.addLayout(hbox_third_vector)


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
        self.transformation_config["third vector"] = None

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        vectors_label = QLabel("Vectors")
        vectors_label_font = QLabel().font()
        vectors_label_font.setItalic(True)
        vectors_label_font.setPointSize(12)
        vectors_label.setFont(vectors_label_font)
        layout.addWidget(vectors_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.pairing_text_base_case = "V=" + self.original_first_particle + "  Y=" + self.original_second_particle
        self.pairing_text_switched = "V=" + self.original_second_particle + "  Y=" + self.original_first_particle
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

        self.create_argument_type_checkboxes(layout, all_particle_names)

        # layout.addLayout(self.arg_type_checkboxes)

        self.submit_cancel_button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.submit_cancel_button_box.accepted.connect(self.accept)
        self.submit_cancel_button_box.rejected.connect(self.reject)
        layout.addWidget(self.submit_cancel_button_box, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)

    def update_submit_buttons_state(self, enabled):
        self.submit_cancel_button_box.button(QDialogButtonBox.Ok).setEnabled(enabled)

    def get_combobox_names(self, candidate_particle_names):
        combobox_names = candidate_particle_names.copy()
        combobox_names.remove(self.original_first_particle)
        combobox_names.remove(self.original_second_particle)
        return combobox_names

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
        self.transformation_config["third_vector"] = self.particle_names_combo_box.currentText()  # "" if none
        super().accept()

    def two_step_transformation_check(self):
        if self.V_plus_Y_argument_type_checkbox.isChecked():
            self.post_transformation_checkbox.setEnabled(True)
        else:
            self.post_transformation_checkbox.setChecked(False)
            self.post_transformation_checkbox.setEnabled(False)


class BackgroundCalculations(QThread):

    finished = Signal()  # Signal emitted when process ends

    def __init__(self, experiment_controller, transformation_vector_pair_indices, V_Y_particle_names, argument_type):
        super().__init__()
        self.experiment_controller = experiment_controller
        self.indices = transformation_vector_pair_indices
        self.VY_names = V_Y_particle_names
        self.arg_type = argument_type
        self._failure_message = None

    def run(self):
        self._failure_message = self.experiment_controller.create_initial_transformation(
            self.indices, self.VY_names, self.arg_type, boost_parameter_A=None, background_thread_preparation=True
        )
        self.finished.emit()

    @property
    def failure_message(self):
        return self._failure_message


class WaitingPopup(QDialog):
    def __init__(
        self,
        parent,
        background_calculations: BackgroundCalculations,
        title="Please Wait",
        text="Please stand by. Solving system of equations....",
        additional_text=None,
    ):
        super().__init__(parent)
        self.background_calculations = background_calculations
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
        self.progress_bar.setMinimum(0)  # Default start point
        self.progress_bar.setMaximum(0)  # Default end point
        self.progress_bar.setValue(0)  # Reset starting value
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        self.background_calculations.finished.connect(self.close_dialog)  # Connect signal to close method
        self.background_calculations.start()

    @Slot()
    def close_dialog(self):
        self.accept()
