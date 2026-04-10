from PySide6.QtWidgets import QMainWindow, QMenu, QMenuBar, QVBoxLayout, QWidget
from PySide6.QtGui import QAction
import qdarktheme

class CustomMenuBar(QMenuBar):
    def __init__(self, view, app, experiment_controller):
        super().__init__()
        self.view = view
        self.app = app
        self.experiment_controller = experiment_controller
        file_menu = self.addMenu("File")
        open_file_action = file_menu.addAction("Open Experiment")
        open_file_action.triggered.connect(self.show_file_browser)
        file_menu.addAction("Save Current")
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)
        
        experiment_menu = self.addMenu("Experiment")
        open_experiment_action = experiment_menu.addAction("Open Experiment File")
        open_experiment_action.triggered.connect(self.show_file_browser)

        exp_submenu = QMenu("Configure Experiment", self)
        experiment_menu.addMenu(exp_submenu)
        create_new_exp_action = QAction("Create new experiment", self)
        exp_submenu.addAction(create_new_exp_action)
        create_new_exp_action.triggered.connect(lambda: self.show_experiment_configuration_form(True))
        experiment_menu.addMenu(exp_submenu)
        edit_current_exp_action = QAction("Edit current experiment", self)
        exp_submenu.addAction(edit_current_exp_action)
        edit_current_exp_action.triggered.connect(lambda: self.show_experiment_configuration_form(False))

        close_experiment_action = experiment_menu.addAction("Close Experiment")
        close_experiment_action.triggered.connect(self.close_experiment)
        save_experiment_action = experiment_menu.addAction("Save Current")
        save_experiment_action.triggered.connect(self.save_experiment)

        help_menu = self.addMenu("Help")
        welcome_action = help_menu.addAction("Welcome")
        manual_action = help_menu.addAction("User's Manual")

        new_submenu = QMenu("Theme", self)
        help_menu.addMenu(new_submenu)
        dark_theme_action = QAction("Dark", self)
        new_submenu.addAction(dark_theme_action)
        dark_theme_action.triggered.connect(self.set_dark_theme)

        light_theme_action = QAction("Light", self)
        new_submenu.addAction(light_theme_action)
        light_theme_action.triggered.connect(self.set_light_theme)

    def set_dark_theme(self):
        qdarktheme.setup_theme("dark")
        # self.set_title_font_for_theme("dark")

    def set_light_theme(self):
        qdarktheme.setup_theme("light")
        # self.set_title_font_for_theme("light")

    def show_file_browser(self):
        print("Show file browser")
    
    def show_experiment_configuration_form(self, create_new=True):
        self.view.show_experiment_configuration_form(create_new)

    def close_experiment(self):
        self.experiment_controller.close_current_experiment()

    def save_experiment(self):
        print("Save")

    def quit_app(self):
        self.app.quit()
