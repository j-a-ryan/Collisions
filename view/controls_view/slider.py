from pyqt_advanced_slider import Slider 
import time
import threading
from PySide6.QtWidgets import  QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtGui import QColor, Qt

import config
from view.common.details import Heading
from view.experiment import widgets

'''
Extends Niklas Henning's slider.
'''
class VectorSlider(Slider):

    lookup_txyz_0123 = {"t": 0, "x": 1, "y": 2, "z": 3}
    lookup_0123_txyz = {"0": "t", "1": "x", "2": "y", "3": "z"}
    component = ["t", "x", "y", "z"]

    def __init__(self, controller, vector_name, axis, initial_value, use_threading, parent=None):
        super().__init__(parent)
        self.use_threading = use_threading
        self.vector_name = vector_name
        
        axis_num = VectorSlider.lookup_txyz_0123[axis]
        self.setRange(-10, 10)  # Set min and max
        self.setValue(initial_value)  # Set value
        
        self.setFixedWidth(160)
        self.setFixedHeight(18)
        self.setFloat(True)
        self.setDecimals(2)
        self.setSingleStep(0.01)
        self.setBackgroundColor(QColor(config.slider_background_color))          # Default: #D6D6D6
        self.setAccentColor(QColor(config.slider_accent_color))  # Default: #0078D7
        self.setBorderRadius(3)
        self.update_problem = False
        self.valueChanged.connect(self.slider_value_changed)
        self.handler = SliderUpdateHandler(controller, vector_name, axis_num, use_threading, initial_value)

    def slider_value_changed(self, value):
        if not self.update_problem:
            self.handler.handle_slide_event(value)
    

class SliderUpdateHandler():
    def __init__(self, controller, vector_name, axis_num, use_threading, initial_value):
        self.post_mediator = None
        self.vector_name = vector_name
        self.axis_num = axis_num
        self.controller = controller
        self.use_threading = use_threading
        self.latest_value = initial_value
        self.update_problem = False
        if use_threading:
            self.lock = threading.Lock()

    def post_value(self, value):
        if not self.update_problem: # TODO: Probably does nothing if there is only one thread. Does slider have its own thread under the hood? Work on this. Does this var do anything to shut down updates? If not fix or delete.
            success, transformation_type = self.controller.change_vector_member_value(self.vector_name, self.axis_num, value)
            if not success:
                self.update_problem = True
                msg = widgets.get_slider_transformation_issue_popup(transformation_type, self.axis_num, value)
                msg.exec()
            self.update_problem = False
        return self.update_problem
    
    def handle_slide_event(self, value):
        self.previous_value = self.latest_value # If we want to revert after issue with value, we can go back to previous.
        self.latest_value = value
        problem = False
        if self.use_threading:
            with self.lock:
                if self.post_mediator is None:
                    self.post_mediator = PostMediator(self)
                self.post_mediator.set_value(value)
                self.post_mediator.post_threaded()
        else:
            problem = self.post_value(value) # TODO: use this boolean?

    def signal_post_stream_end(self):
        del self.post_mediator
        self.post_mediator = None


class PostMediator():
    def __init__(self, handler):
        self.wait_limit = 5 # Wait five seconds, then give up on further updates
        self.handler = handler
        self.latest_value = None
        self.lock = threading.Lock()

    def post(self, value):
        self.handler.post_value(value)

    def post_threaded(self):
        elapsed = 0
        current = True
        while current:
            
            # Sleep for 200ms (0.2 seconds)
            time.sleep(1)

            # If updates, post the latest to the controller
            with self.lock:
                if self.latest_value is not None:
                    self.post(self.latest_value)
                    self.latest_value = None
                else:
                    # Else check timeout. If timed out, exit loop.
                    elapsed += 0.2
                    if elapsed > self.wait_limit:
                        current = False
                        self.handler.signal_post_stream_end()

    def start_thread(self):
        thread = threading.Thread(target=self.post_threaded, args = (10, ))
        thread.start()
        thread.join()

class SliderGroupFrame(QFrame):
    def __init__(self, controller, vector_name, initial_vector): # TODO: default value for testing. Delete
        super().__init__()
        self.controller = controller
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedWidth(200)
        self.inner_layout = QVBoxLayout(self)

        heading = Heading(vector_name, "Tahoma", False)
        self.inner_layout.addWidget(heading, alignment=Qt.AlignmentFlag.AlignCenter)
        for i in range(len(VectorSlider.component)):
            axis = VectorSlider.component[i]
            initial_value = initial_vector[i]
            hbox = QHBoxLayout()
            axis_label = QLabel(axis)
            hbox.addWidget(QLabel(axis))
            axis_label.adjustSize()
            hbox.addWidget(VectorSlider(controller, vector_name, axis, initial_value, False))
            self.inner_layout.addLayout(hbox)


















        # sliders_grid = QGridLayout()
        # sliders_grid.addWidget(QLabel("x"), 0, 0, 1, 1)
        # sliders_grid.addWidget(VectorSlider(None, vector_name, False), 0, 1, 1, 10)
        # sliders_grid.addWidget(QLabel("y"), 1, 0, 1, 1)
        # sliders_grid.addWidget(VectorSlider(None, vector_name, False), 1, 1, 1, 10)
        # sliders_grid.addWidget(QLabel("z"), 2, 0, 1, 1)
        # sliders_grid.addWidget(VectorSlider(None, vector_name, False), 2, 1, 1, 10)
        # self.inner_layout.addLayout(sliders_grid)
