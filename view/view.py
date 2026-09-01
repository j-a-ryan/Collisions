import csv
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QMessageBox,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

import config
from controller.experiment_controller import ExperimentController
from view.controls import ControlsLayout
from view.experiment.experiment_configuration import ExperimentConfigurationForm
from view.plot import PlotQFrame
from view.plot_view.plot_tabs_widget import PlotTabsWidget
from view.util import PlotStatus

"""

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
"""


class View(QWidget):

    def __init__(self, app):
        super().__init__()
        self.experiment_controller = ExperimentController(self)
        self.app = app
        self.experiment_configuration_form = None
        self.set_up_view()

    def set_up_view(self):
        self.plot_qframe = None
        self.plot_qframe_transformed = None
        self.splitter = None
        self.plot_tabs = None
        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.control_panel = QVBoxLayout()
        self.control_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.set_up_control_panel()

        self.main_layout.addLayout(self.control_panel)
        self.plot_qframe = PlotQFrame(self, self.experiment_controller)
        self.set_plot_tab_widget(self.plot_qframe)

        self.setLayout(self.main_layout)

    def show_experiment_configuration_form(self, create_new, vector_data=None):
        if self.experiment_configuration_form is not None:
            if create_new:
                self.experiment_controller.close_current_experiment()
                self.delete_experiment()  # I had commented this out for some reason. ??? Uncommenting it....
                self.experiment_configuration_form = ExperimentConfigurationForm(self, int(config.max_num_vectors), vector_data)
            else:
                self.experiment_configuration_form.show()
        elif create_new:
            self.experiment_configuration_form = ExperimentConfigurationForm(self, int(config.max_num_vectors), vector_data)
        if self.experiment_configuration_form is not None:
            if self.experiment_configuration_form.exec() == 1:
                self.experiment_controller.plot_current_experiment(initial_plot=True)
            else:  # == 0, presumably
                self.delete_experiment()

    def plot_experiment_vectors(self, collision, extra_circles=None):

        self.clear_experiment_plot(False)

        if self.plot_qframe is not None:  # TODO: This seems to be false always
            frame_to_delete = self.plot_qframe
            self.main_layout.removeWidget(self.plot_qframe)
            frame_to_delete.deleteLater()
        self.plot_qframe = PlotQFrame(self, self.experiment_controller, plot_status=PlotStatus.EXPERIMENT)
        self.plot_qframe.plot(collision, extra_circles)
        self.set_plot_tab_widget(self.plot_qframe, experiment_vectors=collision)

    def plot_transformed_experiment_vectors(self, vectors_transformed, experiment_vectors, extra_circles):

        self.clear_experiment_plot(False)

        if self.plot_qframe is not None:
            frame_to_delete = self.plot_qframe
            self.main_layout.removeWidget(self.plot_qframe)
            frame_to_delete.deleteLater()

        self.plot_qframe = PlotQFrame(self, self.experiment_controller, plot_status=PlotStatus.EXPERIMENT)
        self.plot_qframe.plot(experiment_vectors, extra_circles)
        self.plot_qframe_transformed = PlotQFrame(self, self.experiment_controller, plot_status=PlotStatus.TRANSFORMED)
        self.plot_qframe_transformed.plot(vectors_transformed, extra_circles)

        self.add_transformation_splitter(experiment_vectors=experiment_vectors, transformed_vectors=vectors_transformed)

    def save_experiment(self, vectors):
        header = config.vector_fields
        data = vectors

        # Ignore the "filter" return.  Starting directory empty = current.
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Experiment File", "", "CSV Files (*.csv)")
        if file_path:
            if not file_path.endswith(".csv"):
                file_path += ".csv"
            try:
                with open(file_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(data)
            except (OSError, csv.Error) as e:
                logging.exception("Failed to save experiment to %s", file_path)
                QMessageBox.warning(self, "Save failed", f"Could not save to {file_path}:\n{e}")

    @staticmethod
    def check_csv_rows(rows):
        """Return a human-readable problem string, or None if ``rows`` is a
        usable experiment CSV: a header row exactly matching
        ``config.vector_fields`` followed by at least one data row of the
        same width."""
        expected = list(config.vector_fields)  # copy: guards against config using a tuple
        width = len(expected)
        if not rows:
            return "The file is empty."
        if rows[0] != expected:
            return f"The file's header row must be exactly {expected}."
        data_rows = rows[1:]
        if not data_rows:
            return "The file has a header row but no vector data."
        for line_number, row in enumerate(data_rows, start=2):
            if len(row) != width:
                return f"Line {line_number} has {len(row)} column(s); expected {width}: {expected}."
        return None

    def load_experiment(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
        if not file_path:
            return

        try:
            with open(file_path, newline="") as file:
                rows = list(csv.reader(file))
        except (OSError, UnicodeError, csv.Error) as e:
            QMessageBox.warning(self, "Open failed", f"Could not read {file_path}:\n{e}")
            return

        problem = self.check_csv_rows(rows)
        if problem is not None:
            QMessageBox.warning(self, "Warning", problem)
            return

        self.show_experiment_configuration_form(True, rows[1:])  # rows[1:] strips the header

    def delete_experiment(self):
        if self.experiment_configuration_form is not None:
            self.experiment_configuration_form.deleteLater()
            del self.experiment_configuration_form
            self.experiment_configuration_form = None

    def set_up_control_panel(self):
        self.controls_layout = ControlsLayout(self.experiment_controller)  # QFrame
        self.scroll_area = QScrollArea()
        self.scroll_area.setFixedWidth(230)
        self.scroll_area.setWidgetResizable(True)  # Allows frame/content to resize
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.controls_layout)
        self.control_panel.addWidget(self.scroll_area)

    def clear_controls_layout(self):
        assert self.scroll_area is not None
        assert self.controls_layout is not None

        self.control_panel.removeWidget(self.scroll_area)
        self.scroll_area.setParent(None)
        self.controls_layout.deleteLater()
        self.scroll_area.deleteLater()
        del self.controls_layout
        del self.scroll_area
        self.controls_layout = None
        self.scroll_area = None

        self.set_up_control_panel()

    def reset_transformation_controls(self):
        assert self.controls_layout is not None
        self.controls_layout.reset_transformation_controls()

    def set_controls_for_transformation_plot(self, boost_parameter_A_initial_value=None):
        assert self.controls_layout is not None
        self.controls_layout.set_controls_for_transformation_plot(boost_parameter_A_initial_value)

    def clear_experiment_plot(self, set_up_blank_afterwards):

        if self.plot_qframe_transformed is not None:
            frame_to_delete_transformed = self.plot_qframe_transformed
            self.main_layout.removeWidget(frame_to_delete_transformed)
            frame_to_delete_transformed.deleteLater()
            self.plot_qframe_transformed = None

        assert self.plot_qframe is not None
        frame_to_delete = self.plot_qframe  # Just being sure no mistaken identity. Probably being superstitious.
        self.main_layout.removeWidget(frame_to_delete)
        frame_to_delete.deleteLater()
        self.plot_qframe = None

        if self.plot_tabs is not None:
            self.plot_tabs.remove()
            self.main_layout.removeWidget(self.plot_tabs)
            plot_tabs_to_delete = self.plot_tabs
            plot_tabs_to_delete.deleteLater()
            self.plot_tabs = None

        if self.splitter is not None:
            splitter_to_delete = self.splitter
            self.main_layout.removeWidget(splitter_to_delete)
            splitter_to_delete.deleteLater()
            self.splitter = None

        if set_up_blank_afterwards:
            # Put the blank plot in
            self.plot_qframe = PlotQFrame(self, self.experiment_controller)
            # self.main_layout.addWidget(self.plot_qframe)
            self.set_plot_tab_widget(self.plot_qframe)

    def add_transformation_splitter(self, experiment_vectors=None, transformed_vectors=None):
        assert self.plot_qframe is not None
        assert self.plot_qframe_transformed is not None

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.plot_qframe)
        self.splitter.addWidget(self.plot_qframe_transformed)
        # self.main_layout.addWidget(self.splitter)
        self.set_plot_tab_widget(self.splitter, experiment_vectors=experiment_vectors, transformed_vectors=transformed_vectors)

    def set_plot_tab_widget(
        self, plot_qframe_to_be_set_in_tab, experiment_vectors=None, transformed_vectors=None
    ):  # Need a name to distinquish it from plot_qframe
        self.plot_tabs = PlotTabsWidget(
            self, plot_qframe_to_be_set_in_tab, experiment_vectors=experiment_vectors, transformed_vectors=transformed_vectors
        )
        self.main_layout.addWidget(self.plot_tabs)

    def set_up_controls(self, vector_names, vector_set_xyz):
        assert self.controls_layout is not None
        self.controls_layout.clear_controls()
        self.controls_layout.add_boost_A_slider(1)
        self.controls_layout.add_txyz_sliders(vector_names, vector_set_xyz)
