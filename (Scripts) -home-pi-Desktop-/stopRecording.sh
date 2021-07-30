#!/bin/bash

# (Stop Recording Script Process ID)
parserProcessID=$(pgrep -f record_one_channel.py)
kill -9 ${parserProcessID}

# (Start LED ReSpeaker Process ID)
parserProcessID=$(pgrep -f pixels_recording.py)
kill -9 ${parserProcessID}

# (Stop LED ReSpeaker Process ID)
parserProcessID=$(pgrep -f pixels_stop.py)
kill -9 ${parserProcessID}




