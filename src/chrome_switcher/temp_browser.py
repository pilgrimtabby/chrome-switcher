"""Docstring"""
import os
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
    print(f"{header}\n\nOpening temporary browser...")
    subprocess.Popen([sys.executable, f"{program_path}/temp_browser_helper.py", chrome_path],
                    start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    time.sleep(1)
    return True
