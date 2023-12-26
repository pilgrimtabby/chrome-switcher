"""Docstring"""
import platform
import time
import common
import persistent_browser
import shortcut_files
import temp_browser
import settings


def main():
    """Docstring"""
    header = common.box("Chrome Switcher")
    if platform.system() == "Windows":
        menu_options = ["Create persistent profile", "Launch temporary browser", "Regenerate "
                        "shortcut files", "Settings", "Quit"]
    else:
        menu_options = ["Create persistent profile", "Launch temporary browser", "Regenerate "
                        "shortcut app and file", "Settings", "Quit"]
    quit_menu = False
    while not quit_menu:
        common.clear()
        print(f"{header}\n\nWelcome to Chrome Switcher!\n")
        for i, option in enumerate(menu_options):
            if option == "Quit":
                print("")
            print(f"{str(i + 1)}: {option}")

        user_input = input(f"\nChoose an option (1 - {len(menu_options)}): ")
        if user_input.isdigit() and 0 < int(user_input) <= len(menu_options):
            choice = menu_options[int(user_input) - 1]

            if choice == "Create persistent profile":
                opened = persistent_browser.main()
                if opened:
                    quit_menu = True

            elif choice == "Launch temporary browser":
                opened = temp_browser.main()
                if opened:
                    quit_menu = True

            elif (choice == "Regenerate shortcut files"
                  or choice == "Regenerate shortcut app and file"):
                shortcut_files.main(from_menu=True)

            elif choice == "Settings":
                settings.main()

            elif choice == "Quit":
                quit_menu = True

        else:
            print("Not a valid option! Please try again.")
            time.sleep(1)

    common.exit_screen()


if __name__ == "__main__":
    main()
