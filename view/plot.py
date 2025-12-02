from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QComboBox, QPushButton

from view.common.details import HorizontalDivider

from view.plot_view.plot_2D import Plot2DPopup, PlotVectorCanvas2D
from view.plot_view.plot_canvas import PlotVectorCanvas


class PlotQFrame(QFrame):

    blank = "BLANK"
    experiment = "EXPERIMENT"
    transformed = "TRANSFORMED"

    def __init__(self, app, experiment_controller, plot_status=blank):
        super().__init__()
        self.app = app
        self.experiment_controller = experiment_controller
        self.plot_status = plot_status
        self.setFrameShape(QFrame.StyledPanel) # Optional: sets a default styled panel look
        # self.setLineWidth(2) doesn't seem to do anything
        plot_label = QLabel("Plot")
        plot_label.setStyleSheet("background-color: green")
        plot_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        inner_layout = QVBoxLayout(self)
        plot_buttons_2D = QHBoxLayout()
        button1 = QPushButton("x-y")
        button2 = QPushButton("x-z")
        button3 = QPushButton("y-z")
        button1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        plot_buttons_2D.addWidget(button1)
        plot_buttons_2D.addWidget(button2)
        plot_buttons_2D.addWidget(button3)
        if plot_status != PlotQFrame.blank:
            button1.clicked.connect(self.pop_up_plot)
            button2.clicked.connect(self.pop_up_plot)
            button3.clicked.connect(self.pop_up_plot)
        else:
            button1.setEnabled(False)
            button2.setEnabled(False)
            button3.setEnabled(False)
        inner_layout.addLayout(plot_buttons_2D)
        self.canvas = PlotVectorCanvas(self.experiment_controller, self)
        
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        inner_layout.addWidget(self.canvas)

        # self.plot([[3, 4, 5], [5, 3, 3]])

    def plot(self, vectors):
        self.vectors = vectors
        self.canvas.plot(vectors)

    def pop_up_plot(self):
        
        sender_button = self.sender()
        
        if sender_button: # TODO: Is this check necessary? Mplcursors doc recommends.
            sender_button.setEnabled(False)
            dialog = Plot2DPopup(self, sender_button, self.vectors, self.experiment_controller, self.plot_status)
            dialog.show()
            # These two are supposed to bring popup to front ant activate it.
            # They don't seem to make any difference. Show() does everything.
            # dialog.raise_()
            # dialog.activateWindow()