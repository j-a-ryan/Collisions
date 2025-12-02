from PySide6.QtWidgets import QWidget, QFrame, QFontComboBox, QVBoxLayout, QLabel, QSizePolicy, QComboBox, QPushButton

from view.common.details import Heading, HorizontalDivider

from PySide6.QtGui import Qt


class TransformationsLayout(QFrame):
    def __init__(self):
        super().__init__()

        # Optional: sets a default styled panel look
        self.setFrameShape(QFrame.StyledPanel)
        self.inner_layout = QVBoxLayout(self)
        # self.inner_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        heading = Heading("TRANSFORMATIONS", "Tahoma", False)
        self.inner_layout.addWidget(heading, alignment=Qt.AlignmentFlag.AlignCenter)

        button = QPushButton("Lab")
        button.setCheckable(True)
        button.clicked.connect(self.clicked)
        self.inner_layout.addWidget(button)

        self.inner_layout.addWidget(HorizontalDivider(1))
        button2 = QPushButton("P1")
        button2.setCheckable(True)
        self.inner_layout.addWidget(button2)
        button3 = QPushButton("P2")
        button3.setCheckable(True)
        self.inner_layout.addWidget(button3)

        self.set_up_buttons("background-color: blue")

    def clicked(self, data):
        print("clicked. Toggled to pressed: ")
        self.inner_layout.removeWidget(self.transformations_label)
        self.set_up_buttons("background-color: yellow")

    def set_up_buttons(self, style):
        self.transformations_label = QLabel("-----Transform----")
        self.transformations_label.setStyleSheet(style)
        self.transformations_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.inner_layout.addWidget(self.transformations_label)
