"""Docstring"""
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import common


def main():
    """Docstring"""
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
            open_chrome_script = (f"{program_path}/scripts/c#/OpenTempChrome/OpenTempChrome/bin/"
                                  "Release/OpenTempChrome.exe")
            subprocess.Popen([open_chrome_script, chrome_path, tempdir],
                             creationflags=subprocess.CREATE_NO_WINDOW).wait()
        else:
            open_chrome_script = f"{program_path}/scripts/bash/open_temp_chrome.sh"
            subprocess.Popen(["bash", open_chrome_script, chrome_path, tempdir]).wait()


if __name__ == "__main__":
    main()
