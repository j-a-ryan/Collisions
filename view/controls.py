from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

import config
from controller.controls_controller import ControlsController
from view.common.details import Heading
from view.controls_view.slider import (
    BoostParameterASlider,
    BoostParameterASliderUpdateHandler,
    SliderGroupFrame,
)


class ControlsLayout(QFrame):
    def __init__(self, experiment_controller):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)  # Optional: sets a default styled panel look
        self.setFixedWidth(220)
        # self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self.controls_controller = ControlsController(experiment_controller)
        # self.setLineWidth(2) doesn't seem to do anything
        self.inner_layout = QVBoxLayout(self)
        self.inner_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        heading = Heading("CONTROLS", "Tahoma", False)
        self.inner_layout.addWidget(heading, alignment=Qt.AlignmentFlag.AlignCenter)
        self.controls_panel = QVBoxLayout()
        self.inner_layout.addLayout(self.controls_panel)

    def reset_transformation_controls(self):
        self.boost_parameter_A_slider.setValue(1)
        self.boost_parameter_A_slider.setEnabled(False)

    def set_controls_for_transformation_plot(self, boost_parameter_A_initial_value=None):
        self.reset_transformation_controls()
        if boost_parameter_A_initial_value is not None:
            self.boost_parameter_A_slider.setValue(boost_parameter_A_initial_value)
        self.boost_parameter_A_slider.setEnabled(True)

    def clear_controls(self):
        # Clear out and renew the controls panel
        self.inner_layout.removeItem(self.controls_panel)
        self.controls_panel.deleteLater()
        del self.controls_panel
        self.controls_panel = QVBoxLayout()

    def add_boost_A_slider(self, initial_value):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFixedWidth(200)
        frame.setContentsMargins(0, 0, 10, 0)
        frame_layout = QVBoxLayout(frame)
        label_A = QLabel("Boost Parameter A:")
        frame_layout.addWidget(label_A, alignment=Qt.AlignmentFlag.AlignCenter)

        self.boost_parameter_A_slider = BoostParameterASlider(initial_value, 0, config.boost_A_max)
        handler = BoostParameterASliderUpdateHandler(self.controls_controller)
        self.boost_parameter_A_slider.set_handler(handler)
        self.boost_parameter_A_slider.setEnabled(False)  # No transformation yet
        frame_layout.addWidget(self.boost_parameter_A_slider, alignment=Qt.AlignmentFlag.AlignCenter)
        self.controls_panel.addWidget(frame)

    def add_txyz_sliders(self, vector_names, vector_set_xyz):

        for i in range(len(vector_names)):
            vector_name = vector_names[i]
            vector = vector_set_xyz[i]
            self.controls_panel.addWidget(SliderGroupFrame(self.controls_controller, vector_name, vector))
        self.inner_layout.addLayout(self.controls_panel)
