import sys

from PySide6.QtWidgets import QApplication


# Delete this file when application is deemd stable.
class ExceptionCatchingApplication(QApplication):
    def notify(self, receiver, event):
        try:
            return super().notify(receiver, event)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            if exc_type is not None and exc_value is not None:
                sys.excepthook(exc_type, exc_value, exc_tb)
            return False
