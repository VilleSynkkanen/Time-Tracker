# TimeTracker

## General

- TimeTracker is a Python 3 application that runs in the background and tracks application use times.
- Saves the data into a JSON file.
- Only looks at the active window.
- Includes a simple GUI that can be used to view tracked statistics.
- Only works on Windows.

## Instructions

- Running the tracker: run TimeTracker.bat.
- Running the GUI: run TimeTrackerGUI.bat.
- Running the tracker on startup: add a shortcut to the bat file to the startup folder of the start menu (C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup).

## Dependencies

- Python3
- PyQt5
- win32process
- win32gui
- WMI
- psutil
- jsons

## Known issues

- Saving when GUI is launched or tracking process is otherwise killed does not work due to Windows not supporting cross-process signals properly. This means that the last 5 minutes of tracked data is lost.
