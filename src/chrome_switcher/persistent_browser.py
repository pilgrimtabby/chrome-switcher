"""Get user info: directory for Chrome profiles, profile name, and where to store profile
shortcuts."""
import os
import platform
import shutil
import subprocess
import sys
import time
import browser_path
import common
import settings
import shortcut_files


def main():
    """Prompt user to choose between a temporary and a persistent new Chrome profile.
    If temporary is selected, return None (this is handled later).
    If persistent is selected, get profile and shortcut directories, as well as name of new 
    profile, and return a path to the new Chrome profile."""
    profiles_directory = common.load_pickle("profiles_directory.txt")
    if not os.path.exists(profiles_directory):
        settings.change_profiles_directory_settings()
        profiles_directory = common.load_pickle("profiles_directory.txt")
        if not os.path.exists(profiles_directory):
            return False

    profile_name = get_profile_name()
    if profile_name is None:
        return False
    unique_profile_name = get_unique_name(profile_name)

    create_profile(unique_profile_name)
    if (not os.path.exists(f"{profiles_directory}/open_profile.bat")
        and not os.path.exists(f"{profiles_directory}/open_profile.app") or
        not os.path.exists(f"{profiles_directory}/default_profile.bat")
        and not os.path.exists(f"{profiles_directory}/default_profile")):
        shortcut_files.main()

    header = common.box("Chrome Switcher | New profile | Open browser")
    common.clear()
    open_it = input(f"{header}\n\nStart a new session of Chrome now with this profile?\n"
                         "Press enter to open, or type \"no\" to go to the menu: ").lower()
    if open_it != "no":
        successfully_opened = open_browser(unique_profile_name)
        return successfully_opened
    return False


def open_browser(profile_name):
    """Docstring"""
    chrome_path = browser_path.get_chrome_path()
    profiles_directory = common.load_pickle("profiles_directory.txt")
    if chrome_path is not None:
        if platform.system() == "Windows":
            program_path = os.path.dirname(os.path.realpath(__file__))
            subprocess.Popen([chrome_path, "chrome://newtab",
                              f"--user-data-dir={profiles_directory}/{profile_name}"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            subprocess.Popen([sys.executable, f"{program_path}/delete_lnk.py"],
                              creationflags=subprocess.DETACHED_PROCESS)
        else:
            subprocess.Popen([chrome_path, "--args", f"--user-data-dir={profiles_directory}/"
                              f"{profile_name}", "--new-window", "chrome://newtab"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
    print("\nGoogle Chrome could not be found. Please verify your installation and try again.")
    time.sleep(2)
    return False


def create_profile(profile_name):
    """Docstring"""
    header = common.box("Chrome Switcher | New profile | Generating files")
    common.clear()
    print(f"{header}\n")

    profiles_directory = common.load_pickle("profiles_directory.txt")
    if not os.path.exists(profiles_directory):
        os.mkdir(profiles_directory)

    new_profile_settings = common.load_pickle("new_profile_settings.txt")
    used_default_instead = False
    if new_profile_settings == "":
        os.mkdir(f"{profiles_directory}/{profile_name}")
    elif new_profile_settings != "" and not os.path.exists(new_profile_settings):
        used_default_instead = True
        os.mkdir(f"{profiles_directory}/{profile_name}")
    else:
        try:
            print(f"Copying base chrome profile to {profiles_directory}/{profile_name}\n"
                  "This may take a few moments...")
            shutil.copytree(new_profile_settings, f"{profiles_directory}/{profile_name}")
        except shutil.Error:
            pass

    if used_default_instead:
        print("The Chrome profile you selected to act as a base for new profiles no longer "
              "exists, or could not be found. Default settings will be used instead.")
        time.sleep(2)
    print(f"New Chrome profile generated:\n{profiles_directory}/{profile_name}")
    time.sleep(1)


def get_profile_name():
    """Prompt user for name of new Chrome profile."""
    header = common.box("Chrome Switcher | New profile | Profile name")
    common.clear()
    profile_name = input(f"{header}\n\nEnter a profile name (press enter to quit): ")
    if len(profile_name) > 0:
        return profile_name
    return None


def get_unique_name(profile_name):
    """Checks the path to a profile to see if the path already exists. If it does, change it to a
    unique name and return the name."""
    target_directory = common.load_pickle("profiles_directory.txt")
    new_profile_name = profile_name
    suffix = 2
    while os.path.exists(f"{target_directory}/{new_profile_name}"):
        new_profile_name = f"{profile_name}-{suffix}"
        suffix += 1
    return new_profile_name
