import sys
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QPushButton
from PySide6.QtGui import Qt
import numpy as np

from main.custom_title_bar import CustomTitleBar


class PlotVectorCanvas2D(FigureCanvas):

    plot_2d_types_vector_indices = {'x-y': [0, 1], 'x-z': [0, 2], 'y-z': [1, 2]}
    axis_labels = ['x', 'y', 'z']

    def __init__(self, experiment_controller=None, parent=None, width=5, height=5, dpi=100): #
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        fig.set_facecolor("#FCFEE7")
        self.ax.set_facecolor("#F2F3EA")
        # fig.tight_layout()
        # self.ax.grid(True)
        self.ax.grid(True, linestyle=':', linewidth=0.5, color='gray', alpha=0.7) 
        self.fig = fig
        super().__init__(fig)
        self.experiment_controller = experiment_controller
        self.setParent(parent)

    def plot(self, collision, plot_2d_type):

        vectors = collision.get_spacial_vectors_xyz()
        index_of_origin_vector = collision.get_id_of_origin_vector()
        origin = [0, 0]

        indices_to_plot = self.plot_2d_types_vector_indices[plot_2d_type]

        arr = np.array(vectors)
        xs = arr[:, indices_to_plot[0]]
        ys = arr[:, indices_to_plot[1]]

        point_characters = ['L', 'h1', 'h2']
        colors = ['black', 'black', 'black']

        # Plot the vector using quiver
        for i in range(len(vectors)):
            if i != index_of_origin_vector:
                self.ax.quiver(origin[0], origin[1], xs[i], ys[i], angles='xy',
                    scale_units='xy', scale=1, color='black', width=0.003, linewidths=0.5)
            self.scatter = self.ax.scatter(xs[i], ys[i], marker=f'${point_characters[i]}$', s=90, color='black') 
        self.ax.scatter(xs, ys, facecolors='none', edgecolors=colors, marker='o', s=160)

        self.ax.set_xlabel(self.axis_labels[indices_to_plot[0]], fontsize=10)
        self.ax.set_ylabel(self.axis_labels[indices_to_plot[1]], fontsize=10)

        # self.ax.set_xlim([-1, 6]) TODO: Do programmatically
        # self.ax.set_ylim([-1, 6])

class Plot2DPopup(QDialog):
    
    screen_locations = {'x-y': [300, 150], 'x-z': [600, 150], 'y-z': [900, 150]}

    def __init__(self, parent, button, vectors, experiment_controller, plot_status):
        super().__init__(parent)
        self.experiment_controller = experiment_controller
        self.plot_status = plot_status
        self.resize(200, 200)
        plot_2d_type = button.text()
        self.button = button
        self.setWindowTitle(f"{plot_2d_type} {plot_status}")
        canvas = PlotVectorCanvas2D(self.experiment_controller, self, 3, 3)
        if vectors is not None:
            canvas.plot(vectors, plot_2d_type)
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        # layout.addWidget(cancel_button, alignment=Qt.AlignmentFlag.AlignRight)
        # cancel_button.clicked.connect(self.closeEvent)
        self.setLayout(layout)
        self.move(self.screen_locations[plot_2d_type][0], self.screen_locations[plot_2d_type][1])

    def closeEvent(self, event):
        self.done(1)
        self.button.setEnabled(True)