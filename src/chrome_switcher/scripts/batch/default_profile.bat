REM Open Google Chrome in a new session using Chrome's default user-data-dir.
REM The Python script replaces "chrome_path" with the path to chrome.exe.


@ECHO OFF

REM Console briefly appears but is quickly minimized (code comes from the link below):
REM stackoverflow.com/questions/9232308/how-do-i-minimize-the-command-prompt-from-my-bat-file
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit

REM `START "" ` forces the shell not to wait for the termination of the command before exiting.
REM This keeps the terminal window from staying open if it wasn't open already.
START "" "chrome_path" chrome://newtab --user-data-dir="%LOCALAPPDATA%/Google/Chrome/User Data"
EXIT
