from PyQt5 import QtWidgets
import sys


class UserInterface(QtWidgets.QMainWindow):

    def __init__(self):
        super(UserInterface, self).__init__()
        self.__scene_size = 880
        self.setCentralWidget(QtWidgets.QWidget())
        self.__main_layout = QtWidgets.QVBoxLayout()
        self.centralWidget().setLayout(self.__main_layout)

        self.setGeometry(0, 0, self.__scene_size + 420, self.__scene_size + 20)
        self.setWindowTitle('TimeTrackerGUI')
        self.show()

        # widgetit
        self.__jatka_nappi = QtWidgets.QPushButton("BUTTON")
        self.__jatka_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__pelaa_nappi = QtWidgets.QPushButton("BUTTON")
        self.__pelaa_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__kenttaeditori_nappi = QtWidgets.QPushButton("BUTTON")
        self.__kenttaeditori_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__poistu_nappi = QtWidgets.QPushButton("POISTU")
        self.__poistu_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.__jatka_nappi.setStyleSheet("font: 10pt Arial")
        self.__pelaa_nappi.setStyleSheet("font: 10pt Arial")
        self.__kenttaeditori_nappi.setStyleSheet("font: 10pt Arial")
        self.__poistu_nappi.setStyleSheet("font: 10pt Arial")

        # nappien yhdistäminen
        '''
        self.__jatka_nappi.clicked.connect()
        self.__pelaa_nappi.clicked.connect()
        self.__kenttaeditori_nappi.clicked.connect()
        self.__poistu_nappi.clicked.connect()
        '''

        # nappi widgetit
        self.__main_layout.addWidget(self.__jatka_nappi, 2)
        self.__main_layout.addWidget(self.__pelaa_nappi, 2)
        self.__main_layout.addWidget(self.__kenttaeditori_nappi, 2)
        self.__main_layout.addWidget(self.__poistu_nappi, 2)

        # keskelle liikuttaminen
        res_x = 2560
        res_y = 1440
        self.move(int(res_x / 2) - int(self.frameSize().width() / 2),
                  int(res_y / 2) - int(self.frameSize().height() / 2))