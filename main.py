from PySide6.QtWidgets import QApplication
from app.application import MainWindow


if __name__ == "__main__":
    # This is the launcher
    app = QApplication()

    window = MainWindow(app)
    window.show()

    app.exec()
"""
TODO:   
1. Round zero in plotted vectors
2. Fix plot margin issue? This seems to have vanished with expanding of frame.

4. Get rid of lab vector, make the plot not require special treatment of lab/origin vector or require one at all.
4. Need matrix images.
"""
