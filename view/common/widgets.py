from PySide6.QtWidgets import QComboBox

import config


class ParticleNamesComboBox(QComboBox):
    def __init__(self, names):
        super().__init__()
        self.update_names(names)
        self.setEditable(True)
        line_edit = self.lineEdit()
        assert line_edit is not None
        line_edit.setReadOnly(True)
        self.setMinimumContentsLength(6)
        self.setCurrentIndex(-1)

    def update_names(self, names, clear_all_existing=False):
        if clear_all_existing:
            self.clear()
        # else: TODO if needed. Get the currently selected one
        # and ensure it is selected after the update.
        #     selected_index = self.currentIndex()
        #     selected_name = self.currentText()

        self.addItems(names)
        if clear_all_existing:
            self.setCurrentIndex(-1)


def create_particle_names_combo_box():
    return ParticleNamesComboBox(config.particle_names)
