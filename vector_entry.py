import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton

from view.vectors.experiment_configuration import ExperimentConfigurationForm



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DEVELOPER TESTING")

        button = QPushButton("Show experiment configuration form")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        print("click", s)
        dlg = ExperimentConfigurationForm(self)
        print(dlg.exec())


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
