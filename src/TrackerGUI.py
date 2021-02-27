from PyQt5.QtWidgets import QApplication
from UserInterface import UserInterface
import sys


def main():
    global app
    app = QApplication(sys.argv)
    gui = UserInterface()
    sys.exit(app.exec_())


main()
