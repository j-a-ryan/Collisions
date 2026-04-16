from PySide6.QtWidgets import QMainWindow, QMenu, QMenuBar, QMessageBox, QVBoxLayout, QWidget
from PySide6.QtGui import QAction
import qdarktheme

class CustomMenuBar(QMenuBar):
    def __init__(self, view, app, experiment_controller):
        super().__init__()
        self.view = view
        self.app = app
        self.experiment_controller = experiment_controller
        # file_menu = self.addMenu("Application")
        # quit_action = file_menu.addAction("Quit")
        # quit_action.triggered.connect(self.quit_app)
        
        experiment_menu = self.addMenu("Experiment")
        open_experiment_action = experiment_menu.addAction("Open Experiment File")
        open_experiment_action.triggered.connect(self.load_experiment_file)
        exp_submenu = QMenu("Set up experiment", self)
        experiment_menu.addMenu(exp_submenu)
        create_new_exp_action = QAction("New experiment", self)
        exp_submenu.addAction(create_new_exp_action)
        create_new_exp_action.triggered.connect(self.show_blank_experiment_configuration_form)
        experiment_menu.addMenu(exp_submenu)
        edit_current_exp_action = QAction("Change current experiment", self)
        exp_submenu.addAction(edit_current_exp_action)
        edit_current_exp_action.triggered.connect(self.show_loaded_experiment_configuration_form)
        close_experiment_action = experiment_menu.addAction("End Experiment")
        close_experiment_action.triggered.connect(self.close_experiment)
        save_experiment_action = experiment_menu.addAction("Save Current")
        save_experiment_action.triggered.connect(self.save_experiment)

        help_menu = self.addMenu("Help")
        welcome_action = help_menu.addAction("Welcome")
        welcome_action.triggered.connect(self.show_welcome)
        manual_action = help_menu.addAction("User's Manual")
        manual_action.triggered.connect(self.show_manual)

        new_submenu = QMenu("Theme", self)
        help_menu.addMenu(new_submenu)
        dark_theme_action = QAction("Dark", self)
        new_submenu.addAction(dark_theme_action)
        dark_theme_action.triggered.connect(self.set_dark_theme)

        light_theme_action = QAction("Light", self)
        new_submenu.addAction(light_theme_action)
        light_theme_action.triggered.connect(self.set_light_theme)

        # configure_new_experiment_action = experiment_menu.addAction("Configure new experiment")
        # configure_new_experiment_action.triggered.connect(self.show_blank_experiment_configuration_form)
        # reconfigure_current_experiment_action = experiment_menu.addAction("Reconfigure current experiment")
        # reconfigure_current_experiment_action.triggered.connect(self.show_loaded_experiment_configuration_form)

    def set_dark_theme(self):
        qdarktheme.setup_theme("dark")
        # self.set_title_font_for_theme("dark")

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

    def show_welcome(self):
        msg = QMessageBox()
        msg.setWindowTitle("Collisions-QCD/TMD")
        msg.setText("Collisions-QCD/TMD")
        msg.setInformativeText("This is an application for use in the visualization of the outcomes of particle " +\
                    "collider experiments in QCD/TMD (quantum chromodynamics/transverse " +\
                    "momentum dependent parton distribution functions).")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        font = msg.font()
        font.setPointSize(11)
        msg.setFont(font)
        msg.exec()

    def show_manual(self):
        manual = get_user_manual()
        manual.exec()

    # def quit_app(self):
    #     self.app.quit()

def get_user_manual():
    msg = QMessageBox()
    msg.setWindowTitle("Collisions-QCD/TMD Quick Start")
    msg.setText("Quick Start\n")
    msg.setInformativeText('1. Experiment -> Configure experiment -> Create new experiment. Fill in the vector member values.\n' +\
                '\n2. Options: (1.) submit the vector set - "experiment" and graph it, (b.) check for transformation issues, '+\
                'or (c.) to save it as a file.\n' +\
                '\n3. After submitting/graphing, use sliders to adjust adjust vectors or click on two points to transform the ' +\
                'vector set. Select the transformation type and proceed. Use sliders to adjust both graphs simultaneously.')
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)
    font = msg.font()
    font.setPointSize(11)
    msg.setFont(font)
    return msg
