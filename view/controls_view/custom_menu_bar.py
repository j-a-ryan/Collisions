from PySide6.QtWidgets import QMainWindow, QMenu, QMenuBar, QVBoxLayout, QWidget
from PySide6.QtGui import QAction
import qdarktheme

from view.vectors.vector_entry import VectorEntryForm


class CustomMenuBar(QMenuBar):
    def __init__(self, app, experiment_controller):
        super().__init__()
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
        create_experiment_action = experiment_menu.addAction("Create Experiment")
        create_experiment_action.triggered.connect(self.show_experiment_creation_form)
        close_experiment_action = experiment_menu.addAction("Close Experiment")
        close_experiment_action.triggered.connect(self.close_experiment)
        experiment_menu.addAction("Save Current")

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
    
    def show_experiment_creation_form(self):
        dlg = VectorEntryForm(self)
        if dlg.exec() == 1:
            self.experiment_controller.plot_current_experiment()

    def close_experiment(self):
        self.experiment_controller.close_current_experiment()

    def quit_app(self):
        self.app.quit()
