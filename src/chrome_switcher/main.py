"""Display the GUI main menu.

Functions:
    main()
    exit_screen()
"""
import platform
import time

if platform.system() != "Windows":
    import chime

import advanced_cursor
import browsers
import common
import shortcut_files
import settings


def main():
    """Display the GUI main menu; prompt the user to choose an option."""
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
                opened = browsers.make_persistent_profile()
                if opened:
                    quit_menu = True  # End program if Chrome is opened

            elif choice == "Launch temporary browser":
                opened = browsers.make_temporary_profile()
                if opened:
                    quit_menu = True  # End program if Chrome is opened

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

    exit_screen()


def exit_screen():
    """Displays splash screen upon exit."""
    if platform.system() != "Windows":
        chime.theme("mario")
        chime.info()
    advanced_cursor.hide()
    common.clear()
    print("\n\n\n"
          "                 Come again soon! \n\n\n"
          "               ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇\n"
          "               ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⢿⡿⢿⣿⣿⣿⠃\n"
          "               ⣿⣿⣿⣿⣿⣿⣥⣄⣀⣀⠀⠀⠀⠀⠀⢰⣾⣿⣿⠏\n"
          "               ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣜⡻⠋\n"
          "               ⣿⣿⡿⣿⣿⣿⣿⠿⠿⠟⠛⠛⠛⠋⠉⠉⢉⡽⠃\n"
          "               ⠉⠛⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⡤⠚⠉\n"
          "               ⣿⠉⠛⢶⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⡇\n"
          "               ⠟⠃⠀⠀⠀⠈⠲⣴⣦⣤⣤⣤⣶⡾⠁\n\n")
    time.sleep(.5)
    common.clear()
    advanced_cursor.show()


if __name__ == "__main__":
    main()
