from PyQt5.QtWidgets import QApplication
from app.maindialog import MainDialog
import sys


class MApp(QApplication):
    def __init__(self):
        super(MApp, self).__init__(sys.argv)
        self.md = MainDialog()
        self.md.show()

