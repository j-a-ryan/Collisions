from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
import sys

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

label1 = QLabel("Left Aligned Text")
label1.setAlignment(Qt.AlignmentFlag.AlignLeft)

label2 = QLabel("Centered Text")
label2.setAlignment( | Qt.AlignmentFlag.AlignVCenter)

label3 = QLabel("Bottom Right Aligned Text")
label3.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

layout.addWidget(label1)
layout.addWidget(label2)
layout.addWidget(label3)

window.setLayout(layout)
window.setWindowTitle("QLabel Alignment Example")
window.show()
sys.exit(app.exec())