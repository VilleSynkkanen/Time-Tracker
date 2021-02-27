import time
import datetime
import psutil
import win32process
import win32gui
import json
import jsons
from AppInfo import AppInfo

polling_time = 1


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


def write_times(applications):
    with open("data/tracked.json", "w") as write_file:
        json.dump(jsons.dump(applications), write_file)


def get_active_window():
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return psutil.Process(pid[-1]).name()
    except psutil.NoSuchProcess:
        return None
    except ValueError:
        return None


def main():
    # suppress no timezones warning
    jsons.suppress_warnings(True)
    tracked_applications = get_tracked_applications()
    active_window = None
    start_time = datetime.datetime.now()
    while True:
        window_name = get_active_window()
        if active_window != window_name:
            end_time = datetime.datetime.now()
            delta = end_time - start_time
            if active_window is not None:
                if active_window in tracked_applications:
                    # update AppInfo
                    tracked_applications[active_window].use_time += delta.seconds
                    tracked_applications[active_window].last = end_time
                else:
                    # create AppInfo instance, add it to tracked apps
                    info = AppInfo(active_window, delta.seconds, start_time, end_time)
                    tracked_applications[active_window] = info
                write_times(tracked_applications)
            start_time = end_time
            active_window = window_name
        time.sleep(polling_time)


main()
