"""Delete unwanted Chrome desktop shortcut.

On Windows, a Chrome desktop shortcut is automatically generated when a
new Chrome session with default settings opens. This module deletes
that shortcut if it wasn't on the desktop before the session started.

This module runs in the background so the program doesn't appear to
hang up after it opens a new session. It can run for a maximum of about
30 seconds, though the new shortcut usually appears in 3-5 seconds
after the session starts. 30 seconds seems like an appropriate balance
between making sure the shortcut is deleted and preventing a looping
program from leaking memory in the background.

Functions:
    main()
"""
import os
import pathlib
import time
import common


def main():
    """Docstring"""
    new_profile_settings = common.load_pickle("new_profile_settings.txt")
    chrome_lnk_path = f"{os.path.join(os.path.expanduser('~'), 'Desktop')}/Google Chrome.lnk"
    # Run loop if the session is using default settings and the Chrome
    # shortcut doesn't yet exist on the desktop. This prevents a wanted
    # shortcut from being deleted.
    if new_profile_settings == "" and not os.path.exists(chrome_lnk_path):
        for _ in range(3000):
            # If the shortcut now exists, attempt to delete it.
            # Sometimes pathlib throws a PermissionError, claiming the
            # shortcut is in use by another program. I've found the
            # most reliable way to deal with this is to write over the
            # shortcut, wait about 5 seconds, and then attempt to
            # delete it again. This seems to consistently remove the
            # shortcut whereas other methods sometimes fail.
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
