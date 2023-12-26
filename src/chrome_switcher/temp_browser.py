"""Docstring"""
import os
import platform
import subprocess
import sys
import time
import browser_path
import common


def main():
    """Docstring"""
    program_path = os.path.dirname(os.path.realpath(__file__))
    chrome_path = browser_path.get_chrome_path()
    if chrome_path is None:
        header = common.box("Chrome Switcher | Chrome path")
        common.clear()
        print(f"{header}\n\nGoogle Chrome could not be found. Please verify your installation and "
              "try again.")
        time.sleep(3)
        return False

    header = common.box("Chrome Switcher | Temporary browsing")
    common.clear()
    user_input = input(f"{header}\n\nNOTE: Temporary browsing data is erased as soon as the "
                       "session ends (on Windows, exiting all windows; on macOS, quitting the "
                       "instance of Chrome). If your battery dies or your computer otherwise "
                       "unexpectedly shuts down, there is a small chance data from your browsing "
                       "session might remain.\n\n"
                       "Type \"yes\" to continue (press enter to go back): ").lower()
    if user_input != "yes":
        return False

    print("\nOpening temporary browser...")

    if platform.system() == "Windows":
        subprocess.Popen([sys.executable, f"{program_path}/temp_browser_helper.py", chrome_path],
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
                         creationflags=subprocess.DETACHED_PROCESS)
        subprocess.Popen([sys.executable, f"{program_path}/delete_lnk.py"],
                          creationflags=subprocess.DETACHED_PROCESS)
    else:
        subprocess.Popen([sys.executable, f"{program_path}/temp_browser_helper.py", chrome_path],
                          stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
                          start_new_session=True)

    time.sleep(1)
    new_profile_settings = common.load_pickle("new_profile_settings.txt")
    if new_profile_settings != "" and not os.path.exists(new_profile_settings):
        print("\nTried to inheret settings from the directory you chose as a base, but it could "
              "not be found. Using default Chrome settings instead.")
        time.sleep(5)
    elif os.path.exists(new_profile_settings):
        print("\nInheriting settings from the directory you chose as a base.\nSit tight! "
              "Depending on your computer speed, it could up to a minute or more to copy the base "
              "profile and open the browsing session after this program exits.")
        time.sleep(5)

    return True
