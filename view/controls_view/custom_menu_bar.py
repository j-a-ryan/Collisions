from PySide6.QtWidgets import   QHBoxLayout, QPushButton
from PySide6.QtGui import Qt
import qdarktheme

from resources.help_html import get_user_manual

class MenuButtonPanel(QHBoxLayout):
    def __init__(self, view, app, experiment_controller):
        super().__init__()
        self.view = view
        self.app = app
        self.experiment_controller = experiment_controller
        self.setContentsMargins(0, 2, 0, 2)
        
        file_button = QPushButton("File")
        file_button.clicked.connect(self.load_experiment_file)
        new_button = QPushButton("New")
        new_button.clicked.connect(self.show_blank_experiment_configuration_form)
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.show_loaded_experiment_configuration_form)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_experiment)
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close_experiment)

        how_button = QPushButton("Help")
        how_button.clicked.connect(self.show_manual)
        dark_button = QPushButton("Dark")
        dark_button.clicked.connect(self.set_dark_theme)
        light_button = QPushButton("Light")
        light_button.clicked.connect(self.set_light_theme)
        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.quit_app)
        file_button.setFixedWidth(100)
        new_button.setFixedWidth(100)
        edit_button.setFixedWidth(100)
        save_button.setFixedWidth(100)
        close_button.setFixedWidth(100)
        how_button.setFixedWidth(100)
        dark_button.setFixedWidth(100)
        light_button.setFixedWidth(100)
        quit_button.setFixedWidth(100)
        
        experiment_buttons_layout = QHBoxLayout()
        experiment_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        experiment_buttons_layout.addWidget(file_button)
        experiment_buttons_layout.addWidget(new_button)
        experiment_buttons_layout.addWidget(edit_button)
        experiment_buttons_layout.addWidget(save_button)
        experiment_buttons_layout.addWidget(close_button)
        self.addLayout(experiment_buttons_layout)
        app_buttons_layout = QHBoxLayout()
        app_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        app_buttons_layout.addWidget(how_button)
        app_buttons_layout.addWidget(dark_button)
        app_buttons_layout.addWidget(light_button)
        app_buttons_layout.addWidget(quit_button)
        self.addLayout(app_buttons_layout)

    def set_dark_theme(self):
        qdarktheme.setup_theme("dark")

    def set_light_theme(self):
        qdarktheme.setup_theme("light")
        # self.set_title_font_for_theme("light")

    def load_experiment_file(self):
        self.view.load_experiment()

    def show_blank_experiment_configuration_form(self):
        self.show_experiment_configuration_form(True)

    def show_loaded_experiment_configuration_form(self):
        self.show_experiment_configuration_form(False)
    
    def show_experiment_configuration_form(self, create_new=True):
        self.view.show_experiment_configuration_form(create_new)

    def close_experiment(self):
        self.experiment_controller.close_current_experiment()

    def save_experiment(self):
        self.experiment_controller.save_current_experiment()

    def show_manual(self):
        manual = get_user_manual()
        manual.exec()

    def quit_app(self):
        self.app.quit()
