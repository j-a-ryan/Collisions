from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QStyle,
    QToolButton,
    QWidget,
)

from view.common.details import Heading


class CustomTitleBar(QWidget):
    def __init__(self, parent, title_text, font_size, appstyle, include_icon=True):
        super().__init__(parent)
        self.initial_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_label = Heading(title_text, "Lucida Sans", False)  # "Lucida Console" "Lucida Sans" "Segoe UI"
        self.title_label.set_font_point_size(font_size)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        if include_icon:
            img_label = QLabel()
            pixmap = QPixmap("resources/collisionicon3.png")
            img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(img_label)

        layout.addWidget(self.title_label)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        close_icon = appstyle.standardIcon(QStyle.StandardPixmap.SP_BrowserStop)  # SP_TitleBarCloseButton)

        min_icon = appstyle.standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton)
        max_icon = appstyle.standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton)
        normal_icon = appstyle.standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton)

        # Min button
        self.min_button = QToolButton(self)
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.window().showMinimized)

        # Max button
        self.max_button = QToolButton(self)
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.window().showMaximized)

        # Close button
        self.close_button = QToolButton(self)
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)

        # Normal button
        self.normal_button = QToolButton(self)
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)

        # Add buttons
        buttons_layout = QHBoxLayout()
        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(16, 16))
            button.setStyleSheet("""QToolButton {
                    border: none;
                    padding: 2px;
                }
                """)

            buttons_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addStretch()  # So the buttons go all the way to the right.
        layout.addLayout(buttons_layout)

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)
