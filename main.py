from PySide6.QtWidgets import QApplication
from app.application import MainWindow


if __name__ == "__main__":
    # This is the launcher
    app = QApplication()

    window = MainWindow(app)
    window.show()

    app.exec()
