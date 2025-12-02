import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)


class PlotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Matplotlib Plot in QDialog")

        # Create the Matplotlib canvas
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        # Plot some data
        x = [0, 1, 2, 3, 4]
        y = [10, 1, 20, 3, 40]
        self.canvas.axes.plot(x, y)

        # Create a layout and add the canvas to it
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = PlotDialog()
    dialog.exec()
    sys.exit(app.exec())
