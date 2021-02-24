import time
from os import system
import datetime
import sys
if sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32gui

polling_time = 1


def get_active_window():
    active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        active_window_name = win32gui.GetWindowText(window)
    return active_window_name


def main():
    active_window = ""
    start_time = datetime.datetime.now()
    while True:
        window_name = get_active_window()
        if active_window != window_name:
            end_time = datetime.datetime.now()
            print("Use time: ", end_time-start_time)
            start_time = end_time

            active_window = window_name
            print("Window name: ", active_window)
        time.sleep(polling_time)


main()
