"""Get info necessary to create a persistent / temp Chrome profile.

Persistent:
    Always prompt user to enter profile name. Also prompt user to select
    directory for Chrome profiles if it hasn't been selected or if its path
    no longer exists.

Temporary:
    Prompt user to confirm, get the Chrome path, and launch
    temp_browser_helper.py in a separate process so it can run in the
    background and safely delete itself once the session ends.

Functions:
    make_persistent_profile() -> bool
    make_temporary_profile() -> bool
    get_profile_name() -> str | None
    get_unique_name(profile_name) -> str
    create_profile(profile_name)
    open_persistent_profile(profile_name) -> bool
"""
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


def make_persistent_profile():
    """Get the information necessary to create and start a new
    persistent Chrome profile / session.
    
    Returns:
        bool: False if--
            1) the user does not choose a profiles dir,
            2) the user enters a blank file name,
            3) the user declines to open a new Chrome session with the 
            created profile, or 
            4) open_browser() returns false because the chrome path 
            cannot be found.

            True if a profile is successfully created and opened.
    """
    # Get profiles directory
    profiles_directory = common.load_pickle("profiles_directory.txt")
    if not os.path.exists(profiles_directory):
        settings.change_profiles_directory_settings()
        profiles_directory = common.load_pickle("profiles_directory.txt")
        if not os.path.exists(profiles_directory):
            return False

    # Get profile name
    profile_name = get_profile_name()
    if profile_name is None:
        return False
    unique_profile_name = get_unique_name(profile_name)

    # Make profile and shortcut files (if they don't exist already)
    create_profile(unique_profile_name)
    if (not os.path.exists(f"{profiles_directory}/open_profile.bat")
        and not os.path.exists(f"{profiles_directory}/open_profile.app") or
        not os.path.exists(f"{profiles_directory}/default_profile.bat")
        and not os.path.exists(f"{profiles_directory}/default_profile")):
        shortcut_files.main()

    # Option to open the just-made profile in a new Chrome session
    header = common.box("Chrome Switcher | New profile | Open browser")
    common.clear()
    open_it = input(f"{header}\n\nStart a new session of Chrome now with this profile?\n"
                         "Press enter to open, or type \"n\" to go to the menu: ").lower()
    if open_it != "n":
        return open_persistent_profile(unique_profile_name)
    return False


def make_temporary_profile():
    """Gathers user information and otherwise prepares a temporary session.
    
    Returns:
        bool: False if--
            1) open_browser() returns false because the chrome path 
            cannot be found, or
            2) the user declines to actually open the session

            True if the temporary session is actually opened.
    """
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
                       "Type \"y\" to continue (press enter to go back): ").lower()
    if user_input != "y":
        return False

    print("\nOpening temporary browser...")

    # Open a temporary session by calling temp_browser_helper, passing
    # chrome_path as an argument. See temp_browser_helper.py's
    # documentation for details.
    if platform.system() == "Windows":
        subprocess.Popen([sys.executable, f"{program_path}/temp_browser_helper.py", chrome_path],
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
                         creationflags=subprocess.DETACHED_PROCESS)
        # See delete_lnk.py's documentation for details on this call.
        subprocess.Popen([sys.executable, f"{program_path}/delete_lnk.py"],
                          creationflags=subprocess.DETACHED_PROCESS)
    else:
        subprocess.Popen([sys.executable, f"{program_path}/temp_browser_helper.py", chrome_path],
                          stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
                          start_new_session=True)

    # Error message if the user specified a base dir to inherit from
    # in settings.change_new_profile_settings() and that dir couldn't
    # be found.
    time.sleep(1)
    new_profile_settings = common.load_pickle("new_profile_settings.txt")
    if new_profile_settings != "" and not os.path.exists(new_profile_settings):
        print("\nTried to inheret settings from the directory you chose as a base, but it could "
              "not be found. Using default Chrome settings instead.")
        time.sleep(5)

    # Warning that copying the base dir, if specified in
    # settings.change_new_profile_settings(), might take a minute.
    elif os.path.exists(new_profile_settings):
        print("\nInheriting settings from the directory you chose as a base.\nSit tight! "
              "Depending on your computer speed, it could take several minutes to copy the base "
              "profile and open the browsing session after this program exits.")
        time.sleep(10)

    return True


def get_profile_name():
    """Prompt user for name of new Chrome profile.
    
    Returns:
        profile_name (str | None): profile name, or None if
            len(profile_name) == 0.
    """
    header = common.box("Chrome Switcher | New profile | Profile name")
    common.clear()
    profile_name = input(f"{header}\n\nEnter a profile name (press enter to quit): ")
    if len(profile_name) > 0:
        return profile_name
    return None


