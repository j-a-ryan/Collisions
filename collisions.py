from PySide6.QtWidgets import QApplication
from main.application import MainWindow

# This is the launcher
app = QApplication()

window = MainWindow(app)
window.show()

app.exec()
