import sys
from PySide6.QtWidgets import QApplication, QDialog

from view.experiment.widgets import VectorIssueCheck

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_dialog = VectorIssueCheck([[1,0.000001,0.00,0.000001,"k1"], [1,0,0,0,"k2"]])
    if main_dialog.exec() == QDialog.Rejected:
        print("User closed")
    
    sys.exit(app.exec())