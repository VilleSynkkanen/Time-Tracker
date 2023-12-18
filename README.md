# TimeTracker

## General

- TimeTracker is an application that runs in the background and tracks application use times.
- Saves the data into a JSON file.
- Only looks at the active window.
- Includes a simple GUI that can be used to view tracked statistics.
- Works on Windows.

## Instructions

- Download the latest release.
- Running the tracker: run TrackerApplication.exe.
- Running the GUI: run TrackerGUI.exe.
- Running the tracker on startup (recommended): add a shortcut to the TrackerApplication.exe file to the startup folder of the start menu (C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup).

## Known issues

- Saving when GUI is launched or tracking process is otherwise killed does not work due to Windows not supporting cross-process signals properly. This means that the last 5 minutes of tracked data is lost.
- The tracker gets restarted after closing the GUI only if the UI window is closed first before closing the console window (may be fixed in the future).
- Sorting by first or last used is not working correctly (may be fixed in the future).
