import math
import threading
import time
from abc import ABC, abstractmethod

from pyqt_advanced_slider import Slider
from PySide6.QtGui import QColor, Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout

import config
from controller.controls_controller import ControlsController
from view.common.details import Heading


class SliderUpdateHandler(ABC):
    def __init__(self, initial_value, use_threading=False):
        super().__init__()
        self.post_mediator = None
        self.latest_value = initial_value
        self.use_threading = use_threading
        if use_threading:
            self.lock = threading.Lock()

    @abstractmethod
    def post_value(self, value) -> bool:
        pass

    def handle_slide_event(self, value):
        self.previous_value = self.latest_value  # If we want to revert after issue with value, we can go back to previous.
        self.latest_value = value
        problem = False
        if self.use_threading:
            with self.lock:
                if self.post_mediator is None:
                    self.post_mediator = PostMediator(self)
                self.post_mediator.set_value(value)
                self.post_mediator.post_threaded()
        else:
            problem = self.post_value(value)  # TODO: use this boolean?
        return problem

    def signal_post_stream_end(self):
        del self.post_mediator
        self.post_mediator = None


class BoostParameterASliderUpdateHandler(SliderUpdateHandler):
    def __init__(self, controller: ControlsController, initial_value, use_threading=False):
        super().__init__(initial_value, use_threading)
        self.controller = controller

    def post_value(self, value):
        success, _ = self.controller.update_boost_parameter_A(value)
        return success


class SliderCoordinationUpdateHandler(SliderUpdateHandler):  # m2 slider uses this one

    def __init__(self, slider_value_name, initial_value, sliders_coordination, use_threading=False):
        super().__init__(initial_value, use_threading)
        self.slider_value_name = slider_value_name
        self.sliders_coordination = sliders_coordination

    def update_coordinator(self, value):
        if not self.sliders_coordination.user_sliding_now:
            self.sliders_coordination.user_sliding_now = True
            self.sliders_coordination.submit_user_selected_value(self.slider_value_name, value)
            self.sliders_coordination.user_sliding_now = False

    def post_value(self, value):
        self.update_coordinator(value)
        return True


class FourVectorSliderUpdateHandler(SliderCoordinationUpdateHandler):  # t, x, y, z sliders use this one

    def __init__(self, axis_name, initial_value, sliders_coordination, use_threading=False):
        super().__init__(axis_name, initial_value, sliders_coordination, use_threading)

    def prepare_to_use_controller(self, controller, vector_name, axis_num):  # The m2 slider does not need this. Only the others do.
        self.controller = controller
        self.vector_name = vector_name
        self.axis_num = axis_num

    def post_value(self, value):
        self.update_coordinator(value)
        success, _ = self.controller.change_vector_member_value(self.vector_name, self.axis_num, value)
        return success


"""
Extends Niklas Henning's slider.
"""


class CollisionsSlider(Slider):
    def __init__(self, initial_value, range_min, range_max, parent=None):
        super().__init__(parent)
        self.handler = None

        self._set_min_max_initial(range_min, range_max, initial_value)
        self.setFixedWidth(150)
        self.setFixedHeight(18)
        self.setFloat(True)
        self.setDecimals(2)
        self.setSingleStep(0.01)
        self.setBackgroundColor(QColor(config.slider_background_color))  # Default: #D6D6D6
        self.setAccentColor(QColor(config.slider_accent_color))  # Default: #0078D7
        self.setBorderRadius(3)
        self.valueChanged.connect(self.slider_value_changed)

    def _set_min_max_initial(self, range_min, range_max, initial_value):
        self.setRange(range_min, range_max)
        self.setValue(initial_value)

    def set_handler(self, handler):
        self.handler = handler

    def slider_value_changed(self, value):
        if self.handler is not None:
            self.handler.handle_slide_event(value)


class VectorSlider(CollisionsSlider):
    def __init__(self, initial_value, range_min, range_max, parent=None):
        super().__init__(initial_value, range_min, range_max, parent)


class BoostParameterASlider(CollisionsSlider):
    def __init__(self, initial_value, range_min, range_max, parent=None):
        super().__init__(initial_value, range_min, range_max, parent)

    def _set_min_max_initial(self, range_min, range_max, initial_value):
        range_max = max(range_max, initial_value)
        self.setRange(range_min, range_max)
        self.setValue(initial_value)


class PostMediator:
    def __init__(self, handler):
        self.wait_limit = 5  # Wait five seconds, then give up on further updates
        self.handler = handler
        self.latest_value = None
        self.lock = threading.Lock()

    def set_value(self, value):
        with self.lock:
            self.latest_value = value

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
        thread = threading.Thread(target=self.post_threaded, args=(10,))
        thread.start()
        thread.join()


