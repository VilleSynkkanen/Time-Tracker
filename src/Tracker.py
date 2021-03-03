import time
import datetime
import psutil
import win32process
import win32gui
import json
import jsons
import os
import signal
import atexit
from AppInfo import AppInfo


class Tracker:

    def __init__(self):
        self.polling_time = 1
        self.save_interval = 1
        self.tracked_applications = Tracker.get_tracked_applications()
        pid = os.getpid()
        Tracker.save_pid(pid)
        jsons.suppress_warnings(True)
        atexit.register(self.handle_exit)
        self.kill_now = False
        signal.signal(signal.SIGTERM, self.handle_exit)
        signal.signal(signal.SIGINT, self.handle_exit)
        self.tracking_loop()

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

    @staticmethod
    def write_times(applications):
        try:
            with open("data/tracked.json", "w") as write_file:
                json.dump(jsons.dump(applications), write_file)
        except OSError:
            pass

    @staticmethod
    def save_pid(pid):
        try:
            file = open("data/pid.txt", "w")
            file.write(str(pid))
            file.close()
        except OSError:
            pass

    @staticmethod
    def get_active_window():
        try:
            pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
            return psutil.Process(pid[-1]).name()
        except psutil.NoSuchProcess:
            return None
        except psutil.AccessDenied:
            return None
        except AttributeError:
            return None
        except PermissionError:
            return None
        except ValueError:
            return None

    def handle_exit(self):
        self.kill_now = True
        Tracker.write_times(self.tracked_applications)

    def tracking_loop(self):
        active_window = None
        start_time = datetime.datetime.now()
        save_time = start_time
        while not self.kill_now:
            time.sleep(self.polling_time)
            window_name = self.get_active_window()
            if active_window != window_name:
                end_time = datetime.datetime.now()
                delta = end_time - start_time
                if active_window is not None:
                    if active_window in self.tracked_applications:
                        # update AppInfo
                        self.tracked_applications[active_window].use_time += delta.seconds
                        self.tracked_applications[active_window].last = end_time
                    else:
                        # create AppInfo instance, add it to tracked apps
                        name = active_window.split(".")[0]
                        info = AppInfo(name, delta.seconds, start_time, end_time)
                        self.tracked_applications[active_window] = info
                    # check save interval
                    if (end_time - save_time).seconds >= self.save_interval:
                        Tracker.write_times(self.tracked_applications)
                        save_time = end_time
                start_time = end_time
                active_window = window_name
