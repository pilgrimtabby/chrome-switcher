"""Open a new Chrome session in the background using tempfile.

This module is designed to run in the background. I couldn't find a way
to open a Chrome session and watch until it shuts in pure Python, so I
used a simple C# (Windows) and Bash (macOS) script instead. 

This module opens the appropriate script, which stays open until the
Chrome session ends. When that happens, this module also exits, erasing
the temporary directory housing the browsing session.

Functions:
    main()
"""
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import common


def main():
    """Open a new Chrome session inside of a directory made using
    tempfile.TemporaryDirectory(). Wait until the Chrome session ends,
    then shut the directory, erasing it."""
    program_path = os.path.dirname(os.path.realpath(__file__))
    chrome_path = sys.argv[1]  # Inherited from temp_browser.main()
    with tempfile.TemporaryDirectory() as tempdir:
        new_profile_settings = common.load_pickle("new_profile_settings.txt")
        if new_profile_settings != "" and os.path.exists(new_profile_settings):
            try:
                shutil.copytree(new_profile_settings, tempdir, dirs_exist_ok=True)
            except shutil.Error:
                pass
        if platform.system() == "Windows":
            open_chrome_script = (f"{program_path}/scripts/C#/OpenTempChrome/OpenTempChrome/bin/"
                                  "Release/OpenTempChrome.exe")
            # Pass chrome_path and tempdir as args into the C# script.
            subprocess.Popen([open_chrome_script, chrome_path, tempdir],
                             creationflags=subprocess.CREATE_NO_WINDOW).wait()
        else:
            open_chrome_script = f"{program_path}/scripts/bash/open_temp_chrome.sh"
            # Pass chrome_path and tempdir as args into the Bash script.
            subprocess.Popen(["bash", open_chrome_script, chrome_path, tempdir]).wait()


if __name__ == "__main__":
    main()
