"""Get user info: directory for Chrome profiles, profile name, and where to store profile
shortcuts."""
import os
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
        open_temporary_browser()
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


def open_temporary_browser():
    """Docstring"""
    program_path = os.path.dirname(os.path.realpath(__file__))
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
