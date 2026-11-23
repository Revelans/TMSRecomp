#!/bin/sh
# From private/tms while tms.exe boots (NX_CONTROL=control.txt NX_LOG=live.log): load slot 2 (Observatory Inside,
# after the first battle), walk to the north door and go through it -> I. Daitama Lower Lv (d002_01, west branch).
# Usage: sh ../../tools/drive/slot2_north.sh [speed]   (stick y +32767 = up on screen = north here)
sh ../../tools/drive/load_slot.sh 2 "${1:-1}"
sleep 2; echo "ls 0 32767 1500" >> control.txt; sleep 3
echo a >> control.txt
until grep -q "d002_01ret_battle" live.log; do sleep 1; done; sleep 2
