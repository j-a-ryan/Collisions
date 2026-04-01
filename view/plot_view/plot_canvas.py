import sys

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLabel, QWidget, QVBoxLayout
import os
import mplcursors
import numpy as np

import config

os.environ["QT_API"] = "PySide6" # Doesn't seem to do anything. What is it?
# from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class PlotVectorCanvas(FigureCanvas):
    def __init__(self, experiment_controller, parent=None, width=7, height=7, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111, projection='3d')
        fig.set_facecolor(config.graph_encasing_area_color)       
        self.ax.set_facecolor(config.graph_area_color)
        # fig.set_facecolor("#FCFEE7")       
        # self.ax.set_facecolor("#FCFEE7")
        # fig.set_facecolor("#FCFEE7")       
        # self.ax.set_facecolor("#FCFEE7")
        self.ax.xaxis._axinfo["grid"].update({"linewidth":0.5})
        self.ax.yaxis._axinfo["grid"].update({"linewidth":0.5})
        self.ax.zaxis._axinfo["grid"].update({"linewidth":0.5})
        fig.tight_layout()
        self.fig = fig
        super().__init__(fig)
        self.experiment_controller = experiment_controller
        self.particles_picked = []

    def plot(self, collision):

        vectors = collision.get_spatial_vectors_xyz()
        vectors_columns = collision.get_vectors_spatial_columns()      
        self.particle_names = collision.get_vectors_name_column()
        edgecolors = ['black'] * len(vectors)
        # facecolorscolors = ['lightcyan', 'tomato', 'aquamarine'] # TODO: add more
        
        # Plot the vectors (no arrowheads: arrow_length_ratio=0) and the names at the tips.
        for i in range(len(vectors)):
            self.ax.quiver(0, 0, 0, # Starting point
                        vectors[i][0], vectors[i][1], vectors[i][2], # Vector components
                        color='black', arrow_length_ratio=0, linewidths=0.7)  # Customize color and arrow size
            self.ax.scatter(vectors[i][0], vectors[i][1], vectors[i][2], marker=f'${self.particle_names[i]}$', s=90, color='black')
        
        # Plot the particle points as circles at the tips of the vectors around the names
        self.scatter = self.ax.scatter(vectors_columns['x'], vectors_columns['y'], vectors_columns['z'], facecolors='none',
                                       edgecolors=edgecolors, marker='o', s=180, picker=True, pickradius=5)
        # Plot lab point
        # self.ax.scatter(0, 0, 0, marker='s', s=150, edgecolors='black', facecolors='white')
        # self.ax.scatter(0, 0, 0, marker='$L$', s=50, color='black')

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # self.ax.set_xlim([-1, 6]) TODO: do this programmatically
        # self.ax.set_ylim([-1, 6]) Low and high for each axis. Add 10% either side.
        # self.ax.set_zlim([-1, 6])
        self.fig.canvas.mpl_connect('pick_event', self.onpick)
        # cursor = mplcursors.cursor(self.ax, hover=mplcursors.HoverMode.Transient)
        # cursor.connect("add", lambda sel: sel.annotation.set_text("Click to apply rest frame"))
    
    def onpick(self, event):
        if event.artist == self.scatter:  # Ensure the event is from our scatter plot
            ind = event.ind  # Indices of the clicked points
            index = ind[0]

            if len(self.particles_picked) == 0:
                name_of_picked_particle = self.particle_names[index]
                popup = PickTwoParticlesPopup([name_of_picked_particle])
                if popup.exec() == QDialog.Accepted:
                    self.particles_picked.append(name_of_picked_particle)
                else:
                    self.particles_picked.clear()
            else: # len(self.particles_picked) == 1                
                name_of_picked_particle = self.particle_names[index]
                popup = PickTwoParticlesPopup(self.particles_picked, name_of_picked_particle)
                if popup.exec() == QDialog.Accepted:
                    self.experiment_controller.plot_transformation(self.particles_picked.copy())
                    self.particles_picked.clear()                  
                else:
                    self.particles_picked.clear()
                    print("User cancelled.")              

class PickTwoParticlesPopup(QDialog):
    def __init__(self, particle_names, newly_picked_particle=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Transformation Matrix")

        names = particle_names[0]
        # if len(particle_names) == 2:
        #     names += (" and " + particle_names[1])
        #     self.instructions_label = QLabel("Proceed with the transformation?")
        if newly_picked_particle:
            if newly_picked_particle == particle_names[0]:
                self.instructions_label = QLabel("Please pick a different particle for your second one \n(or " \
                "cancel to discard the transformation)")
            else:
                particle_names.append(newly_picked_particle)
                names += (" and " + particle_names[1])
                self.instructions_label = QLabel("Proceed with the transformation?")
        else:
            self.instructions_label = QLabel("Please pick a second particle \n(or " \
                "cancel to discard the transformation)")
        self.name_label = QLabel("You picked: " + names)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.instructions_label)
        layout.addWidget(self.button_box)
        self.setLayout(layout)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     main_dialog = PickTwoParticlesPopup(["k2", "k1"])
#     if main_dialog.exec() == QDialog.Accepted:
#         print("User okayed")
#     else:
#         print("User cancelled.")

#     sys.exit(app.exec())


