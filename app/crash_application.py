import sys

from PySide6.QtWidgets import QApplication


# Delete this file when application is deemd stable.
class ExceptionCatchingApplication(QApplication):
    def notify(self, receiver, event):
        try:
            return super().notify(receiver, event)
        except Exception:
            sys.excepthook(*sys.exc_info())
            return False
