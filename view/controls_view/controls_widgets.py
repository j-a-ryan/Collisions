from pyqt_advanced_slider import Slider 
import time
import threading

'''
Extends Niklas Henning's slider.
'''
class VectorSlider(Slider):

    def __init__(self, controller, use_threading, parent=None):
        super().__init__(parent)
        self.use_threading = use_threading
        self.handler = SliderUpdateHandler(controller, use_threading)
    

class SliderUpdateHandler():
    def __init__(self, vector_name, axis, controller, use_threading):
        self.post_mediator = None
        self.vector_name = vector_name
        self.axis = axis
        self.controller = controller
        self.use_threading = use_threading
        if use_threading:
            self.lock = threading.Lock()

    def post_value(self, value):
        self.controller.post_vector_alteration(self.vector_name, self.axis, value)
    
    def handle_slide_event(self, value):
        latest_value = value

        if self.use_threading:
            with self.lock:
                if self.post_mediator is None:
                    self.post_mediator = PostMediator(self)
                self.post_mediator.post_threaded(value)
        else:
            self.post_value(value)

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

    def post_threaded(self, value):
        elapsed = 0
        current = True
        while current:
            
            # Sleep for 200ms (0.2 seconds)
            time.sleep(0.2)

            # If updates, post the latest to the controller
            with self.lock:
                if self.latest_value is not None:
                    self.post(value)
                else:
                    # Else check timeout. If timed out, exit loop.
                    elapsed += 0.2
                    if elapsed > self.wait_limit:
                        current = False
                        self.handler.signal_post_stream_end()