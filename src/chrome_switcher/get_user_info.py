"""Get user info: directory for Chrome profiles, profile name, and where to store profile
shortcuts."""
import os
import platform
import subprocess
import sys
import time
import common


def main():
    """Prompt user to choose between a temporary and a persistent new Chrome profile.
    If temporary is selected, return None (this is handled later).
    If persistent is selected, get profile and shortcut directories, as well as name of new 
    profile, and return a path to the new Chrome profile."""
    profile_type = get_profile_type()
    if profile_type == "temporary":
        go_to_temporary_browser()
        return None

    profiles_directory = common.load_pickle("profiles_directory.txt")
    if not os.path.exists(profiles_directory):
        change_profiles_directory_settings()

    shortcuts_directory = common.load_pickle("shortcuts_directory.txt")
    if not os.path.exists(shortcuts_directory):
        change_shortcuts_directory_settings()

    profile_name = get_profile_name()
    while profile_name == "":
        settings_menu()
        profile_name = get_profile_name()

    profiles_directory = common.load_pickle("profiles_directory.txt")  # In case chgd. in settings
    profile_path = get_profile_path(profiles_directory, profile_name)
    return profile_path


def go_to_temporary_browser():
    """Docstring"""
    program_path = os.path.dirname(os.path.realpath(__file__))
    chrome_path = get_chrome_path()
    if chrome_path is None:
        header = common.box("Chrome Switcher | Chrome path")
        common.clear()
        print(f"{header}\n\nGoogle Chrome could not be found. Please verify your installation and "
              "try again.")
        time.sleep(3)
        return
    header = common.box("Chrome Switcher | Temporary browsing")
    common.clear()
    print(f"{header}\n\nOpening temporary browser...")
    subprocess.Popen([sys.executable, f"{program_path}/temporary_browser.py"],
                         start_new_session=True)


def get_profile_type():
    """Prompt user to choose between temporary or persistent profile type, and return the type."""
    header = common.box("Chrome Switcher | New profile | Profile type")
    common.clear()
    user_input = ""
    while True:
        user_input = input(f"{header}\n\nWelcome to Chrome Switcher!\n"
            "Please choose between a temporary or a persistent profile type.\n\n"
            "1) Temporary: all its data is deleted when the computer is shut down. Essentially "
            "functions like an incognito browser, but you can access history, maintain cookies, "
            "and so on.\n\n"

            "2) Persistent: will not be deleted. A shortcut will be created that allows re-access. "
            "Especially useful for managing multiple sign-ins for certain services, since you can "
            "have multiple instances of Google Chrome running simultaneously and independently of "
            "one another.\n\n"

            "Enter your choice (e.g. 1): ")

        if user_input.strip() == "1":
            return "temporary"
        if user_input.strip() == "2":
            return "persistent"


def change_profiles_directory_settings():
    """Helper function for change_directory_settings(). Changes setting for profiles directory."""
    header = common.box("Chrome Switcher | Settings | Profiles location")
    prompt = "Pease select a directory for new Chrome profiles:"
    pickle_name = "profiles_directory.txt"
    default_new_target = f"{os.path.join(os.path.expanduser('~'), 'Desktop')}/chrome-profiles"
    change_directory_settings(header, prompt, pickle_name, default_new_target)


def change_shortcuts_directory_settings():
    """Helper function for change_directory_settings(). Changes setting for shortcuts directory."""
    header = common.box("Chrome Switcher | Settings | Shortcuts location")
    prompt = "Pease select a directory for shortcuts to new Chrome profiles:"
    pickle_name = "shortcuts_directory.txt"
    default_new_target = os.path.join(os.path.expanduser('~'), 'Desktop')
    change_directory_settings(header, prompt, pickle_name, default_new_target)


def change_directory_settings(header, prompt, pickle_name, default_new_target):
    """Function that prompts users to choose a directory, then pickles it."""
    common.clear()
    print(f"{header}")

    current_target_directory = common.load_pickle(pickle_name)
    if os.path.exists(current_target_directory):
        print(f"\nCurrent directory: {current_target_directory}")
        print("\nTo choose a new directory, press space. To exit, press enter.")
        user_input = common.get_one_char()
        if user_input != " ":
            return

    print(f"\n{prompt}")
    new_target_directory = common.get_dir_path()
    if new_target_directory == "" and not os.path.exists(current_target_directory):
        common.dump_pickle(default_new_target, pickle_name)
        print(f"\nSet directory to {default_new_target}")
        time.sleep(1)
    elif os.path.exists(new_target_directory):
        common.dump_pickle(new_target_directory, pickle_name)
        common.clear()
        print(f"{header}\n\nSet directory to {new_target_directory}")
        time.sleep(1)


def change_new_profile_settings():
    return


def get_profile_name():
    """Prompt user for name of new Chrome profile."""
    header = common.box("Chrome Switcher | New profile | Profile name")
    common.clear()
    profile_name = input(f"{header}\n\nPlease enter a name for the new profile\n"
                       "             (press enter for settings): ")
    return profile_name


def settings_menu():
    """Menu to change program settings."""
    menu_options = ["Profiles directory", "Shortcuts directory", "New profile settings", "Go back"]
    quit_menu = False
    while not quit_menu:
        common.clear()
        header = common.box("Chrome Switcher | Settings")

        print(f"{header}\n")
        for i, option in enumerate(menu_options):
            if option == "Go back":
                print("")
            print(f"{str(i + 1)}: {option}")
        print(f"\nChoose an option (1 - {len(menu_options)}): ")

        user_input = ""
        # Keep going until user presses a valid number or enter / return
        while not user_input.isdigit() and user_input != "\r":
            user_input = common.get_one_char()

        if user_input == "\r":  # Pressed enter / return
            quit_menu = True

        elif 0 < int(user_input) <= len(menu_options):  # Pressed valid number
            choice = menu_options[int(user_input) - 1]
            if choice == "Profiles directory":
                change_profiles_directory_settings()
            elif choice == "Shortcuts directory":
                change_shortcuts_directory_settings()
            elif choice == "New profile settings":
                change_new_profile_settings()
            elif choice == "Go back":
                quit_menu = True


def get_profile_path(target_directory, profile_name):
    """Checks the path to a profile to see if the path already exists. If it does, change it to a
    unique name. Returns the complete path."""
    new_profile_name = profile_name
    suffix = 2
    while os.path.exists(f"{target_directory}/{new_profile_name}"):
        new_profile_name = f"{profile_name}-{suffix}"
        suffix += 1

    return f"{target_directory}/{new_profile_name}"


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
