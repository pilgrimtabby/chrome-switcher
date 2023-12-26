"""Docstring"""
import os
import platform
import subprocess
import time
import browser_path
import common
import settings


def main(from_menu=False):
    """Docstring"""
    chrome_path = browser_path.get_chrome_path()
    header = common.box("Chrome Switcher | Shortcut file")
    if chrome_path is None:
        common.clear()
        print(f"{header}\n\nGoogle Chrome could not be found. Please verify your installation and "
              "try again.")
        time.sleep(3)
    else:
        program_path = os.path.dirname(os.path.realpath(__file__))
        profiles_directory = common.load_pickle("profiles_directory.txt")
        if not os.path.exists(profiles_directory):
            settings.change_profiles_directory_settings()
            profiles_directory = common.load_pickle("profiles_directory.txt")
            if not os.path.exists(profiles_directory):
                return

        if platform.system() == "Windows":
            script_path = f"{program_path}/scripts/batch/open_profile.bat"
            with open(script_path, "r", encoding="UTF-8") as file:
                script = file.read()
            script = script.replace("chrome_path", chrome_path)

            new_script_path = f"{profiles_directory}/open_profile.bat"
            with open(new_script_path, "w", encoding="UTF-8") as file:
                file.write(script)

            if from_menu:
                common.clear()
                print(f"{header}")
                input(f"\nGenerated shortcut file:\n{new_script_path}\n\n"
                       "To use this shortcut file, drag and drop Chrome profile folders onto "
                       "it.\n\n"
                       "Press enter to return to the menu: ")
            else:
                input(f"\nGenerated shortcut file:\n{new_script_path}\n\n"
                       "If you want to use the Chrome profile you just made later on, drag and "
                       "drop it onto the shortcut file.\n\n"
                       "Press enter to continue: ")

        else:
            script_path = f"{program_path}/scripts/applescript/open_profile.applescript"
            with open(script_path, "r", encoding="UTF-8") as file:
                script = file.read()
            script = script.replace("chrome_path", chrome_path)

            new_script_path = f"{profiles_directory}/tmp.applescript"
            with open(new_script_path, "w", encoding="UTF-8") as file:
                file.write(script)

            compiled_app_path = f"{profiles_directory}/open_profile.app"
            subprocess.Popen(["osacompile", "-x", "-o", compiled_app_path, new_script_path],
                             stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).wait()
            subprocess.Popen(["cp", "-f", f"{program_path}/scripts/applescript/droplet.icns",
                              f"{compiled_app_path}/Contents/Resources/droplet.icns"])
            os.remove(new_script_path)

            if from_menu:
                common.clear()
                print(f"{header}")
                input(f"\nGenerated shortcut app:\n{compiled_app_path}\n\n"
                       "To use this shortcut app, drag and drop Chrome profile folders onto "
                       "it.\n\n"
                       "Press enter to return to the menu: ")
            else:
                input(f"\nGenerated shortcut app:\n{compiled_app_path}\n\n"
                       "If you want to use the Chrome profile you just made later on, drag and "
                       "drop it onto the shortcut file.\n\n"
                       "Press enter to continue: ")
