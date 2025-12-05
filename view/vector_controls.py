from PySide6.QtWidgets import QVBoxLayout, QFrame, QSlider, QLabel, QSizePolicy
from PySide6.QtGui import Qt, QColor, QFont
from view.common.details import Heading
from pyqt_advanced_slider import Slider

class ExperimentControls(QFrame):
    def __init__(self, particle_id, particle_type, new_slider=False):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.inner_layout = QVBoxLayout(self)

        heading = Heading(f"Particle {particle_id}: {particle_type}", "Tahoma", False)
        self.inner_layout.addWidget(heading, alignment=Qt.AlignmentFlag.AlignLeft)

        if new_slider:
            self.slider1 = Slider(self)  # Add slider
            self.slider1.setRange(-50, 100)  # Set min and max
            self.slider1.setValue(25)  # Set value
            self.slider1.valueChanged.connect(self.slider_value_changed)
            self.slider1.setFixedWidth(120)
            self.slider1.setFixedHeight(18)
            # self.slider1.setTextColor(QColor('#0F0F0F'))                # Default: #000000
            # self.slider1.setBackgroundColor(QColor('#9B9D06'))          # Default: #D6D6D6
            # self.slider1.setAccentColor(QColor('#F4F835'))  # Default: #0078D7
            # self.slider.setBorderColor(QColor.fromRgb(0, 0, 0))        # Default: #D1CFD3
            self.slider1.setBorderRadius(3)  # Default: 0
            # font = QFont()
            # font.setFamily('Times')
            # font.setPointSize(10)
            # font.setBold(True)
            # slider.setFont(font)
            
            self.inner_layout.addWidget(self.slider1)

            self.slider2 = Slider(self)  # Add slider
            self.slider2.setRange(-50, 100)  # Set min and max
            self.slider2.setValue(25)  # Set value
            self.slider2.valueChanged.connect(self.slider_value_changed)
            self.slider2.setFixedWidth(120)
            self.slider2.setFixedHeight(18)
            # self.slider2.setTextColor(QColor('#0F0F0F'))                # Default: #000000
            # self.slider2.setBackgroundColor(QColor('#9B9D06'))          # Default: #D6D6D6
            # self.slider2.setAccentColor(QColor('#F4F835'))  # Default: #0078D7
            # self.slider.setBorderColor(QColor.fromRgb(0, 0, 0))        # Default: #D1CFD3
            self.slider2.setBorderRadius(3)  # Default: 0
            # font = QFont()
            # font.setFamily('Times')
            # font.setPointSize(10)
            # font.setBold(True)
            # slider.setFont(font)
            
            self.inner_layout.addWidget(self.slider2)
        else:
            self.slider1 = QSlider(Qt.Horizontal)  # Or Qt.Vertical for a vertical slider
            self.slider1.setMinimum(0)
            self.slider1.setMaximum(100)
            self.slider1.setValue(50)  # Initial value
            self.slider1.setSingleStep(1)
            self.slider1.setPageStep(10)
            self.slider1.setTickPosition(QSlider.TicksBelow)
            self.slider1.setTickInterval(10)
            # self.slider1.setMinimumWidth(100)
            self.slider1.setFixedWidth(120)
            self.slider1.setFixedHeight(18)
            self.slider1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            # Create a QLabel to display the slider's value
            self.value_label1 = QLabel(f"V: {self.slider1.value()}")
            self.value_label1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            # Connect the slider's valueChanged signal to an update function
            self.slider1.valueChanged.connect(self.update_label1)

            self.inner_layout.addWidget(self.slider1)
            self.inner_layout.addWidget(self.value_label1)

            self.slider2 = QSlider(Qt.Horizontal)  # Or Qt.Vertical for a vertical slider
            self.slider2.setMinimum(0)
            self.slider2.setMaximum(100)
            self.slider2.setValue(50)  # Initial value
            self.slider2.setSingleStep(1)
            self.slider2.setPageStep(10)
            self.slider2.setTickPosition(QSlider.TicksBelow)
            self.slider2.setTickInterval(10)
            # self.slider.setMinimumWidth(100)
            self.slider2.setFixedWidth(120)
            self.slider2.setFixedHeight(18)
            self.slider2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            # Create a QLabel to display the slider's value
            self.value_label2 = QLabel(f"V: {self.slider2.value()}")
            self.value_label2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            # Connect the slider's valueChanged signal to an update function
            self.slider2.valueChanged.connect(self.update_label2)

            self.inner_layout.addWidget(self.slider2)
            self.inner_layout.addWidget(self.value_label2)
            
    def slider_value_changed(self, value):
        # print(value)
        pass

    def update_label1(self, value):
        """Updates the label with the current slider value."""
        self.value_label1.setText(f"V: {value}")
    
    def update_label2(self, value):
        """Updates the label with the current slider value."""
        self.value_label2.setText(f"V: {value}")
