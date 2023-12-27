(*
 * Brings the Terminal window with the name passed into this program from the command line to the front.
 *
 * Args:
 *     item 1 of argv (str): The name of the Terminal window you want to bring to the front.
 *)

on run argv
	tell application "Terminal" to set index of (window (quoted form of (item 1 of argv))) to 1
end run
