(*
 * Get path to Google Chrome if its not open, even if its been renamed or moved from /Applications.
 * 
 * First, open Chrome using its application id. Wait until it opens (wait about 10 seconds before giving up), 
 * then immediately tell the front window to minimize (to keep annoyance to the user to a minimum). Get the
 * POSIX path of the application id, then quit Chrome and return the path.
 *)

tell application id "com.google.Chrome" to activate

-- Wait until Chrome is running, in front, and has a window open
repeat 4000 times -- try for roughly 10 seconds
	try
		if application id "com.google.Chrome" is running then
			if frontmost of application id "com.google.Chrome" then
				if window 1 of application id "com.google.Chrome" exists then
					exit repeat
				end if
			end if
		end if
		-- ignore errors (if this block doesnt work, it doesnt matter too much, because it is what helps the
		-- minimize code work, and it will only run for 4000 tries anyway)		
	end try
end repeat
-- Minimize window
tell application "System Events"
	set minimized to false
	repeat while not minimized
		tell window 1 of process "Google Chrome" to set value of attribute "AXMinimized" to true
		set minimized to (value of attribute "AXMinimized" of window 1 of process "Google Chrome")
	end repeat
end tell

set chrome_path to POSIX path of (path to application id "com.google.Chrome")
tell application id "com.google.Chrome" to quit
return chrome_path
