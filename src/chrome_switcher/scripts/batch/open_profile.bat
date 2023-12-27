REM Open Google Chrome in a new session using the directory "%~1" as the user-data-dir.
REM Drag and drop a directory on this batch file to use it.


@ECHO OFF

REM Console briefly appears but is quickly minimized (code comes from the link below):
REM stackoverflow.com/questions/9232308/how-do-i-minimize-the-command-prompt-from-my-bat-file
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit

REM `START "" ` forces the shell not to wait for the termination of the command before exiting.
REM This keeps the terminal window from staying open if it wasn't open already.
START "" "chrome_path" chrome://newtab --user-data-dir="%~1"
EXIT
