from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QSizePolicy, QLabel, QLineEdit, QSpacerItem
from PySide6.QtGui import Qt
from view.plot_view.plot_2D import PlotVectorCanvas2D

class PlotTabsWidget(QTabWidget):

    plot_2d_types = ['x-y', 'x-z', 'y-z']

    # plot_qframe(s) already plotted. plot_widget_3d could be one or a splitter of two. Vectors to plot the 2D plots
    def __init__(self, parent, plot_widget_3d, experiment_vectors=None, transformed_vectors=None): 
        super().__init__(parent=parent)
        self.widget_plots_2d_exp = None
        self.widget_plots_2d_transf = None

        # Projection Plots
        self.widget_plots_2d_exp = self.plot_2d_plots(experiment_vectors)

        # Add tabs to widget
        self.addTab(plot_widget_3d, "3D Plots")
        if transformed_vectors is not None:
            self.addTab(self.widget_plots_2d_exp, "2D Plots: Experiment")
            self.widget_plots_2d_transf = self.plot_2d_plots(transformed_vectors)
            self.addTab(self.widget_plots_2d_transf, "2D Plots: Transformed")
        else:
            self.addTab(self.widget_plots_2d_exp, "2D Plots")

        self.setStyleSheet("""
            QTabBar::tab {
                border: 1px solid gray; /* General border for all tabs */
                border-bottom-color: #C2C7CB; /* Match the pane border color */
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 5px;
            }
            QTabBar::tab:selected {
                border-color: #0078D7; /* Border color for the selected tab */
                border-bottom-color: transparent; /* Hide bottom border for selected tab */
            }
            QTabWidget::pane { /* The tab widget frame */
                border: 1px solid #C2C7CB;
            }
        """)

    def plot_2d_plots(self, vectors):
        self.plot_2d_widget_all_three = QHBoxLayout()
        for plot_2d_type in self.plot_2d_types:
            self.plot_widget_2d = QWidget()
            canvas = PlotVectorCanvas2D(None, self, 3, 3)#self.experiment_controller, self, 3, 3)
            if vectors is not None:
                canvas.plot(vectors, self.plot_2d_types[0])
            plot_layout = QVBoxLayout()
            heading = QLabel(plot_2d_type)
            heading.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            heading.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            plot_layout.addWidget(heading, alignment=Qt.AlignmentFlag.AlignTop)
            plot_layout.addWidget(canvas, alignment=Qt.AlignmentFlag.AlignCenter)
            self.plot_widget_2d.setLayout(plot_layout)
            self.plot_widget_2d.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.plot_2d_widget_all_three.addWidget(self.plot_widget_2d)
        widget_plots_2d = QWidget()
        widget_plots_2d.setLayout(self.plot_2d_widget_all_three)
        return widget_plots_2d

    def remove(self):
        self.removeTab(1)
        plot_widget_2d_to_remove = self.plot_widget_2d
        self.plot_2d_widget_all_three.removeWidget(plot_widget_2d_to_remove)
        self.plot_2d_widget_all_three = None
        self.plot_widget_2d.deleteLater()
        self.plot_widget_2d = None
        if self.widget_plots_2d_exp is not None:
            self.removeTab(2)
            self.widget_plots_2d_exp.deleteLater()
            self.widget_plots_2d_exp = None
        if self.widget_plots_2d_transf is not None:
            self.removeTab(3)
            self.widget_plots_2d_transf.deleteLater()
            self.widget_plots_2d_transf = None

class ProjectionPlotsTab(QWidget):
    def __init__(self, plot_qframe):
        super().__init__()