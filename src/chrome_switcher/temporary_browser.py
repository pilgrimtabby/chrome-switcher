"""Docstring"""
import os
import platform
import subprocess
import tempfile


def open_temporary_browser(chrome_path):
    """Docstring"""
    program_path = os.path.dirname(os.path.realpath(__file__))
    with tempfile.TemporaryDirectory() as tempdir:
        if platform.system() == "Windows":
            open_chrome_script = (f"{program_path}/scripts/c#/OpenTempChrome/OpenTempChrome/bin/"
                                  "Release/OpenTempChrome.exe")
            subprocess.Popen([open_chrome_script, chrome_path, tempdir]).wait()
        else:
            open_chrome_script = f"{program_path}/scripts/bash/launch_temp.sh"
            subprocess.Popen(["bash", open_chrome_script, chrome_path, tempdir]).wait()
