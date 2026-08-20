from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from view.plot_view.plot_2D import Plot2DPopup
from view.plot_view.plot_canvas import PlotVectorCanvas
from view.util import PlotStatus


class PlotQFrame(QFrame):

    def __init__(self, view, experiment_controller, plot_status=PlotStatus.BLANK):
        super().__init__()
        self.view = view
        self.experiment_controller = experiment_controller
        self.plot_status = plot_status
        self.setFrameShape(QFrame.Shape.StyledPanel)  # Optional: sets a default styled panel look
        # self.setLineWidth(2) doesn't seem to do anything
        plot_label = QLabel("Plot")
        plot_label.setStyleSheet("background-color: green")
        plot_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        inner_layout = QVBoxLayout(self)
        plot_buttons_2D = QHBoxLayout()
        button1 = QPushButton("x-y")
        button2 = QPushButton("x-z")
        button3 = QPushButton("y-z")
        button1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        button2.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        button3.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        plot_buttons_2D.addWidget(button1)
        plot_buttons_2D.addWidget(button2)
        plot_buttons_2D.addWidget(button3)
        if plot_status != PlotStatus.BLANK:
            button1.clicked.connect(self.pop_up_plot)
            button2.clicked.connect(self.pop_up_plot)
            button3.clicked.connect(self.pop_up_plot)
        else:
            button1.setEnabled(False)
            button2.setEnabled(False)
            button3.setEnabled(False)
        inner_layout.addLayout(plot_buttons_2D)
        self.canvas = PlotVectorCanvas(self.view, self.experiment_controller, plot_status, self)

        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        inner_layout.addWidget(self.canvas)

    def plot(self, collision, extra_circles=None):
        self.vectors = collision
        self.canvas.plot(collision, extra_circles)

    def pop_up_plot(self):

        sender_button = self.sender()

        if isinstance(sender_button, QPushButton):
            sender_button.setEnabled(False)
            dialog = Plot2DPopup(self, sender_button, self.vectors, self.experiment_controller, self.plot_status)
            dialog.show()
            # These two are supposed to bring popup to front ant activate it.
            # They don't seem to make any difference. Show() does everything.
            # dialog.raise_()
            # dialog.activateWindow()
