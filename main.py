############### Old imports ###################
# from PySide6.QtWidgets import QApplication
# from app.application import MainWindow
##############################################
import sys
from crash_handler import redirect_streams, install_excepthook, log_environment


# Comment out this function when application is deemed stable enough.
def bootstrap():
    redirect_streams()  # 1. Fix stdout/stderr first — everything else may depend on them
    install_excepthook()  # 2. Then install the crash handler
    log_environment()  # 3. Log OS/Python/PySide6/app version once at startup

    # Importing here, rather than at top of file, out an abundance of caution
    # and as stylistic reminder that application is instantiated only after logging
    # is set up.
    from app.crash_application import ExceptionCatchingApplication
    from app.application import MainWindow

    app = ExceptionCatchingApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    bootstrap()  # Remove when application is deemed stable enough.

    ###################################################
    # The old code. When the crash handling is removed,
    # go back to this old code, including uncommenting
    # the old imports.
    # Launch the application
    # app = QApplication()

    # window = MainWindow(app)
    # window.show()

    # app.exec()
    ###################################################
