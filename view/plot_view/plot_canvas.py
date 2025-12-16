from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
import os
import mplcursors
import numpy as np

os.environ["QT_API"] = "PySide6" # Doesn't seem to do anything. What is it?
# from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class PlotVectorCanvas(FigureCanvas):
    def __init__(self, experiment_controller, parent=None, width=7, height=7, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111, projection='3d')
        fig.set_facecolor("#FCFEE7")       
        self.ax.set_facecolor("#FCFEE7")
        self.ax.xaxis._axinfo["grid"].update({"linewidth":0.5})
        self.ax.yaxis._axinfo["grid"].update({"linewidth":0.5})
        self.ax.zaxis._axinfo["grid"].update({"linewidth":0.5})
        fig.tight_layout()
        self.fig = fig
        super().__init__(fig)
        self.experiment_controller = experiment_controller

    def plot(self, collision):

        # Get the lab point/vector and the rest/origin vector.
        # lab_vec = vectors.get_lab_vector() # needs box, not circle.
        # rest_vec = vectors.get_rest_vector() # By definition/stipulation at origin [0,0,0]
        index_of_origin_vector = 0#collision.get_id_of_origin_vector()
        vectors = collision.get_spacial_vectors_xyz()
        origin = [0, 0, 0]  # same as rest_vec, actually

        arr1 = []
        arr2 = []  # Use np slices for this
        arr3 = []
        for i in range(len(vectors)):
            arr1.append(vectors[i][0])
            arr2.append(vectors[i][1])
            arr3.append(vectors[i][2])
        
        point_characters = ['L', 'h1', 'h2']
        colors = ['black', 'black', 'black']
        
        for i in range(len(vectors)):
            if i != index_of_origin_vector:
                self.ax.quiver(origin[0], origin[1], origin[2], # Starting point
                            vectors[i][0], vectors[i][1], vectors[i][2], # Vector components
                            color='black', arrow_length_ratio=0.06, linewidths=0.5)  # Customize color and arrow size
            self.ax.scatter(vectors[i][0], vectors[i][1], vectors[i][2], marker=f'${point_characters[i]}$', s=90, color='black')
        self.scatter = self.ax.scatter(arr1, arr2, arr3, facecolors='none', edgecolors=colors, marker='o', s=160, picker=True, pickradius=5) 
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

    # def plot(self, vectors):

    

    #     origin = [0, 0, 0]  

    #     arr1 = []
    #     arr2 = []
    #     arr3 = []
    #     for i in range(len(vectors)):
    #         arr1.append(vectors[i][0])
    #         arr2.append(vectors[i][1])
    #         arr3.append(vectors[i][2])
        
    #     point_characters = ['h1', 'h2']
    #     colors = ['red', 'aqua']
        
    #     for i in range(len(vectors)):
    #         self.ax.quiver(origin[0], origin[1], origin[2], # Starting point
    #                        vectors[i][0], vectors[i][1], vectors[i][2], # Vector components
    #                        color='black', arrow_length_ratio=0.06, linewidths=0.5)  # Customize color and arrow size
    #         m = point_characters[i]
    #         self.ax.scatter(vectors[i][0], vectors[i][1], vectors[i][2], marker=f'${point_characters[i]}$', s=90, color='black')
    #     self.scatter = self.ax.scatter(arr1, arr2, arr3, facecolors='none', edgecolors=colors, marker='o', s=160, picker=True, pickradius=5) 
    #     # Plot lab point
    #     self.ax.scatter(0, 0, 0, marker='s', s=150, edgecolors='black', facecolors='white')
    #     self.ax.scatter(0, 0, 0, marker='$L$', s=50, color='black')

    #     self.ax.set_xlabel('X')
    #     self.ax.set_ylabel('Y')
    #     self.ax.set_zlabel('Z')

    #     self.ax.set_xlim([-1, 6])
    #     self.ax.set_ylim([-1, 6])
    #     self.ax.set_zlim([-1, 6])
    #     self.fig.canvas.mpl_connect('pick_event', self.onpick)
    #     # cursor = mplcursors.cursor(self.ax, hover=mplcursors.HoverMode.Transient)
    #     # cursor.connect("add", lambda sel: sel.annotation.set_text("Click to apply rest frame"))
    
    def onpick(self, event):
        if event.artist == self.scatter:  # Ensure the event is from our scatter plot
            ind = event.ind  # Indices of the clicked points
            index = ind[0]
            print(f"Clicked on point(s) with index(es): {index}, type " + str(type(index)))
            self.experiment_controller.plot_transformation(index)
        


