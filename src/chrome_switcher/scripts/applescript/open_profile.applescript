(*
 * Open Google Chrome with user-data-dir `theDroppedItem`, or with default profile.
 *
 * Drag-and-drop script. After `chrome-path` is replaced with the path to the Chrome executable
 * by shortcut_file.py, this script is compiled into a .scpt file and bundled with
 * open_profile.app. If the user drops a Chrome profile folder on the app (or any folder,
 * really), it will open Chrome with that folder as the user data directory.
 *
 * In addition, if this app is double-clicked, it will open Chrome with the default profile.
 *
 * Args:
 * theDroppedItem (str): The absolute path to the item dropped onto this script after compilation.
 *)

on open theDroppedItem
	-- Make sure dragged and dropped item is a folder
	tell application "Finder"
		set isFolder to folder (theDroppedItem as string) exists
	end tell
	
	-- Use the dropped folder's name as the parameter for user-data-dir
	if isFolder = true then
		set fileName to (the POSIX path of theDroppedItem)
		do shell script "'chrome_path' --args --user-data-dir=" & quoted form of fileName & " --new-window 'chrome://newtab' >/dev/null 2>&1 &"
		quit
	end if
	quit
end open

on run
	do shell script "'chrome_path' --args --user-data-dir='' --new-window 'chrome://newtab' >/dev/null 2>&1 &"
end run
