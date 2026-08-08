import sys
import logging
import platform
from datetime import datetime
from pathlib import Path
from PySide6 import __version__ as pyside_version

LOG_DIR = Path.home() / ".collisions" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / f"crash_{datetime.now():%Y%m%d_%H%M%S}.log"
STDLOG_FILE = LOG_DIR / "stdout_stderr.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def redirect_streams():
    """Redirect stdout/stderr to a file if they don't exist (windowed build)."""
    if sys.stdout is None or sys.stderr is None:
        log_stream = open(STDLOG_FILE, "a", buffering=1, encoding="utf-8")
        sys.stdout = log_stream
        sys.stderr = log_stream


def safe_print(text):
    """Write to stderr only if it exists (won't work in --windowed builds)."""
    try:
        if sys.stderr is not None:
            print(text, file=sys.stderr)
    except Exception:
        pass


def is_frozen():
    return getattr(sys, "frozen", False)


def get_app_version():
    # However you're tracking version — hardcode, or read a VERSION file bundled as data
    return "0.3.0-alpha"


def log_environment():
    logging.error(
        "Environment: OS=%s, Python=%s, PySide6=%s, App=%s, Frozen=%s",
        platform.platform(),
        platform.python_version(),
        pyside_version,
        get_app_version(),
        is_frozen(),
    )


def excepthook(exc_type, exc_value, exc_tb):
    """Global handler for uncaught exceptions."""
    import traceback

    tb_text = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logging.error("Unhandled exception:\n%s", tb_text)
    safe_print(tb_text)

    try:
        from PySide6.QtWidgets import QApplication, QMessageBox

        if QApplication.instance():
            QMessageBox.critical(
                None,
                "Unexpected Error",
                "Something went wrong and the application needs to be closed.\n\n"
                f"A log file has been saved at:\n{LOG_FILE}\n\n"
                "Please send this file to the software developer.\n\n"
                "You probably ran across a bug in the code. After you\n"
                "close the application you can relaunch it and use it.",
            )
    except Exception:
        pass  # don't let the error handler itself crash

    sys.__excepthook__(exc_type, exc_value, exc_tb)


def thread_excepthook(args):
    import traceback

    tb_text = "".join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback))
    logging.error("Unhandled thread exception:\n%s", tb_text)


def install_excepthook():
    import threading

    sys.excepthook = excepthook
    threading.excepthook = thread_excepthook
