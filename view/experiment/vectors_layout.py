from PySide6.QtCore import Signal
from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
)

import config
from view.common.widgets import create_particle_names_combo_box
from view.experiment.vectors import VectorsGrid


class VectorsFramedLayout(QFrame):
    # Emitted when the grid's contents change whether the form's buttons should be enabled.
    buttons_enabled_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.vector_form = QVBoxLayout(self)
        self.vector_form.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vectors_qvbox_layout = QVBoxLayout()
        self.vectors_qvbox_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vector_form.addLayout(self.vectors_qvbox_layout)

        # Set up vectors grid, its header, its layout, and its parent layout.

        vectors_grid_layout = QGridLayout()
        self.vectors_grid = VectorsGrid(vectors_grid_layout, self)

        header_label = QLabel("Enter four-vectors:")
        requirements_label1 = QLabel(
            f"{config.gui_x}, {config.gui_y}, {config.gui_z} in [{config.xyz_min}, {config.xyz_max}]"
        )  # Insert header and grid for vectors layout
        requirements_label2 = QLabel(f"{config.gui_t} in [0, {config.xyz_max}]")
        requirements_label3 = QLabel(
            f"{config.xyz_decimal_precision}-decimal precision"
        )
        header_label_layout = QHBoxLayout()
        header_label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header_label_layout.addWidget(header_label)
        header_label_layout.addWidget(requirements_label1)
        header_label_layout.addWidget(requirements_label2)
        header_label_layout.addWidget(requirements_label3)
        self.vectors_qvbox_layout.addLayout(header_label_layout)
        self.insert_vectors_grid_layout(
            vectors_grid_layout
        )  # Insert the grid layout into its parent.

        # Add dependent vector panel. In the code, we'll use the term "dependant"
        # for variables, instead of "dependent vector," the term used in th GUI labels.
        self.dependant_layout = QHBoxLayout()
        self.dependant_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        dependant_label = QLabel("Add dependent vector:")
        self.dependant_layout.addWidget(dependant_label)
        self.dependant_combo_box_1 = create_particle_names_combo_box()
        self.dependant_layout.addWidget(self.dependant_combo_box_1)
        self.dependant_sign_plus = QRadioButton("+")
        self.dependant_sign_minus = QRadioButton("-")
        font = QFont()
        font.setPointSize(16)
        # Alternatively, you can specify family and size: font = QFont("Arial", 14)
        self.dependant_sign_plus.setFont(font)
        font = QFont()
        font.setPointSize(20)
        self.dependant_sign_minus.setFont(font)
        self.dependant_sign_plus.setChecked(True)
        self.dependant_sign_group = QButtonGroup(self)
        self.dependant_sign_group.addButton(self.dependant_sign_plus)
        self.dependant_sign_group.addButton(self.dependant_sign_minus)
        dependant_sign_layout = QVBoxLayout()
        dependant_sign_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        dependant_sign_layout.setSpacing(0)
        dependant_sign_layout.setContentsMargins(6, 0, 0, 0)
        dependant_sign_layout.addWidget(self.dependant_sign_plus)
        dependant_sign_layout.addWidget(self.dependant_sign_minus)
        self.dependant_layout.addLayout(dependant_sign_layout)
        self.dependant_combo_box_2 = create_particle_names_combo_box()
        self.dependant_layout.addWidget(self.dependant_combo_box_2)
        self.add_dependant_button = QPushButton("Add")
        self.add_dependant_button.clicked.connect(self.add_dependant)
        self.dependant_combo_box_1.activated.connect(
            self.check_dependant_combo_box_selections
        )
        self.dependant_combo_box_2.activated.connect(
            self.check_dependant_combo_box_selections
        )
        self.dependant_layout.addWidget(self.add_dependant_button)
        self.vector_form.addLayout(self.dependant_layout)
        self.update_combo_boxes(self.vectors_grid.get_particle_names_combo_boxes())

    def initialize_grid_rows(self, set_focus=False, grid_data=None):
        if grid_data:
            self.vectors_grid.add_vector_rows(grid_data)
            self.vectors_grid.refresh_grid()
        else:
            self.vectors_grid.add_vector_row(set_focus)  # Add empty row
            self.vectors_grid.refresh_grid()

    def delete_grid_for_refresh(self):
        while self.vectors_grid_layout.count():
            item = self.vectors_grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.vectors_qvbox_layout.removeItem(self.vectors_grid_layout)

        self.vectors_grid_layout.deleteLater()
        del self.vectors_grid_layout

    def insert_vectors_grid_layout(self, vectors_grid_layout, remove_current=False):
        self.vectors_grid_layout = vectors_grid_layout
        self.vectors_qvbox_layout.addLayout(vectors_grid_layout)
        self.update()  # or more immediate repaint()

    def add_dependant(self):
        coeff2 = 1 if self.dependant_sign_plus.isChecked() else -1
        name1 = self.dependant_combo_box_1.currentText()
        name2 = self.dependant_combo_box_2.currentText()
        available_names = self.get_available_vector_names()
        if len(available_names) > 0:  # Should never be false but....
            new_vector_name = available_names[0]
            dependant = self.vectors_grid.create_linearly_dependent_vector(
                new_vector_name, name1, name2, 1, coeff2
            )
            self.vectors_grid.add_vector_row(False, dependant)
            self.vectors_grid.refresh_grid()

    def set_widgets_to_enable_disable(self, widgets_to_enable_disable):
        self.vectors_grid.set_widgets_to_enable_disable(widgets_to_enable_disable)

    @property
    def backing_vectors(self):
        return self.vectors_grid.backing_vectors

    @property
    def grid_row_count(self):
        return self.vectors_grid.grid_row_count

    def set_buttons_enabled_state(self, enabled: bool) -> None:
        self.buttons_enabled_changed.emit(enabled)

    def get_currently_selected_vector_names(self):
        currently_selected_names = []
        particle_names_combo_boxes = self.vectors_grid.get_particle_names_combo_boxes()
        for combo_box in particle_names_combo_boxes:
            name = combo_box.currentText()
            if len(name) > 0:
                currently_selected_names.append(name)
        return currently_selected_names

    def get_available_vector_names(self, currently_selected_names=None):
        if currently_selected_names is None:
            currently_selected_names = self.get_currently_selected_vector_names()
        available_names = [
            name
            for name in config.particle_names
            if name not in currently_selected_names
        ]
        return available_names

    def update_combo_boxes(self, grid_particle_names_combo_boxes):
        currently_selected_names = self.get_currently_selected_vector_names()

        # Clear the dependant boxes' items and add the currently_selected_items
        self.dependant_combo_box_1.update_names(currently_selected_names, True)
        self.dependant_combo_box_2.update_names(currently_selected_names, True)

        # Iterate over the grid combo boxes, removing from each every item that is in
        # currently_selected_items, with the exception of the item that it has as its selection.
        available_names = self.get_available_vector_names(currently_selected_names)

        for combo_box in grid_particle_names_combo_boxes:
            currently_selected_name = None
            names_to_use = [*available_names]
            if combo_box.currentIndex() != -1:
                currently_selected_name = combo_box.currentText()
                names_to_use.append(currently_selected_name)
                names_to_use = sorted(names_to_use)
            combo_box.update_names(names_to_use, True)
            index_required = combo_box.findText(
                currently_selected_name, Qt.MatchFlag.MatchFixedString
            )

            # Check if the text was actually found (findText returns -1 if not found)
            if index_required >= 0:
                combo_box.setCurrentIndex(index_required)
        if len(available_names) == 0 or len(currently_selected_names) == 0:
            self.add_dependant_button.setEnabled(False)
            self.dependant_combo_box_1.setEnabled(False)
            self.dependant_combo_box_2.setEnabled(False)
            self.dependant_sign_plus.setEnabled(False)
            self.dependant_sign_minus.setEnabled(False)
        else:
            self.add_dependant_button.setEnabled(True)
            self.dependant_combo_box_1.setEnabled(True)
            self.dependant_combo_box_2.setEnabled(True)
            self.dependant_sign_plus.setEnabled(True)
            self.dependant_sign_minus.setEnabled(True)
        self.check_dependant_combo_box_selections()

    def check_dependant_combo_box_selections(self):
        if (
            self.dependant_combo_box_1.currentText()
            and self.dependant_combo_box_2.currentText()
        ):
            self.add_dependant_button.setEnabled(True)
            if (
                self.dependant_combo_box_1.currentText()
                == self.dependant_combo_box_2.currentText()
            ):
                self.dependant_sign_plus.setChecked(True)
                self.dependant_sign_minus.setEnabled(False)
            else:
                # There should be no overriding to disable
                # the minus button at this point.
                self.dependant_sign_minus.setEnabled(True)
        else:
            self.add_dependant_button.setEnabled(False)
