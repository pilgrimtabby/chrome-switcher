"""Docstring"""
import os
import platform
import subprocess
import common


def get_chrome_path():
    """Docstring"""
    chrome_path = ""
    if platform.system() == "Windows":
        possible_chrome_paths = ["C:/Program Files/Google/Chrome/Application/chrome.exe",
                                 "C:/Program Files (x86)/Google/Chrome/Application/"
                                 "chrome.exe",
                                 "C:/Program Files (x86)/Google/Application/chrome.exe",
                                 "C:/Users/UserName/AppDataLocal/Google/Chrome/chrome.exe",
                                 "C:/Documents and Settings/UserName/Local Settings/"
                                 "Application Data/Google/Chrome/chrome.exe"]
        for path in possible_chrome_paths:
            if os.path.exists(path):
                return path

        return prompt_user_for_chrome_path()

    # macOS
    default_chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(default_chrome_path):
        return default_chrome_path
    try:
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
                            end if
                        end if
                    end if
                on error -- ignore errors (if this block doesn't work, it doesn't matter too much)
                end try
            end repeat
            tell application "System Events" -- Minimize window
                set minimized to false
                repeat while not minimized
                    tell window 1 of process "Google Chrome" to set value of attribute "AXMinimized" to true
                    set minimized to (value of attribute "AXMinimized" of window 1 of process "Google Chrome")
                end repeat
            end tell

            set chrome_path to POSIX path of (path to application id "com.google.Chrome")
            tell application id "com.google.Chrome" to quit
            return chrome_path
            '''
            chrome_path_raw = subprocess.check_output(["osascript", "-e",
                                                        get_chrome_path_not_open_script])
        else:
            get_chrome_path_open_script = 'POSIX path of (path to application id "com.google.Chrome")'
            chrome_path_raw = subprocess.check_output(["osascript", "-e",
                                                        get_chrome_path_open_script])
        chrome_path_parsed = chrome_path_raw.decode("UTF-8").replace("/n", "")
        chrome_path = f"{chrome_path_parsed}Contents/MacOS/Google Chrome"
        if os.path.exists(chrome_path):
            return chrome_path
    except:
        return prompt_user_for_chrome_path()


def prompt_user_for_chrome_path():
    """Docstring"""
    if platform.system() == "Windows":
        chrome_name = "chrome.exe"
        subdirectories = ""
    else:
        chrome_name = "Google Chrome.app"
        subdirectories = "/Contents/MacOS/Google Chrome"
    header = common.box("Chrome Switcher | Chrome path")
    common.clear()
    print(f"{header}\n\nUnable to find {chrome_name}. Please select it:")
    chrome_path = common.get_file_path()
    chrome_path_file_name = os.path.basename(os.path.normpath(chrome_path))

    if chrome_path_file_name == chrome_name:
        full_chrome_path = f"{chrome_path}{subdirectories}"
        return full_chrome_path

    return None


def get_window_count():
    """Uses Applescript to get number of Chrome windows (macOS only)."""
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
