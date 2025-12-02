from PySide6.QtWidgets import QApplication
from main.application import MainWindow


app = QApplication()

window = MainWindow(app)
window.show()

app.exec()
