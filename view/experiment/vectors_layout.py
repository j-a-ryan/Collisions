from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
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
        self.dependant_sign_plus = QRadioButton("+")
        self.dependant_sign_minus = QRadioButton("-")
        self.dependant_sign_plus.setChecked(True)
        self.dependant_sign_group = QButtonGroup(self)
        self.dependant_sign_group.addButton(self.dependant_sign_plus)
        self.dependant_sign_group.addButton(self.dependant_sign_minus)
        dependant_sign_layout = QVBoxLayout()
        dependant_sign_layout.setSpacing(0)
        dependant_sign_layout.setContentsMargins(0, 0, 0, 0)
        dependant_sign_layout.addWidget(self.dependant_sign_plus)
        dependant_sign_layout.addWidget(self.dependant_sign_minus)
        self.dependant_layout.addLayout(dependant_sign_layout)
        self.add_dependant_button = QPushButton("Add")
        self.add_dependant_button.clicked.connect(self.add_dependant)
        self.dependant_layout.addWidget(self.add_dependant_button)
        self.vector_form.addLayout(self.dependant_layout)

    def initialize_grid_rows(self, set_focus=False, grid_data=None):
        if grid_data:
            self.vectors_grid.add_vector_rows(grid_data)
            self.vectors_grid.refresh_grid()
        else:
            self.vectors_grid.add_vector_row(set_focus)  # Add empty row

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
        pass  # is_add = self.dependant_sign_plus.isChecked()

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
