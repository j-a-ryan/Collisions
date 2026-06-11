from PySide6.QtWidgets import  QDialog, QHBoxLayout, QMessageBox, QPushButton, QTextBrowser, QVBoxLayout
from PySide6.QtGui import Qt
import qdarktheme

def get_user_manual():
    dialog = QDialog()
    dialog.setWindowTitle("Collisions User Manual")
    dialog.resize(750, 500)

    browser = QTextBrowser(dialog)
    
    html_content = """
    <html>
    <head>
        <style>
            p { font-size: 16px; text-align: left;}
            <!--h2 { color: #2c3e50; }
            a { color: #3498db; text-decoration: none; }-->
        </style>
    </head>
    <body>
        <h1><img src="resources/collisionicon.png" alt="Collisions icon" width="100" height="100">  Collisions User Manual</h1>
        <h2>Introduction</h2>
        <p>Collisions is a tool for visualizing the vectors of particles emerging from events ("collision") during particle accelerator experiments.
            The vectors are four-vectors entered by the user as a set and then graphed. The user can transform the collision vectors with a 
            transformation matrix which is described below. The application is specific to a certain stream of QCD research, in particular transverse
            momentup distribution research. However, much of the code offers itself as a platform for other research programs that similarly
            consider the vectors of particles emerging from accelerator events.
        </p>
        <h2>Quick Start</h2>
        <p>Usage
        <ol>
            <li>Use buttons to open an experiment file, create a new experiment, edit the currently loaded experiment,
                save, or close the currently loaded experiment. Configure your vectors in the form. To learn how to do this, click the "new"
                button to open the experiment configuration form. Type your vectors' components into the form fields and press the "submit" button.</li>
            <li>Options when the experiment configuration form is visible:
                <ol type="a">
                    <li>Submit the vector set and graph it</li>
                    <li>Check for transformation issues</li>
                    <li>Save the vector set as a file.</li>
                </ol>
            <li>After submitting the experiment and seeing the graph, you can use the sliders to adjust adjust vectors. You can
                also transform the collision by clicking on two particles in the graph and then selecting the transformation type and proceeding.
                After transformation, you will see the resulting graph next to the untransformed graph. Use sliders to adjust both graphs simultaneously.</li>
        </ol>
        </p>
        <h2>Details</h2>
        <p>There are three transformation types. All of them use the same 4x4 transformation matrix. The matrix, along with
            some explanatory remarks, is seen below in an image of an excert from a current work-in-progress by Ted C. Rogers's group at ODU.
            (The images that follow are meant only to be suggestive. Please consult the article for the full details.) Note that two vectors, 
            V and Y, are used to configure the matrix.
        </p>
        <div style="text-align: center;">
            <img src="resources/LCC-RapidityBoost.png" style="display: block; margin: 0 auto;" alt="Matrix" width="645" height="330">
        </div>
        <p>In configuring a transformation of a vector set, the user will select two of its vectors to be V and Y. They will
            be transformed, along with all the vectors in the set. Having been transformed, they may be marked as such as V' and Y' and used again
            for additional transformation as V' and Y'. Below we see that the user has selected two vectors and immediatley been
            shown a popup that suggests a simple transformation with a pre-checked checkbox.
        </p>
        </br>
        <div style="text-align: center;">
            <img src="resources/MatrixConfig.png" style="display: block; margin: 0 auto;" alt="popup" width="600" height="375">
        </div>
        </br>
        <p>More complicated transformations may be selected. Below we see that there are two more checkboxes below the first.
            The one on the left uses the sum of the two user-selected vectors as "V" in configuring the matrix, Y still being 
            used as before. The user has checked it, causing the checkbox on the right to become enabled. The latter offers 
            an additional after the transformation that the user has selected is done, so that we have a two-step transformation. 
            In the second step, V and Y have been transformed and are V' and Y'. Their difference is used as "V" to configure 
            the matrix, while Y' is used as "Y".
        </p>
        </br>
        <div style="text-align: center;">
            <img src="resources/MatrixConfig2.png" alt="popup" width="350" height="135">
        <div>
        </br>
        <p>Sliders are used to change the components of the vectos in the graph, as well as, for graphs of a two-step transformation,
            a parameter called, for lack of a better term, "A". A is a calculated value, found during the second step of a two-step transformation
            by solving a set of three equations as seen below.
        </p>
        <div style="text-align: center;">
            <img src="resources/equations.png" alt="popup" width="700" height="240">
        <div>
        <p>The exception to this derivation of A is the case in which the user's vector set has only two vectors in it. In that case, a
            value of 1 is used for A, leaving the user to adjust it with the slider afterwards. 
        </p>
    </body>
    </html>
    """
    browser.setHtml(html_content)

    # Layout for the dialog
    layout = QVBoxLayout()
    layout.addWidget(browser)
    dialog.setLayout(layout)
    return dialog

def get_user_manualOLD():
    msg = QMessageBox()
    msg.setWindowTitle("Collisions-QCD/TMD Quick Start")
    msg.setText("Quick Start\n")
    
    msg.setInformativeText("1. Use buttons to open an experiment file, create a new experiment, edit the currently loaded experiment, " +\
                "save, or close the currently loaded experiment. Configure your vectors in the form. To learn how to do this, click the \"new\""+\
                " button to open the experiment configuration form. Type your vectors' components into the form fields and press the \"submit\" button."
                "\n\n2. Options when the experiment configuration form is visible: (a.) submit the vector set - \"experiment\" and graph it,"+\
                " (b.) check for transformation issues, or (c.) to save it as a file." +\
                "\n\n3. After submitting the experiment and see the graph, use sliders to adjust adjust vectors or click on two points to"+\
                " transform the vector set. Select the transformation type and proceed. Use sliders to adjust both graphs simultaneously.")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)
    font = msg.font()
    font.setPointSize(11)
    msg.setFont(font)
    return msg

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
