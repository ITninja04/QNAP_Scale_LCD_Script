#!/bin/bash

SCRIPTPATH=$(realpath "$0")
SCRIPTDIR=$(dirname "$SCRIPTPATH")

PID_PATH="/var/run/qnapdisplay_truenas.pid"
EXE_PATH="$SCRIPTDIR/launcher.sh"

if [ -f "$PID_PATH" ];
then
        echo "Killing Found Process..."
        kill $(cat "$PID_PATH")
        rm "$PID_PATH"
fi

nohup "$EXE_PATH" &
echo $! > "$PID_PATH"
