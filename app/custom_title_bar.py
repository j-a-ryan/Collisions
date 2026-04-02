from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QStyle,
    QToolButton,
    QWidget,
    QFontComboBox
)
from PySide6.QtGui import QPixmap, QIcon

from view.common.details import Heading

class CustomTitleBar(QWidget):
    def __init__(self, parent, title_text, font_size, include_icon=True, appstyle=None):
        super().__init__(parent)
        self.initial_pos = None
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_label = Heading(title_text, "Lucida Sans", False) #"Lucida Console" "Lucida Sans" "Segoe UI"
        self.title_label.set_font_point_size(font_size)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        if include_icon:
            img_label = QLabel()
            pixmap = QPixmap('resources/collisionicon3.png')
            img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignLeft)

            # self.title_label.setText(
            #     """
            #     <span style="font-family: 'Arial', sans-serif; font-style: italic; font-size: 12pt; color: black;">Col</span><!--
            #     --><span style="font-family: 'Times New Roman'; font-size: 16pt; font-style: italic; color: black;">V</span><span style="font-family: 'Arial', sans-serif; font-style: italic; font-size: 12pt; color: black;">ision</span>
            #     """
            # )
            
            layout.addWidget(img_label)
        layout.addWidget(self.title_label)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # layout.addWidget(QFontComboBox())

        close_icon = appstyle.standardIcon(QStyle.StandardPixmap.SP_BrowserStop)#SP_TitleBarCloseButton)
        # new_size = QSize(64, 64) 

        # # Convert the QIcon to a QPixmap and scale it
        # # You can specify the mode and state if needed, e.g., QIcon.Normal, QIcon.Off
        # close_icon_larger = close_icon.pixmap(new_size) 

        # # Create a new QIcon from the scaled QPixmap
        # resized_icon = QIcon(close_icon_larger)

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
            button.setStyleSheet(
                """QToolButton {
                    border: none;
                    padding: 2px;
                }
                """
            )
            
            buttons_layout.addWidget(button, alignment=Qt.AlignRight)
        layout.addStretch() # So the buttons go all the way to the right.
        layout.addLayout(buttons_layout)

    # def set_title_font_for_theme(self, theme):
    #     pass
        # Dark: background: #202124, border: #3f4042, foreground: #e4e7eb
        # Light: base: #202124, border: #dadce0, foreground: #4d5157
        # if theme is "dark":
        #     self.title_label.setStyleSheet("color: #e4e7eb;")
        # elif theme is "light":
        #     self.title_label.setStyleSheet("color: #4d5157;")

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)