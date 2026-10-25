from PySide6.QtWidgets import QMessageBox


def show_confirmation_popup(parent, title, question):
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(question)
    msg_box.setIcon(QMessageBox.Icon.Question)
    msg_box.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    return msg_box.exec()
