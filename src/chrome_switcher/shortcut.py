"""Create shortcut file / app and place it with the persistent profiles.

The shortcut file (open_profile.bat / open_profile.app) performs two
functions:

1) It is a drag and drop program. If users drag and drop previously
created persistent profile directories onto it, a new Chrome session 
with that profile will open.

2) If users double click it, it will open a new Chrome session with the
user's default Chrome profile. This matters because if a non default
Chrome session is already open, it can be difficult to open a default
session without closing the non-default session.

Templates for these files are in src/chrome-switcher/scripts. This
module copies them and replaces the variable "chrome_path" with the
user's actual path to Google Chrome, and (in the case of the macOS
app) compiles the file and codesigns it.

Functions:
    main(from_menu)
    make_file_executable(file_path)
"""
import os
import platform
import subprocess
import time
import browser_path
import common
import settings


def main(from_menu=False):
    """Create the shortcut file (Windows) / app (macOS).
    
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
        # Copy the .bat file to profiles_directory and replace
        # "chrome_path" with user's actual path to Chrome.
        script_path = f"{program_path}/scripts/batch/open_profile.bat"
        with open(script_path, "r", encoding="UTF-8") as file:
            script = file.read()

        script = script.replace("chrome_path", chrome_path)

        new_script_path = f"{profiles_directory}/{os.path.basename(script_path)}"
        with open(new_script_path, "w", encoding="UTF-8") as file:
            file.write(script)

        if from_menu:
            common.clear()
            print(f"{header}")
            input(f"\nGenerated shortcut file:\n{new_script_path}"
                    "\n\n"
                    "To use this shortcut file, drag and drop Chrome profile folders onto "
                    "it.\n"
                    "You can also double-click it to open your default Chrome profile anytime.\n\n"
                    "Press enter to return to the menu: ")
        else:
            input(f"\nGenerated shortcut file:\n{new_script_path}"
                    "\n\nIf you want to use the Chrome profile you just made later on, drag and "
                    "drop it onto the shortcut file.\n"
                    "You can also double-click the shortcut file at any time to open your default "
                    "Chrome profile.\n\n"
                    "Press enter to continue: ")

    # macOS
    else:
        # Copy open_profile.applescript to a temp file with
        # "chrome_path" replaced with the user's Chrome path. Then
        # compile open_profile.applescript into open_profile.app
        applescript_path = f"{program_path}/scripts/applescript/open_profile.applescript"
        compiled_app_path = f"{profiles_directory}/open_profile.app"
        with open(applescript_path, "r", encoding="UTF-8") as file:
            script = file.read().replace("chrome_path", chrome_path)

        with open(f"{program_path}/scripts/applescript/tmp.txt", "w", encoding="UTF-8") as file:
            file.write(script)

        subprocess.Popen(["osacompile", "-x", "-o", compiled_app_path, file.name],
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).wait()
        os.remove(file.name)

        # Inject custom icon into open_profile.app
        subprocess.Popen(["cp", "-f", f"{program_path}/scripts/applescript/droplet.icns",
                            f"{compiled_app_path}/Contents/Resources/droplet.icns"])

        # Overwrite Info.plist so that app doesn't appear in dock.
        # Also stops the app from asking permission to access the
        # directory the profile is in, which is good because it doesn't
        # need access anyway.
        with open(f"{compiled_app_path}/Contents/Info.plist", "r", encoding="UTF-8") as file:
            contents = file.readlines()
        contents.insert(4, "\t<key>LSBackgroundOnly</key>\n")
        contents.insert(5, "\t<true/>\n")
        with open(f"{compiled_app_path}/Contents/Info.plist", "w", encoding="UTF-8") as file:
            file.writelines(contents)

        if from_menu:
            common.clear()
            print(f"{header}")
            input(f"\nGenerated shortcut app:\n{compiled_app_path}\n\n"
                    "To use this shortcut app, drag and drop Chrome profile folders onto "
                    "it.\n"
                    "You can also double-click it to open your default Chrome profile anytime.\n\n"
                    "Press enter to return to the menu: ")
        else:
            input(f"\nGenerated shortcut app:\n{compiled_app_path}\n\n"
                    "If you want to use the Chrome profile you just made later on, drag and "
                    "drop it onto the shortcut app.\n"
                    "You can also double-click the shortcut app at any time to open your default "
                    "Chrome profile.\n\n"
                    "Press enter to continue: ")
