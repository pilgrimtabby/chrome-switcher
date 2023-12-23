import subprocess
def main():
    if get_window_count() == 0:
        get_chrome_path_not_open_script = '''
        tell application id "com.google.Chrome" to activate

        -- Wait until Chrome is running, in front, and has a window open
        repeat 4000 times -- try for roughly 10 seconds
            try
                if application id "com.google.Chrome" is running then
                    if frontmost of application id "com.google.Chrome" then
                        if window 1 of application id "com.google.Chrome" exists then
                            exit repeat
                        else
                            tell application id "com.google.Chrome" to make new window  -- if Chrome is running but no windows open
                        end if
                    end if
                end if
            on error -- ignore errors (if this block doesn't work, it doesn't matter too much)
            end try
        end repeat
        try
            tell application "System Events" -- Minimize window
                set minimized to false
                repeat 4000 times -- try for roughly 10 seconds
                    tell window 1 of process "Google Chrome" to set value of attribute "AXMinimized" to true
                    set minimized to (value of attribute "AXMinimized" of window 1 of process "Google Chrome")
                    if minimized is true then exit repeat
                end repeat
            end tell
        end try

        set chrome_path to POSIX path of (path to application id "com.google.Chrome")
        tell application id "com.google.Chrome" to quit
        return chrome_path
        '''
        chrome_path_raw = subprocess.check_output(["osascript", "-e",
                                                    get_chrome_path_not_open_script])
    else:
        get_chrome_path_open_script = 'POSIX path of (path to application "Chrome")'
        chrome_path_raw = subprocess.check_output(["osascript", "-e", 
                                                    get_chrome_path_open_script])
    chrome_path_raw_parsed = chrome_path_raw.decode("UTF-8").replace("\n", "")
    chrome_path = f"{chrome_path_raw_parsed}Contents/MacOS/Google Chrome"
    print(chrome_path)


def get_window_count():
    """Uses Applescript to get number of currently open Chrome windows (macOS only)."""
    get_window_count_script = '''
    if application id "com.google.Chrome" is running then tell application id "com.google.Chrome"
        set window_count to the index of windows
        return (number of items in window_count)
    end tell
    '''
    # Run script, convert output from byte to string
    window_count = subprocess.check_output(['osascript', '-e',
                                            get_window_count_script]).decode("UTF-8")
    if window_count == "":  # Chrome not running
        return 0
    return int(window_count)


main()