class SliderGroupFrame(QFrame):

    dict_txyz_0123 = config.lookup_gui_txyz_0123
    dict_0123_txyz = config.lookup_gui_0123_txyz
    component = (config.gui_t, config.gui_x, config.gui_y, config.gui_z)

    def __init__(self, controller, vector_name, initial_vector):  # TODO: default value for testing. Delete
        super().__init__()
        self.controller = controller
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedWidth(200)
        self.setContentsMargins(0, 0, 10, 0)
        self.inner_layout = QVBoxLayout(self)

        heading = Heading(vector_name, "Tahoma", False)
        self.inner_layout.addWidget(heading, alignment=Qt.AlignmentFlag.AlignCenter)

        self.sliders_grid = QGridLayout()
        sliders_coordination = TimeM2SlidersCoordinator()

        # Add the m2 slider
        slider_label = QLabel(config.gui_m2)
        self.sliders_grid.addWidget(slider_label, 0, 0, alignment=(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop))
        # This also adds the slider to the coordinator's collection
        slider_m2 = sliders_coordination.create_m2_slider(initial_vector, sliders_coordination)
        self.sliders_grid.addWidget(slider_m2, 0, 1, alignment=(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop))
        line = QFrame(frameShape=QFrame.Shape.HLine, frameShadow=QFrame.Shadow.Sunken, lineWidth=90)
        self.sliders_grid.addWidget(line, 1, 1, Qt.AlignmentFlag.AlignCenter)

        for i in range(len(SliderGroupFrame.component)):  # Add the vectors, starting on the third row of the grid (index 2)
            axis_name = SliderGroupFrame.component[i]  # Axis is simply the vector name string, e.g. "y"
            initial_value = initial_vector[i]
            axis_label = QLabel(axis_name)
            rownum = i + 2
            self.sliders_grid.addWidget(axis_label, rownum, 0, alignment=(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop))
            axis_num = SliderGroupFrame.dict_txyz_0123[axis_name]
            handler = FourVectorSliderUpdateHandler(axis_name, initial_value, sliders_coordination)
            handler.prepare_to_use_controller(controller, vector_name, axis_num)
            min_val = 0 if axis_name == config.gui_t else config.xyz_min
            max_val = config.t_max if axis_name == config.gui_t else config.xyz_max
            slider = VectorSlider(initial_value, min_val, max_val)
            slider.set_handler(handler)
            sliders_coordination.add_slider(axis_name, slider)
            self.sliders_grid.addWidget(slider, rownum, 1, alignment=(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop))
            # sliders_coordination.add_slider(axis_label, slider)

        self.inner_layout.addLayout(self.sliders_grid)


class TimeM2SlidersCoordinator:

    def __init__(self):  # Construct the object using vector initial values.

        self.sliders = {}
        self._user_sliding_now = False  # Like a thread lock, but there is only one thread.

    def add_slider(self, slider_name, slider):
        self.sliders[slider_name] = slider

    @property
    def user_sliding_now(self):
        return self._user_sliding_now

    @user_sliding_now.setter
    def user_sliding_now(self, sliding_now):
        self._user_sliding_now = sliding_now

    def calculate_initial_m2(self, vector):
        return self.calculate_m2(vector[0], vector[1], vector[2], vector[3])

    def calculate_m2(self, t, x, y, z):
        # Square each value from the vector
        t2 = t**2
        x2 = x**2
        y2 = y**2
        z2 = z**2
        m2 = t2 - x2 - y2 - z2  # Calculate m2 as a difference.
        return m2

    def update_m2(self):
        t = self.sliders[config.gui_t].getValue()
        x = self.sliders[config.gui_x].getValue()
        y = self.sliders[config.gui_y].getValue()
        z = self.sliders[config.gui_z].getValue()
        m2 = self.calculate_m2(t, x, y, z)
        self.sliders[config.gui_m2].setValue(m2)

    def calculate_t(self, m2, x, y, z):
        t2 = m2 + x**2 + y**2 + z**2
        # print(f"{m2} {x**2} {y**2} {z**2}   {t2}")
        t = math.sqrt(t2)
        return t

    def update_t(self):
        m2 = self.sliders[config.gui_m2].getValue()
        x = self.sliders[config.gui_x].getValue()
        y = self.sliders[config.gui_y].getValue()
        z = self.sliders[config.gui_z].getValue()
        t = self.calculate_t(m2, x, y, z)
        self.sliders[config.gui_t].setValue(t)

    def submit_user_selected_value(self, axis_name, value):
        if axis_name == config.gui_m2:
            self.update_t()
        else:  # It's t, x, y, or z
            self.update_m2()
            if axis_name != config.gui_t:
                self.update_m2_slider_limits()

    def initialize_m2_slider_limits(self, vector):
        self.calculate_and_set_m2_slider_limits(vector[1], vector[2], vector[3])

    def update_m2_slider_limits(self):
        self.calculate_and_set_m2_slider_limits(
            self.sliders[config.gui_x].getValue(), self.sliders[config.gui_y].getValue(), self.sliders[config.gui_z].getValue()
        )

    def calculate_and_set_m2_slider_limits(self, x, y, z):
        x2 = x**2
        y2 = y**2
        z2 = z**2
        m2_min = math.ceil(-(x2 + y2 + z2))  # Using ceil because rounding errors were causing t2 < 0 issue at calculate_t t = math.sqrt(t2)
        m2_max = config.t_max**2 + m2_min  # This is t_max^2 -(x^2 + y^2 + z^2)
        self.sliders[config.gui_m2].setRange(m2_min, m2_max)
        # print(f"RESET M2 range {m2_min} {m2_max}, current m2: {self.sliders[config.gui_m2].getValue()} now")

    def create_m2_slider(self, initial_vector, sliders_coordination):
        initial_value = self.calculate_initial_m2(initial_vector)
        handler = SliderCoordinationUpdateHandler(config.gui_m2, initial_value, sliders_coordination)
        slider_m2 = VectorSlider(initial_value, initial_value - 10, initial_value + 10)  # temp limits reset in the next line of code.
        self.add_slider(config.gui_m2, slider_m2)
        self.initialize_m2_slider_limits(initial_vector)
        slider_m2.set_handler(handler)  # Now set handler only after slider fully set up, otherwise trouble from setRange -> sets value
        return slider_m2
