from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
import sys
import os
os.environ["QT_API"] = "PySide6" # Doesn't seem to do anything. What is it?
# from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class PlotVectorCanvas(FigureCanvas):
    def __init__(self, parent=None, width=7, height=7, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111, projection='3d')
        fig.set_facecolor("#4e5d6c")       
        self.ax.set_facecolor("#ABB6C2")
        super().__init__(fig)

    def plot(self, vectors):
        origin = [0, 0, 0]
        for vector in vectors:
            self.ax.quiver(origin[0], origin[1], origin[2],  # Starting point
                           # Vector components
                           vector[0], vector[1], vector[2],
                           color='black', arrow_length_ratio=0.1)  # Customize color and arrow size
            # c for color, marker for shape, s for size
            self.ax.scatter(vector[0], vector[1],
                            vector[2], c='blue', marker='o', s=100)

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        self.ax.set_xlim([-1, 6])
        self.ax.set_ylim([-1, 6])
        self.ax.set_zlim([-1, 6])

    def plot2D(self):
        self.ax.plot([0,1,2,3,4], [10,1,20,3,40])

class ApplicationLayout(QWidget):

    def __init__(self, parent=None):
        super(ApplicationLayout, self).__init__(parent)

        # Set properties of the window
        # self.resize(600, 490)
        self.title = 'Test Plot'
        self.setWindowTitle(self.title)

        # Create the matplotlib canvas
        canvas = PlotVectorCanvas(self)
        vectors = [[3, 4, 5], [5, 3, 3]]
        canvas.plot(vectors)

        layout = QVBoxLayout()
        layout.addWidget(canvas)
        self.setLayout(layout)

# class ApplicationMainWindow(QMainWindow):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Set properties of the window
#         # self.resize(600, 490)
#         self.title = 'Test Plot'
#         self.setWindowTitle(self.title)

#         # Create the matplotlib canvas
#         canvas = PlotVectorCanvas(self)
#         vectors = [[3, 4, 5], [5, 3, 3]]
#         canvas.plot(vectors)

#         self.setCentralWidget(canvas)
#         self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # widget = ApplicationMainWindow()
    
    widget = ApplicationLayout()
    widget.show()
    
    app.exec()
