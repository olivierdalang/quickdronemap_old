import os

from PyQt5 import uic
from PyQt5 import QtWidgets

UI_FILE_PATH = os.path.join(os.path.dirname(__file__), 'quick_drone_map_dialog_base.ui')

class QuickDroneMapDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(UI_FILE_PATH, self)
