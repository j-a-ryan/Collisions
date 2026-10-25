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
        if self.count() > 1:
            self.setCurrentIndex(-1)

    def update_names(self, names, names_already_selected=None):
        if names_already_selected is None:
            names_already_selected = []
        names_to_show = [x for x in names if x not in names_already_selected]
        for name in names_to_show:
            self.addItem(name)


def create_particle_names_combo_box(names=None):
    return ParticleNamesComboBox(config.particle_names)
