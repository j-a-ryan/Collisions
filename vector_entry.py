import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton

from view.vectors.vector_entry import VectorEntryForm



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press me for a vector entry form")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        print("click", s)
        dlg = VectorEntryForm(self)
        print(dlg.exec())


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
