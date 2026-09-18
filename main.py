import sys

from PySide6.QtWidgets import QApplication

from database.database import Session
from gui.windows.home_window import HomeWindow

session = Session()

app = QApplication(sys.argv)

window = HomeWindow(session)
window.show()

app.exec()
