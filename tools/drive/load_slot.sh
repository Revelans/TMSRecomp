#!/bin/sh
# Run from private/tms while tms.exe (started with NX_CONTROL=control.txt NX_LOG=live.log) boots: waits for the title
# movie, opens LOAD and loads slot N (default 2; the cursor starts on the newest slot), then waits for the map.
# Usage: sh ../../tools/drive/load_slot.sh [N] [speed]
n=${1:-2}; speed=${2:-1}
until grep -q "movie: first frame" live.log 2>/dev/null; do sleep 1; done
sleep 8; echo a >> control.txt; sleep 5
# measured: the cursor starts on slot 2 with saves in 1 and 2; move from there
i=2; while [ $i -lt "$n" ]; do echo down >> control.txt; sleep 0.5; i=$((i+1)); done
while [ $i -gt "$n" ]; do echo up >> control.txt; sleep 0.5; i=$((i-1)); done
echo a >> control.txt
sleep "$(awk "BEGIN { print 16 / $speed + 4 }")"
