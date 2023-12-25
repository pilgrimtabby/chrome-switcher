"""Docstring"""
import os
import platform
import subprocess
import sys
import tempfile


def main():
    """Docstring"""
    program_path = os.path.dirname(os.path.realpath(__file__))
    chrome_path = sys.argv[1]  # Inherited from temp_browser.main()
    with tempfile.TemporaryDirectory() as tempdir:
        if platform.system() == "Windows":
            open_chrome_script = (f"{program_path}/scripts/c#/OpenTempChrome/OpenTempChrome/bin/"
                                  "Release/OpenTempChrome.exe")
            subprocess.Popen([open_chrome_script, chrome_path, tempdir]).wait()
        else:
            open_chrome_script = f"{program_path}/scripts/bash/launch_temp.sh"
            subprocess.Popen(["bash", open_chrome_script, chrome_path, tempdir]).wait()


if __name__ == "__main__":
    main()
