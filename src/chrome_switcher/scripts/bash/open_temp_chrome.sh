#!/usr/bin/env bash


"$1" --args --new-window --user-data-dir="$2" & CHROME_PID=$!
wait $CHROME_PID
