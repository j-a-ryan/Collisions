from PySide6.QtWidgets import QComboBox

import config


def create_particle_names_combo_box(names=None):
    particle_combo_box = QComboBox()
    if names is None:
        names = config.particle_names
    for name in names:
        particle_combo_box.addItem(name)
    particle_combo_box.setEditable(True)
    particle_combo_box.lineEdit().setReadOnly(True)
    particle_combo_box.setMinimumContentsLength(6)
    particle_combo_box.setCurrentIndex(-1)
    return particle_combo_box
