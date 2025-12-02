from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QSizePolicy

from view.common.details import HorizontalDivider

class ButtonsLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        button = QPushButton("Lab")
        button.setCheckable(True)
        button.clicked.connect(self.clicked)
        self.addWidget(button)
        
        self.addWidget(HorizontalDivider(1))
        button2 = QPushButton("P1")
        button2.setCheckable(True)
        self.addWidget(button2)
        button3 = QPushButton("P2")
        button3.setCheckable(True)
        self.addWidget(button3)

        self.set_up_buttons("background-color: blue")
        
        

    def clicked(self, data):
        print("clicked. Toggled to pressed: ")
        self.removeWidget(self.transformations_label)
        self.set_up_buttons("background-color: yellow")

    def set_up_buttons(self, style):
        self.transformations_label = QLabel("-----Transform----")
        self.transformations_label.setStyleSheet(style)
        self.transformations_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.inner_layout.addWidget(self.transformations_label)

