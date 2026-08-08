from PySide6.QtWidgets import QDialog, QTextBrowser, QVBoxLayout


def get_user_manual():
    dialog = QDialog()
    dialog.setWindowTitle("Collisions User Manual")
    dialog.resize(1150, 600)

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
        <p>For more information, <a href="https://github.com/j-a-ryan/Collisions/tree/main">right-click on this link, copy it, and then paste it
            into your Web browser</a>. This will take you to the README of the code repository.
        <h2>Quick Start</h2>
        <p>How to use the application:
        <ol>
            <li>Click "New" and enter a vector set. Then, click Submit to graph the set.</li>
            <li>Use buttons to open an experiment file, create a new experiment, edit the currently loaded experiment,
                save, or close the currently loaded experiment. Configure your vectors in the form. To learn how to do this, click the "new"
                button to open the experiment configuration form. Type your vectors' components into the form fields and press the "submit" button.</li>
            <li>Options when the experiment configuration form is visible:
                <ol type="a">
                    <li>Submit the vector set and graph it</li>
                    <li>Check for transformation issues</li>
                    <li>Save the vector set as a file.</li>
                </ol>
            </li>
            <li>After submitting the experiment and seeing the graph, you can use the sliders to adjust adjust vectors. You can
                also transform the collision by clicking on two particles in the graph and then selecting the transformation type and proceeding.
                After transformation, you will see the resulting graph next to the untransformed graph. Use sliders to adjust both graphs simultaneously.</li>
            </li>
        </ol>
        </p>
        <h2>Details</h2>
        <h3>Test Crash Logging</h3>
        <p>Please click the "Do not click this" button and follow the instructions in the popup you will see, expect for the part
            about sending the software developer the log. This is simply a test that crash logging works on your computer. If you
            are sure that the file was not created, let the software developer know. Afterwards, if you do get an unexpected crash, 
            send him the file.
        </p> 
        <h3>Core Usage</h3>
        <p>There are three transformation types. All of them use the same 4x4 transformation matrix. The matrix, along with
            some explanatory remarks, is seen below in an image of an excerpt from a current work-in-progress by Ted C. Rogers's group at ODU.
            (The images that follow are meant only to be suggestive. Please consult the article for the full details.) Note that two vectors, 
            V and Y, are used to configure the matrix.
        </p>
        <div style="text-align: center;">
            <img src="resources/LCC-RapidityBoost.png" style="display: block; margin: 0 auto;" alt="Matrix" width="968" height="494">
        </div>
        <p>In configuring a transformation of a vector set, the user will select two of its vectors to be V and Y. Simply click on the
            particles in the graph. After the second one is clicked on, a popup will appear, allowing you to configure your transformation.
            These two vectors - dubbed V and Y - will then be transformed, along with all of the other vectors in the set. Having been 
            transformed, they may be marked as such as V' and Y' and used again for additional transformation as V' and Y'. Below we see 
            that the user has selected two vectors and immediatley been shown a popup that suggests a simple transformation with a 
            pre-checked checkbox.
        </p>
        </br>
        <div style="text-align: center;">
            <img src="resources/MatrixConfig.png" style="display: block; margin: 0 auto;" alt="popup" width="600" height="375">
        </div>
        </br>
        <p>More complicated transformations may be selected. Below we see that there are two more checkboxes below the first.
            The one on the left uses the sum of the two user-selected vectors as "V" in configuring the matrix, Y still being 
            used as before. The user has checked it, causing the checkbox on the right to become enabled. The latter offers 
            an additional after the transformation already selected is done, so that we have a two-step transformation. 
            In the second step, V and Y have been transformed and are V' and Y'. Their difference is used as "V" to configure 
            the matrix, while Y' is used as "Y".
        </p>
        </br>
        <div style="text-align: center;">
            <img src="resources/MatrixConfig2.png" alt="popup" width="350" height="135">
        </div>
        </br>
        <p>Sliders are used to change the components of the vectos in the graph, as well as, for graphs of a two-step transformation,
            a boost factor parameter dubbed "A".
        </p>
        <!-- Will we ever need this? The calculations proved difficult and were postponed.
        <p>A is a calculated value used in the second step of a two-step transformation:
        <div style="text-align: center;">
            <img src="resources/A.png" alt="popup" width="1125" height="155">
        </div>
        <p>The values needed to solve for A are found by solving a set of three equations:
        </p>
        <div style="text-align: center;">
            <img src="resources/equations.png" alt="popup" width="853" height="313">
        </div>
        <p>These calculations require a third vector be used. For this purpose the user selects a vector from the vector set when configuring
            a two-step transformation. It can take the software several seconds (for example, seven) for this set of equations to be solved
            so that the user's transformation may be completed and graphed. In the event that the vector set has only two vectors, a value 
            of 1 is used for A, instead of solving a system of equations. After a two-step transformation the user can adjust the value of 
            A using a slider. 
        </p>
        -->
        <p>A fresh transformation can be made when both the original graph and the transformation graph are showing. Simply click
            on one of the selected particles in the original graph and begin the process again.
        </p>
        <h3>Graphs</h3>
        <p>The graphs are made with Python's Matplotlib library. The vector arrow tips are represented by circles in which
            the name of the vector is seen and which are clicked on by the user to indicate selection of the vector for
            the configuration of the transformation matrix. The production of graphs usable in article publications is not
            contemplated here. Matplotlib does not offer good arrow heads for 3D graphs, although custom-made arrowheads 
            may be created and might be included in Collisions in the future.
        </p>
        <p>2D projections of the 3D graphs may be seen by clicking on the appropriate tabs or buttons. The buttons offer
            floating graphs that may be moved around by the a user by dragging. Right-click on a particle to see its coordinates.
        </p>
        <h3>CSV Files for Storing Vector Sets</h3>
        <p>Simple CSV files are used to store vector sets. These are not meant to be created by hand, though they may be.
            To learn the structure of these files, the user should simply create a set of vectors in the experiment
            configuration form, save the set, and then inspect the file.
        </p>
        <p>Currently, the application does not allow the user to update a file with changes to vector components made by
            the use of the sliders. Only changes made in the experiment configuration form can used to update a file.
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
