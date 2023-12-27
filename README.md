# About

Create new Google Chrome sessions, persistent and temporary, separate from your default Chrome profiles. 

New sessions start with default Chrome settings by default, but it is possible to base new sessions off of others. Some possibilities include:

- Browsing in a temporary session that inherits bookmarks, cookies, and extensions from your default Chrome profile without impacting it or leaving a history

- Browsing in persistent sessions that can be accessed repeatedly, each with their own bookmarks, history, extensions, and cookies (no more signing in and out of different profiles on certain websites!)

# Usage

After [installation](#installation), run `$ cswitch` to open the GUI interface.

A command line interface will be added in the future.

# Options

### New persistent session

Create and open a new persistent session. 

Choosing this option automatically generates a shortcut file in the same directory as the new session. To use the shortcut file, drag and drop persistent session directories onto it, and that session will open.

Choosing this option also automatically generates a default profile shortcut in the same directory (double click it to open it). If you're running a separate session from the default,  use this to open your default profile without being forced to exit the other session.

### New temporary session

Create and open a new temporary session.

On Windows, this session's data is deleted when you close the last remaining tab of the session. On macOS, it's deleted when you quit that session of Chrome (`cmd+Q`). If your computer shuts off unexpectedly (e.g. dead battery), there is a small chance some data could remain.

### Regenerate shortcut files

Remakes the shortcut files mentioned [above](#new-persistent-session) if they get lost or damaged.

# Settings

As mentioned [above](#about), you can select an existing Chrome session directory that new sessions will inherit from. For instance, you might want to inheret from the default session directory. On most computers, that directory is at:

Windows: `%LOCALAPPDATA%\\Google\\Chrome\\User Data`

macOS: `~/Library/Application Support/Google/Chrome`

Start new sessions with this base (or another) in the settings menu by following the GUI and selecting a folder.

NOTE: Doing this may slow down new session generation as files have to be copied over.

# Installation

Python is required. This program was tested on Python 3.11 but should work on all maintained Python versions.

### Windows and macOS

#### Option 1: pip

The easiest way to install this program is using pip: `$ pip install chrome-switcher`

#### Option 2: download and run

Download the source code and run main.py: `$ python3 /path/to/main.py`

### Linux

This program has not been tested on Linux.
