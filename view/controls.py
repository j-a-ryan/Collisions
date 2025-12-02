from PySide6.QtWidgets import QHBoxLayout, QFrame, QButtonGroup, QVBoxLayout, QLabel, QSizePolicy, QComboBox, QPushButton

from view.common.details import Heading, HorizontalDivider
from PySide6.QtGui import Qt, QFont

from view.vector_controls import ExperimentControls


class ControlsLayout(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel) # Optional: sets a default styled panel look
        # self.setLineWidth(2) doesn't seem to do anything
        inner_layout = QVBoxLayout(self)
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        heading = Heading("CONTROLS", "Tahoma", False)        
        inner_layout.addWidget(heading, alignment=Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(QLabel("Palettes:"), alignment=Qt.AlignmentFlag.AlignCenter)

        controls_combo_box = QComboBox()
        controls_combo_box.addItem("Particle Physics")
        controls_combo_box.addItem("QCD")
        controls_combo_box.addItem("Nuclear Physics")
        inner_layout.addWidget(controls_combo_box)

        
        inner_layout.addWidget(ExperimentControls("1", "h1", new_slider=True))
        inner_layout.addWidget(ExperimentControls("2", "h2", new_slider=True))

        inner_layout.addWidget(TransformationButtons())


class TransformationButtons(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.inner_layout = QVBoxLayout(self)
        
        heading = Heading("TRANSFORMATIONS", "Tahoma", False)
        self.inner_layout.addWidget(heading, alignment=Qt.AlignmentFlag.AlignCenter)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        button1 = QPushButton("Lab")
        button1.setCheckable(True)
        self.button_group.addButton(button1)
        self.inner_layout.addWidget(button1)

        self.inner_layout.addWidget(HorizontalDivider(1))

        button2 = QPushButton("h1")
        button2.setCheckable(True)
        self.button_group.addButton(button2)
        self.inner_layout.addWidget(button2)

        button3 = QPushButton("h2")
        button3.setCheckable(True)
        self.button_group.addButton(button3)
        self.inner_layout.addWidget(button3)
        
        self.button_group.buttonClicked.connect(self.on_button_clicked)

        # Add one set of these to each transformation button in a QFrame?
        # plot_buttons_2D = QHBoxLayout()
        # button1 = QPushButton("x-y")
        # button2 = QPushButton("x-z")
        # button3 = QPushButton("y-z")
        # # button1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # # button2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # # button3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # plot_buttons_2D.addWidget(button1)
        # plot_buttons_2D.addWidget(button2)
        # plot_buttons_2D.addWidget(button3)
        # self.inner_layout.addLayout(plot_buttons_2D)
    
    def on_button_clicked(self, button):
        print(f"Selected: {button.text()}")

