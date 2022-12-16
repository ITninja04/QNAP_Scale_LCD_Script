#!/bin/bash

SCRIPTPATH=$(realpath "$0")
SCRIPTDIR=$(dirname "$SCRIPTPATH")

cd "$SCRIPTDIR/qnapdisplay_truenas" && python start.py
