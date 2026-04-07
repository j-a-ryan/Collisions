from PySide6.QtWidgets import QComboBox

import config

class VectorValidation():

    def __init__(self, vectors_grid):
        self.vectors_grid = vectors_grid
        self.fields = []
        self.name_combo_boxes = []
        box = QComboBox()
        self.default_combobox_stylesheet = box.styleSheet()

    def add_widget(self, widget):
        self.widgets_to_enable_disable.append(widget)

    def add_fields(self, name_combo_box, *fields):
        self.name_combo_boxes.append(name_combo_box)
        self.fields.extend(fields)

    def remove_fields(self):
        self.fields.clear()

    def remove_field(self, field):
        if field in self.fields: # Shouldn't be necessary, but error if not in list
            self.fields.remove(field)

    def field_updated(self, validly):
        if not validly:
            self.vectors_grid.set_widgets_enabled_states(False)
        else:
            self.run_validation()    

    # Check each field. If all are valid, tell the vectors object
    # to update its backing grid and ensure widgets' enabled state is
    # correct.
    def run_validation(self, backing_grid_update_prudent=True):
        all_valid = True
        for field in self.fields:
            if not field.currently_valid:
                all_valid = False
                break

        valid = self.check_name_combo_boxes() # We still need to check even if LineEdits are invalid, so as to update boxes' colors
        if not valid:
            all_valid = False # all_valid might already be false here but we needed to update combobox's colors.
        
        if all_valid:
            if backing_grid_update_prudent:
                self.vectors_grid.update_backing_grid() 
        self.vectors_grid.set_widgets_enabled_states(all_valid)

    def check_name_combo_boxes(self):
        boxes_with_invalid_text = [] # duplicates and empty strings
        valid = True
        
        for i in range(len(self.name_combo_boxes)):
            boxi = self.name_combo_boxes[i]
            if not boxi.currentText(): # Empty string is invalid
                boxes_with_invalid_text.append(boxi)
            else:
                for j in range(len(self.name_combo_boxes)):
                    if i != j:                        
                        boxj = self.name_combo_boxes[j]
                        if not boxi.currentText(): # Empty string is invalid
                            boxes_with_invalid_text.append(boxi)
                        else: # Now check for duplicates
                            if boxi.currentText() == boxj.currentText():
                                if boxi not in boxes_with_invalid_text:
                                    boxes_with_invalid_text.append(boxi)
                                if boxj not in boxes_with_invalid_text:
                                    boxes_with_invalid_text.append(boxj)
        if len(boxes_with_invalid_text) > 0:
            valid = False
        for box in self.name_combo_boxes: # The QLineEdits handle their own validity colorization. QComboBoxes we do by hand.
            if box in boxes_with_invalid_text and box.currentText(): # Do not show red/invalid color just for empty string.
                box.setStyleSheet("background-color: " + config.form_field_invalid_color + ";")
            else:
                box.setStyleSheet(self.default_combobox_stylesheet)
        return valid

