from PyQt5 import QtWidgets, QtCore
import atexit
import os
import signal
import subprocess
from Tracker import Tracker


class UserInterface(QtWidgets.QMainWindow):

    def __init__(self):
        UserInterface.kill_tracker()
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

        self.sorting_button = QtWidgets.QPushButton("SORTING BY \nUSE TIME")
        self.sorting_button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.ascending_sorting_button = QtWidgets.QPushButton("DESCENDING\nSORTING")
        self.ascending_sorting_button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.hide_button = QtWidgets.QPushButton("HIDDEN\nINVISIBLE")
        self.hide_button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.favourites_button = QtWidgets.QPushButton("FAVOURITES\nOFF")
        self.favourites_button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.sorting_button.setStyleSheet("font: 10pt Arial")
        self.ascending_sorting_button.setStyleSheet("font: 10pt Arial")
        self.hide_button.setStyleSheet("font: 10pt Arial")
        self.favourites_button.setStyleSheet("font: 10pt Arial")

        self.__button_layout.addWidget(self.sorting_button)
        self.__button_layout.addWidget(self.ascending_sorting_button)
        self.__button_layout.addWidget(self.hide_button)
        self.__button_layout.addWidget(self.favourites_button)

        res_x = 2560
        res_y = 1440
        self.move(int(res_x / 2) - int(self.frameSize().width() / 2),
                  int(res_y / 2) - int(self.frameSize().height() / 2))

        self.tracked = Tracker.get_tracked_applications()

        self.scroll_area_widget = QtWidgets.QWidget()
        self.__scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.scroll_area_widget)
        self.scroll_area_table = QtWidgets.QTableWidget(len(self.tracked), 7)
        self.scroll_area_layout.addWidget(self.scroll_area_table)
        self.scroll_area_table.setHorizontalHeaderLabels(["Executable", "Name", "First used", "Last used",
                                                          "Use time (hours)", "Favourite", "Hidden"])
        self.sorting_mode = 4  # from 1 to 4
        self.sorting_descriptions = ["NAME", "FIRST USED", "LAST USED", "USE TIME"]
        self.ascending_sorting = False

        self.favourites_only = False
        self.hide_hidden = True

        row = 0
        for application in self.tracked:
            app = self.tracked[application]
            exe_name = QtWidgets.QTableWidgetItem(application)
            name = QtWidgets.QTableWidgetItem(app.name)
            started = QtWidgets.QTableWidgetItem(app.started.strftime("%m/%d/%Y, %H:%M:%S"))
            ended = QtWidgets.QTableWidgetItem(app.last.strftime("%m/%d/%Y, %H:%M:%S"))
            time_displayed = round(app.use_time / 3600, 2)
            use_time = QtWidgets.QTableWidgetItem()
            use_time.setData(QtCore.Qt.ItemDataRole.DisplayRole, time_displayed)
            favourite = QtWidgets.QTableWidgetItem(str(app.favourite))
            hidden = QtWidgets.QTableWidgetItem(str(app.hidden))
            if self.hide_hidden and app.hidden:
                self.scroll_area_table.hideRow(row)

            exe_name.setFlags(started.flags() ^ (QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEditable))
            started.setFlags(started.flags() ^ (QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEditable))
            ended.setFlags(ended.flags() ^ (QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEditable))
            use_time.setFlags(use_time.flags() ^ (QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEditable))
            favourite.setFlags(favourite.flags() ^ (QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEditable))
            hidden.setFlags(hidden.flags() ^ (QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEditable))
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

        self.scroll_area_table.clicked.connect(self.cell_clicked)

        self.sorting_button.clicked.connect(self.change_sorting)
        self.ascending_sorting_button.clicked.connect(self.change_ascending_sorting)
        self.hide_button.clicked.connect(self.toggle_hiding)
        self.favourites_button.clicked.connect(self.toggle_favourites)

        atexit.register(self.save_changes)
        atexit.register(UserInterface.start_tracker)

    @staticmethod
    def start_tracker():
        subprocess.call(["TrackerApplication.exe"])

    @staticmethod
    def kill_tracker():
        try:
            file = open("data/pid.txt")
            pid = int(file.readline().rstrip())
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass

    def toggle_favourites(self):
        self.favourites_only = not self.favourites_only
        if self.favourites_only:
            self.favourites_button.setText("FAVOURITES\nON")
            for row in range(self.scroll_area_table.rowCount()):
                if self.scroll_area_table.item(row, 5).text() == "False":
                    self.scroll_area_table.hideRow(row)
        else:
            self.favourites_button.setText("FAVOURITES\nOFF")
            if self.hide_hidden:
                for row in range(self.scroll_area_table.rowCount()):
                    if self.scroll_area_table.item(row, 5).text() == "False" and \
                            self.scroll_area_table.item(row, 6).text() == "False":
                        self.scroll_area_table.showRow(row)
            else:
                for row in range(self.scroll_area_table.rowCount()):
                    if self.scroll_area_table.item(row, 5).text() == "False":
                        self.scroll_area_table.showRow(row)

    def toggle_hiding(self):
        self.hide_hidden = not self.hide_hidden
        if self.hide_hidden:
            self.hide_button.setText("HIDDEN\nINVISIBLE")
            for row in range(self.scroll_area_table.rowCount()):
                if self.scroll_area_table.item(row, 6).text() == "True":
                    self.scroll_area_table.hideRow(row)
        else:
            self.hide_button.setText("HIDDEN\nVISIBLE")
            if self.favourites_only:
                for row in range(self.scroll_area_table.rowCount()):
                    if self.scroll_area_table.item(row, 5).text() == "True" and \
                            self.scroll_area_table.item(row, 6).text() == "True":
                        self.scroll_area_table.showRow(row)
            else:
                for row in range(self.scroll_area_table.rowCount()):
                    if self.scroll_area_table.item(row, 6).text() == "True":
                        self.scroll_area_table.showRow(row)

    def cell_clicked(self, item):
        col = item.column()
        row = item.row()
        print(row, col)
        if col == 5:
            it = self.scroll_area_table.item(row, col).text()
            if it == "False":
                self.scroll_area_table.item(row, col).setText("True")
                self.tracked[self.scroll_area_table.item(row, 0).text()].favourite = True
            elif it == "True":
                self.scroll_area_table.item(row, col).setText("False")
                self.tracked[self.scroll_area_table.item(row, 0).text()].favourite = False
                if self.favourites_only:
                    self.scroll_area_table.hideRow(row)
        elif col == 6:
            it = self.scroll_area_table.item(row, col).text()
            if it == "False":
                self.scroll_area_table.item(row, col).setText("True")
                self.tracked[self.scroll_area_table.item(row, 0).text()].hidden = True
                if self.hide_hidden:
                    self.scroll_area_table.hideRow(row)
            elif it == "True":
                self.scroll_area_table.item(row, col).setText("False")
                self.tracked[self.scroll_area_table.item(row, 0).text()].hidden = False

    def sort(self):
        if self.ascending_sorting:
            self.scroll_area_table.sortItems(self.sorting_mode, QtCore.Qt.SortOrder.AscendingOrder)
        else:
            self.scroll_area_table.sortItems(self.sorting_mode, QtCore.Qt.SortOrder.DescendingOrder)

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
                self.tracked[self.scroll_area_table.item(row, 0).text()].name = \
                    self.scroll_area_table.item(row, 1).text()
        Tracker.write_times(self.tracked)

