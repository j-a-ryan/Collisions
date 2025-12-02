from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QSizePolicy, QComboBox, QPushButton
from PySide6.QtCore import QSize, Qt

from controller.experiment_controller import ExperimentController
from view.controls import ControlsLayout
from view.controls_view.custom_menu_bar import CustomMenuBar
from view.plot import PlotQFrame
from view.transformations import TransformationsLayout

'''

To remove an existing layout from a PySide6 widget and replace it 
with a new one, you can follow these steps:

    Clear the existing layout: You need to remove all items (widgets 
    and sub-layouts) from the current layout. A safe way to do this 
    is to iterate through the layout items and explicitly delete any
    widgets using deleteLater(). This ensures proper cleanup and 
    prevents memory leaks.

    from PySide6.QtWidgets import QLayout, QWidget, QLayoutItem

    def clear_layout(layout: QLayout):
        if layout is None:
            return
        while layout.count():
            item: QLayoutItem = layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()
            elif item.layout() is not None:
                clear_layout(item.layout()) # Recursively clear sub-layouts

Unset the old layout: After clearing its contents, you can effectively "unset" 
the old layout from the widget by setting a new layout.

widget.setLayout(None) # Unset the old layout

Next set the new layout: widget.setLayout(newLayout)
'''
class View(QWidget):

    def __init__(self, app):
        super().__init__()
        self.experiment_controller = ExperimentController(self)
        self.app = app
        self.set_up_view()

    def set_up_view(self, plot_qframe=None):
        self.plot_qframe = None
        self.plot_qframe_transformed = None
        self.splitter = None
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        controls_layout = ControlsLayout()
        control_panel = QVBoxLayout()
        control_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        menu_bar = CustomMenuBar(self.app, self.experiment_controller)
        menu_bar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        control_panel.addWidget(menu_bar)
        control_panel.addWidget(controls_layout)

        self.layout.addLayout(control_panel)
        if plot_qframe is not None:
            print("vectors")
            self.plot_qframe = plot_qframe
        else:
            print("plot blank")
            self.plot_qframe = PlotQFrame(self.app, self.experiment_controller)
        self.layout.addWidget(self.plot_qframe)

        self.setLayout(self.layout)

    def plot_experiment_vectors(self, vectors):
        print("Plot...")

        self.clear_experiment_plot()

        if self.plot_qframe is not None:
            print("deleting")
            frame_to_delete = self.plot_qframe
            self.layout.removeWidget(self.plot_qframe)
            frame_to_delete.deleteLater()
        self.plot_qframe = PlotQFrame(self.app, self.experiment_controller, plot_status=PlotQFrame.experiment)
        self.plot_qframe.plot(vectors=vectors)
        self.layout.addWidget(self.plot_qframe)        

    def plot_transformed_experiment_vectors(self, vectors):
        print("Plot transformed...")

        self.clear_experiment_plot()

        if self.plot_qframe is not None:
            print("deleting2 to replot")
            frame_to_delete = self.plot_qframe
            self.layout.removeWidget(self.plot_qframe)
            frame_to_delete.deleteLater()
        self.plot_qframe = PlotQFrame(self.app, self.experiment_controller, plot_status=PlotQFrame.experiment)
        self.plot_qframe.plot(vectors=vectors)

        self.plot_qframe_transformed = PlotQFrame(self.app, self.experiment_controller, plot_status=PlotQFrame.transformed)
        self.plot_qframe_transformed.plot(vectors=vectors)

        # self.layout.addWidget(self.plot_qframe)
        # self.layout.addWidget(self.plot_qframe_transformed)

        self.add_transformation_splitter(self.plot_qframe, self.plot_qframe_transformed)

    def clear_experiment_plot(self):
        print("clear")
        # self.set_up_view()
        # self.layout.removeWidget(self.plot_qframe)
        print("deleting3")

        if self.plot_qframe_transformed is not None:
            print("delete transformed frame")
            frame_to_delete_transformed = self.plot_qframe_transformed
            self.layout.removeWidget(frame_to_delete_transformed)
            frame_to_delete_transformed.deleteLater()
            self.plot_qframe_transformed = None
        else:
            print("no transformed frame to delete")

        frame_to_delete = self.plot_qframe # Just being sure no mistaken identity. Probably being superstitious.
        self.layout.removeWidget(frame_to_delete)
        frame_to_delete.deleteLater()
        self.plot_qframe = None

        if self.splitter is not None:
            splitter_to_delete = self.splitter
            self.layout.removeWidget(splitter_to_delete)
            splitter_to_delete.deleteLater()
            self.splitter = None
        

        self.plot_qframe = PlotQFrame(self.app, self.experiment_controller)
        self.layout.addWidget(self.plot_qframe)

    def add_transformation_splitter(self, plot_qframe, plot_qframe_transformed):

        # self.hbox_layout = QHBoxLayout() #or (self)?
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(plot_qframe)
        self.splitter.addWidget(plot_qframe_transformed)
        # self.hbox.addWidget(splitter)
        self.layout.addWidget(self.splitter)
