#!/bin/sh
# From private/tms: press A every 1.5 s until the player is back in the field ("pos" answers) or N presses (default 40).
n=${1:-40}; i=0
while [ $i -lt "$n" ]; do
  echo a >> control.txt; sleep 1.5; echo pos >> control.txt; sleep 0.3
  tail -c 300000 live.log | grep -a "\[pos\]" | tail -1 | grep -q "player" && { tail -c 300000 live.log | grep -a "\[pos\]" | tail -1; exit 0; }
  i=$((i+1))
done
echo "still not in the field after $n presses"; exit 1
