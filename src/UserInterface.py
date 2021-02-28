from PyQt5 import QtWidgets
import sys
import json
import jsons
from AppInfo import AppInfo


class UserInterface(QtWidgets.QMainWindow):

    def __init__(self):
        super(UserInterface, self).__init__()
        self.__scene_size = 880
        self.setCentralWidget(QtWidgets.QWidget())
        self.__main_layout = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.__main_layout)

        self.setGeometry(0, 0, self.__scene_size + 420, self.__scene_size + 20)
        self.setWindowTitle('TimeTrackerGUI')
        self.show()

        self.__scroll_area = QtWidgets.QScrollArea()
        self.__scroll_area.setWidgetResizable(True)
        self.__main_layout.addWidget(self.__scroll_area)

        self.__button_layout = QtWidgets.QVBoxLayout()
        self.__main_layout.addLayout(self.__button_layout)

        # widgetit
        self.__jatka_nappi = QtWidgets.QPushButton("BUTTON")
        self.__jatka_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__pelaa_nappi = QtWidgets.QPushButton("BUTTON")
        self.__pelaa_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__kenttaeditori_nappi = QtWidgets.QPushButton("BUTTON")
        self.__kenttaeditori_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__poistu_nappi = QtWidgets.QPushButton("BUTTON")
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
        self.__button_layout.addWidget(self.__jatka_nappi)
        self.__button_layout.addWidget(self.__pelaa_nappi)
        self.__button_layout.addWidget(self.__kenttaeditori_nappi)
        self.__button_layout.addWidget(self.__poistu_nappi)

        # keskelle liikuttaminen
        res_x = 2560
        res_y = 1440
        self.move(int(res_x / 2) - int(self.frameSize().width() / 2),
                  int(res_y / 2) - int(self.frameSize().height() / 2))

        self.tracked = UserInterface.get_tracked_applications()
        print(self.tracked)

        self.scroll_area_widget = QtWidgets.QWidget()
        self.__scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.scroll_area_widget)

        for application in self.tracked:
            app = self.tracked[application]
            name = QtWidgets.QLabel("Name: " + app.name)
            started = QtWidgets.QLabel("First used: " + app.started.strftime("%m/%d/%Y, %H:%M:%S"))
            ended = QtWidgets.QLabel("Last used: " + app.last.strftime("%m/%d/%Y, %H:%M:%S"))
            time_used = app.use_time
            if time_used < 60:
                time_string = str(app.use_time, ) + " seconds"
            elif time_used / 60 < 60:
                time_string = str(round(app.use_time / 60, 1)) + " minutes"
            else:
                time_string = str(round(app.use_time / 3600, 2)) + " hours"
            use_time = QtWidgets.QLabel("Use time: " + time_string)
            spacer = QtWidgets.QLabel("")
            self.scroll_area_layout.addWidget(name)
            self.scroll_area_layout.addWidget(started)
            self.scroll_area_layout.addWidget(ended)
            self.scroll_area_layout.addWidget(use_time)
            self.scroll_area_layout.addWidget(spacer)

    def edit_app_name(self, key, name):
        # change name in tracked dictionary
        # save to file with another button or on exit
        pass


    @staticmethod
    def get_tracked_applications():
        tracked = {}
        try:
            with open("data/tracked.json", "r") as read_file:
                data = json.load(read_file)
                for application in data:
                    tracked[application] = jsons.load(data[application], AppInfo)
        except OSError:
            pass
        return tracked
