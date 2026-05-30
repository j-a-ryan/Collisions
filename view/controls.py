from PySide6.QtWidgets import QFrame, QVBoxLayout

from controller.controls_controller import ControlsController
from view.common.details import Heading
from PySide6.QtGui import Qt

from view.controls_view.slider import SliderGroupFrame


class ControlsLayout(QFrame):
    def __init__(self, experiment_controller):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel) # Optional: sets a default styled panel look
        self.setFixedWidth(220)

        self.controls_controller = ControlsController(experiment_controller)
        # self.setLineWidth(2) doesn't seem to do anything
        self.inner_layout = QVBoxLayout(self)
        self.inner_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        heading = Heading("CONTROLS", "Tahoma", False)        
        self.inner_layout.addWidget(heading, alignment=Qt.AlignmentFlag.AlignCenter)
        self.controls_panel = QVBoxLayout()
        self.inner_layout.addLayout(self.controls_panel)

    def clear_controls(self):
        # Clear out and renew the controls panel
        self.inner_layout.removeItem(self.controls_panel)
        self.controls_panel.deleteLater()
        del self.controls_panel
        self.controls_panel = QVBoxLayout()

    def add_txyz_sliders(self, vector_names, vector_set_xyz):

        self.clear_controls()

        for i in range(len(vector_names)):
            vector_name = vector_names[i]
            vector = vector_set_xyz[i]
            self.controls_panel.addWidget(SliderGroupFrame(self.controls_controller, vector_name, vector))
        self.inner_layout.addLayout(self.controls_panel)
