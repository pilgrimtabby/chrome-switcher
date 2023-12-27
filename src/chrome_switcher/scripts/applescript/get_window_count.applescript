(*
 * Returns number of Google Chrome windows currently open in the first session opened (usually there is only 
 * one open session).
 *)

if application id "com.google.Chrome" is running then tell application id "com.google.Chrome"
	set window_count to the index of windows
	return (number of items in window_count)
end tell
