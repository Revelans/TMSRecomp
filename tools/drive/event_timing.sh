#!/bin/sh
# Frame-rate check for scripted events: slot 2 -> north door -> d002_01 map load, then idle 20 s; the log (with run-time
# stamps) is copied to timing_<tag>.log. Compare script/flag line spacing between 30 fps and NX_GAME_INTERVAL=1.
# Run from private/tms with tms.exe NOT running. Usage: sh ../../tools/drive/event_timing.sh <tag> [interval] [extra env...]
tag=$1; iv=$2; shift 2 2>/dev/null || shift $#
: > control.txt
env ${iv:+NX_GAME_INTERVAL=$iv} "$@" NX_LOG_TIME=1 NX_CONTROL=control.txt NX_LOG=live.log ./build/tms.exe --data . > /dev/null 2>&1 &
pid=$!
timeout 120 sh ../../tools/drive/slot2_north.sh || echo "slot2_north did not reach d002_01"
sleep 20
kill $pid
cp live.log "timing_$tag.log"
