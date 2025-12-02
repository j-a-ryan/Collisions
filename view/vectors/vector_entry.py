from PySide6.QtWidgets import QComboBox, QVBoxLayout, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QDialog, QLabel


class VectorEntryForm(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("New Experiment")
        self.setGeometry(100, 100, 400, 300)

        self.main_layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        
        header_layout = QHBoxLayout()
        time_name = QLabel('t')
        x_name = QLabel('X')
        y_name = QLabel('Y')
        z_name = QLabel('Z')
        particle_name = QLabel('Particle Type')
        # time_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # x_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # y_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # z_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        dud = QLabel()
        header_layout.addWidget(time_name)
        header_layout.addWidget(x_name)
        header_layout.addWidget(y_name)
        header_layout.addWidget(z_name)
        header_layout.addWidget(particle_name)
        self.form_layout.addRow(QLabel("Enter 4-momentum vector"))
        self.form_layout.addRow(dud, header_layout)

        self.main_layout.addLayout(self.form_layout)

        self.row_count = 0
        self.add_new_row()

        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.clicked.connect(self.add_new_row)
        self.test_button = QPushButton("Test")
        self.test_button.clicked.connect(self.test)

        self.main_layout.addWidget(self.add_row_button)
        self.main_layout.addWidget(self.test_button)

        self.setLayout(self.main_layout)

    def add_new_row(self):
        self.row_count += 1
        label = QLabel(f"{self.row_count}:")
        time_field = QLineEdit()
        x_field = QLineEdit()
        y_field = QLineEdit()
        z_field = QLineEdit()
        row_layout = QHBoxLayout()
        row_layout.addWidget(time_field)
        row_layout.addWidget(x_field)
        row_layout.addWidget(y_field)
        row_layout.addWidget(z_field)
        particle_combo_box = QComboBox()
        particle_combo_box.setEditable(True)
        particle_combo_box.addItem("e+")
        particle_combo_box.addItem("π")
        particle_combo_box.addItem("p")
        particle_combo_box.setMinimumContentsLength(6)
        particle_combo_box.setCurrentIndex(-1)
        row_layout.addWidget(particle_combo_box)
        self.form_layout.addRow(label, row_layout)

    def test(self):
        self.done(1) # self.close() instead? See the plot2d form, same question