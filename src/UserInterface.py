from PyQt5 import QtWidgets, QtCore
import sys
import json
import jsons
import atexit
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
        self.sorting_button = QtWidgets.QPushButton("SORTING BY \nUSE TIME")
        self.sorting_button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.ascending_sorting_button = QtWidgets.QPushButton("DESCENDING\nSORTING")
        self.ascending_sorting_button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__kenttaeditori_nappi = QtWidgets.QPushButton("BUTTON")
        self.__kenttaeditori_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__poistu_nappi = QtWidgets.QPushButton("BUTTON")
        self.__poistu_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.sorting_button.setStyleSheet("font: 10pt Arial")
        self.ascending_sorting_button.setStyleSheet("font: 10pt Arial")
        self.__kenttaeditori_nappi.setStyleSheet("font: 10pt Arial")
        self.__poistu_nappi.setStyleSheet("font: 10pt Arial")

        self.sorting_button.clicked.connect(self.change_sorting)
        self.ascending_sorting_button.clicked.connect(self.change_ascending_sorting)

        # nappi widgetit
        self.__button_layout.addWidget(self.sorting_button)
        self.__button_layout.addWidget(self.ascending_sorting_button)
        self.__button_layout.addWidget(self.__kenttaeditori_nappi)
        self.__button_layout.addWidget(self.__poistu_nappi)

        # keskelle liikuttaminen
        res_x = 2560
        res_y = 1440
        self.move(int(res_x / 2) - int(self.frameSize().width() / 2),
                  int(res_y / 2) - int(self.frameSize().height() / 2))

        self.tracked = UserInterface.get_tracked_applications()

        # Table creation
        self.scroll_area_widget = QtWidgets.QWidget()
        self.__scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.scroll_area_widget)
        self.scroll_area_table = QtWidgets.QTableWidget(len(self.tracked), 7)
        self.scroll_area_layout.addWidget(self.scroll_area_table)
        self.scroll_area_table.setHorizontalHeaderLabels(["Executable", "Name", "First used", "Last used", "Use time", "Favourite",
                                                          "Hidden"])
        self.sorting_mode = 4 # from 1 to 4
        self.sorting_descriptions = ["NAME", "FIRST USED", "LAST USED", "USE TIME"]
        self.ascending_sorting = False

        row = 0
        for application in self.tracked:
            app = self.tracked[application]
            exe_name = QtWidgets.QTableWidgetItem(application)
            name = QtWidgets.QTableWidgetItem(app.name)
            started = QtWidgets.QTableWidgetItem(app.started.strftime("%m/%d/%Y, %H:%M:%S"))
            ended = QtWidgets.QTableWidgetItem(app.last.strftime("%m/%d/%Y, %H:%M:%S"))
            time_used = app.use_time
            time_string = str(round(app.use_time / 3600, 3)) + " hours"
            use_time = QtWidgets.QTableWidgetItem(time_string)
            favourite = QtWidgets.QTableWidgetItem(str(app.favourite))
            hidden = QtWidgets.QTableWidgetItem(str(app.hidden))

            exe_name.setFlags(started.flags() ^ (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable))
            started.setFlags(started.flags() ^ (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable))
            ended.setFlags(ended.flags() ^ (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable))
            use_time.setFlags(use_time.flags() ^ (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable))
            favourite.setFlags(favourite.flags() ^ (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable))
            hidden.setFlags(hidden.flags() ^ (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable))
            self.scroll_area_table.setItem(row, 0, exe_name)
            self.scroll_area_table.setItem(row, 1, name)
            self.scroll_area_table.setItem(row, 2, started)
            self.scroll_area_table.setItem(row, 3, ended)
            self.scroll_area_table.setItem(row, 4, use_time)
            self.scroll_area_table.setItem(row, 5, favourite)
            self.scroll_area_table.setItem(row, 6, hidden)
            row += 1

        self.scroll_area_table.horizontalHeader().setStretchLastSection(True)
        self.scroll_area_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.sort()

        atexit.register(self.save_changes)

    def sort(self):
        if self.ascending_sorting:
            self.scroll_area_table.sortItems(self.sorting_mode, QtCore.Qt.AscendingOrder)
        else:
            self.scroll_area_table.sortItems(self.sorting_mode, QtCore.Qt.DescendingOrder)

    def change_ascending_sorting(self):
        self.ascending_sorting = not self.ascending_sorting
        if self.ascending_sorting:
            self.ascending_sorting_button.setText("ASCENDING\nSORTING")
        else:
            self.ascending_sorting_button.setText("DESCENDING\nSORTING")
        self.sort()

    def change_sorting(self):
        # sorting by: name, started, last, time
        self.sorting_mode += 1
        if self.sorting_mode > 4:
            self.sorting_mode = 1
        self.sorting_button.setText("SORTING BY\n" + self.sorting_descriptions[self.sorting_mode - 1])
        self.sort()

    def save_changes(self):
        for row in range(self.scroll_area_table.width()):
            if self.scroll_area_table.item(row, 0) is not None:
                self.tracked[self.scroll_area_table.item(row, 0).text()].name = self.scroll_area_table.item(row, 1).text()
                #print(self.scroll_area_table.item(row, 1).text())
        UserInterface.write_times(self.tracked)

    @staticmethod
    def write_times(applications):
        try:
            with open("data/tracked.json", "w") as write_file:
                json.dump(jsons.dump(applications), write_file)
        except OSError:
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
