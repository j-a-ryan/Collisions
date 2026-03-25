from PySide6.QtWidgets import QPushButton, QStyle
from PySide6.QtGui import QIcon

class DeleteVectorRowButton(QPushButton):

    def __init__(self, parent_form_style):
        super().__init__()
        self.parent_form_style = parent_form_style
        self.setStyleSheet("border: none;")
        self.disabled_icon = QIcon()
        self.delete_icon = self.parent_form_style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical) #SP_BrowserStop
    
    # Make button visible and enabled.
    def activate(self):
        self.setIcon(self.delete_icon)
        self.setEnabled(True)
    
    # Make butten just a spacer. N.B.: spacer and invisible don't work.
    def deactivate(self):
        self.setIcon(self.disabled_icon)
        self.setEnabled(False) # In effect, a spacer. Spacer and blank widget didn't work

    @staticmethod # Currently just activating. May need deactivation in future.
    def check_button_states(grid_layout):
        # Row 0 is header. Get row 1's button, which is in col 7.
        first_row_delete_button = grid_layout.itemAtPosition(1, 7).widget() # This should never throw exception.
        if grid_layout.rowCount() > 2:
            first_row_delete_button.activate() # We were deactivating her (first row of several). Decided not needed
        else:
            first_row_delete_button.activate()
