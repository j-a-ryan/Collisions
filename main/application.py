from PySide6.QtWidgets import QMainWindow, QMenu, QMenuBar, QVBoxLayout, QWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QEvent
import sys
import qdarktheme

from main.custom_title_bar import CustomTitleBar
from view.common.details import HorizontalDivider
from view.view import View


class MainWindow(QMainWindow):

    def __init__(self, app):
        super().__init__()
        self.initial_pos = None
        self.resize(1200, 700)

        qdarktheme.setup_theme()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.title_bar = CustomTitleBar(self, "Collisions", 14, appstyle=app.style())
        self.app = app # TODO: needed?

        
        centra_widget_layout = QVBoxLayout()
        centra_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        centra_widget_layout.addWidget(self.title_bar)
        centra_widget_layout.addWidget(HorizontalDivider(3))
        # menu_bar = CustomMenuBar(app)
        # centra_widget_layout.addWidget(menu_bar)

        centra_widget_layout.addWidget(View(app))
        
        central_widget = QWidget()
        # This container holds the window contents, so we can style it.
        central_widget.setObjectName("Container")
        central_widget.setLayout(centra_widget_layout)
        self.setCentralWidget(central_widget)
    
    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()

    def window_state_changed(self, state):
        self.normal_button.setVisible(state == Qt.WindowState.WindowMaximized)
        self.max_button.setVisible(state != Qt.WindowState.WindowMaximized)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()
