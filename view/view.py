from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QSizePolicy, QComboBox, QPushButton
from PySide6.QtCore import QSize, Qt

from controller.experiment_controller import ExperimentController
from view.controls import ControlsLayout
from view.controls_view.custom_menu_bar import CustomMenuBar
from view.plot import PlotQFrame
from view.plot_view.plot_tabs_widget import PlotTabsWidget
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

    def set_up_view(self):
        self.plot_qframe = None
        self.plot_qframe_transformed = None
        self.splitter = None
        self.plot_tabs = None
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
        self.plot_qframe = PlotQFrame(self.app, self.experiment_controller)
        # self.layout.addWidget(self.plot_qframe) # Set up with a blank plot
        self.set_plot_tab_widget(self.plot_qframe)

        self.setLayout(self.layout)

    def plot_experiment_vectors(self, vectors):

        self.clear_experiment_plot(False)

        if self.plot_qframe is not None:
            frame_to_delete = self.plot_qframe
            self.layout.removeWidget(self.plot_qframe)
            frame_to_delete.deleteLater()
        self.plot_qframe = PlotQFrame(self.app, self.experiment_controller, plot_status=PlotQFrame.experiment)
        self.plot_qframe.plot(vectors=vectors)
        # self.layout.addWidget(self.plot_qframe)
        self.set_plot_tab_widget(self.plot_qframe, experiment_vectors=vectors)    

    def plot_transformed_experiment_vectors(self, vectors_transformed, experiment_vectors):

        self.clear_experiment_plot(False)

        if self.plot_qframe is not None:
            frame_to_delete = self.plot_qframe
            self.layout.removeWidget(self.plot_qframe)
            frame_to_delete.deleteLater()

        self.plot_qframe = PlotQFrame(self.app, self.experiment_controller, plot_status=PlotQFrame.experiment)
        self.plot_qframe.plot(vectors=experiment_vectors)
        self.plot_qframe_transformed = PlotQFrame(self.app, self.experiment_controller, plot_status=PlotQFrame.transformed)
        self.plot_qframe_transformed.plot(vectors=vectors_transformed)

        self.add_transformation_splitter(experiment_vectors=experiment_vectors, transformed_vectors=vectors_transformed)

    def clear_experiment_plot(self, set_up_blank_afterwards):

        if self.plot_qframe_transformed is not None:
            frame_to_delete_transformed = self.plot_qframe_transformed
            self.layout.removeWidget(frame_to_delete_transformed)
            frame_to_delete_transformed.deleteLater()
            self.plot_qframe_transformed = None
        
        frame_to_delete = self.plot_qframe # Just being sure no mistaken identity. Probably being superstitious.
        self.layout.removeWidget(frame_to_delete)
        frame_to_delete.deleteLater()
        self.plot_qframe = None

        if self.plot_tabs is not None:
            self.plot_tabs.remove()
            self.layout.removeWidget(self.plot_tabs)
            plot_tabs_to_delete = self.plot_tabs
            plot_tabs_to_delete.deleteLater()
            self.plot_tabs = None

        if self.splitter is not None:
            splitter_to_delete = self.splitter
            self.layout.removeWidget(splitter_to_delete)
            splitter_to_delete.deleteLater()
            self.splitter = None

        if set_up_blank_afterwards:
            # Put the blank plot in
            self.plot_qframe = PlotQFrame(self.app, self.experiment_controller)
            # self.layout.addWidget(self.plot_qframe)
            self.set_plot_tab_widget(self.plot_qframe)

    def add_transformation_splitter(self, experiment_vectors=None, transformed_vectors=None):

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.plot_qframe)
        self.splitter.addWidget(self.plot_qframe_transformed)
        # self.layout.addWidget(self.splitter)
        self.set_plot_tab_widget(self.splitter, experiment_vectors=experiment_vectors, transformed_vectors=transformed_vectors)

    def set_plot_tab_widget(self, plot_qframe_to_be_set_in_tab, experiment_vectors=None, transformed_vectors=None): # Need a name to distinquish it from plot_qframe
        self.plot_tabs = PlotTabsWidget(self, plot_qframe_to_be_set_in_tab,
                                        experiment_vectors=experiment_vectors, transformed_vectors=transformed_vectors)
        self.layout.addWidget(self.plot_tabs)
