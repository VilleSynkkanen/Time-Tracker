import time
import os
import datetime
import sys
import psutil
import win32process
import win32gui

polling_time = 1


def get_tracked_applications():
    file = open("tracked.txt", 'r')
    tracked = {}
    for line in file:
        line = line.split(":")
        for i in range(0, len(line)):
            line[i] = line[i].strip()
        tracked[line[0]] = int(line[1])
    file.close()
    #print(tracked)
    return tracked


def write_times(applications):
    file = open("tracked.txt", 'w')
    for app in applications:
        file.write(app + ":" + str(applications[app]) + "\n")
    file.close()


def get_active_window():
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return psutil.Process(pid[-1]).name()
    except psutil.NoSuchProcess:
        return None
    except ValueError:
        return None


def main():
    tracked_applications = get_tracked_applications()
    active_window = None
    start_time = datetime.datetime.now()
    while True:
        window_name = get_active_window()
        if active_window != window_name:
            end_time = datetime.datetime.now()
            delta = end_time - start_time
            if active_window is not None:
                #print("Executable:", active_window, "\nUse time:", delta.seconds, "seconds")
                if active_window in tracked_applications:
                    tracked_applications[active_window] += delta.seconds
                else:
                    tracked_applications[active_window] = delta.seconds
                write_times(tracked_applications)
            start_time = end_time
            active_window = window_name

        time.sleep(polling_time)


main()
