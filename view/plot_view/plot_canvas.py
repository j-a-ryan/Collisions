import sys

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLabel, QWidget, QVBoxLayout
import os
import mplcursors
import numpy as np
import config
from controller.transformation_controller import TransformationController
from model import util
from view.plot_view.widgets import ConfigureTransformationPopup

os.environ["QT_API"] = "PySide6" # Doesn't seem to do anything. What is it?


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
    
    @property
    def particle_indices_picked(self):
        return self.experiment_controller.particle_indices_picked_for_transformation

    def plot(self, collision, extra_circles=None):

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
        
        # Plot the particle points as circles at the tips of the vectors around the names. Catch
        # the scatter return for event handling (event source identification) later.
        self.scatter = self.ax.scatter(vectors_columns['x'], vectors_columns['y'], vectors_columns['z'], facecolors='none',
                                       edgecolors=edgecolors, marker='o', s=180, picker=True, pickradius=5)
        
        # Plot the extra circles, if any.
        if extra_circles:
            extra_circles_edgecolors = [config.slider_accent_color] * len(extra_circles) #config.slider_accent_colorconfig.slider_accent_color
            xs = [vectors_columns['x'][i] for i in extra_circles]
            ys = [vectors_columns['y'][i] for i in extra_circles]
            zs = [vectors_columns['z'][i] for i in extra_circles]
            # for index in extra_circles: # extra_circles is a list of the indices of the points that need extra circles drawn around them.
            self.ax.scatter(xs, ys, zs, facecolors='none', depthshade=False, edgecolors=extra_circles_edgecolors, marker='o', linewidths=4, s=600)

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # self.ax.set_xlim([-1, 6]) TODO: do this programmatically
        # self.ax.set_ylim([-1, 6]) Low and high for each axis. Add 10% either side.
        # self.ax.set_zlim([-1, 6])
        self.fig.canvas.mpl_connect('pick_event', self.onpick_circles)
        # cursor = mplcursors.cursor(self.ax, hover=mplcursors.HoverMode.Transient)
        # cursor.connect("add", lambda sel: sel.annotation.set_text("Click to apply rest frame"))

    def onpick_circles(self, event):
        if event.artist == self.scatter:  # Ensure the event is from our scatter plot
            ind = event.ind  # Indices of the clicked points
            index = ind[0]

            if len(self.particle_indices_picked) == 0:
                self.particle_indices_picked.append(index)
                self.experiment_controller.plot_current_experiment(extra_circles=self.particle_indices_picked.copy()) # Zero or one picked now.
            else: # len(self.particles_indices_picked) == 1 or 2                
                if index in self.particle_indices_picked:
                    self.particle_indices_picked.remove(index)
                    self.experiment_controller.plot_current_experiment(extra_circles=self.particle_indices_picked.copy()) # Zero or one picked now.
                else:
                    self.particle_indices_picked.append(index) # two picked now
                    indices = self.particle_indices_picked.copy()
                    self.experiment_controller.plot_current_experiment(extra_circles=indices)
                    popup = ConfigureTransformationPopup(indices, self.particle_names)
                    if popup.exec() == QDialog.Accepted:
                        
                        self.experiment_controller.plot_current_experiment() # Get rid of circles
                        self.particles_picked = [popup.transformation_config["V"], popup.transformation_config["Y"]]
                        
                        self.particle_indices_picked.clear() # Get rid of circles

                        V_plus_Y = popup.transformation_config["V+YConfig"]
                        V_minus_Y = popup.transformation_config["ApplyPostTransformationV'-Y'"]
                        argument_type = util.get_config_argument(V_plus_Y, V_minus_Y)
                        V_Y_particle_names = self.particles_picked.copy()
                        self.experiment_controller.plot_transformation(V_Y_particle_names, argument_type)
                        
                        self.particles_picked.clear()                  
                    else:
                        self.particle_indices_picked.clear()
                        self.experiment_controller.plot_current_experiment()