def get_unique_name(profile_name):
    """Changes a name if such a file exists in a given directory
    (defined internally as target_directory).

    Args:
        profile_name (str): The name to be checked.

    Returns:
        new_profile_name (str): profile_name if such a file didn't
            already exist, or else a uniquely numbered version of
            profile_name.
    """
    target_directory = common.load_pickle("profiles_directory.txt")
    new_profile_name = profile_name
    suffix = 2
    while os.path.exists(f"{target_directory}/{new_profile_name}"):
        new_profile_name = f"{profile_name}-{suffix}"
        suffix += 1
    return new_profile_name


def create_profile(profile_name):
    """Create a directory with name profile_name in profiles_directory.
    
    Args:
        profile_name (str): The profile name
    """
    header = common.box("Chrome Switcher | New profile | Generating files")
    common.clear()
    print(f"{header}\n")

    # Make profiles_directory if it doesn't exist
    profiles_directory = common.load_pickle("profiles_directory.txt")
    if not os.path.exists(profiles_directory):
        os.mkdir(profiles_directory)

    # If a base dir hasn't been chosen in
    # settings.change_new_profile_settings(), or if one was chosen but
    # doesn't exist anymore, set used_default_instead = True so the
    # error message at the end of this function prints, and create the
    # new profile as an empty dir in profiles_directory.
    new_profile_settings = common.load_pickle("new_profile_settings.txt")
    used_default_instead = False
    if new_profile_settings == "":
        os.mkdir(f"{profiles_directory}/{profile_name}")
    elif new_profile_settings != "" and not os.path.exists(new_profile_settings):
        used_default_instead = True
        os.mkdir(f"{profiles_directory}/{profile_name}")

    # Use the base dir chosen in settings.change_new_profile_settings()
    # to make the new profile if one was specified and exists.
    else:
        # Sometimes shutil has a hard time copying files, but this
        # doesn't seem to matter, so I just ignore it.
        try:
            print(f"Copying base chrome profile to {profiles_directory}/{profile_name}\n"
                  "This may take a few moments...")
            shutil.copytree(new_profile_settings, f"{profiles_directory}/{profile_name}")
        except shutil.Error:
            pass

    # Error msg. if base dir was chosen in
    # settings.change_new_profile_settings() but doesn't exist.
    if used_default_instead:
        print("The Chrome profile you selected to act as a base for new profiles no longer "
              "exists, or could not be found. Default settings will be used instead.")
        time.sleep(2)
    print(f"New Chrome profile generated:\n{profiles_directory}/{profile_name}")
    time.sleep(1)


def open_persistent_profile(profile_name):
    """Open a new Chrome session with the just-made profile.

    The subprocess calls send stdout and stderr to devnull because
    otherwise text can continue to show up in the shell if left open.
    
    Args:
        profile_name (str): Name of the profile just generated.
    
    Returns:
        bool: True if the browser window opens (essentially, if
            chrome_path is not None), and False otherwise. This depends
            on the return value of browser_path.get_chrome_path().
    """
    chrome_path = browser_path.get_chrome_path()
    profiles_directory = common.load_pickle("profiles_directory.txt")
    if chrome_path is not None:
        if platform.system() == "Windows":
            program_path = os.path.dirname(os.path.realpath(__file__))
            # A call to Windows' cmd.exe. It looks like this:
            # path/to/chrome.exe chrome://newtab
            # --user-data-dir="path/to/new/profile".
            subprocess.Popen([chrome_path, "chrome://newtab",
                              f"--user-data-dir={profiles_directory}/{profile_name}"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            # See delete_lnk.py's docstring for details on this call.
            subprocess.Popen([sys.executable, f"{program_path}/delete_lnk.py"],
                              creationflags=subprocess.DETACHED_PROCESS)
        else:
            # A call to the default macOS shell. It looks like this:
            # path/to/chrome --args --user-data-dir="path/to/new/prof"
            # --new-window chrome://newtab
            # For some reason, --new-window is necessary on macOS but
            # not Windows.
            subprocess.Popen([chrome_path, "--args", f"--user-data-dir={profiles_directory}/"
                              f"{profile_name}", "--new-window", "chrome://newtab"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
    print("\nGoogle Chrome could not be found. Please verify your installation and try again.")
    time.sleep(2)
    return False
