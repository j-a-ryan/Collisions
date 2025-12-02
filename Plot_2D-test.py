from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
import sys
from view.plot_view.plot_2D import PlotVectorCanvas2D

class ApplicationLayout(QWidget):

    def __init__(self, parent=None):
        super(ApplicationLayout, self).__init__(parent)

        # Set properties of the window
        # self.resize(600, 490)
        self.title = 'Test Plot'
        self.setWindowTitle(self.title)

        # Create the matplotlib canvas
        canvas = PlotVectorCanvas2D(self)
        vectors = [[3, 4, 5], [5, 3, 3]]
        canvas.plot(vectors)

        layout = QVBoxLayout()
        layout.addWidget(canvas)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # widget = ApplicationMainWindow()

    widget = ApplicationLayout()
    widget.show()

    app.exec()
