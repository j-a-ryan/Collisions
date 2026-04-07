import config
from PySide6.QtWidgets import QComboBox, QGridLayout, QLabel, QLineEdit, QSizePolicy, QSpacerItem, QStyle, QWidget
from PySide6.QtGui import Qt

from view.experiment.validation import VectorValidation
from view.experiment.vector_components import VectorMemberField
from view.experiment.widgets import DeleteVectorRowButton

"""
Encapsulates the 4-vector collection on the GUI side. (This is not the model.)
Handles the user's CRUD actions, such as adding/deleting a vector. Includes
the GUI widget 
"""
class VectorsGrid:

    header_row = config.gui_vectors_header
    num_columns = len(header_row)
    max_num_vectors = config.max_num_vectors

    def __init__(self, grid_layout, form): # We may need the whole parent, but for now just the style.
        self._grid_layout = grid_layout
        self.parent_form = form
        self._backing_vectors = [] # 2D array, array of vectors
        self.set_up_grid(self._grid_layout)

    def set_widgets_to_enable_disable(self, widgets_to_enable_disable):
        self.widgets_to_enable_disable = widgets_to_enable_disable
        self.vector_validation = VectorValidation(self)
        
    def __backing_vectors_row_index(self, grid_layout_row_index):
        return grid_layout_row_index - 1
    
    @property
    def grid_row_count(self):
        return self._grid_layout.rowCount() # Should be same as len(self.backing_vectors) + 1
    
    @property
    def backing_vectors(self):
        return self._backing_vectors
    
    @property
    def grid_layout(self):
        return self._grid_layout
    
    def set_up_grid(self, grid_layout):
        t_label = QLabel("t")
        x_label = QLabel("X")
        y_label = QLabel("Y")
        z_label = QLabel("Z")
        pt_label = QLabel("Name")

        # Set up the grid layout and the Vectors backing object for it.
        # Load these header lables into grid layout, leaving the first column blank. It is
        # the vector index column and we don't need or want a header for it.
        grid_layout.addWidget(t_label, 0, 1, alignment=(Qt.AlignCenter | Qt.AlignTop))
        grid_layout.addWidget(x_label, 0, 2, alignment=(Qt.AlignCenter | Qt.AlignTop))
        grid_layout.addWidget(y_label, 0, 3, alignment=(Qt.AlignCenter | Qt.AlignTop))
        grid_layout.addWidget(z_label, 0, 4, alignment=(Qt.AlignCenter | Qt.AlignTop))
        grid_layout.addWidget(pt_label, 0, 5, alignment=(Qt.AlignCenter | Qt.AlignTop))

    """
    After user enters data and grid entries are all deemed valid, this method updates the backing
    grid.
    """
    def update_backing_grid(self):
        num_rows = self.grid_layout.rowCount()
        # num_columns = self.grid_layout.columnCount()
        del self._backing_vectors # Good idea? Set to None instead?
        self._backing_vectors = []
        for i in range(1, num_rows): # Skip over the header row
            row = []
            for j in range(1, 6): # Skip the index column (0) and get the 4-vector and its name
                item = self.grid_layout.itemAtPosition(i, j) # Skip over the header row and index label column
                if item: # Needed?
                    widget = item.widget()
                    if widget:
                        if isinstance(widget, QLineEdit):
                            row.append(widget.text())
                        else: # assuming QComboBox for now
                            row.append(widget.currentText())
            self._backing_vectors.append(row)
            
    
    """
    Multipurpose. When adding a blank row as a result of user click event, set_focus should be True, and the
    other two arguments left to default None. When refreshing the grid from backing vectors, set_focus should
    be left to False and the fresh grid layout and a row from the backing vectors should be passed in as
    arguments for the other two parameters. Presumably, both fresh_grid_layout and field_values are None or
    both are not None, but it's possible that there may be a use case for only the former to be not None (a 
    fresh grid that we don't want to populate with values.)

    N.B.: If fresh_grid_layout is used using field_values, then these will be considered valid and
    form validation will not be run, as we would presumably be in the midst of a repaint using valid values. 
    To run validation would call refresh of backing vectors using the stale grid, ruining the refresh.
    """
    def add_vector_row(self, set_focus=False, field_values=None):

        new_row_index = self.grid_row_count # We already have at least a header row at index 0.
        set_field_values = field_values is not None
        row_index_label = QLabel(f"{new_row_index}:")
        time_field = VectorMemberField(self.vector_validation, set_field_values)
        x_field = VectorMemberField(self.vector_validation, set_field_values)
        y_field = VectorMemberField(self.vector_validation, set_field_values)
        z_field = VectorMemberField(self.vector_validation, set_field_values)
        particle_combo_box = QComboBox()
        particle_combo_box.addItem("k1")
        particle_combo_box.addItem("k2")
        particle_combo_box.addItem("k3")
        particle_combo_box.addItem("k4")
        particle_combo_box.addItem("k5")
        particle_combo_box.addItem("k6")
        particle_combo_box.setEditable(True)
        particle_combo_box.lineEdit().setReadOnly(True)
        particle_combo_box.setMinimumContentsLength(6)
        particle_combo_box.setCurrentIndex(-1)
        particle_combo_box.activated.connect(self.activated)

        if set_field_values:
            time_field.setText(field_values[0])
            x_field.setText(field_values[1])
            y_field.setText(field_values[2])
            z_field.setText(field_values[3])
            index = particle_combo_box.findText(field_values[4], Qt.MatchFixedString)
            # If the text is found (index is not -1), set the current index
            if index >= 0: # Should not be necessary
                particle_combo_box.setCurrentIndex(index)

        self.grid_layout.addWidget(row_index_label, new_row_index, 0, alignment=Qt.AlignTop)
        self.grid_layout.addWidget(time_field, new_row_index, 1, alignment=Qt.AlignTop)
        self.grid_layout.addWidget(x_field, new_row_index, 2, alignment=Qt.AlignTop)
        self.grid_layout.addWidget(y_field, new_row_index, 3, alignment=Qt.AlignTop)
        self.grid_layout.addWidget(z_field, new_row_index, 4, alignment=Qt.AlignTop)
        self.grid_layout.addWidget(particle_combo_box, new_row_index, 5)
        
        delete_row_button = DeleteVectorRowButton(self.parent_form.style())  # Row's index = row count. The 0th row is the headers.
        if new_row_index != 1:
            delete_icon = self.parent_form.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical) #SP_BrowserStop
            delete_row_button.setIcon(delete_icon)
        else:
            delete_row_button.setEnabled(False) # In effect, a spacer. Spacer and blank widget didn't work
            delete_row_button.setStyleSheet("border: none;")
        delete_row_button.setFocusPolicy(Qt.NoFocus)
        delete_row_button.clicked.connect(lambda: self.delete_vector(delete_row_button))
        self.grid_layout.addWidget(delete_row_button, new_row_index, 7, alignment=Qt.AlignTop)
            
        self.vector_validation.add_fields(particle_combo_box, time_field, x_field, y_field, z_field)
        self.parent_form.set_buttons_enabled_state(False)

        # Check delete button activation states.
        DeleteVectorRowButton.check_button_states(self.grid_layout)

        if set_focus:
            first_line_edit_in_new_row = self.grid_layout.itemAtPosition(new_row_index, 1) # Column 0 is index label; column 1 is presumably time field. 
            first_line_edit_in_new_row.widget().setFocus()

    def activated(self, index):
        self.update_backing_grid()
        self.vector_validation.run_validation(False)

    """
    Deletes vector from both grid layout and backing vectors. The problem is that the deletion from
    the former won't occur until the method has run. So, confusion about row indices must be carefully
    avoided.

    N.B.: If any item has a layout in it, instead of a widget, we may need to delete
    recursively. See research delete_gridlayout_row.py.
    """
    def delete_vector(self, delete_row_button):
        
        # Get needed parameters
        num_grid_vectors_before_deletion = self.grid_row_count - 1
        index = self.grid_layout.indexOf(delete_row_button)
        index_of_grid_row_to_delete, _, _, _ = self.grid_layout.getItemPosition(index)

        # Delete old grid layout and initialize new one.
        self.parent_form.delete_grid_for_refresh()
        del self._grid_layout
        self.vector_validation.remove_fields()
        self._grid_layout = QGridLayout()
        self.set_up_grid(self._grid_layout) # put the column headers in

        # From the backing vectors delete the unwanted row.
        backing_vectors_row_index = self.__backing_vectors_row_index(index_of_grid_row_to_delete)
        
        # Ensure the row to be deleted isn't just an new GUI row that does not yet
        # have a backing vectors counterpart yet.
        if len(self._backing_vectors) > backing_vectors_row_index:
            del self._backing_vectors[backing_vectors_row_index]

        if len(self._backing_vectors) == 0: # We deleted the only row that had a backing vector.
            self.add_vector_row(set_focus=True)
        else:
            for row in self._backing_vectors:
                self.add_vector_row(set_focus=False, field_values=row)
        # We may need to add more rows to recreate the grid which may have had several GUI-only rows in
        # certain edge cases.
        # So, num_grid_rows_we_should_have = num_grid_vectors_before_deletion - 1
        # Need (self._grid_layout.rowCount() - 1) to equal num_grid_rows_we_should_have
        # Hence:
        while self._grid_layout.rowCount() < num_grid_vectors_before_deletion:
            self.add_vector_row(set_focus=True)

        self.parent_form.insert_vectors_grid_layout(self._grid_layout, True)
        
        # Check delete button activation states.
        DeleteVectorRowButton.check_button_states(self.grid_layout)

        self.vector_validation.run_validation(False) # All should be valid, but we need to refresh button enablement statuses

    def set_widgets_enabled_states(self, enabled):
        for name, widget in self.widgets_to_enable_disable.items():
            if name != "ADD_ROW" or (self.grid_row_count - 1) < self.max_num_vectors:
                widget.setEnabled(enabled)
            # elif name == "ADD_ROW":
            #     print("Not enabled add row button because row count " + str(self.grid_row_count))