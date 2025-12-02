from PySide6.QtWidgets import QFrame, QLabel
from PySide6.QtGui import QFont


class HorizontalDivider(QFrame):
    def __init__(self, thickness):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(0) # Prevents problems with border
        self.setMidLineWidth(thickness)
        self.setMinimumHeight(thickness)  # Ensures layout respects the size

class Heading(QLabel):
    def __init__(self, heading_text, font_name, italic):
        super().__init__()
        self.setText(heading_text)
        heading_font = QFont()
        heading_font.setFamily(font_name)
        heading_font.setItalic(italic)
        self.setFont(heading_font)
    
    def set_font_point_size(self, size):
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)
