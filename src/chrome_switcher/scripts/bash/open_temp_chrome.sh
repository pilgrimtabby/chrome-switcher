#!/usr/bin/env bash

# Open Chrome in a temporary session.
#
# Args:
# $1 (str): Absolute path to Google Chrome.
# $2 (str): Absolute path to user-data-dir. For this script's use case,
# absolute path to the tempfile.TemporaryDirectory() opened by Python.


"$1" --args --new-window --user-data-dir="$2" & CHROME_PID=$!
wait $CHROME_PID
