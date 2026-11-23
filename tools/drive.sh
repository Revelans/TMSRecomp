#!/bin/sh
# Feed a scripted input sequence to a running tms.exe started with NX_CONTROL=control.txt (run from private/tms).
# Usage: sh ../../tools/drive.sh <script> [speed]   script lines: "<button|shot|...> [seconds to wait after]",
# or "<command with arguments> ; <seconds>" (e.g. "ls 0 32767 2000 ; 1"), "#" comments. With a speed (game started
# with NX_SPEED=n or sent "speed n"), waits are divided by it.
# Example scripts: tools/drive/*.txt
speed=${2:-1}
while IFS= read -r line; do
    case "$line" in ""|\#*) continue ;; esac
    case "$line" in
        *" ; "*) cmd=${line% ; *}; wait=${line##* ; } ;;
        *) cmd=${line%% *}; wait=${line#"$cmd"}; wait=${wait# } ;;
    esac
    [ "$cmd" = wait ] || echo "$cmd" >> control.txt
    sleep "$(awk "BEGIN { print ${wait:-2} / $speed }")"
done < "$1"
