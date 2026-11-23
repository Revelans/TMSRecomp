#!/bin/sh
# Boot -> title -> new game (Normal) -> opening movie -> first 3D scene (elevator hall dialogue), at game speed N,
# then one shot. Start tms.exe first (from private/tms, with run_in_background):
#   : > control.txt && NX_SPEED=4 NX_CONTROL=control.txt NX_LOG=live.log ./build/tms.exe --data .
# then: sh ../../tools/drive/fast_to_3d.sh [N=4]   (~2.5 min at 4; ~6 min at 1). Send "speed 1" afterwards for
# real-time play. Speed changes timing only; nothing in the game is skipped.
speed=${1:-4}
d=$(dirname "$0")
until grep -q "movie: first frame" live.log 2>/dev/null; do sleep 1; done
# menu waits stay real time: loading (file reads, first-time shader translation) does not speed up
sh "$d/../drive.sh" "$d/newgame_1.txt"
sh "$d/../drive.sh" "$d/newgame_2.txt"
# the event hall follows ~2 min (real time) after the 4th movie decoder starts; the elevator dialogue ~40 s later at x4
until [ "$(grep -c 'movie::Decoder(' live.log)" -ge 4 ]; do sleep 1; done
sleep "$(awk "BEGIN { print 160 / $speed }")"
echo shot >> control.txt
