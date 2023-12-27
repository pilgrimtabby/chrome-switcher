"""Display GUI for settings menu.

Functions:
    main()
    change_profiles_directory_settings()
    get_unique_name(profile_name) -> str
    change_new_profile_settings()
"""
import os
import time
import common


def main():
    """Display settings menu."""
    menu_options = ["Profiles directory", "New profile settings", "Go back"]
    quit_menu = False
    while not quit_menu:
        common.clear()
        header = common.box("Chrome Switcher | Settings")

        print(f"{header}\n")
        for i, option in enumerate(menu_options):
            if option == "Go back":
                print("")
            print(f"{str(i + 1)}: {option}")

        user_input = input(f"\nChoose an option (1 - {len(menu_options)}): ")
        if user_input.isdigit() and 0 < int(user_input) <= len(menu_options):
            choice = menu_options[int(user_input) - 1]
            if choice == "Profiles directory":
                change_profiles_directory_settings()
            elif choice == "New profile settings":
                change_new_profile_settings()
            elif choice == "Go back":
                quit_menu = True
        else:
            print("Not a valid option! Please try again.")
            time.sleep(1)


def change_profiles_directory_settings():
    """Prompt user for directory for storing persistent profiles."""
    header = common.box("Chrome Switcher | Settings | Profiles location")
    profiles_directory = common.load_pickle("profiles_directory.txt")
    common.clear()
    print(f"{header}")

    # Dialog if a dir has already been chosen and exists
    if os.path.exists(profiles_directory):
        print(f"\nCurrent directory for newly generated persistent profiles:\n{profiles_directory}")
        user_choice = input("\nTo choose a new directory, press \"y\" (press enter to exit): "
                            ).lower()
        if user_choice != "y":
            return

    # Dialog regardless of whether a dir has already been chosen
    print("\nPlease select a directory for new Chrome profiles:")
    new_target_directory = common.get_file_path(file_type="dir")

    # Desktop is default if user cancels and no previous setting exists
    if new_target_directory == "" and not os.path.exists(profiles_directory):
        common.dump_pickle(os.path.join(os.path.expanduser("~"), "Desktop"),
                           "profiles_directory.txt")
        print(f"\nSet directory to {os.path.join(os.path.expanduser('~'), 'Desktop')}")
        time.sleep(1)

    # Pickle choice if it's a real path
    elif os.path.exists(new_target_directory):
        common.dump_pickle(new_target_directory, "profiles_directory.txt")
        common.clear()
        print(f"{header}\n\nSet directory to {new_target_directory}")
        time.sleep(1)


def change_new_profile_settings():
    """Allows user to choose a base profile directory that new profiles
    will inherit settings from.
    """
    header = common.box("Chrome Switcher | Settings | New profile settings")
    quit_menu = False
    while not quit_menu:
        new_profile_settings = common.load_pickle("new_profile_settings.txt")
        common.clear()
        print(f"{header}")
        if new_profile_settings == "":
            print("\nCurrent setting: default")
        else:
            print(f"\nCurrent setting: Inheret Chrome settings from:\n{new_profile_settings}")
        user_choice = input("\nThis setting determines whether new profiles, temporary and "
                            "persistent, are generated with Chrome's default settings "
                            "(\"default\") or whether they inherit settings, bookmarks, history, "
                            "extensions, etc. from an existing Chrome profile.\n\n"
                            "To inherit from an existing profile, select the profile folder of "
                            "the profile you want to inherit from. For instance, to inheret "
                            "settings, etc. from your default Chrome profile, press \"y\", then "
                            "navigate to:\n\n"
                            "Windows: %LOCALAPPDATA%\\Google\\Chrome\\User Data\n"
                            "Mac: ~/Library/Application Support/Google/Chrome/\n\n"
                            "Options:\n"
                            "Press \"y\" to choose a directory.\n"
                            "Press \"d\" to restore this setting to default.\n"
                            "Press enter to go back.\n"
                            "Your choice: ").lower()
        if user_choice == "y":
            common.clear()
            print(f"{header}\n\nSelect a new base directory:")
            new_base_directory = common.get_file_path(file_type="dir")
            if new_base_directory != "":
                common.dump_pickle(new_base_directory, "new_profile_settings.txt")
                common.clear()
                print(f"{header}\n\nNew profiles will inherit settings from:\n"
                      f"{new_base_directory}")
                time.sleep(2)
        elif user_choice == "d":
            common.dump_pickle("", "new_profile_settings.txt")
            common.clear()
            print(f"{header}\n\nSettings set to default. New profiles will be initiated with "
                  "default settings.")
            time.sleep(2)
        else:
            quit_menu = True
