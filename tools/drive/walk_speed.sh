#!/bin/sh
# Frame-rate check: load slot 2, log the player position, hold the stick north for HOLD ms (default 1000), log it again.
# The distance must match between the game's 30 fps and NX_GAME_INTERVAL=1 (60 fps).
# Run from private/tms with tms.exe NOT running. Usage: sh ../../tools/drive/walk_speed.sh [interval] [extra env...]
iv=$1; shift
: > control.txt
env ${iv:+NX_GAME_INTERVAL=$iv} "$@" NX_CONTROL=control.txt NX_LOG=live.log ./build/tms.exe --data . > /dev/null 2>&1 &
pid=$!
sh ../../tools/drive/load_slot.sh 2 1
sleep 2; echo pos >> control.txt; sleep 1
echo "ls 0 32767 ${HOLD:-1000}" >> control.txt; sleep $(( ${HOLD:-1000} / 1000 + 2 ))
echo pos >> control.txt; sleep 1
grep -E "player|pos|frame step" live.log | tail -6
kill $pid
