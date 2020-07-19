from PySide2 import QtWidgets

from src.gui.edit_pipes_dialog import Ui_edit_pipes_dlg


class EditPipes(QtWidgets.QDialog, Ui_edit_pipes_dlg):
    """Edit pipes dialog wrapper."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
