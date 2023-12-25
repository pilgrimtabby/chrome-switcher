@ECHO OFF

REM Opens Google Chrome in a new session using the directory %~1 as the user-data-dir.
REM Drag and drop a directory on this batch file to use it.

chrome_path chrome://newtab --user-data-dir="%~1"
EXIT
