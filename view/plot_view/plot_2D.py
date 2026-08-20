from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QDialog, QVBoxLayout

import config


class PlotVectorCanvas2D(FigureCanvas):

    plot_2d_types_vector_indices = {"x-y": [0, 1], "x-z": [0, 2], "y-z": [1, 2]}
    axis_labels = ["x", "y", "z"]

    def __init__(self, experiment_controller=None, parent=None, width=5, height=5, dpi=100):  #
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        fig.set_facecolor(config.graph_encasing_area_color)
        self.ax.set_facecolor(config.graph_area_color)
        self.ax.grid(True, linestyle=":", linewidth=0.5, color="gray", alpha=0.7)
        self.fig = fig
        super().__init__(fig)
        self.experiment_controller = experiment_controller
        self.setParent(parent)

    def plot(self, collision, plot_2d_type):

        vectors = collision.get_spatial_vectors_xyz()
        indices_to_plot = self.plot_2d_types_vector_indices[plot_2d_type]
        particle_names = collision.get_vectors_name_column()

        xs = vectors[:, indices_to_plot[0]]
        ys = vectors[:, indices_to_plot[1]]

        edgecolors = ["black"] * len(vectors)

        # Plot the vector using quiver
        for i in range(len(vectors)):
            self.ax.quiver(0, 0, xs[i], ys[i], angles="xy", scale_units="xy", scale=1, color="black", width=0.003, linewidths=0.5)
            self.scatter = self.ax.scatter(xs[i], ys[i], marker=f"${particle_names[i]}$", s=90, color="black")

        self.ax.scatter(xs, ys, facecolors="none", edgecolors=edgecolors, marker="o", s=160)

        # These are not literally x an y label but refer to horizontal and vertical axes, respectively.
        self.ax.set_xlabel(self.axis_labels[indices_to_plot[0]], fontsize=10)
        self.ax.set_ylabel(self.axis_labels[indices_to_plot[1]], fontsize=10, rotation=0)


class Plot2DPopup(QDialog):

    screen_locations = {"x-y": [300, 150], "x-z": [600, 150], "y-z": [900, 150]}

    def __init__(self, parent, button, vectors, experiment_controller, plot_status):
        super().__init__(parent)
        self.experiment_controller = experiment_controller
        self.plot_status = plot_status
        self.resize(400, 400)
        plot_2d_type = button.text()
        self.button = button
        self.setWindowTitle(f"{plot_2d_type} {plot_status}")
        canvas = PlotVectorCanvas2D(self.experiment_controller, self, 3, 3)
        if vectors is not None:
            canvas.plot(vectors, plot_2d_type)
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        self.setLayout(layout)
        self.move(self.screen_locations[plot_2d_type][0], self.screen_locations[plot_2d_type][1])

    def closeEvent(self, event):
        self.done(1)
        self.button.setEnabled(True)
