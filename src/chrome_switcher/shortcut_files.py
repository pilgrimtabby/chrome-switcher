"""Create shortcut files and place them with the persistent profiles.

Two shortcuts are created:
    1) open_profile.bat (Windows) | open_profile.app (macOS)
        A drag and drop program. If users drag and drop previously
        created persistent profile directories onto it, a new Chrome
        session with that profile will open.
    2) default_profile.bat (Windows) | default_profile (macOS)
        A double-click file. Opening it will open a new Chrome session
        with the user's default Chrome profile. Useful because if a non
        default Chrome session is already open, it is difficult to open
        a default session without closing the non-default session.

Templates for these files are in src/chrome-switcher/scripts. This
module copies them and replaces the variable "chrome_path" with the
user's actual path to Google Chrome, and (in the case of the macOS
files) compiles the files/ makes them executable.

Functions:
    main(from_menu)
    make_file_executable(file_path)
"""
import os
import platform
import stat
import subprocess
import time
import browser_path
import common
import settings


def main(from_menu=False):
    """Copy and prepare the two shortcut files.
    
    Args:
        from_menu (bool): Should be True if the function is called from
            main.main() and False otherwise. Doesn't impact the code,
            but displays different text depending on the value.
    """
    chrome_path = browser_path.get_chrome_path()
    header = common.box("Chrome Switcher | Shortcut file")
    if chrome_path is None:
        common.clear()
        print(f"{header}\n\nGoogle Chrome could not be found. Please verify your installation and "
              "try again.")
        time.sleep(3)
        return

    # Get profiles_directory from user if not yet defined
    program_path = os.path.dirname(os.path.realpath(__file__))
    profiles_directory = common.load_pickle("profiles_directory.txt")
    if not os.path.exists(profiles_directory):
        settings.change_profiles_directory_settings()
        profiles_directory = common.load_pickle("profiles_directory.txt")
        if not os.path.exists(profiles_directory):
            return

    if platform.system() == "Windows":
        # Copy both .bat files to profiles_directory and replace 
        # "chrome_path" with user's actual path to Chrome
        script_paths = [f"{program_path}/scripts/batch/open_profile.bat",
                        f"{program_path}/scripts/batch/default_profile.bat"]
        for script_path in script_paths:
            with open(script_path, "r", encoding="UTF-8") as file:
                script = file.read()

            script = script.replace("chrome_path", chrome_path)

            new_script_path = f"{profiles_directory}/{os.path.basename(script_path)}"
            with open(new_script_path, "w", encoding="UTF-8") as file:
                file.write(script)

        if from_menu:
            common.clear()
            print(f"{header}")
            input(f"\nGenerated shortcut file:\n{program_path}/scripts/batch/open_profile.bat"
                    "\n\n"
                    "To use this shortcut file, drag and drop Chrome profile folders onto "
                    "it.\n\n"
                    "Also generated a file that will open your default Chrome profile anytime:\n"
                    f"{profiles_directory}/default_profile.bat\n"
                    "Double click it to use it.\n\n"
                    "Press enter to return to the menu: ")
        else:
            input(f"\nGenerated shortcut file:\n{program_path}/scripts/batch/open_profile.bat"
                    "\n\nIf you want to use the Chrome profile you just made later on, drag and "
                    "drop it onto the shortcut file.\n\n"
                    "Also generated a file that will open your default Chrome profile anytime:\n"
                    f"{profiles_directory}/default_profile.bat\n"
                    "Double click it to use it.\n\n"
                    "Press enter to continue: ")

    # macOS
    else:
        # Copy open_profile.applescript into profiles_directory,
        # replace "chrome_path" with the user's Chrome path, and
        # compile open_profile.applescript into open_profile.app
        applescript_path = f"{program_path}/scripts/applescript/open_profile.applescript"
        with open(applescript_path, "r", encoding="UTF-8") as file:
            script = file.read()

        script = script.replace("chrome_path", chrome_path)

        new_script_path = f"{profiles_directory}/tmp.applescript"
        with open(new_script_path, "w", encoding="UTF-8") as file:
            file.write(script)

        compiled_app_path = f"{profiles_directory}/open_profile.app"
        subprocess.Popen(["osacompile", "-x", "-o", compiled_app_path, new_script_path],
                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).wait()

        # Inject custom icon into open_profile.app
        subprocess.Popen(["cp", "-f", f"{program_path}/scripts/applescript/droplet.icns",
                            f"{compiled_app_path}/Contents/Resources/droplet.icns"])

        # Delete profiles_dir/open_profile.applescript after compile
        os.remove(new_script_path)

        # Copy default_profile into profiles_directory, replace the
        # "chrome_path" variable with actual Chrome path, and make the
        # script executable
        default_profile_script_path = f"{program_path}/scripts/bash/default_profile"
        with open(default_profile_script_path, "r", encoding="UTF-8") as file:
            script = file.read()
        script = script.replace("chrome_path", chrome_path)

        new_script_path = f"{profiles_directory}/default_profile"
        with open(new_script_path, "w", encoding="UTF-8") as file:
            file.write(script)
        make_file_executable(new_script_path)

        if from_menu:
            common.clear()
            print(f"{header}")
            input(f"\nGenerated shortcut app:\n{compiled_app_path}\n\n"
                    "To use this shortcut app, drag and drop Chrome profile folders onto "
                    "it.\n\n"
                    "Also generated a file that will open your default Chrome profile anytime:\n"
                    f"{profiles_directory}/default_profile\n"
                    "Double click it to use it.\n\n"
                    "Press enter to return to the menu: ")
        else:
            input(f"\nGenerated shortcut app:\n{compiled_app_path}\n\n"
                    "If you want to use the Chrome profile you just made later on, drag and "
                    "drop it onto the shortcut file.\n\n"
                    "Also generated a file that will open your default Chrome profile anytime:\n"
                    f"{profiles_directory}/default_profile\n"
                    "Double click it to use it.\n\n"
                    "Press enter to continue: ")


def make_file_executable(file_path):
    """Allow the file at file_path to run as an exectable on macOS.

    Equivalent to running `chmod +x` in the shell.
    """
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
