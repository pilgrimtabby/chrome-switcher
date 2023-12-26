"""Docstring"""
import os
import pathlib
import time
import common


def main():
    """Docstring"""
    new_profile_settings = common.load_pickle("new_profile_settings.txt")
    chrome_lnk_path = f"{os.path.join(os.path.expanduser('~'), 'Desktop')}/Google Chrome.lnk"
    if new_profile_settings == "" and not os.path.exists(chrome_lnk_path):
        for _ in range(3000):
            if os.path.exists(chrome_lnk_path):
                try:
                    pathlib.Path.unlink(chrome_lnk_path)
                    break
                except PermissionError:
                    while not os.path.exists(chrome_lnk_path):
                        dummy = open(chrome_lnk_path, "w")
                        dummy.close()
                    time.sleep(5)
                    pathlib.Path.unlink(chrome_lnk_path)
                    break
            time.sleep(0.01)


if __name__ == "__main__":
    main()
