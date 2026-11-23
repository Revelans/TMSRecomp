# TMSRecomp notes

Static recompilation of Tokyo Mirage Sessions #FE Encore (Switch) to a native Windows program.

## PORTABILITY RULE (user 2026-11-10, firm): "This must not only work on my machine." Players have every kind of GPU/CPU (NVIDIA, AMD, Intel, old and new, low VRAM). The point of a recomp port is that EVERYONE can play: no low fps, no crash, no stutter, smooth and optimised. Several other ports (GOW3, Gravity Rush 1/2, Drakengard 3, MediEvil, Crash NF, Bloodborne) are stable and good; we must not ship a bad recomp. Every feature needs a capability check + safe fallback (vendor-specific paths like DLSS/NGX optional), sane defaults for weak PCs, no hard dependency on the user's own setup (drivers, installed runtimes, paths, caches).
## RESUME HERE: v0.1.0-beta PUBLISHED 2026-11-24 at github.com/godofknife/TMSRecomp (branch `public` = the pushed history, noreply identity; never push this history). Read "Milestone 5, session 102" at the END first (2026-11-24: Overworld costume setting field_costume (verified slot 20: field / battle / back), Hard difficulty formula from the code, all_difficulties unlock + launcher rows; NEXT: user playtest, more v0.1.1 fixes, then publish v0.1.1 per "v0.1.1 queue").
## Previous RESUME: v0.1.0-beta PUBLISHED 2026-11-24 at github.com/godofknife/TMSRecomp (branch `public` = the one pushed commit, noreply 7660956+godofknife@users.noreply.github.com; push future releases from a commit on top of `public`, never this history). Read "Milestone 5, session 101" at the END first (2026-11-23 evening: user playtest OK except a RAM leak, 51 GB private after ~40 battles at 4K; fixed: shared descriptor-set / pipeline layouts, e858815; NEXT: user re-check of RAM, then GitHub upload).
## Previous RESUME: read "Milestone 5, session 100" at the END first (2026-11-23 overnight: fresh-ZIP NSP setup OK, reveal-map retry fix, crash batch 4x676 s 0 crashes; optimisation measured after the encode: GPU-bound at the Shibuya spot, no safe change; ALL DONE; NEXT: user playtest + GitHub upload). Before that: session 99 (2026-11-23, user asleep: DLSS model setting, VRR mode, TMS icon + launcher picture from the player's own game, reveal-map setting, no-mod check; ALL DONE + regression OK; NEXT: user playtest, then GitHub upload (private/RELEASE_GITHUB.md)).
## Previous RESUME: read "Milestone 5, session 98" at the END first (2026-11-22, launcher Guide page + one-click installs, P5R key dropped (custom_bgm_key); NEXT: user playtest of the release ZIP, then fresh-history GitHub upload (private/RELEASE_GITHUB.md)).
## Previous RESUME: read "Milestone 5, session 97" at the END first (2026-11-22, release check: fresh-ZIP setup + replay OK, game icon removed from release exes, legal audit, GitHub guide private/RELEASE_GITHUB.md; NEXT: user decisions: account name, history, keys mode; merge OK).
## Previous RESUME: read "Milestone 5, session 96" at the END first (2026-11-21/22, with user; branch perf/lows-1121 from feat/moviehd-1121: periodic 27 ms hitch every ~6 s FIXED (diagnostic guest VirtualQuery walk under g_lock), measured: Shibuya 1% low 88-103 -> 107-123, 60 fps cap 1 late vsync / 10 s -> 0; part 2: DLSS live mode switch device lost FIXED (98 switches 0 faults); camp menu flower flicker FIXED (4K movie image per address reused at another size); NEXT: user playtest + merge OK of settings-items / moviehd / lows branches).
## Previous RESUME: read "Milestone 5, session 95" at the END first (2026-11-21 scheduled run, branch feat/moviehd-1121: story + uncensored-mod movies in 4K DONE (MovieHD ZIP), 4K key collision FIXED, weak-PC defaults, 5 shader misses FIXED (0 misses on a scan-only cache), B on Apply dialog FIXED; NEXT: user playtest + merge OK).
## Previous RESUME: read "Milestone 5, session 94" at the END first (2026-11-21: story movie 4K batch running, Shibuya cars off-road = yaw glide read back as heading FIXED + measured (warp undo too), uncommitted; NEXT: user test + commit OK). Before that: "Milestone 5, session 93" at the END first (2026-11-21, s92 merged to master by user OK; branch feat/settings-items-1121: PC 3/4 row 10 filled, PC 4/4 empty slider rows drawn as blank rows (3 new hooks, re-lift), setting item_max99 (consumables stock 99), story movie 4K = user decision (~4 h batch, ~2.3 GB); NEXT: user playtest + merge OK)
## Previous RESUME: read "Milestone 5, session 92" at the END first (2026-11-21, same branch fix/help-text-exp-1120: USER playtest of s91: random-encounter retry works; dungeon music under the retry box FIXED (our SE call played BGM index 0), field KO mark vanishing with DLSS / FSR 3 FIXED (depth twins synced), new setting ko_revive (1 HP after won / escaped battles); NEXT: user playtest + merge OK)
## Previous RESUME: read "Milestone 5, session 91" at the END first (2026-11-20, s90 merged to master by user OK; branch fix/help-text-exp-1120: skill help fits the battle HELP bar, new Sub Cast EXP + EXP level-gap settings (native PC 4/4 page), battle retry after a wipe (setting battle_retry); NEXT: user playtest + merge OK), then s90
## Previous RESUME: read "Milestone 5, session 90" at the END first (2026-11-20, branch fix/unity-prime-movie-1120 from master (s89 merged): uncensored-mod Prime movies m06/m07/m12 FIXED, Unity performance timeline drift FIXED, Radiant Unity cast smoothing FIXED, all measured; NEXT: user playtest + merge OK), then s89
## Previous RESUME: read "Milestone 5, session 89" at the END first (2026-11-20, branch fix/turn-end-cross-1120: Tsubasa turn in m1029_01 at 240 FIXED + measured), then s88
## Previous RESUME: read "Milestone 5, session 88" at the END first (2026-11-18; merged to master; then branch feat/cli-set-portable-shaderc: --set flag + self-contained shaderc + REFERENCE release basics; before that: SMT3 Fiend custom track noise FIXED (keyed frames, header flag 0), skill help shows ailment % (Poison Skewer 50%); NEXT: user playtest + merge OK), then s87
## Previous RESUME: read "Milestone 5, session 87" at the END first (2026-11-17 14:10-, branch fix/s86-report-1117: item 6 verified (black card shards = item 5 twin fix; Carnage Form white measured same at 30 / 240), button-atlas hitch fixed (title 147 ms, battle 86 ms), RAM growth analysed = NVIDIA compiler heap, no fix; NEXT: user playtest + merge OK), then s86, s85
## Previous RESUME: read "Milestone 5, session 86" at the END first (2026-11-17 ~09:20-, branch fix/s86-report-1117 from fix/live-upscale-1116: user report 11-17 items 2-5 FIXED + measured (giant dress flail, black battle-start at 4K + DLSS, 1.2 s title freeze, target flash 8x fast), item 1 answered (Screen scaler row), item 6 analysed (no bug found: swimwear = costume set); NEXT: see s86 "Next"; scheduled task tms-recomp-s86-1411 continues), then s85
## Previous RESUME: read "Milestone 5, session 85" at the END first (2026-11-16, branch fix/live-upscale-1116: command lists recycled + handle leak fixed, res auto for weak PCs, pipelines + shader modules shared by content (battle mash RAM growth 1916 -> 1114 MB, plateaus), NX_MEM_REGIONS, walker / car yaw glide; NEXT: user OK to merge, then target highlight rig, fern (user check), OPEN LIST), then s84
## Previous RESUME: read "Milestone 5, session 84" at the END first (2026-11-16 ~10:40, branch fix/live-upscale-1116 from perf/cpu-lows-1115: user "fps regression 80-90" = their start setting fsr3_quality 0 (DLAA at native 4K) + mode read only at start; FSR 3 / DLSS mode now LIVE, MSAA copies freed (sample change / image death), empty VRAM blocks returned; NEXT: 1% low whole-process stalls, weak-PC defaults, open bugs; merge both branches to master after user OK), then s83
## Previous RESUME: read "Milestone 5, session 83" at the END first (2026-11-16, branch perf/cpu-lows-1115: "Vulkan: r failed (-4)" = s83 no-wait EXPERIMENT only (reverted, not in any build); clock thread sleeps at fps 0 / > 60; job-worker pause measured = no gain, dropped; 1% low still OPEN; NEXT: user OK to merge, then 1% low lead (whole-process stalls)), then s82
## Previous RESUME: read "Milestone 5, session 82" at the END first (2026-11-16 ~04:30, branch perf/cpu-lows-1115: render thread TESTED (Shibuya spot 80-102 -> 115-135 fps, user 130-152 at 4K), 1% low NOT improved; DLSS answered (works; mode needs a restart); NEXT: 1% low, merge to master after user OK), then s81
## Previous RESUME: read "Milestone 5, session 81" at the END first (2026-11-15, branch perf/cpu-lows-1115, STOPPED BY USAGE LIMIT: render thread for draw replay BUILT BUT NOT RUN ONCE; test before anything else), then s80
## Previous RESUME: read "Milestone 5, session 80" at the END first (2026-11-14 ~18:05, branch perf/walk-hitch-1114 from perf/msaa-prewarm-1114: cache-hit pipelines created inline (walking spike frames ~-15%), NX_HITCH_MS; NEXT: user test, then merge the three perf branches), then s79
## Previous RESUME: read "Milestone 5, session 79" at the END first (2026-11-14 ~12:05, branch perf/msaa-prewarm-1114: MSAA pipelines now prewarmed (recipes keep sample count), walking 4K 8x measured (-20% vs off, no MSAA-only spikes), crash batch 0 crashes; NEXT: user test, then merge both perf branches), then s78
## Previous RESUME: read "Milestone 5, session 78" at the END first (2026-11-14 ~08:15-, branch perf/msaa-resolve-1114: MSAA 8x resolve fix (Shibuya 4K 8x 57-60 -> 84-90 fps), L1 fast travel to visited shops, vehicles merged to master; NEXT: see s78 "Next"), then s77
## Previous RESUME: read "Milestone 5, session 77" at the END first (2026-11-14 ~04:30, branch feat/tokyo-map-shortcut: F1 / L3+R3 menu "Open Tokyo Map" in town free roam (indoors too; streets already have the game's X), dungeons excluded, verified; NEXT: user test of the menu row, async replay or CPU items), then s76
## Previous RESUME: read "Milestone 5, session 76" at the END first (2026-11-14 ~03:00, branch fix/shibuya-cars-fps: MSAA real 8x fixed + shadow maps excluded + VRAM cap, measured (4K Shibuya off 112 / 4x 97 / 8x 69 fps); fast travel ANALYZED (game's Tokyo Map already has Shibuya shop points; proposal L3+R3 opens it), USER DECISION; NEXT: async replay or CPU items), then s75
## Previous RESUME: read "Milestone 5, session 75" at the END first (2026-11-14 ~01:30, branch fix/shibuya-cars-fps: cars shake FIXED, Shibuya 4K MSAA ping-pong FIXED (+20% fps, GPU -43%), MSAA 8x found not applied to main scene (user decision); NEXT: crash batch + ZIP, fast-travel analysis, async replay), then s74
## Previous RESUME: read "Milestone 5, session 74" at the END first (2026-11-13 ~21:30, branch fix/movie-hle-leak: Shibuya crash FIXED (movie decoder leak filled the HLE region), Shibuya cars + crowd at Switch speed and smooth FIXED + measured; OPEN: enemy target highlight (item 2, rig not deterministic), Shibuya / crowd CPU (items 1+4); NEXT: user test in Shibuya at 240), then s73, s72
## Previous RESUME: read "Milestone 5, session 73" at the END first (2026-11-13 19:00: write-watch per-pool idea measured = no gain, reverted; later Bloom Palace Unity screens (task 0x38fe58) gated like Carnage Unity, build only; crash batch 0 crashes, saves intact; NEXT: user test at 240), then s72, s71
## Previous RESUME: read "Milestone 5, session 72" at the END first (2026-11-13 15:51 scheduled: items 7+8 Records / Unity bubbles FIXED + measured, CPU +16% (b20 720p 189.5 fps), crash batch 4x420 s 0 crashes, saves + pipeline cache intact; NEXT: write-watch per-pool skip, gate lead 0x38fe58, user test at 240), then s71, s70 + s70 part 2
## Previous RESUME: read "Milestone 5, session 71" at the END first (2026-11-13 10:51 scheduled: item 9 boss white FIXED + measured, item 4 CPU -16% replay FIXED + measured, items 7+8 Records / Carnage Unity bubbles still OPEN with leads), then s70 + s70 part 2
## Previous RESUME: read "Milestone 5, session 70" and "session 70 part 2" at the END first (2026-11-13: 4 items fixed in s70; open: 9 boss white, 7+8 menu effects, 4 crowd fps)
## Previous RESUME: read "Milestone 5, session 69" + "session 69 part 2" at the END first (2026-11-10 16:21, scheduled: COMBO number p38 at Switch pace, CPU +9% big areas, log noise cut), then 68, 67
## Previous RESUME: read "Milestone 5, session 68" at the END first (2026-11-10 11:21, scheduled: CALL ring fixed, GOOD pop measured + aligned, AMD/low-VRAM fallbacks), then 67
## Previous RESUME: "Milestone 5, session 67" at the END first (2026-11-10, user report on s66 build: upscaler row on PC page, level-up wipe glitch, GOOD/CALL too fast, portability audit), then 66, 65, 64, 63, 62, 61, 60, 59, then 39 (OPEN LIST)
## Previous RESUME: "Milestone 5, session 65"
## Previous RESUME: "Milestone 5, session 64"
## Previous RESUME: "Milestone 5, session 62"
## Previous RESUME: "Milestone 5, session 61"
## Previous RESUME: "Milestone 5, session 58"
## Previous RESUME: "Milestone 5, session 57"
## Previous RESUME: "Milestone 5, session 56"
## Previous RESUME: "Milestone 5, session 54"
## Previous RESUME: "Milestone 5, session 53"
## Previous RESUME: "Milestone 5, session 51"
## Previous RESUME: "Milestone 5, session 50"
## Previous RESUME: "Milestone 5, session 49"
## Previous RESUME: "Milestone 5, session 47"
## Previous RESUME: "Milestone 5, session 46"
## Previous RESUME: "Milestone 5, session 44"
## Previous RESUME: "Milestone 5, session 43"
## RULE (user 2026-10-31): END OF EVERY SESSION rebuild the release ZIP: powershell -NoProfile -File tools/package/package.ps1 (Desktop\TMSRecomp-<date>.zip), even with no code change; report path + size.
## Previous RESUME: "Milestone 5, session 42"
## Previous RESUME: "Milestone 5, session 41"
## Previous RESUME: "Milestone 5, session 40"
## Previous RESUME: "Milestone 5, session 39"
## Previous RESUME: "Milestone 5, session 38"
## Previous RESUME: "Milestone 5, session 37"
## Previous RESUME: "Milestone 5, session 36"

## Previous RESUME: "Milestone 5, session 35"

## Previous RESUME: "Milestone 5, session 34"

## Previous RESUME: "Milestone 5, session 33"

## Previous RESUME: "Milestone 5, session 32" (2026-10-30, scheduled run, user asleep)

## Previous RESUME (2026-10-30 07:55): "Milestone 5, session 32 user report", then session 31

## Previous RESUME (2026-10-30 morning, session 30): read "Milestone 5, session 30" at the end

## Previous RESUME (2026-10-30 night, session 29): read "Milestone 5, session 29" at the end

## Previous RESUME (2026-10-29 night, session 28): read "Milestone 5, session 28" at the end

## Previous RESUME (2026-10-29 afternoon, session 27): read "Milestone 5, session 27" at the end

## Previous RESUME (2026-10-29 night, session 26): read "Milestone 5, session 26" at the end

## Previous RESUME (2026-10-28 night, session 25): read "Milestone 5, session 25" at the end

## Previous RESUME (2026-10-27 night, session 24): read "Milestone 5, session 24" at the end

## Previous RESUME (2026-10-27 night, session 23): read "Milestone 5, session 23" at the end

## Previous RESUME (2026-10-27 evening, session 22): read "Milestone 5, session 22" at the end

## Previous RESUME (2026-10-27 evening, session 21): read "Milestone 5, session 21" at the end

## Previous RESUME (2026-10-27 day, session 20): read "Milestone 5, session 20" at the end

## Previous RESUME (2026-10-27 night, session 19): read "Milestone 5, session 19" at the end

## Previous RESUME (2026-10-26 night, session 18): read "Milestone 5, session 18" at the end

## Previous RESUME (2026-10-26 evening, session 17): read "Milestone 4, session 17" at the end

## Previous RESUME (2026-10-26 afternoon, session 16): read "Milestone 4, session 16" at the end

## Previous RESUME (2026-10-26 midday, session 15): read "Milestone 4, session 15" at the end

## Previous RESUME (2026-10-26, session 14): read "Milestone 4, session 14" at the end

## Previous RESUME (2026-10-26, session 13): read "Milestone 4, session 13" at the end

## Previous RESUME (2026-10-24, session 12): read "Milestone 4, session 12" at the end

## Previous RESUME (state 2026-10-23 late night, session 11)

- Session 11: read "Milestone 4, session 11" at the end. User tested 60 and uncapped (session 10 build) and reported
  (2026-10-23): treasure pickup T-pose flash, field enemies dash far too fast, battle attack/skill animations too fast
  and out of sync. Fixes in this session (commit after aea830b): script time per resume (info.delta, GetUpdateTime),
  dt-scaled field enemy table. **Not verified by the user yet**: all three need a play test at 60 and uncapped.
- New: borderless (play.bat default, Alt+Enter / F11), internal resolution `NX_RES=4k|1440p|1080p|720p` (play.bat
  default 4k), verified by screenshots (field + battle at 3840x2160). Debug: NX_CONTROL `watch addr len [r]`,
  `NX_ANIM_PROBE=1`, `tools/lua/luadis.py`, Ghidra `g.sh Decomp|Xrefs addr...`, `armdis.py`, `findld.py`.
- Next: user play test; then optimization (replays show 46-55 frames/s at NX_FPS=60 with hitches: profile CPU side,
  per-frame `end_and_wait` in present_async).

## Previous RESUME (2026-10-23 night, session 10)

- Session 10: read "Milestone 4, session 10" at the end. User decision 2026-10-23: **true 60 fps game logic (not
  interpolation) plus an uncapped mode**. `NX_FPS=60` / `NX_FPS=N` (> 60, capped) / `NX_FPS=0` (uncapped) work in the
  field (walk speed and the door/map-change timing match 30 fps by log). `play.bat 60` / `play.bat 144` / `play.bat 0`.
  Commits 7970df7 + the NX_FPS commit after it.
- Not verified yet: battles, menus, event cutscenes with voice, effects at 60+ (the user plays and reports anything
  too fast or slow; fixes go in hle_sys.cpp "frame step" section). Animation speed above 60 only by code reading.
- Ghidra headless project of main: `private/tms/ghidra` (see the session 10 notes for the decompile command).

## Previous RESUME (2026-10-23 evening, session 9)

- Session 9: read "Milestone 2, session 9" at the end. **Slot 2 is NOT stuck**: the north door works. Session 8
  had the stick sign wrong (`ls 0 32767` = up on screen = north from the load position; `-32767` turns Itsuki
  around). `tools/drive/slot2_north.sh` loads slot 2 and goes through the north door.
- Played on (agent, verified 2026-10-23): north door -> d002_01 west branch -> T_ATTACK tutorial + battle (won,
  Cleave learned) -> treasure (Medicine x2) -> m0009_04 (Chrom heal advice) -> east along z=-760 -> lift Up at
  (380,-240,-760) -> m0009_02 event battle (auto-battle, won) -> m0009_03 (Performa), Lv 3, free roam
  I. Daitama Upper Lv. Flags on: 0x456 FLG_EVM_0009_02, 0x45e FLG_EVM_0009_03. **Not saved** (no save point used).
- Next story step (from data, not reached yet): m0010_00 fires at d002_01 trigger 0x385 = the door at
  (710, 71, -167.5) (Upper Lv), which leads to d002_03 (m0010_01 on entry). The straight-line `goto.py` got stuck on
  walls on the way (at (204,50,-499) and (669,50,-737)); the user took over manually at that point.
- New tools: control `flag n [0|1]`, `pos`; `tools/lua/flagnames.py` (-> `private/tms/flags.txt`, names in the
  `[flag]` log), `tools/lyts.py` (map layout records), `tools/drive/goto.py X Z`, `tools/drive/advance.sh`.

## Previous RESUME (2026-10-23 morning, session 8, autonomous overnight run)

- Session 8: read "Milestone 2, session 8" at the end. Commits 015e2ca (Lua log, on-demand coverage,
  NX_GAME_INTERVAL) + the notes commit after it.
- Slot 2 (verified 2026-10-23): the round room's **east door** has an "(A) Exit" prompt when Itsuki stands right in
  front of it facing it; A -> `warp/PlaySE_d002_door.lua` -> I. Daitama Lower Lv corridor. BUT the corridor has a
  **one-way marker (cyan arrow pointing west)** where Itsuki gets stuck (x ~ 170 px on the minimap), so the
  elevator is not reachable by design. The north door of the round room never showed a prompt. **Still stuck**:
  the way on is probably the north door, possibly unlocked by the automap tutorial. Lead (assumed, from data): the
  d002_02 layout (model.apak at 0xfa11cd) has a trigger `T_MAPSYSTEM` with flags FLG_EVM_0007_03 /
  FLG_MAP_TUTORIAL_AUTOMAP and a 5x5x5 box near (-22.8, 0.03, -117.8); eventTable `MAP_TUTORIAL` (needs 0x412 on,
  0x8831 off) runs `script_map/.../event/T_CAMERA_MAPSYSTEM.lua`, which sets FLG_MAP_TUTORIAL_AUTOMAP. Next steps:
  (1) read the save's flag bits for 0x412 / 0x8831 (save/ format unknown) or log FlagOn/IsFlagOn calls (Lua
  bindings, hook like AtPrintf) to see the state; (2) find where that trigger box is (log the player position:
  find chrGetPlayer/chrGetActorPos bindings); (3) if the tutorial already ran, look for why the north door has no
  access (compare the two door records in the layout).
  Navigation is slow: zone cameras cut often and the stick is camera-relative, so holds ping-pong between zones;
  check the minimap arrow after every move. `NX_RECORD` a run that gets somewhere so it can be replayed.
- Milestone 4 result (verified): the game's frame step = its present interval, but field movement ignores it (see
  session 8 notes); 60 fps needs more work.

## Previous RESUME (2026-10-23 early morning, session 7)

- Session 7 (user asleep, agent alone): read "Milestone 2, session 7" at the end. Texture mip fix committed (7011b3b).
  Fast restart + load: start tms.exe (run_in_background, `NX_SPEED=2`), then from `private/tms`
  `sh ../../tools/drive/load_slot.sh 2 2` (waits for the title, loads slot 2) and `sh s.sh [cmds...]` (sends control
  lines, then `shot` -> `shots/now.png`). Slot 2 = Observatory Inside, after the first battle. Story objective there:
  unknown yet (the `!` door north leads to the Lower Lv lift alcove; the lift did not react to `a`).
- Done this session: mip fix (7011b3b), **input record/replay = milestone 3 core** (3de4348; play.bat records every
  run to input.rec, archived in logs/). Measured: game logic is per frame (60 fps = double speed), see the 60 fps entry.
- Next, in order: (1) find the story objective from slot 2 and play on; (2) milestone 4: find the game's frame step
  so interval 1 runs at normal speed; (3) dev settings. A one-time scheduled task `tms-recomp-overnight-continue`
  (04:15 UTC 10-23) was created to resume after the usage limit reset.

## Previous RESUME (end of 2026-10-22, session 6)

- Read "Milestone 2, session 6" at the end first (prologue playthrough, new control commands).
- **Game state (verified 2026-10-22 session 6):** title -> new game -> opening movie -> elevator dialogue -> Topic
  screen -> free roam in Daitama Observatory -> Tsubasa event -> audition + Mirage attack -> gate -> first dungeon
  (I. Daitama Upper Lv, lift, Lower Lv) -> boss door -> anime movies + Chrom scene -> **first battle** (won by
  pressing A) -> post-battle scene -> free roam "Observatory Inside" at Lv 2. **Save and Load work**: slot 1 = before
  the gate, slot 2 = after the first battle (`private/tms/save/`). Title goes straight to LOAD when saves exist.
- The shader sidecar needs `tools/shaderc/patches/spirv-no-elseif.patch` applied to the Ryujinx checkout
  (`private/third_party/ryubing`, already applied on this PC; `git apply` / `patch -p1` from the checkout root).
- Next steps, in order:
  1. Load slot 2 from the title (the LOAD cursor starts on the first empty slot: move with `up`/`down`, then `a`)
     and keep playing (Observatory Inside -> Chapter 1) with `NX_CONTROL`; look for the next visual or logic bug.
  2. Known small issues: `drawlog` "fs" field always 0; `shader_glsl.py` hangs on some fragment shaders (GLSL backend
     only; SPIR-V is fine); NEON flush-to-zero not modelled.
  3. Per-submit GPU wait only matters in heavy scenes.
- **Workflow from 2026-10-22 (user decision): the user plays, the agent fixes.** The user starts `play.bat`
  (repo root): the game runs with `NX_LOG=live.log`, and the bat window follows `private/tms/issues.log` live.
  issues.log = only problem lines (FATAL/CRASH + backtrace, stubs, unimplemented, unknown, failed, error, [cri],
  non-zero skip counters), each with wall-clock time and run time; repeats of the same message (numbers ignored) are
  written 3 times, then at 10/100/1000...; boot-time items seen since milestone 1 are tagged "(known, harmless)".
  Each start moves the previous live/issues logs to `private/tms/logs/<name>_<time>.log`, so every run is kept.
  The user reports with a screenshot + time + save slot; the agent reads issues.log/live.log and reproduces from the
  save (automation only for replaying a bug).
- Driving the game (agent workflow): start it with run_in_background (not `&` inside a Bash call):
  `cd private/tms && : > control.txt && NX_CONTROL=control.txt NX_LOG=live.log ./build/tms.exe --data .`
  then from the title (~8 s after the log line "movie: first frame") `sh ../../tools/drive.sh ../../tools/drive/newgame_1.txt`
  and `newgame_2.txt` (glasses help -> opening movie, ~4 min; the 3D event hall follows ~2 min after the 4th
  "movie::Decoder(" log line). Control lines: button names (`a b x y up down left right plus minus l r zl zr`, 150 ms),
  `shot` (next frame -> `shots/live_NNNNN.bmp`, view with `python tools/bmp2png.py <bmp> out.png`), `drawlog`, `rt`,
  `ls x y ms` / `rs x y ms` (hold a stick, -32767..32767, ms of game time; camera-relative in the game), `verbose 1|0`.
  `tools/drive/to_free_roam.txt` continues from `fast_to_3d.sh` to free roam in the observatory.
  Yes/No prompts default to **No**: `up`, then `a`. Movies cannot be skipped with `plus`.
- Build: `build.cmd` (from PowerShell: `cmd /c .\build.cmd`; kill tms.exe first or the link fails). Sidecar:
  `dotnet build tools/shaderc/NxShader.csproj -c Release -o private/tms/shaderc`. After editing
  `tools/recomp/names.txt` or the lifter, re-lift first: `python tools/recomp/lift.py private/tms/link private/tms/gen`.
  Lifter tests: `private/venv/Scripts/python.exe tools/recomp/test_a32.py --n 300`.
- Git: no global identity on this PC; commit with
  `git -c user.name=<name> -c user.email=<email> commit ...` (identity in the agent memory, not here).

## Facts (verified 2026-10-20)

- Dump: the user's own NSP, ASIA base game (path kept outside the repo).
  - 12,092,457,723 bytes, title ID 0100A9400C9C2000, base game, no update.
- Keys: `%APPDATA%\eden\keys\prod.keys` + `title.keys` (user's Eden install). Never copy into the repo.
- Host: Ryzen 7 9800X3D, 63.6 GB RAM, RTX 5070 Ti (driver 32.0.16.1742), Windows 11. C: 2.3 TB free.
- Toolchain present: LLVM/clang 23.1.3 (`C:\Program Files\LLVM\bin`), VS 2022 + VS 18 (bundled CMake/Ninja),
  .NET SDK 10.0.402, Python 3.12, git. Missing: Vulkan SDK/headers, SDL3, gh.

## Prior art (checked 2026-10-20)

- **BelmanteGu/SuperMarioWonderRecomp** (MIT, commit 665b2f9, 2026-10-18), part of SwitchGamesRecomp. Reference only:
  first considered as a base, then the user decided we write our own code (2026-10-20).
  - `recomp/` Python AArch64 -> C++ lifter (NSO input, `--base`), `runtime/` kernel/IPC/nn:: HLE + platform layers,
    `runtime/src/nvn/` NVN reimplemented over Vulkan, Maxwell shaders -> SPIR-V offline via Ryujinx translator (MIT).
  - Per-game glue in `games/<name>/game.cpp`, chosen with `-DNX_GAME=<name>`. Hades + Wonder use it.
  - Importer `android/wonder/importer` (`nximport --exefs --title <id> --out <dir> prod.keys title.keys x.nsp`)
    takes NSP and writes exefs NSOs + romfs; no nstool needed.
  - Wonder-specific: shader container extraction (`tools/maxwell/containers.py` knows bfsha/sarc/esetb/blarc).
    TMS uses a different engine, so its shader containers must be found and parsed anew.
  - Clone for reading only: `ref/smbw` (not part of our repo).
- Others seen, not used: suyu recompiler mode (GPL-3.0-or-later, conflicts with GPL-2.0-or-later goal),
  ssbu-recomp (SSBU-specific runtime), ScarletNX (GPLv3), mk8-recomp (on suyu).
- No existing TMS decomp/recomp/PC port found.

## Recon results (verified 2026-10-20)

- Extraction: `nstool -k prod.keys -x / private/tms/nsp <nsp>` (no ticket: standard key-area crypto, keygen 8),
  then `-x /0 private/tms/exefs` and `-x /1 private/tms/romfs` on `08148f8b05a99d3fb7fa27ec770ebcac.nca`.
  RomFS = 17 CRI `.cpk` packs under `Pack/`, 12.05 GB. Partition 2 = logo.
- **The game is 32-bit ARM (AArch32).** `main.npdm` MmuFlags 0x04: Is64BitInstruction=0, address space type 2
  (32-bit, no reserve). Main thread prio 44, stack 1 MB. Code starts with A32 `push {r4,r5,r11,lr}`.
  Consequence: every AArch64 lifter (SMBW, suyu, ssbu) is useless here; we need an A32 (+VFP/NEON) lifter.
  ELF32 dynamic: REL relocations (not RELA), 16-byte symbols.
- SDK 7.4.0 (NCA SdkAddon). Modules (`tools/nso.py`):
  | module | text | imports | exports | what |
  |---|---|---|---|---|
  | main | 0x4efbe0 | 350 | 17 | the game |
  | sdk | 0x5472a0 | 13 | 25048 | nn:: SDK + NVIDIA driver stack (NvRm, NvOs, android::) |
  | subsdk0 | 0x51f7c0 | 103 | 20 | NVIDIA `glslc` (runtime GLSL compiler) |
  | subsdk1 | 0x3be8a0 | 669 | 10866 | NVIDIA multimedia: `movie::` (VP9, mkvparser), silk, h264 |
- main's import surface is small: 202 `nn::` functions, libc/libm/aeabi, `nvnBootstrapLoader`, 8 `glslc*`,
  17 `movie::` (VP9 decoder), 3 `nv::` graphics allocator calls. Plan: recompile `main` only; implement its
  imports on the host (nn:: HLE, host libc, NVN over Vulkan, movie via a VP9 decoder). sdk/subsdk not lifted.
- Graphics: NVN. Shaders are precompiled **BNSH** (Maxwell) in `pack_030_etc.cpk:Shaders/` (`.pso/.vso` = single
  BNSH, `.pspk/.vspk/.cspk` = `APAK` packs of BNSH). glslc imports likely a debug path (unverified).
  -> Maxwell -> SPIR-V with the Ryujinx translator (approved dependency).
- Scripts: compiled Lua 5.2 bytecode (`LuaR`, 4-byte size_t) in `pack_999_lua.cpk` (11,688 files).
- Assets: Wii U-era formats: `gtx` textures, `bfres`, `ptcl`, `msbt`, ADX/ACB/AWB audio (CRI), USM movies (66).
- CPK quirk (measured): TOC `FileOffset` counts from 0x800 (end of CPK header), not `TocOffset`; with that all
  10,355 compressed entries start with `CRILAYLA`.

## Plan

Milestones (check in with user at each): 1 SDK built + boots to title; 2 crash fixes; 3 input record/replay;
4 stable 60 fps (frame times; DONE 2026-10-26, user play test); 5 QoL (settings menu, locate-game prompt, shortcut/icon); 6 publish GitHub
GPL-2.0-or-later, source-only releases.

Decisions 2026-10-22 (user): **libvpx** (BSD-3-Clause) is approved for VP9 movie decoding.
Endgame (after the game is fully playable): a launcher like the "SpartanPort" GOW3 PC port: sidebar Home (quick
settings), Graphics (display mode, VSync, HDR, anisotropic filtering, performance overlay, F12 screenshots),
Performance (frame-rate limit, frames queued, engine frame rate, aspect ratio, render resolution, shader cache
options), Game, Controls, Mods, Advanced; Save + PLAY; an in-game menu hotkey; and self-update from GitHub releases.

Milestone 1 steps:
1. Import NSP -> `private/tms/{exefs,extract/romfs,analysis}` (needs user OK).
2. Inventory NSOs (main, sdk, subsdk*), imports, graphics API (expect NVN), engine, shader containers.
3. Recompile main + sdk; build runtime with `games/tms/`.
4. Find + translate Maxwell shaders; boot until the title screen draws.

## Progress 2026-10-20 (session 1, continued)

Verified by running `private/tms/build/tms.exe --data private/tms`:
- Lifter: 53.7k functions, 2.57M instructions, 37 C files (~110 MB), builds with clang -O1 in a few minutes.
  Unicorn diff test (`tools/recomp/test_a32.py`): 4400 random cases, all classes match except MRS mode bits and
  NEON flush-to-zero on denormals (known).
- Boot path (from rtld + SDK disassembly): runtime does rtld's job, calls `nn::init::Start(handle, 0, cb1, cb2)`;
  cb2 runs each module's DT_INIT (sdk, then main). SDK's real nn::os runs on our HLE kernel (svc level).
- Reaches nnMain: heap 2 GiB, romfs mounted ("Contents"), AudioOut opened, NVN device + memory pools created,
  then crashes on stubbed NVN answers.
- Real NVN driver entry points dumped (`NX_DUMP_NVN=file`): all 513 names -> distinct SDK functions
  (`private/tms/analysis/nvn_real.txt`, short disassembly in `nvn_short.txt`). Builder/state setters are tiny and
  pure: run them as-is, HLE only object init / commands / queues / present.

Lifter details learned the hard way:
- CPK offsets: from 0x800. PLT stubs resolved statically (8k). setjmp lifted inline (host __builtin_setjmp).
- Jump tables: `add pc, pc, rX, lsl #2` (branch tables) and clang's relative tables
  (`add rA, pc, #k; ldr rB, [rA, rX, lsl #2]; add pc, rA, rB`, rA sometimes hoisted): 1265 found.
- Code pointers without relocations: `ldr rY, [pc, #k]; add rX, pc, rY` (595) added as roots.

## MILESTONE 1 REACHED (2026-10-20): boots to the title menu

Verified by frame dump (`NX_SHOT_EVERY`, `private/tms/milestone1_title.png`): title menu (ruins background,
copyright lines, DEBUT / LOAD menu), stable, no input needed after the intro movies (which play black).

Key fixes on the way (each found from logs / frame dumps, kept because it moved the boot forward):
- rtld emulation: cb2 runs DT_INIT of sdk then main; nn::init::Start(handle, 0, cb1, cb2).
- Heap: GetInfo total memory must equal heap region + used (SDK asks total - used).
- Thread start: a higher-priority thread runs until its first svc before the creator continues (games read
  arguments from the creator's stack). GetCurrentProcessorNumber returns the thread's core (0-2).
- setjmp/longjmp: CRT setjmp (restores callee-saved host registers); __builtin_setjmp corrupted locals.
- NVN: real driver code for builders/state objects/GetInteger; HLE for objects/commands. Programs are bound per
  stage (BindProgram bits: vertex 1, fragment 2, ...). size_t args are 32-bit. Pools nest (innermost lookup).
- NVN -> Vulkan: uniform binding N = Maxwell cbuf slot N+3; bound texture binding N = handle word N+8;
  texture handle = id | sampler << 20; NDC +Y is up (negative-height viewport); textures live in pools as
  block-linear data (untiled at first bind); the frame ends with CopyTextureToTexture into the window texture.
- movie::Decoder: MediaCodec-style fake decoder (black NV12 frames, one per input, EOS honoured).

Known gaps (milestone 2+): VP9 decoding (movies black), one compute shader fails to translate
("global memory" without storage buffer), CommandBufferClearTexture stub, presents run at the monitor rate
(~140/s on a 144 Hz display: needs pacing), every submit waits for the GPU, no texture invalidation, audio untested.

## Milestone 2, session 2 (2026-10-21): the known gaps

Baseline before any change (title menu, uncapped by the game): ~150 presents/s, FIFO-limited on the 144 Hz display.

Done, each verified by a run (log + frame dump):
- **Present pacing.** The game sets present interval 2 itself (`nvnWindowSetPresentInterval`), i.e. 30 fps like the
  console. `nvnQueuePresentTexture` now waits for the n-th tick of the 60 Hz vsync clock (ui.cpp) after the last
  present. Measured: 30.0 frames/s, worst gap ~36 ms (the clock thread sleeps in 1 ms steps). `NX_PRESENT_INTERVAL=1`
  forces 60: holds 60.0/s at the title. `NX_NO_VSYNC` skips pacing (uncapped: 152/s). A `frames:` line is logged
  every 10 s.
- **Per-submit GPU wait: left as is.** Uncapped, a whole frame (including every wait) costs ~6.6 ms at the title, far
  under the 33 ms budget. Revisit with a heavy 3D scene (milestone 4); pipelining needs real NVN sync objects, because
  the game rewrites uniform data in pool memory the GPU reads zero-copy.
- **ClearTexture / ClearTexturei / ClearTextureui** (real driver: `(cmd, tex, view, region*, colour*, mask)`): recorded
  and replayed as `vkCmdClearColorImage` / `vkCmdClearDepthStencilImage` of level 0. The game issues 4-6 per frame,
  all full-size with mask 0xF (partial regions or masks would be logged). Also no-op'd SetConservativeRaster*: no NVN
  stubs are hit at the title any more.
- **Compute shaders.** Compute code has no NVN header and no SPH: it starts with the first Maxwell scheduling word
  (we skipped 0x30 bytes, hence the "global memory" failure). Its control section (magic 0x98761234) holds the
  workgroup size at +0x748 (64, 1, 1); the shaderc protocol now carries it for compute. The one shader seen is
  per-tile light binning (forward+): 60 groups, 1 dispatch per frame. Dispatch is replayed (compute pipeline per
  program, same descriptor code as draws). Verified: a sentinel written over its output before a dispatch was
  overwritten by the dispatch in the same submit.
- **Buffer addresses in c0 (measured on that shader).** Ryujinx reports global-memory buffers by where their address
  lives in driver cbuf c0: uniform buffer i at c0+0x210+16i (glslc reaches UBOs beyond the 8 hardware slots this
  way; the light list is UBO 11, 0x7810 bytes = 384 lights x 80 + 16), storage buffer i at c0+0x310+16i (output:
  SSBO 0, 4 MiB). Graphics stages have not shown any yet; assumed the same table. Storage ranges are no longer capped
  at 64 KiB.
- **Texture invalidation.** Guest memory is reserved with `MEM_WRITE_WATCH`. At a pool texture's first use in a
  submit we ask Windows whether the CPU wrote its pages since the upload; if so it is uploaded again. GPU writes do
  not trip it. Measured: 412 re-uploads while booting, 0 per frame at the title, no fps cost (uncapped 152/s).
- **WriteTexels.** The game calls it once, on a 32x32x32 3D texture (probably a colour-grading LUT). The texels are
  kept linear and copied into the image at its next use (any target, level 0), skipping block-linear tiling. Not
  exercised yet: that texture is not bound at the title.

Found, not fixed:
- ~~Audio is silent~~: FIXED in session 3 (the lifter dropped every STL store-release, see below).
- **VP9 movies** still black (fake decoder). Needs a VP9 decoder, which is not on the approved dependency list
  (candidates: libvpx, BSD-3-Clause; or our own decoder, large). User decision.
- Validation layer is not installed (no Vulkan SDK), so `NX_VK_VALIDATION` fails at instance creation.

New debug switches: `NX_PRESENT_INTERVAL`, `NX_DUMP_SHADER` also writes compute control sections to
`analysis/ctrl_<addr>.bin`; `-v` logs every fs read.

## Milestone 2, session 3 (2026-10-21): audio, UI, past the title

Root-cause fixes (each verified in game):
- **Lifter bug, big:** ARMv8 `LDA/LDAB/LDAH` and `STL/STLB/STLH` (plain load-acquire / store-release, bits 9:8 = 00)
  were decoded as exclusive LDREX/STREX. A store-release became `c->r[15] = excl_store32(...)`, which fails without a
  prior LDREX, so **the store was silently dropped** (1662 sites: SDK nn::os, CRI atomics). Fixed in `a32.py synch()`
  -> `acq_loadN` / `rel_storeN` (guest.h); Unicorn test class `acqrel` (300 cases, 0 bad). This silenced CRI audio
  (its low-level atom players never left idle) and can explain other lost thread handoffs.
- **NVN depth mode:** the game never calls nvnDeviceSetDepthMode, so NVN's default NEAR_IS_MINUS_W (OpenGL clip z in
  [-w, w]) applies; Vulkan's [0, w] clipped all UI with z < 0 (title HELP bar and Ver.1.0, every dialog). Now
  `VK_EXT_depth_clip_control` negativeOneToOne when the mode is 0; nvnDeviceGetDepthMode returns the tracked mode;
  nvnCommandBufferSetDepthRange is applied to the viewport.
- **Texture views:** NVNtextureView (driver layout: flags byte @0 [bit0 levels @1/@2, bit1 layers @4/@6, bit2 format
  @8, bit3 swizzle @0xc..0x18, bit4 ds mode @0x1c, bit5 target @0x20]) now sets swizzle + view type
  (`sampled_view()` in vk.cpp, cached per image). Fonts are BC4 atlases registered as 2D arrays with swizzle
  ONE ONE ONE R; without it glyphs drew as solid boxes. NVN swizzle enum: ZERO 0, ONE 1, R 2, G 3, B 4, A 5.
- Kernel: SetThreadCoreMask sets the thread's core (games choose per-core job queues from GetCurrentProcessorNumber;
  CreateThread core -2 = 0). SignalToAddress type 2 values match Horizon (waiters and count <= 0: v-2;
  waiters <= count: v-1; more waiters: v; none: v+1). Signal counts no longer wake everyone after the first (also in
  SignalProcessWideKey). oe PopNotificationMessage returns FocusStateChanged (15) once at launch, then blocks.

Game / CRI facts (main, 1.0.0):
- Game debug log `0x5d7e1c (mask, fmt, ...)` (CRI's `#CRIATOM` API trace also goes through it); vsnprintf `0x69d0f8`.
- criErr_Notify family: `0x69d3c4 (level,msg)`, `0x69d4d8 (level,msg,code)`, `0x69d774 (+1 arg)`, `0x69d868 (+2)`,
  `0x69d660 (+3)`.
- PCM output: a CRI thread fills AudioOut buffers through callback `0x697c00`; output handle global `0x101d32c`;
  float->s16 `0x691a88`; CRI server loop `0x6a1488` (60 Hz); CRI NX file read wrapper `0x6bf450`.
- Thread names (ThreadType +0xe4): CRI FS File Access / Memory File System / Data Decompression, CRI Server Manager,
  CriManaDecodeThread, CRI MPV Worker, core[N] AtJob / AtJobMp / AtFile / AtSound / AtGraphicsVsync / AtDeviceMessage.
- Game job system: workers poll job callbacks every 50 ms until they return non-zero; main waits on `[job+0x1c] & 2`.
- Sound: all ADX (Common.awb 510 MB streamed; Common.acb 20 MB in memory with the AWB header embedded). Movies: CRI Mana
  USM (VP9 through nvidia movie::Decoder + CRI audio), pack_050_movie.cpk, m01.usm = opening.
- DEBUT opens the saveload screen (Interface/_US/saveload/*.gtx). Boot checks `save:/system.bin` (absent on first run).

Debug tooling added (details in code comments):
- `tools/recomp/names.txt`: `0xADDR name` internal functions -> hookable (HLE_FN) + probe slot (PROBE_FN). Re-lift.
- `lift.py --probe-range LO:HI` (hex) + `NX_COVER=1`: call counts per function every 10 s (`cover:` log lines).
  Re-lift WITHOUT the range afterwards. `NX_COVER=manual` + control line `cover`: report on demand, so windows line up
  with actions (lines split at 3 KB, the last one is `cover-end:`). Diff script idea: functions only in the window with
  the action (session 8 used a scratch script; ~1500 functions run per idle window in the field).
- `[lua] ...` = game script prints (AtPrintf/print/AtConsoleOut/AtTraceOut, empty in retail; off: `NX_LUA_LOG=0`),
  `[lua error] ...` = script_error reports and every Lua `error()` raised (luaG_errormsg). Lua C API in main:
  lua_gettop 0x529964, lua_type 0x529f88, lua_tolstring 0x52aa6c; Lua binding table = {name ptr, fn ptr} pairs
  (e.g. AtPrintf at 0x9ebbbc). Script error reporter 0x5b4ca8 (L, kind, function, message).
- `NX_GAME_INTERVAL=n`: replaces every present interval the game sets (= its frame step), see milestone 4 notes.
- `NX_PROBE=name,...`: log calls (args, caller) of names-file functions.
- `[game m] ...` = game's own debug log (off: `NX_GAME_LOG=0`); `[cri] ...` = CRI errors/warnings.
- `NX_LOG_DRAWS=<n>`: every draw of frame n (state, viewport, bindings, UBO floats, texture format/swizzle).
- `NX_DUMP_RT=<n>`: every colour target drawn in frame n -> `shots/rt_*.bmp` (HDR targets are B10G11R11:
  `bmp2png.py --r11g11b10`). `NX_DEBUG_PRESENT=<n>`: op/draw counts of 6 presents from n.
- `NX_TRACE_CV=1`: condvar waits/signals with thread names. `NX_THREAD_DUMP=<s>` shows names + cores.
- `-v` also logs fs reads, entry-type, open-dir, create, delete.
- `NX_CONTROL=<file>`: live input + `shot` (see RESUME HERE).

## Milestone 2, session 4 (2026-10-22): VP9 movies, shader constants, texture bindings

User decision: libvpx is approved (VP9). Verified in game: the opening movie m01.usm plays with correct colours at
30 fps, no dropped frames (frame 150 dumped with `NX_DUMP_MOVIE=<file>` and converted by hand matched the screen).
- **movie::Decoder output is copy-out.** The game passes its own buffer: GetOutputBufferSize(int* size, int* align)
  -> (w*h + 2*(w/2)*(h/2), 1), then GetOutputBuffer(index, Buffer*) copies into Buffer base+offset (subsdk1
  `DecoderImpl::GetOutputBuffer` @0x150430, format 4 = tight NV12: Y rows of w bytes, then h/2 rows of UV). Our old
  stub replaced the buffer pointer and returned the width as size: that was the "blue/noise". libvpx (generic C,
  4 threads) decodes on the thread that sends input; streams seen: I420 1280x720, BT.601 (cs 3).
- **Maxwell cbuf 1 = the shader's embedded constants** (glslc literal tables, e.g. the movie shader's YUV matrix
  1.16438 / 1.59603 / -0.812812). Control section +0x6fc = size, +0x700 = offset from the start of the code (with
  the NVN header); now bound for c1. Before, c1 was an uninitialised dummy buffer (random colours per run). Many
  shaders have constants (4-44 bytes seen), so 3D materials are affected too.
- **Texture bindings: NVN binding i = c0 handle word 8 + 2i** (64-bit handles), measured on the movie draw (game
  binds Y at 0, UV at 1; shader reads handles 8 and 10). We had 8 + i, so every second+ texture of a draw was wrong.
- New live control commands: `drawlog` (log every draw of the next frame; texture binds are logged too) and `rt`
  (dump the colour targets of the next frame). Drive scripts: `sh ../../tools/drive.sh ../../tools/drive/newgame_1.txt`
  (from the title; start ~8 s after "movie: first frame") and `newgame_2.txt` (glasses help -> opening movie).

### Session 4 continued: first 3D scene (verified in game 2026-10-22)

After the opening movie the event hall (crowd, posters, stage lights, shadows) and the first dialogue's elevator
hall render in 3D (`private/tms/m2_first_3d_scene.png`), 30 fps. Open: Itsuki's model shows only his hair (face and
body missing); see "Next" below.
- **CallCommands / CopyCommands were dropped.** The game pre-records state blocks (program, blend, colour, channel
  mask, depth-stencil, polygon, vertex layout/buffers, blend colour, stencil ref) into command handles and calls them
  per material. We recorded OP_CALL but never replayed it, so 3D draws ran with stale state (shadow pass without
  depth, G-buffer pass with colour writes masked). Now the handle's commands are copied in at record time (a
  finished handle never changes).
- **GPU hang (TDR, Windows LiveKernelEvent 141) that this exposed: BRX jump tables.** Skinning vertex shaders
  switch on the bone count (UBO c8[22].x, 1-4) with an indirect branch whose table is in cbuf 1 (the shader's
  constants). Ryujinx reads it through `IGpuAccessor.ConstantBuffer1Read`, which our sidecar left at the default 0,
  so only the 1-bone case survived and `while (true)` never exited for 2-4 bones. The sidecar protocol now carries
  the constants' offset/size (in the code) and implements ConstantBuffer1Read.
- Graphics stages read storage buffer i at c0 + 0x510 + 16 i (compute: 0x310), measured on forward+ material
  fragment shaders (handle word 0x144).
- NVN formats 0x69-0x6c = RGB10A2 SN / I / UI2F / I2F (vertex normals). robustBufferAccess on.
- Debug tools added: `NX_CHECKPOINTS=1` (NV diagnostic checkpoints: on device loss the log names the last draw the
  GPU started/finished, then `vk: recent draw N` lines list the last 1024 draws with vertex/fragment code
  addresses); VK_EXT_device_fault info is logged on device loss; `NX_SKIP_CODE=lo-hi` (hex) drops draws whose shader
  code lies there; `NX_LOG_PROGRAMS=1` logs each translated stage's resources; `NXSHADER_DUMP_GLSL=<dir>` (sidecar)
  writes readable GLSL; `drawlog` now also logs state ops and colour targets 1-7.
- Driving: a game started from a Bash call with `&` dies when that call ends; start it with run_in_background.
  Every GPU hang resets the display driver on the user's PC: keep hang repros few.

Next:
1. Itsuki's face/body missing (hair renders). Checked 2026-10-22: pipeline/translation failures 0, no unbound
   buffers; frame state now sane (shadow pass ch 0 ds 0x47; depth prepass ch 0 ds 0x43 (21 draws); colour pass
   ds 0x31 = EQUAL (20 draws) and 29 opaque draws ds 0x43; MRT mask 0x0f0f). Ruled out: depth EQUAL mismatch
   (forcing EQUAL -> LEQUAL changed nothing). The multi-bone skinning switch now compares c1 jump-table values at
   runtime (needs c1 bound = shader constants, which it is). Still suspect: the big forward+ character fragment
   shaders (code 0x9b06c700-0x9b0caf00, light list SSBO via c0+0x510, guessed table) or the face/body vertex
   streams (attr 8 comes from stream 1; drawlog prints only stream 0's stride). Next: `NX_SKIP_CODE` on the
   hair's shaders vs the body's to tell which draws are the body, then `drawlog` those draws (stream 1 stride,
   UBO c8[22].x bone count, textures) and `rt` to see whether they reach the colour targets.
2. g_handles (finished command handles) are never freed: memory grows with play time.

## Milestone 2, session 5 (2026-10-22): fast test runs, integer vertex inputs, command handle freeing, buffer copies

- **Game speed (`NX_SPEED=n`, live `speed n`).** Guest clock (CNTPCT / `guest_counter`), kernel timeouts and
  SleepThread, the 60 Hz vsync clock and AudioOut pacing run n times faster (audio is dropped while n > 1). Nothing is
  skipped, so game logic stays identical. Measured at x4: 117-120 presents/s, boot -> elevator dialogue in ~2.5 min
  instead of ~6. One command: `sh ../../tools/drive/fast_to_3d.sh 4` (tms.exe started with `NX_SPEED=4`). Menu
  scripts keep real-time waits: at x4 with divided waits the inputs were eaten while the game loaded (file reads and
  first-time shader translation do not speed up).
- **Integer vertex attributes.** Ryujinx's default `QueryGraphicsState` declares every vertex input float. Bone
  indices are RGBA8UI / R8UI, and a float input fed from a UINT format is undefined in Vulkan. The sidecar protocol now
  carries 32 attribute types for vertex shaders (Ryujinx AttributeType: 0 float, 1 sint, 2 uint) and the runtime keeps
  per-type variants of each vertex stage (`vertex_module`, built at pipeline creation from the attrib formats; the
  `*2F` formats 0x51-0x68 stay float). Verified in the GLSL (`uvec4 in_attr7`, `int(in_attr7.x)` instead of
  `floatBitsToInt`). Did NOT fix the missing body (NVIDIA passed the raw bits anyway), kept because it is spec-correct.
- **Command handles freed.** Measured: two per-frame command buffers, each given its 4 MiB chunk again every frame
  (`AddCommandMemory`, pool bc1ae1d0, offsets 0x4800000 / 0x4c00000). Freeing every handle of a re-added chunk dropped
  live state blocks (the game keeps calling them: "CallCommands with unknown handle"). Rule now: on chunk re-add, free
  only handles that went to `nvnQueueSubmitCommands`. Measured: live handles plateau at 2296 (was +1 per frame).
- **Itsuki's missing body, narrowed down.** Body/face meshes = every multi-bone mesh (stream 0 stride 20: pos,
  RGBA8UI indices @12, RGBA8 weights @16, bone count c8[22].x = 3); hair is single-bone (R8UI index 103). Draws run
  (no skips, no pipeline errors) but cover zero pixels (`NX_DEBUG_SKIN=1` paints multi-bone draws magenta without
  depth test: nothing). CPU emulation of the depth shader on dumped inputs (`drawlog` writes `analysis/skin_<vbuf>.bin`):
  bone 103 has world translation (y 15.97, the scene's height) but bones 0-102 sit near the origin, so the body lands
  at NDC y -3.4, off screen. The c9 palette's other bones are stale on the GPU. Suspect found:
  **`nvnCommandBufferCopyBufferToBuffer` was recorded (OP_COPY_BUF_BUF) but never replayed.** Now replayed as
  vkCmdCopyBuffer (args: r1 padding, src r2:r3, dst [sp], size [sp+8] (32-bit size_t)). OP_COPY_TEX_BUF has no
  recorder or replay yet.
- Debug tools added: `drawlog` lines now show all stream strides, vbuf1, vertex/fragment code, raw first vertex words,
  non-zero 48-byte rows of big UBOs (bone palettes) and c8[22]; each stage's code is written once to
  `analysis/code_<src>_<stage>_<consts off>_<consts size>.bin`; `python ../../tools/shader_glsl.py <code.bin> <dir>
  [7=2,...]` turns one into GLSL. `NX_DEBUG_SKIN=1` (above).

### Session 5, continued (2026-10-22 evening, after the session-limit cut)

- **Lifter fixes (uncommitted until this entry, verified by the new `test_a32.py --only game --link private/tms/link`
  class: every distinct VFP/NEON word in main+sdk, 31080 cases, 45 left = known flush-to-zero + VRECPE/VRSQRTE estimate
  precision):** `vmov.32 dN[x], rT` / `vmov.32 rT, dN[x]` lane now from encoding bits (Capstone's fmdhr/fmdlr names and
  vector_index were wrong: `vmov.32 d0[0], r0` came back as lane 1); NEON VSHL/VRSHL by register used an int8 shift
  and `-s` wrapped for -128 (now int). Re-lifted + rebuilt.
- After the fixes the bone palette (c9, 104 bones) looks valid: model-space skin matrices, bone 103 = head
  (T 0.09, 15.97, 0.12), hair = rigid mesh on bone 103. c8 (model matrix) identity for hair and body.
- **GLSL-on-CPU check:** the translated vertex shader (Ryujinx GLSL) compiled as C++ (scratch `glslemu/mk.py`: strips
  the header, adds vec4/uvec4/UB structs + GLSL builtins, feeds `analysis/skin_<vbuf>.bin`) gives, for the elevator
  frame: face mesh 9a871c90 at NDC (0.1, 0.40), neck 9a86a7d0 (0.05, -0.2), torso 9a859f90 (0.16, -0.68), i.e. right
  under the hair, which the same matrices put at (0.12..0.15, 0.78) and the GPU draws there. So palette, c4/c8, the
  translated skinning loop and BRX table (c1 = 0x158 0x170 0x180 0x198 0x900 0x918 0x930 0x940) are all right on the CPU.
- Ruled out this session: index buffers (`drawlog` now prints `indices lo..hi (base vertex)`: sane, 0..N-1, base 0),
  skipped draws (skip counters all 0), vertex formats (0x22 RGB32F pos, 0x25 RGBA8 weights @16, 0x27 RGBA8UI indices
  @12; hair 0x03 R8UI), stream strides, UBO ranges/alignment.
- **NX_DEBUG_SKIN is a flawed test:** its blend is src * CONSTANT(magenta), so a black FS output or an alpha-test
  `discard` shows nothing. Next: check the body fragment shaders for discard (alpha from a texture), then a
  constant-attribute experiment (bind bone indices/weights to a stride-0 buffer {103 x4, 255 0 0 0}) to split
  "vertex fetch/skinning on GPU" from "fragment side".
- Body colour-pass vertex shaders: 7e942600 (toon outline: pushes along the view normal, +0.003 z), 7e794600,
  7e93d300, 7e6a9000. Depth prepass: 009a0000. The `drawlog` "fs" field is always 0 (prints progs[1]->stages[1]).
- **ROOT CAUSE FOUND + FIXED (verified in game, `private/tms/m2_itsuki_fixed.png`): Ryujinx SPIR-V codegen drops
  `else if`.** Ryujinx's `AstOptimizer` folds `else { if (..) }` into an `ElseIf` block for every backend, but
  `CodeGen/Spirv/SpirvGenerator.cs` only knows If -> Else: an If followed by ElseIf branches to the merge block on
  false and the ElseIf bodies become unreachable. The GLSL backend prints `else if` correctly, which is why reading the
  GLSL (and running it on the CPU) looked right. Here it hit the BRX-lowered bone-index chain of every skinned vertex
  shader (`c1[i] == 0x158 -> idx.x, else if 0x170 -> idx.y, ...`): only bone x survived and the driver got an invalid
  structured CFG; every multi-bone primitive was rejected. Fix: `tools/shaderc/patches/spirv-no-elseif.patch`
  (AstOptimizer gets `foldElseIf`, false for TargetLanguage.Spirv; nested else/if is valid SPIR-V). Rebuild the
  sidecar after applying it. Any other shader with an else-if chain (lots: BRX tables, material switches) was also
  wrong before this, so re-check scenes that looked off.
- How it was found (method worth reusing): (1) `drawlog` now records **per-draw pipeline statistics** (Vulkan query:
  VS invocations, clipper in/out primitives, FS invocations; lines `stats vbuf0 ... vs ... count ...`): skinned draws
  had `clip out 0`, hair had out = in. (2) Writing bone count 1 into c8[22] (single-bone path) made the body appear,
  so the weight loop was at fault. (3) `tools/spirv_dump.py <code.bin> out.txt [7=2]` prints the SPIR-V the runtime
  gets (opcode names from the Ryujinx source enum): the `OpBranchConditional` false target was the merge block.
- New debug tools (session 5): `NX_NO_KILL=1` turns fragment `OpKill`/`OpTerminateInvocation` into `OpReturn` (shows alpha-test /
  dither losses; it made dithered fades visible as blocks), `tools/glsl_emu.py` (GLSL vertex shader on the CPU),
  `tools/spirv_dump.py`, `drawlog` index ranges + pipeline statistics. Device features added: pipelineStatisticsQuery,
  hostQueryReset (both core, debug use only). Fixed: a literal NUL char in `vk_shader.cpp` (made git treat it as binary).

## Milestone 2, session 6 (2026-10-22 night): prologue playthrough, stick control

Verified in game (x4 speed, agent-driven), no new bug found on this stretch:
- Event hall, elevator dialogue, "Communication Tool: Topic" help, Topic screen (Touma chat with stickers), free roam
  in Daitama Observatory (map f002_01), NPC talk + poster "Check", Y menu, Topic MAP tab, Tsubasa event (m0001_00,
  fully skinned, facial animation), audition cutscene (several characters, depth of field), Mirage attack, gate,
  "Main Menu and Saving" help, **Save to slot 1** (`save/save_1.bin` 341440 bytes + `system.bin` 512; save list
  shows Prologue / Daitama Observatory / play time / date), Touma message, first dungeon I. Daitama Upper Lv.
- Minimaps show only explored parts (fog of war in the dungeon; the observatory map is a plain floor disc). Assumed
  correct, not compared with real hardware.
- Prologue route (for replays): from the elevator go left around the stage booths to the queue pens in front of the
  "One of Millennium" stage; Tsubasa (long dark hair, orange cardigan) stands at the railing there; talk to her, then
  walk to the opening in the pink wall at the back left of the pen; after the attack walk north to the gate (`!`).
- Game scripts: `pack_999_lua.cpk` `Event/field/script/field/<map>/event/mNNNN_NN.lua` (story events),
  `npc/*.lua` (talk handlers; `m0001_01.lua` = Tsubasa, starts `m0001_00`), `script_map/...` (map objects). Lua 5.2
  bytecode; string constants are enough to read the flow (`tools/cpk.py extract ... --grep <path>`).

New control commands (`runtime/src/ui.cpp`): `ls x y ms` / `rs x y ms` hold the left/right stick (game ms, scaled by
the speed), `verbose 1|0` toggles `-v` logging live. Field cameras are fixed per zone and the stick is camera-relative,
so a direction that works in one zone points elsewhere in the next: move in short steps with a `shot` after each.

### Session 6, continued: crash at the first boss scene (fixed, verified in game)

- `FATAL: branch to unknown code 00521d88 from 00520308` right after the boss door scene (libc++ `std::__sort`
  helper at 0x5216bc, switch on a range length 0..5). **Lifter bug:** `rel_table` took the table size from the first
  `cmp rX, #N` found scanning backwards from the `ldr`, but the table block (0x521c40) is only reached by a branch
  (`cmp r0, #5; bls 0x521c40` at the function start); the scan crossed an unconditional `b` and found an unrelated
  `cmp r0, #4`, so case 5 (0x521d88) was never lifted. Fix (`lift.py table_bound`): the scan stops at a block end; if
  the block is a branch target, the bound comes from the `cmp` before the `bls`/`blo` that jumps there. Same fix in
  `jtab_count`. Measured over the whole image: 25 tables changed, 24 grew 5 -> 6 (the same libc++ sort switch,
  inlined in many places; all were missing their last case), 1 went unbounded -> 5 (same targets). Verified: generated
  `f_011.c` now has `case 0x00521d88u`, and the game went through that scene into the first battle.
- `test_a32.py` without `--only` no longer stops at class `game` (that class needs `--only game --link ...`).
  Current result: all classes clean except the known MRS mode bits (misc) and one NEON vmla rounding case.
- `drive.sh` accepts commands with arguments: `ls 0 32767 2000 ; 1` (command ; seconds).
  `tools/drive/gate_to_boss.txt` replays slot 1 -> Upper Lv reliably; past that the timing drifts (stick moves are
  timed by sleeps), so drive by screenshots after that point.
- The battle (Itsuki vs Blob, Tiki portrait, turn order bar, Chrom/Tsubasa Mirages), level-up to 2 and the
  "Making the Most of the Map" help all rendered correctly (`private/tms/m2_first_battle.png`).

## Milestone 2, session 7 (2026-10-23, agent alone overnight): texture mips, sampler borders

Verified in game (slot 2, Observatory Inside; before/after crops `shots/crop.png`, not kept):
- **Mip levels of packaged textures were mis-untiled** (far floor tiles crumbly/dark grout; `NX_LOD0=1`, a new debug
  switch that samples level 0 only, made them clean, which proved the mip data was bad). Cause: offline textures pass
  their block height through `nvnTextureBuilderSetPackagedTextureLayout` (driver @0x21be4cc): builder +0x48 halfword,
  bits 0-3 = 1 (valid), bits 4-7 / 8-11 / 12-15 = the layout's three nibbles (bits 4-7 = log2 GOBs per block in Y;
  the others assumed Z / tile X). We always started from 16 GOBs. Now `Texture::layout`, `block_height_max()`;
  per-level shrinking starts from it (upload and `storage_size`). Layouts seen: 0x01, 0x11, 0x21, 0x31, 0x41 (logged
  once each: `nvn: texture layout ... first seen`). After the fix the floor is clean at all distances.
- Array textures: guest layout is layer-major (all levels of layer 0, then layer 1), each layer aligned to a level-0
  block (Ryujinx SizeCalculator.AlignLayerSize). We read level-major. Fixed in upload and storage_size; only one
  array texture seen so far (128x128 fmt 0x29), so not visibly tested.
- Sampler border colour (builder +0x2c..0x38) is now applied (Vulkan's fixed colours; others logged). Shadow sampler
  (compare LESS, clamp to border) has border 1.0 = lit outside the shadow map. No visible change in this scene.
- `drawlog` prints each bound texture's sampler (id, min/mag, wrap, compare, border, aniso, reduction).
- Not a bug (assumed): the outer floor of Observatory Inside breaks up into irregular pixel-edged holes that show the
  void below; not grid-aligned, unchanged with `NX_NO_KILL`, looks like an intended noise dissolve.
- Shadow maps: depth textures fmt 0x35 (1024x2048, 1024x1024), sampler 261.
- Tools: `bmp2png.py --crop x0,y0,x1,y1 --zoom n`; `tools/drive/load_slot.sh [slot] [speed]`; `private/tms/s.sh`.
  System python has no PIL (s.sh's resize is a silent no-op; shots stay 1280x720).

### Session 7: input record / replay (milestone 3), verified 2026-10-23

- `NX_RECORD=<file>`: writes the pad state the game reads (`nn::hid::GetNpadState`, player 1 full key), one line per
  change: `<read index> <buttons hex> <lx> <ly> <rx> <ry>`; flushed per line (survives a crash). Keyed by the game's
  read count (one per game frame), not wall time. The previous run's file is archived to `logs/` like the logs.
- `NX_REPLAY=<file>`: the game reads the recorded states until the file ends (`input: replay finished at read N`),
  then live input resumes. Live keys/pad are ignored while replaying.
- **play.bat now sets `NX_RECORD=input.rec`**: every user run leaves its input next to its logs, so a reported bug
  can be replayed: `NX_REPLAY=logs/input_<time>.rec`.
- Verified: recorded title -> LOAD slot 2 -> two stick moves at x2 speed (9 changes, last at read 1910); replay in a
  new run (no live input) ended on the identical frame (same position/camera, compared screenshots by eye).
- Limit (assumed, not measured): pad reads during loading depend on load speed, so long replays across many loads may
  drift. Saves are not reset by a replay: replay from the same save state as the recording.

### Session 7: 60 fps check (milestone 4), measured 2026-10-23

- `NX_PRESENT_INTERVAL=1` (60 presents/s of game time) with the same game-timed stick moves (`ls 0 -32767 1500`,
  `ls 32767 0 1000` after loading slot 2) moved Itsuki about **twice as far** as at the game's own interval 2 (minimap:
  past the round hall's south edge vs inside it). So field movement is per frame, not delta time: forcing interval 1
  makes the game run at double speed. Real 60 fps needs the game's frame step found and halved (where the game turns
  its present interval 2 into a per-frame step; candidates: the code around `nvnWindowSetPresentInterval` callers,
  a "frame rate"/"vsync count" global read by the field/battle update). Not started.
- Lead (verified 2026-10-23): the game calls `nvnWindowSetPresentInterval(2)` once at boot from **0x004faeb4
  (nnMain+0x20f14)**; the log line `nvn: present interval 2 (lr ...)` now names the caller. Start milestone 4 there:
  see which global the same code fills with the frame step (2 vsyncs) and who reads it in the field/battle update.

## Milestone 2, session 8 (2026-10-23, agent alone): Lua log, door "bug" was not a bug, frame step

### Game script log (verified 2026-10-23)
- Lua bindings AtPrintf/print/AtConsoleOut/AtTraceOut are `mov r0,#0; bx lr` in retail. Hooked (names.txt
  lua_AtPrintf etc.): every script trace now appears as `[lua] ...`. Map loads print e.g.
  `[GimmickInitializeScript] initialize!!` + the map id (slot 2 = **d002_02**), door warps print
  `[ PlaySE_d002_door ] initialize!!`. Script errors: `script_error` (0x5b4ca8) and `luaG_errormsg` (0x530440) probes
  log `[lua error] ...` (none seen so far). These lines reach issues.log through the "error" keyword.
- Map/event data: `Map/dungeon/d002/d002_0N/model.apak` (pack_000_map), event tables
  `Event/field/script/dungeon/<d>/<map>/eventTable.tbl` (pack_030_etc): header 0x60 bytes, entries 0xa0 bytes
  (folder 0x40, script name 0x40, ints: type, flag that must be ON, flag that must be OFF; -1 = none). d002_02:
  default_in (0x40e on), m0009_01 (0x410 on, 0x412 off), MAP_TUTORIAL (0x412 on, 0x8831 off), m0007_01 (0x40e off).
  The prologue dungeon is d002 (Illusory Daitama); d001 has only stub event scripts and no map.
- Messages: MSBT is UTF-8 here (header byte 0x0c = 0). Common/MapMessage.msbt has the gate texts (`Gate_out` =
  "Looks like this leads outside..."), AutoMapIconHelp.msbt the minimap legend.

### Slot 2 "stuck" (not a bug, verified)
- The `!` balloons on the doors are only markers. The interaction prompt ("(A) Exit") appears at the bottom of
  Itsuki only when he stands directly in front of a door facing it; without the prompt A does nothing (coverage
  diff over a 3 s window: no function ran only in the A window). The north door had no prompt from any angle tried
  (assumed: locked in this story state). The east door works (see RESUME). Session 7's "lift did not react" is
  probably the same thing (not re-tested).
- Seen while walking (by eye, no comparison with hardware): menu, Topic (Main Story / Contacts / Map / Icon Help),
  Lower Lv corridor with flames, waterfall and city backdrop all render correctly; no new issues.log lines.

### Milestone 4: frame step (measured 2026-10-23)
- Present path: 0x55d3b4 reads the interval from `gfx+0x58c0` and calls the present wrapper 0x4fae68 (which calls
  nvnWindowSetPresentInterval only when it changes). Setter 0x55d72c (names.txt gfx_set_present_interval), called
  with 2 from 6 places (0x248ffc ... 0x4da3c8, a scene state machine) and with **1** from one (0x2494bc, scene type
  unknown). Getter 0x55d51c (gfx_get_present_interval) is read by 0x203150 and 0x5c0508, which use
  `float(n)` (0 -> 1) as a per-frame time step, and by 0x246318 (stores it at manager+0x10 every update).
- New `NX_GAME_INTERVAL=n` forces the setter value. With n=1 the game presents 60 frames per second of game time
  (`frames: 119.8/s` at NX_SPEED=2), but the same stick input (`ls 0 -32767 1500`, `ls 32767 0 1000` after loading
  slot 2) moved Itsuki about twice as far as with the game's 2 (screenshots by eye, minimap past the room's south
  edge vs inside it). So **player movement is a fixed amount per frame**; only some animation updates use the step.
  Real 60 fps therefore needs either (a) the movement/camera/NPC updates scaled by step/2 (find them, e.g. with a
  coverage diff idle vs moving), or (b) logic kept at 30 Hz with interpolated extra frames (hard with replayed NVN
  command buffers). Not decided; NX_GAME_INTERVAL stays an experiment (default off, game behaviour unchanged).
- Coverage diff idle vs walking (slot 2, 2.8 s hold, measured 2026-10-23): 712 functions only while walking, most in
  0x5e0000-0x6a0000 (CRI audio: footsteps). About once per frame (85-98 calls): 0x205764, 0x3a2efc, 0x3c8734,
  0x409348, 0x40b6fc, 0x40c0e0, 0x40c5c4, 0x411648, 0x549940. 0x40c5c4 -> 0x411648 is a stick-history check
  (input ring buffer at obj+0x1c, 20-byte entries), not the position update. Not followed further yet.

### Session 8, later (2026-10-23): one-way corridor, north door lead
- Verified: after the east door, the Lower Lv corridor toward the elevator stops at the minimap's one-way arrow
  (several tries from both camera zones; Itsuki walks into a wall at the same spot). So slot 2's way on is not the
  elevator. North door: no "(A)" prompt from straight in front (load position + 1.2 s north), walking into it for
  4 s only plays footsteps.
- Lead (assumed): automap tutorial trigger `T_MAPSYSTEM` in the d002_02 layout, see RESUME HERE.
- Exe rebuilt without probes at the end of the session (normal build).

## Milestone 2, session 9 (2026-10-23 evening): game flags, player position, slot 2 unstuck

### Game flags (verified 2026-10-23)
- Story/system flags are bits at `flags+0xa4` (flags object pointer at 0x9ef37c -> global). C functions behind the Lua
  bindings: flag_on 0x351c94 (FlagOn binding 0x42fac8), flag_off 0x354674 (0x42fbd0), is_flag_on 0x353568
  (0x42fcd8). Binding tables in main are {name, function} pairs (file offset + 0x200000 = runtime address).
- Names: `ScriptCommon/Flag/Flag{Eva,Evc,Evm,Evs,Map,Sys}.lua` are compiled Lua that assign `FLG_* = n` globals;
  `tools/lua/flagnames.py` decodes them (LOADK/SETTABUP) into `private/tms/flags.txt` (12459 names). The runtime
  reads that file: every change logs `[flag] on 0x412 FLG_EVM_0009_01`; control `flag n` logs, `flag n 0|1` sets.
- Slot 2 flags: 0x40e, 0x410, 0x412, 0x8831 (FLG_MAP_TUTORIAL_AUTOMAP) all ON, so session 8's automap lead was wrong.

### Story triggers (verified 2026-10-23)
- `Event/Event_MapLayoutEventTable.bin` (pack_030_etc) maps layout triggers to story events: record =
  (map kind, dungeon, floor), trigger id, flag that must be on, ?, flag that must be off, script name. Examples:
  m0009_02 = d002_01 trigger 8 (layout record type 0 id 8 at (330,55,-760)), on 0x412, off 0x456; m0009_04 = trigger 6
  at (-520,-240,-676), on 0x3e13; m0010_00 = trigger 0x385 (type 0xc door at (710,71,-167.5)), off 0x413.
  The per-map `eventTable.tbl` only holds on-load events.
- `tools/lyts.py <model.apak>`: LYTS block = "LYTS", version 9, record count, header size; records 0xa0 bytes: type,
  flags, id, pos xyz, size xyz, rot y, ints (doors 0x16: map kind/dungeon/floor + target entry id), string offsets
  (relative to the LYTS start; flag names, script names). Types seen: 0 trigger, 1 entry point, 2 level link, 4/5/8
  spawns, 0xc door marker, 0x15 lift ends, 0x16 door, 0x1e free event box.

### Player position
- `pos` control command: player actor = chrGetPlayer's lookup (field global 0x9f47f4, handle at +0x1f4, actor list
  object 0x9f4510: nodes at +4, next +4, actor +8, id +4; tag 0x514c4742 at actor+8, xyz at actor+0xc). Coordinates
  are the layout's; -z = north. First version dereferenced the list pointer once too often and crashed (fixed; reads
  are now range-checked with mem_query).
- `tools/drive/goto.py X Z`: closed-loop walk; the stick->world rotation is re-learned from each step's movement
  (stick up = world north when the camera looks north; world uses (x, -z) so the map is a rotation, not a mirror).
  Limit: straight line only, no path finding; walls stop it ("stuck").

### Seen, not fixed
- `[lua error] RUN DeleteEffect: Effect Not Active...` twice during m0009_02/03 (a script deleting an effect that
  already ended; assumed harmless, no visible problem).

## Milestone 4, session 9 (2026-10-23 evening): frame pacing at 30 fps (verified by log stats)

Work split from 2026-10-23 (user decision): the USER navigates/plays the story; the agent works on features that need
no navigation (60 fps, pacing, audio sync, settings) and fixes from the user's logs.

- Measured before (slot 2, idle, speed 1, display 3840x2160 @ 160 Hz): 30.0 frames/s but worst present gaps 41-73 ms
  every 10 s. Causes, one by one (each measured with the new stats):
  1. FIFO swapchain with 2 images: acquire/blit/present blocked the game thread up to 29-38 ms, and FIFO beat against
     our own 60 Hz timer. Now mailbox (NX_PRESENT_MODE=fifo|mailbox|immediate), 3 images.
  2. The present blit waited on the acquire semaphore (the display releases images late under DWM): moved to
     present_thread on a second queue of the same family (NX_SYNC_PRESENT=1 = old inline path). The game thread only
     copies the frame into one of 3 staging images. Acquire uses a CPU fence, not a GPU semaphore wait.
  3. Staging can finish up to ~15 ms after the frame's tick (the game queue is shared with the next frame's work), so
     present_thread shows each frame exactly NX_PRESENT_DELAY ticks (default 1) after the game released it.
  4. The vsync clock itself fired up to 20-36 ms late: with the test window in the background Windows ignores
     timeBeginPeriod(1); the high-resolution waitable timer and Sleep(1) both overslept, even with power throttling
     turned off (SetProcessInformation succeeded) and HIGH_PRIORITY_CLASS. The clock now has its own TIME_CRITICAL
     thread that spins (one core busy; NX_VSYNC_SPIN=0 = sleep until 3 ms before, then spin) on an absolute,
     drift-free schedule. SDL event pumping is no longer in that loop.
- After (same test, 60 s): vsync clock max late 0.0-0.15 ms; `present:` 300 per 10 s, gaps 32.9-33.7 ms, 0 frames
  off-cadence (more than 4 ms from 33.3) in 3 of 4 windows, 2 of 300 in the other (present_thread woke 11 ms late).
- Stats lines (every 10 s): `frames:` (game side: late vsyncs, longest frame, present blocked), `present:` (what the
  display gets), `vsync clock:` (clock health). Commit df9af33.
- Audio: nn::audio output is clocked by real playback (SDL), the system tick is real time, so the game's movie and
  voice timing follow real time; cutscene drift can only come from frames slower than 33 ms (none in this test).
- Not verified by eye on the user's screen yet (judder is a visual judgement; the user should compare).

### 60 fps: findings and options (not started)
- The game only asks for interval 1 on loading screens (log: `frame step: game asks for interval 1` between map
  loads), so gameplay was never built for 60. Lua `WaitForCnt(n)` (EventUtility) yields n frames; `WaitForTimer`
  uses `GetUpdateTime` (time). Event cameras/moves are frame-counted, player movement is a fixed amount per frame, and
  only 3 functions read the frame step (0x203150, 0x5c0508, 0x246318 -> manager+0x10).
- Option A, game logic at 60 Hz (NX_GAME_INTERVAL=1 + halve every per-frame quantity): hundreds of places (movement,
  cameras, effects, UI tweens, Lua frame counts, battle timing); any miss = double speed or audio desync.
- Option B, logic stays 30 Hz, the renderer adds one interpolated frame between two game frames: needs per-frame
  capture of command lists and snapshots of the constant buffers (we replay against live guest memory today), draw
  matching between frames, and interpolating matrices only (not other cbuf data). Audio/cutscene sync stays exact.
  Adds one frame (33 ms) of latency.

## Milestone 4, session 10 (2026-10-23 night): 60 fps game logic and uncapped frame rate

User decision 2026-10-23: real 60 fps game logic (option A), plus an unlimited mode "without breaking things".

### How the game times itself (verified by decompiling, Ghidra headless project `private/tms/ghidra`)
- Decompile: `analyzeHeadless.bat <dir> tms -process main.bin -noanalysis -readOnly -scriptPath <dir> -postScript
  Decomp.java <dir> 0xADDR...` -> `<dir>/out.c` (main.bin = main module image at 0x200000; CreateFuncs.java seeded the
  lifter's 19269 function starts before auto-analysis).
- Insight from the Wii U version's Cemu "60FPS" graphic pack (description only, no code used): the engine is mostly
  time based; it passes a constant frame time 1/30 s. On Switch that constant is in **31 literal-pool words**
  (0x3d088889, read by vldr -> real memory loads, so the runtime can rewrite them) plus two movw/movt copies
  (0x363314: the global 0x9f4498 that Lua `GetUpdateTime` returns; 0x3f8d34). Users: camera orbit 0x5c4f84, tween
  manager 0x2314d0, player movement 0x40b594/0x40b6fc, timers, event/battle states. One unclear use: 0x3f27b8
  `x / (y * dt)` (kept in the list; bisect it if something is off).
- The animation manager 0x5c0508 steps float(present interval) 60 Hz frames x speed (+0x98), so it is right at
  interval 1. 0x246318 stores the int interval at game manager (global 0x9f3738)+0x10 for objects updated through
  virtual calls (readers not found yet). `x / (1/60)` literals (0x555b94...) convert seconds to 60 Hz frames (content).
- Frame-counted parts found and fixed: Lua event scripts (WaitForCnt yields once per frame; `script_resume_all`
  0x5acac0 resumes all scripts of one manager, called for several managers per frame; lua_resume = 0x531124), screen
  fades (`fade_update` 0x20ba14: progress += 1/frames, frames = seconds*30 from FadeOut/FadeIn), walk speed smoothing
  (v = 0.8 v + 0.2 target per frame, literals 0x40b690/0x40b68c and 0x40b7f4/0x40b7f8).

### What the runtime does (hle_sys.cpp "frame step", ui.cpp pace_present)
- `NX_FPS=30` (default): unchanged game. `NX_FPS=60`: interval forced to 1, dt literals = 1/60. `NX_FPS=N > 60` or
  `0`: interval 1, no vblank pacing (present_thread shows frames as they come, mailbox), each frame's dt = measured
  time of the previous frame, clamped to [1/1000, 1/30] (slower than 30 fps slows the game, as on the Switch); N caps
  with sleep + spin.
- dt changes: the 31 literals, smoothing keep^(dt*30), scripts resumed once per 1/30 s of game time (per manager
  accumulator), fades scaled by dt*30, animation speed scaled by dt*60 (variable mode only). Hooks use
  `call_unhooked`, now per thread via `Cpu.hook_bypass` (HOOK macro clears it and runs the guest code).
- Lifter: `MOVT_LOADS` (movt -> load of the function's 1/30 literal), generated files written only when changed
  (a lift + build after a hook change takes ~1 min; guest.h changes rebuild everything in ~40 s).

### Measured (slot 2, `tools/drive/walk_speed.sh`, `tools/drive/event_timing.sh`, `NX_LOG_TIME=1`)
- Walk 1 s north: 30 fps 49.9 units (deterministic); before this session 60 fps ran ~2x; now 60 fps 48.2-49.2,
  uncapped (138 fps) 48.7-49.0. The small spread is the stick hold edges.
- Door -> map unload: 30 fps 0.43 s; 60 fps 0.22 s before the fixes, 0.38 s after; uncapped 0.36 s (within one 30 Hz
  script/fade step).
- Uncapped reaches ~138-140 fps in the slot 2 field on this PC (CPU bound); present gaps show occasional 30-60 ms
  hitches (not investigated).
- Not tested: battles, menus, voiced cutscenes, effects, anything driven by the int step at 0x9f3738+0x10.

## Milestone 4, session 11 (2026-10-23 late night): 60 fps fixes from the user's test, borderless, 4K

User report (2026-10-23, play60.bat and play_uncapped.bat, session 10 build): smoother, but (1) treasure pickup shows
Itsuki in T-pose for a split second, (2) field enemies dash far too fast, (3) battle attack/skill animations play too
fast and out of sync. Same in 60 and uncapped.

### Findings (verified by decompiling + runtime probes on a replay of the user's 60 fps run, logs/input_20261023_222809.rec)
- Skeletal animation is time-based: model_anim_update 0x5563c8 / 0x555ab0 advance frames by dt / (1/60); every caller
  passed dt = 1/60 at NX_FPS=60 (`NX_ANIM_PROBE=1` logs callers + dt; the g3d play policies 0x4e3974 loop / 0x4e3958
  once give every frame-controller step). The effect manager 0x5c0508 is particles (4 layers), not characters.
- Action timelines are Lua: the action manager 0x5b9144 (battle/field actions, cuts) sets `info.delta` = dt x speed
  (lua_set_number 0x5acfdc) and resumes its scripts; ScriptCommon/Action/Utility.lua waits by summing info.delta per
  resume. Session 10 resumed scripts once per 1/30 s but left info.delta (and GetUpdateTime, global 0x9f4498) at 1/60:
  timed waits ran at half speed against full-speed animations = the battle desync / pickup T-pose (assumed for the
  pickup: same action system). Fix: script_resume_all scales info.delta and UPDATE_TIME by the frames since that
  manager's last resume.
- Field enemies: EnemyServerParam.lua values (speeds per frame, frame counts) are copied into a table (store 0x3e54c8,
  getter 0x3e30d8, 0x18c bytes, map: ghidra/parammap.py); performers read speeds at state changes (0x3ef5ac normal
  move, 0x3f094c discovered move/charge/escape; found with the new `watch` command). Fix: the getter hook serves
  speeds x dt*30 and frame counts / (dt*30) from a pristine copy (refreshed on store). Replay: battle contact moved
  from 44 s to 49 s (enemy slower), log `field enemy speeds x0.500, frame counts x2.000`.

### Borderless and resolution
- `NX_WINDOW=borderless` = SDL borderless fullscreen; Alt+Enter / F11 toggle (ui.cpp).
- `NX_RES` / `NX_RES_SCALE`: integer scale of render targets (NVN flag 0x8 compressible + 2D; assets are 0x4, movie
  planes 0x14). The game renders 1280x720, so 4k = 3x. Viewports, scissors, texture copies scale; buffer -> scaled
  texture copies are skipped and logged (none seen); pool uploads never go into a scaled target.
- Ryujinx's translated shaders read a support buffer at set 0 binding 0 (gl_FragCoord / render_scale[0], texelFetch
  and textureSize scales). It was NEVER bound before this session (no layout binding; compute cbuf 0 also used
  binding 0): undefined reads, e.g. a tiled shader dividing gl_FragCoord by render_scale[0]. Now: sidecar compute
  bindings start at 6*256, every layout has binding 0, bind_resources writes per-draw scales (distinct contents cached
  in a host-visible buffer, vk_replay.cpp support_buffer).
- Measured (replay, slot run to the first battle): 1x and 3x both ~46-55 frames/s at NX_FPS=60 with load hitches, so
  4K is not the limit (CPU side is). Screenshots shots/r3a.png (field), r3b.png (battle) at 3840x2160 look right.

### Tools added
- NX_CONTROL `watch addr len [r]` / `watch off` (main.cpp): guard page + single step, logs the generated function
  (F_<guest addr>, dbghelp + tms.pdb) touching guest memory. `NX_LOG_IMAGES=1`: every image created.
- `tools/lua/luadis.py`: Lua 5.2 bytecode listing (the game's scripts are little-endian despite the header byte).
- Ghidra headless helpers in private/tms/ghidra: `g.sh Decomp|Xrefs addr...`, `armdis.py`, `pcref.py`, `findld.py`.

## Milestone 4, session 12 (2026-10-24, stopped for usage limit): battle sync root cause, WIP

**RESUME HERE (session 12).** Uncommitted work in runtime/src/hle_sys.cpp, ui.cpp, rt.h, tools/recomp/names.txt.
Build compiles. NOT given to the user yet.

User report (session 11 build, 60 + uncapped, logs/live_20261023_232332.log = 60, logs/live_20261023_23xxxx uncapped
= previous live.log): chest T-pose flash still there; battle attack/skill/session still too fast and out of sync; 4K
not sharp (textures, text, people soft); halo artifacts around characters/objects; fps drops (needs optimization).

### Battle sync: root cause FOUND (verified by cue timings)
- Measure: CRI log lines `ExPlaybackId ... Cue:<name>` = sound start times. `/tmp/cues.sh` equivalent:
  `grep ExPlaybackId log | sed -E 's/.*CRIATOM, ([0-9]+),.*Acb:([A-Za-z_0-9]+), Cue:([^,]*).*/\1 \2 \3/'` (us).
  Reference 30 fps: logs/live_20261023_181459.log. bt_attack_<chara> (voice at cut start) -> bact_flex_* (swing):
  30 fps 0.67-0.78 s; 60 fps 0.33 s; uncapped 0.25 s. Enemy beatk_blob -> bact_meet: 0.82 vs 0.27-0.32. Magic
  chant05 -> bska_bufu 1.10 vs 0.53.
- dt of action_update / action_group_update / cut_update is correct (1/60, probes). Cause: **battle sequence tasks**
  (vtables 0x7d6eb0..0x7d9xxx, step fn 0x2d0268 = `btl_task_step`): delay +0x10 in 30 Hz frames (17, 20, 21, 47...),
  minus +0x20 (always 1) per update, one update per game frame. Found via `NX_CUE_TRACE=Cue:bact_flex` stack scan:
  scheduler 0x5bddd0 (`task_run_phase`) -> 0x2d0014 (`btl_seq_update`, root) -> 0x2d03ac children -> 0x2d0268.
- Fix in code now: `frame_begin()` (called from pace_present) keeps a 30 Hz tick clock `g_ticks30`;
  `btl_task_step` hook skips the call on non-tick frames while delay > 0 and not done. Result: cue timings match 30 fps
  (Itsuki swing 0.665 vs 0.668, Tsubasa 0.68-0.70, enemy 0.85, bufu 1.05-1.09).
- **OPEN PROBLEM: crash** with the gating (not without): ~1 in 2 replay/mash runs, `btl_apply_action` (0x304664)
  called with a stale action record (seen 3x: actor 1, target 4, skill 0, +0x68 = 84, during Tsubasa Dia /
  bskre_dear) -> unit lookup 0x2b4c2c returns null -> null deref (guest addr 0 or 0x818). Ungated: 0 crashes.
  Meaning: a delayed task outlives its action record; something else in battle decides "action done" earlier than at
  30 fps. Tried gating the whole tree at btl_seq_update: also crashed AND turn changes got 40% slower (2.8 s vs 2.0 s
  at 30 fps; ungated 60 already matched 2.0) -> reverted to delay-only gating.
  Next ideas: (1) check IsFast/fast-forward (mash presses A; maybe fast mode makes the cut end early while gated tasks
  wait; check whether +0x20 > 1 in fast mode); (2) find who frees the record (hook game free, or `watch` the record
  address from the apply probe); (3) measure cut end vs task completion (cut_update 0x5bc10c: +0x20 = -1 when done);
  (4) band-aid: in btl_apply_action, skip if actor/target unit lookup is null (log it).
- Test rigs (private/tms): `analysis/cut2110.rec` (user 60 run cut at battle start) + `analysis/mash.py ctl log seed
  secs` (random battle buttons after replay end); `analysis/cut4416.rec` (after first battle, field, for the chest).
  Run 2-4 instances in parallel with separate NX_LOG / NX_CONTROL (PowerShell Start-Process, see session 12 commands:
  NX_FPS=60 NX_RES=720p NX_LOG_TIME=1 NX_REPLAY=...). Saves unchanged since 21:29 10-23, replays valid.
- TEMP code to remove before commit: env `NX_OFF_BTL`, `NX_OFF_FRESH` toggles; probes `btl_apply_action`,
  `task_run_phase` (logs [btl]/[task]); replay "replay at read N" log every 300 reads (keep? useful for cutting).
  Keep: `NX_CUE_TRACE=<text>` (stack scan of a game log line), probes action/cut dt (NX_ANIM_PROBE).

### Chest T-pose (NOT reproduced yet)
- Hypothesis + code: script_resume_all now resumes a manager immediately when it has a new script (node +0x10 == 1)
  so an action's first resume (plays its anim) is not delayed to the next 30 Hz tick. Unverified; disabled by
  NX_OFF_FRESH in crash tests. Chests in d002_01: layout type 0x14 at (-447,-240,-383), (-80,-240,-380),
  (900,50,-380). Plan: replay cut4416.rec, goto.py to a chest, NX_SHOT_EVERY=1 around the A press, look for T-pose.

### Graphics / performance (not started, findings only)
- Only targets with NVN flag 0x8 + 2D are scaled (vk.cpp image_of). Unscaled intermediate targets -> soft image;
  mixed scaled/unscaled passes -> likely the halos. Next: 4K run, NX_CONTROL `rt` dump, list targets + sizes.
- Perf: vk.cpp end_and_wait waits for the GPU after EVERY submit (and present_async copy); syncs are fake
  (nvnSyncWait returns signaled). At 4K uncapped 65-75 fps vs 138 at 1x = GPU time serialised with CPU. Plan: ring of
  command buffers/fences/staging/descriptor pools, real NVN syncs (queue fence -> submit serial). Hitches 100-500 ms:
  no shader/pipeline disk cache (sidecar translation + vkCreate*Pipelines each run, VK_NULL_HANDLE cache) -> add
  SPIR-V disk cache + VkPipelineCache file.

## Milestone 4, session 13 (2026-10-26): skill/session crash at 60 fps fixed

User report (2026-10-26, session 12 WIP build edadae8, play60 + uncapped): battle sync and pacing better, but using a
skill in battle crashes, and so does a session skill. Same as the open session 12 crash. Their run: logs/live_20261024_
044450.log + private/tms/live.log (Tsubasa Dia, `btl_task_step+0x8ecc`, guest address 0); its input recording
(analysis/crash0444.rec) does not replay into the battle (desyncs), so the session 12 rig was used.

### Root cause (verified by probes, logs in private/tms/crashlogs/)
- The apply task (vtable 0x7d8458: +0x30 battle object, +0x34 action record, +0x38 = 0x2d6860 calls
  btl_apply_action, flag record +0x2d0) waits its delay (Dia 61, Zio 54, Bufu 43 ticks; attacks 20-26). The record is
  a plain struct owned by an **action process** (vtable 0x7d56a0, record at +0x48, destructor 0x2879b8 delete[]s it).
- Battle processes are a second task system (0x27fdb8 root -> 0x280514 list: vt+8 update, +0x10 done, +4 delete). Base
  class: state +0x10, **state timer +0x18 += step +0x34 per update** (0x28042c, after the state's work; 0x28041c sets
  state and zeroes the timer). The action process is done when its timer reaches +0x50 + 7 (0x287b30) and an effect is
  finished. At 60 fps the timer ran 2x: the action process ended ~50 ticks after the skill started, freed the record
  (heap free 0x5a8ea0 via _ZdaPv 0x5a8864, caught with a probe), the heap reused it (HUD widgets 0x2f62f0 / 0x2f50a4
  allocate 0x40-byte objects there), and the delayed damage task applied garbage -> null unit -> crash. Short attacks
  fired before the free, so only long skills (and sessions, same flow) crashed. Ungated 60 fps (session 11) did not
  crash because the damage came 2x early too.
- Fix: hook `btl_proc_advance` (0x28042c): advance the timer only when a 30 Hz tick has passed since that process's last
  advance. The battle task gating was also changed from "step only on frames with a tick" to the same per-object rule
  (`tick_due`, map object -> last tick, g_tick30 = 30 Hz ticks of game time from frame_begin): tasks are not stepped
  every frame, so the old test could miss ticks (a delay-61 task that never fired was seen once).

### Verified (replays of analysis/cut2110.rec + analysis/mash.py, 4 instances at a time, NX_FPS=60 NX_RES=720p)
- Before: 11 crashes in ~24 runs (always at the apply of a long skill). After: 0 crashes in 12 runs with ~60 long skill
  casts (Dia, Zio, Bufu, items).
- Timings match 30 fps (30 fps reference logs/live_20261023_181459.log): swing after attack voice 0.65-0.85 s (30:
  0.67-0.78), enemy 0.82-0.95 (0.82), chant -> Bufu 1.07-1.08 (1.08-1.13), chant -> Dia 0.78-0.97 (0.83-0.92); action to
  next action ~2 s as at 30.
- NOT verified: uncapped (NX_FPS=0) and session skills. A 60 fps recording desyncs at a variable frame rate (replays are
  keyed by pad reads, the game step differs), so uncapped needs a user test; no session happened in the mash runs.
  30 fps is unchanged (both hooks pass straight through at NX_FPS=30).

### Tools added / removed
- `rt::guest_chain()` (main.cpp): guest call chain from the generated functions on the host stack; the `watch` log
  prints it (`[watch]   chain ...`). Useful with probes: `log(..., guest_chain().c_str())`.
- Test helpers used (scratchpad, not in repo): run.ps1 (one replay instance), batch.ps1 (4 mash runs + crash summary).
- Removed the session 12 TEMP code: NX_OFF_BTL / NX_OFF_FRESH, the btl_apply_action probe, the record watch/trace.

### Still open (from the user's session 11/12 reports)
- Chest pickup T-pose flash (not reproduced; fresh-script resume in script_resume_all is the untested candidate fix).
- 4K not sharp + halos around characters (only NVN flag 0x8 + 2D targets are scaled; see session 12 notes).
- Performance (per-submit GPU wait, no shader/pipeline cache; see session 12 notes).

## Milestone 4, session 14 (2026-10-26 day, agent alone; user asleep, asked for T-pose, 4K, stutter, optimisation)

**NEXT (resume here):** chest/pickup T-pose (step 3 below), then a user-facing summary. Helper scripts were copied to
`private/tms/agent_scripts/` (run.ps1, batch.ps1, to_field.sh, sheet.ps1, goto_t2.py; they reference the old scratchpad
path C:/Users/user/AppData/Local/Temp/claude/C--Users-user/ad6e1a5c-.../scratchpad: edit the paths to agent_scripts).

Safety net: scheduled task `tms-recomp-overnight-resume` (every 30 min) resumes the work in a new session when
private/tms/AGENT_HEARTBEAT.txt is older than 40 min (stops after 2026-10-27 12:00 or if private/tms/AGENT_STOP.txt
exists). Test helpers (scratchpad, recreate if lost): run.ps1 = one replay instance (`run.ps1 tag rec K=V...`), batch.ps1
= 4 mash replays + crash summary.

### 4K softness + halos: FXAA constants (fixed, commit 773c670, verified by 4K screenshots)
- Frame (tools/drawlog_passes.py on a drawlog): scene HDR (B10G11R11) -> bloom (320x180 ping-pong) -> DOF (160x120 and
  640x360 blurs + R32F depth) -> pass 15 FXAA -> UI. All render targets were already scaled 3x.
- FXAA reads its pixel size from uniform 1 in 1280x720 units: fragment {0.5/w, 0.5/h, 2/w, 2/h, 1/w, 1/h, 0, 8, 0.01,
  0.01, 0.75}, vertex {1/w, 1/h}. At 3x it filtered 3 pixels wide = soft image + halos along edges.
  `fxaa_rescale` (vk_replay.cpp) finds that block by its values and divides it by the render scale (guest memory, per
  draw; a rescaled block no longer matches). Log: `vk: FXAA pass found`. Edges are crisp now; the DOF blur is the game's
  own look (same at 720p).
- Target dumps (NX_CONTROL rt) now decode B10G11R11 to 8-bit.

### Performance (commit 6064a09)
- Shader translation disk cache `<data>/cache/shaders.bin` (vk_shader.cpp): lookup by hash of the first 256 code bytes
  + inputs, verified by a hash of the translated length + constants; header = NxShader.dll size/time. Pipeline cache
  `<data>/cache/pipelines.bin` (VkPipelineCache, saved every 10 s when new pipelines exist). Frame stats line
  `frames: shaders N translated (ms) + M from cache, P pipelines created (ms)`. Warm run: 0 translations (cold ~680 ms
  over the replay), pipeline time ~4x lower.
- `NX_PROFILE=1` (main.cpp): 1 kHz sampler of the game thread (leaf host function + innermost generated function),
  top 25 every 10 s. Battle at 4K/60 before: game thread ~45% inside the NVN queue submit (0x4fadb8), 20% of all time
  waiting for the GPU after every submit.
- **Asynchronous submits** (vk.cpp): 3 slots (command buffer, descriptor pools, upload ring each), timeline semaphore
  serial per submit, slot reused after its serial; present copy is async too (present_thread waits its serial).
  NVN syncs are real now: FenceSync in a command buffer = the serial of the submit it is replayed in (OP_SYNC ->
  sync_mark), QueueFenceSync = last submitted, SyncWait waits (timeout -> 2), QueueFinish waits all.
  `NX_SYNC_SUBMIT=1` = old behaviour (A/B). Drawlog frames still wait (statistics).
  Result (replay cut2110 + mash, 4K, NX_FPS=60): battle 56-60 fps (was 49-53), field 59-60. Screenshots correct,
  0 crashes in 4 mash runs.

### Load hitches (commit 47e7461, verified by the hitch log)
- New hitch log: every game frame > 50 ms logs its slow work (shader translation, pipeline creation, texture uploads,
  GPU waits, image creation, pool imports, texture write checks, replay + submit total).
- Cause: guest memory pool imports (vkAllocateMemory with a host pointer) 50-120 ms per map/battle load: the game frees
  and re-creates pools at the same addresses and every pool was imported again (old imports leaked). `g_imports`
  (vk.cpp) keeps imports by page range; a new pool inside one reuses it. Result (cut2110 replay, 4K/60): hitches at
  5.6 s, 15.4 s, 38.8 s gone; battle start 196 -> 75 ms (pipelines 12, uploads 11, ~45 ms other replay work); the
  154 ms one at 1.6 s is startup game code. A brand-new shader still costs ~150 ms once (then cached on disk).

### Chest / pickup T-pose (IN PROGRESS, not reproduced yet)
- Debug controls added: `shots N` (capture the next N
  presented frames), `setpos x y z` (moves the player actor, camera follows; works). Contact sheets:
  agent_scripts/sheet.ps1 out.png x y w h cols.
- Field access: agent_scripts/to_field.sh t2 = replay cut4416 + presses through the post-battle scenes -> d002_01 at
  (-499.6, -240, -766.4) after ~220 s (720p, NX_FPS 60). goto is straight-line and gets stuck on walls: use setpos.
- The user's chest open (logs/live_20261023_222810.log, NX_FPS 60) was in d002_01 at game time ~274 s (cue
  fld_treasurebox_ok, landing cue fld_land_grass). Layout chests (type 0x14): (-447,-240,-383) id 1, (-80,-240,-380)
  id 2, (900,50,-380) id 3, (-317,-190,-0.7) id 0x4b0. At (-447,-383) nothing was visible (flag-gated? wrong spot?).
  A golden floating polyhedron near (-520..-540, -600..-640) is visible; A / X near it did nothing yet (ItemGet free
  event (-520,-602) runs "executing!/finalize!!" at once). Next: setpos to the other chests / scan around the polyhedron,
  press A with `shots 120`, look for a bind-pose frame.
- Mechanism hypothesis (ScriptCommon/Map/Gimmick/GimmickTreasureBox.lua, luadis): open_box = chrWaitArmedOffActionEnd,
  chrRotToPos, chrWaitRot, chrPlayAction(ACTION_ID_SWITCH_IN), chrWaitActionEnd, effects + WaitForTimer,
  chrPlayAction(ACTION_ID_SWITCH_OUT), gimPlayAction... At 60 fps the script only resumes on 30 Hz ticks, so an action can
  end on a frame where the script does not run; if that frame renders the actor without an action -> bind pose. Fix
  idea once reproduced: resume a script manager on any frame where one of its actors' actions ended (or treat
  chrWait* polls as time-based and resume every frame).


## Milestone 4, session 15 (2026-10-26 midday, scheduled resume, agent alone)

**NEXT (resume here):** user play test of the session 13-15 build (60 + uncapped, 4K): chest T-pose, battle sync,
skills/sessions. Nothing code-side is open from the user's list; if the user reports the T-pose again, get the save +
time and repeat the test below from that state.

### Chest / pickup T-pose: NOT reproducible with the current build (verified by frame captures)
- Repro rig (private/tms/agent_scripts/chest.sh `<tag>` [env]): loads the newest save, setpos next to the d002_01
  treasure box at (-530.3, -240, -559.1) (golden polyhedron = TMS treasure box), presses A and captures every frame
  (`shots N`): shots/<tag>_open (420 frames: walk-up, SWITCH_IN, open, effects, item message) and <tag>_close
  (message dismissed, SWITCH_OUT, box idle). Contact sheets: `sheet.ps1 <dir> <out.png> x y w h cols start count`.
  Options: `PRE=x` swings the sword first (sets FLG_MAP_TUTORIAL_ATTACK 0x8832, which gates the field attack; it is off
  in that save), `MASH=n` presses A every 0.2 s (first accepted press = earliest moment after the swing, exercises
  chrWaitArmedOffActionEnd). Capturing slows the game, so wall-clock delays between presses are not game time.
- Results (720p): NX_FPS=60, NX_FPS=0 (uncapped, ~42 fps while capturing), NX_FPS=60 with the session 12 fresh-script
  resume disabled (temporary toggle, removed again), NX_FPS=60 sword swing + A mash: every frame of walk-up,
  SWITCH_IN, open, item message and SWITCH_OUT shows a proper pose. No bind-pose frame in ~2700 captured frames.
- **The user's case (chest right after a battle) also tested**: agent_scripts/chest_battle.sh `<tag>` replays
  analysis/cut4416.rec (ends in the first d002_01 battle), presses A/B through the results until in the field, setpos
  to the box (STOP=1 leaves the game running for steering). Itsuki is then in the post-battle armed stance; A on the
  box plays armed-off (sword dissolves, chrWaitArmedOffActionEnd), idle, turn, reach, open: all frames posed (pb3,
  420 frames, NX_FPS=60).
- So the fresh-script resume is not what removed it (no T-pose without it either); the user's reports were on the
  session 10/11 builds. Needs the user's confirmation on the current build.
- Replays of the user's runs desync now (input_20261023_222809.rec: field enemies are dt-scaled since session 11, the
  sword misses; input_20261023_232644.rec at NX_FPS=0: menu key repeat runs faster, the load menu cursor goes to the
  wrong slot).

### Incident: a desynced replay saved over slot 1 (fixed)
- The 232644 replay (wrong load slot, live input afterwards) wrote save/save_1.bin + system.bin at 12:12. Restored
  from save_bak_1023b (md5 63294bb1...); the overwritten pair is kept in private/tms/save_overwritten_1026 (it is the
  state chest.sh was run from: d002_01 by the exit portal; copy it into save/ to rerun chest.sh, restore afterwards).
  **After any replay test, check `md5sum save/*` against save_bak_1023b.**

### Stability (verified)
- 4 parallel mash replays (cut2110 + mash.py, NX_FPS=60, NX_RES=4k, 150 s): 0 crashes, 8-24 battle action cues each,
  53-60 fps with 4 instances at 4K on one GPU.

## Milestone 4, session 16 (2026-10-26 afternoon, scheduled resume, agent alone; commit 5fdc3d0)

**NEXT (resume here):** still the user play test of the session 13-16 build (60 + uncapped, 4K): chest T-pose, battle
sync, skills/sessions. No agent-side item is open from the user's list. A scheduled resume with nothing new from the
user should only re-run a quick check (batch) and exit; do not invent large features (the launcher is the endgame,
after the game is fully playable).

### Performance check, single instance 4K/60 (verified, log p1.log, NX_PROFILE=1)
- cut2110 replay + mash: 59.3-60.0 frames/s every 10 s window incl. the battle; worst gaps 149 ms at 1.5 s (startup
  game code), 74 ms at battle start (pipelines 12 + uploads 10 ms), otherwise < 44 ms. The session 14 figure 56-60
  was 4 instances on one GPU.
- "N pipelines created" (up to ~2000 per 10 s in battle) is not churn: `NX_PIPE_DEBUG=1` (new, vk_replay.cpp) logs
  which key bytes differ from an existing pipeline of the same combo; the differences are vertex attribute formats
  (key bytes 128+) and stream strides = the same shaders drawn with different vertex layouts. Each costs ~25 us
  (driver pipeline cache hit), ~0.5% of frame time. Not worth dynamic vertex input.
- Memory: working set grows to ~4.37 GB in the first ~60 s and stays there (guest RAM + caches), no leak seen.

### Uncapped battles: 0 crashes, timing matches 60 (verified)
- Replays desync at NX_FPS=0 (the cut2110 replay never reaches the battle uncapped), so: new live control
  **`fps N`** (ui.cpp -> rt::set_fps, hle_sys.cpp): switches between 60, capped N > 60 and 0 while running; to/from
  30 is refused (30 has its own pacing without per-object ticks). The fps_setting() caches (anim_update,
  gfx_set_present_interval, pace_present, present asap) read the live value now.
- agent_scripts/uncap_batch.sh `<seed0> <secs>`: batch.ps1 at NX_FPS=60 4K, each instance gets `fps 0` when its replay
  ends (before the battle). batch.ps1 now counts `Acb:Battle` sound cues (the old "apply action" log line is gone).
- Result (4 instances, 4K, 150 s mash): battle cues 59/43/38/38, 0 crashes, 58-75 frames/s each (one 186/s).
- Sync (wall-clock gaps between battle cues): bt_attack_* -> bact_flex_* 0.66 s at 60 and uncapped, r_swing -> r_sword
  0.11 s at both.
- Saves checked after the tests: md5 = save_bak_1023b.

### Scheduled resume check (2026-10-26 15:05, agent alone)
- No new user play logs since the session 16 batch (newest private/tms/logs entry 14:12, agent's own). Git tree clean,
  no code change since f9a86b5, so no batch re-run. Saves md5 = save_bak_1023b. Still awaiting the user play test.

### Scheduled resume check (2026-10-26 16:02, agent alone)
- No new user play logs (newest private/tms/logs entry still 14:12, agent's own), no tms.exe running, tree clean, no
  code change since f9a86b5. Saves md5 = save_bak_1023b. No work done; still awaiting the user play test.

### Scheduled resume check (2026-10-26 17:02, agent alone)
- No new user play logs (newest private/tms/logs entry still 14:12, agent's own), no tms.exe running, tree clean, no
  code change since f9a86b5. Saves md5 = save_bak_1023b. No work done; still awaiting the user play test.

### Scheduled resume check (2026-10-26 18:02, agent alone)
- No new user play logs (newest private/tms/logs entry still 14:12, agent's own), no tms.exe running, tree clean, no
  code change since f9a86b5. Saves md5 = save_bak_1023b. No work done; still awaiting the user play test.

## Milestone 4, session 17 (2026-10-26 evening, scheduled resume, agent alone; commit 1fade7a)

**NEXT (resume here):** user feedback on the session 13-17 build. The user's two runs (below) had no crash and no
written report. Open, small: single dropped vsyncs (25-40 ms game frames) in the first battle; programs re-set at
another code address ("moved code", ~165 per run) still get a new ProgramVk (content-only sharing would need the
constant/vertex-variant reads to stop using the first program's address). Do not invent large features.

### User play runs found in the logs (2026-10-26 18:49 and 18:54, build Oct 26 14:13)
- private/tms/logs/live_20261026_185349.log: NX_FPS 0 (uncapped), battle with skills (jio, bufu, magic chants, attacks,
  enemy dead), 84-170 frames/s, window closed normally after ~4.5 min. First-time content: 22 + 13 shaders translated
  (hitches 221 / 157 / 250 ms from shader translation + pipeline creation).
- live.log (18:54-18:57, not yet archived): NX_FPS 60, battle with skills, window closed normally. 59.0-60.0 frames/s;
  shader cache warm (0 translations); on screen one 33 ms present gap in about half the 10 s windows (1-6 late vsyncs).
- No crash in either run: the session 13 skill/session crash fix holds in the user's own play (60 and uncapped).

### Pipeline churn from re-set programs fixed (verified)
- nvnProgramSetShaders sets p->host = nullptr, so every re-set program got a new ProgramVk (new shader modules) and new
  combos, whose pipelines were all created again. combo_of was also keyed by nvn::Program*, so a program re-set with
  other shaders would have kept its old combo (stale shaders).
- Fix (vk_shader.cpp): program_of shares one ProgramVk per shader set (per stage: code + control address + fnv of the
  first 512 code bytes); combo_of is keyed by ProgramVk*.
- Frame stats now log `programs N new (M moved code) + K shared`. Replay p5 (cut2110 + mash seed 7, 4K/60): ~200
  shared, ~470 new of which ~165 are the same code at another address.
- Pipelines created per 10 s after the first battle warm-up: 50-130 (old build p2: 550-1100); late vsyncs 0 there.
  The first battle still creates 1600-3100 per 10 s (render-state/vertex-layout variants, driver cache hits ~25 us).
- Crash batch 4x150 s 4K/60 mash: 0 crashes (battle cues 65/58/3/54; m3 replay desynced but kept rendering 60/s).
  Battle screenshots at 4K correct. Saves md5 = save_bak_1023b.

### NX_PROFILE spike frames (new, main.cpp)
- With NX_PROFILE=1, every game frame (pace_present to pace_present) over NX_PROFILE_SPIKE ms (default 20) logs its own
  samples as guest function / runtime caller (first tms.exe frame when the leaf is in a DLL) / leaf.
- Findings: a "spike" includes the vsync wait in pace_present (shown as `rt::g_ui_lock / ZwWaitForAlertByThreadId`).
  The real work in the 25-40 ms battle frames is replay in F_004fadb8 (the guest's NVN submit): driver time
  (pipeline creation, nvGetCompilerInterface, unresolved driver symbols), upload_from_pool, image_of waits.
  Runtime-caller names are sometimes nearest data symbols (`t`, `` `string' ``, `nvn::g_st`): treat as unreliable.

## Milestone 5, session 18 (2026-10-26 night, user asked to continue the milestones and check everything)

**NEXT (resume here):** user play test of the settings file / shortcut start (tms.exe directly, without play.bat).
Real icon when J: (the NSP) is mounted: extract the control NCA romfs with nstool, `tools/make_icon.ps1
<romfs>/icon_AmericanEnglish.dat`, delete build/build.ninja, build.cmd. Then the rest of M5 / the launcher (endgame).

### Milestone 4 closed (user decision 2026-10-26: "I already playtested it")
- The user's runs 18:49 (uncapped) and 18:54 (60) are the play test: battles with skills, 0 crashes; issues logs only
  the known harmless stubs (checked again this session: no errors, no unknown warnings in live logs).
- No user run after 18:57. Remaining frame gaps > 40 ms (replay p5) are one per 10 s in the first minute = battle load
  transitions; pipeline creation is 2-76 ms per 10 s in all. Not worth more work now.

### Milestone 5: settings file, data folder, icon, shortcut
- `settings.ini` next to tms.exe (main.cpp load_settings): written with defaults on the first run (fps 30, res 4k,
  window borderless, data commented); `key = value` -> NX_KEY unless the environment variable is set, so play.bat,
  run.ps1 and all test scripts keep working (verified: run.ps1 replay logged NX_FPS 60 + 1x with ini 30 / 4k).
  NX_SPEED and NX_TRACE_CV are read in static initialisers: environment only.
- play.bat no longer sets NX_RES / NX_WINDOW (the ini has the same defaults).
- Data folder: --data > NX_DATA (ini `data`) > `<exe dir>\..` > cwd private/tms > folder picker (SHBrowseForFolder),
  saved as `data = ...` in the ini; a message box if nothing valid (link\image.bin + romfs). Verified: tms.exe started
  from build\ with no arguments found private\tms and wrote the ini; ini fps 60 + env NX_RES=720p -> 60 / 1x.
  NOT tested: the picker itself (needs a click).
- Started without a console (double-click, shortcut): FreeConsole (no console window) and message boxes on fatal()
  and on crash (log path). play.bat and scripts share a console, so no boxes there (they would block test batches).
- Icon: tools/make_icon.ps1 (System.Drawing, 256x256 PNG-in-ICO) -> private/tms/icon.ico; CMake embeds it as
  resource 1 when present; SDL hints WINDOWS_INTRESOURCE_ICON(_SMALL) use it for the window. Verified with a test
  image (ExtractAssociatedIcon showed it), then removed: the exe has no icon until the real one is made.
- tools/make_shortcut.ps1 [folder]: shortcut to tms.exe (default Desktop; tested into the scratchpad only).
- README: status, run without --data, Settings section.

### Checks this session
- Crash batch 4x120 s 720p/60 mash (seeds 31-34): 0 crashes, battle cues 51/32/51/65, 60.0 frames/s,
  0 late vsyncs after warm-up. Saves md5 = save_bak_1023b.

## Milestone 5, session 19 (2026-10-27 just after midnight, agent alone; user out, said "do the rest whatever you can")

**NEXT (resume here):** user tests the launcher (Desktop shortcut via `tools/make_shortcut.ps1`, then PLAY) and F12.
J: still not mounted, so still no real icon (steps in session 18). M6 (publish) needs the user: decisions below.

### Launcher (new, `runtime/launcher/launcher.cpp` -> `private/tms/build/launcher.exe`)
- Plain Win32 window, no new dependency (common controls v6 manifest embedded with `-Wl,/manifest:embed`, system
  DPI aware, system message font). Fields: frame rate (editable combo: 30/60/120/144/0, any N >= 60), render
  resolution, display mode, VSync (`present_mode` mailbox/fifo/immediate -> NX_PRESENT_MODE), mute (NX_MUTE), game
  data folder (edit + Browse, checked for link\image.bin + romfs). Buttons: Open folder, Save, PLAY (saves, starts
  tms.exe from its folder, closes).
- Rewrites only its own keys in settings.ini; comments and other lines (any NX_ key) stay. `mute` off = `mute = `
  (empty values are skipped by tms.exe). Defaults text now in `runtime/src/settings.h`, shared by tms.exe and the
  launcher (the launcher writes it when the ini is missing).
- No sidebar pages yet: everything real fits one page. The SpartanPort-style sidebar (Home/Graphics/Performance/...)
  comes when there are settings to fill it (HDR, anisotropic, overlay, controls do not exist in the runtime yet).
- Verified (scratch copy + real build dir, window captures): defaults written on first start; Save of 60 / 1080p /
  fifo / mute wrote exactly those keys, reopening showed them; a bad data folder is refused with a message and the
  ini is unchanged; PLAY in the build dir started tms.exe with 720p / window (log: render scale 1x, mailbox). The
  user's settings.ini was backed up and restored after (fps 30, 4k, borderless).
- `tools/make_shortcut.ps1` now points at launcher.exe (`-game` = tms.exe directly). Tested into the scratchpad.

### F12 screenshots (ui.cpp g_user_shot, vk.cpp)
- F12 in game writes `<data>/shots/screenshot_<date>_<time>_N.bmp` (same dump_frame as the NX_CONTROL shot).
  Verified: title screen at 720p, 1280x720 8-bit BMP correct. The test file was deleted.

### Milestone 6 (publish) preparation, nothing pushed (no remote is set)
- `LICENSE` added: GPL-2.0 text (copied from Git for Windows' xz COPYING.GPLv2); README has a License section
  (GPL-2.0-or-later, our code only).
- Scan of the 64 tracked files: no keys (no 32-hex-digit strings outside NOTES), no game files, `ref/` and
  `private/` ignored. NOTES.md had the user's NSP path and email: removed 2026-10-27 at the user's request
  (the email stays in commit author lines and in old history).
- Also for the user: GitHub repository name/visibility, and whether NOTES.md (95 KB dev log) ships as is.

### Checks
- Saves md5 = save_bak_1023b after the PLAY test (title screen only).

### Icon + user decisions (2026-10-27, session 19 continued)
- Real icon done: control NCA (6d2a8ad3..., already in private/tms/nsp, J: not needed) extracted with
  `nstool -k prod.keys -x / private	ms\control <nca>` (Windows backslash paths: nstool rejects mixed separators),
  `tools/make_icon.ps1 private\tms\control\0\icon_AmericanEnglish.dat`, build.ninja deleted, build.cmd.
  Verified: tms.exe and launcher.exe both carry it (ExtractAssociatedIcon), launcher title bar shows it.
- **User decision 2026-10-27: do NOT publish to GitHub until the user has done a full test of the game.**
- User decision: the endgame launcher (sidebar pages, new runtime settings) waits until the user asks, at a time
  they are not using the computer.


## Milestone 5, session 20 (2026-10-27 09:50-11:30, with the user: launcher redesign, uncapped test report, extras)

**NEXT (resume here):** user tests the new build (launcher, 4K uncapped). Open: (1) menus / loading icon / some
effects too fast above 60 fps (NOT fixed, leads below); (2) Tsubasa face shadow not checked (needs a user screenshot
spot or save); (3) a crash batch for the precise-sleep change (only single 70-200 s runs so far); (4) launcher
`k_update_repo` once the GitHub repo exists (user: no upload until the full test).

### User report 2026-10-27 (run 09:15-09:19, build Oct 27 00:07, uncapped 4K, issues.log + nx.log)
1. White halo around characters (red-robe field enemy, battle enemy, Itsuki, sword): FIXED (below).
2. Menus, loading icon, effects too fast at uncapped; battle and skill animations fine: NOT fixed.
3. Tsubasa's face has a shadow: not looked at.
4. FPS ok but pacing bad; wants >= 144 at 4K on the 5070 Ti: big CPU win (below).
Extras asked: beautiful launcher (Bloodborne / GOW style) with updates; UHD texture pack; uncensored patch; walk speed.

### Halo = depth-of-field / bloom blur at 3x (vk.cpp image_of, verified)
- `rt` dumps of a field frame at 720p and 4K (same position, same draw counts, agent_scripts/to_field.sh): the
  640x360 DOF targets (bc983b50 / bc984210; 1920x1080 at 4K) blur with a few taps at fixed UV spacing. From a 3x
  sharper source each tap shows its own copy: ringed ghost outlines around Itsuki (shots/zz.png: 720p smooth, 4K
  ringed). The final image had a light fringe around every silhouette.
- Fix: colour targets with game size <= 640x360 stay at 1x (`NX_POST_NATIVE`, default 1; ini/launcher post_native).
  Verified at 4K: fringe gone, sword and jacket edges clean (shots/zn.png: 720p / old 4K / new 4K).

### Performance (uncapped 4K battle: replay cut4416 at 60 + live `fps 0`, NX_PROFILE=1)
- Before: 80-98 fps. 14.7% of the game thread in strchr = getenv() per draw (vk_replay.cpp blend constants, debug
  blend, clear) -> static bools: 123-131 fps.
- 25-31% in ZwDelayExecution: guest SleepThread(50 us) polling from `main` (lr 0x5a76f8) and both `core[n] AtJob`
  workers (lr 0x5a7140), 10k+ per 30 s (new `NX_SLEEP_LOG=1`). Windows sleeps >= 1 ms. Fix (kernel.cpp svc 0x0B):
  sleeps < 1 ms yield-spin to the deadline -> 152-168 fps. The remaining 15% Sleep in the profile: assumed driver /
  GPU waits (not checked).
- Not verified: a multi-run crash batch with the spin change; CPU use is higher (3 threads spin-yield).

### Menus / loading icon too fast above 60 (NOT fixed)
- Cause class: code that counts 60 Hz frames per update (uncapped: every frame is one step). Particles (0x5c0508)
  are already dt-scaled (anim_update hook). The interval getter 0x55d51c has 3 callers (0x202fa0 init, 0x246318 task
  manager stores it at +0x10, 0x5c0508); readers of that +0x10 not found statically (findld.py on GOT 0x9eef94 gave
  false positives).
- Menus are Lua-driven (TM_*, CAMP_MENU_*), and Lua is already gated at 30 Hz, so the fast part is C++ tweening.
  Example: TM_MoveRoteSprite (binding 0x45f824) sets a tween: +0x54 start, +0x68 end, +0x90 counter = 0, +0x94
  frames, +0x98 ease. The updater that advances +0x90 is the target (63 functions touch those offsets: static scan
  useless). lua_check_sprite 0x5ade80 is a generic userdata check (watching its first object hit battle memory).
  The prologue replay never calls TM_MoveRoteSprite. Next: hook it in a menu the user opens (Y menu / Topic), watch
  +0x90 with the `watch` control. Plan once found: run that updater only on 60 Hz ticks (like tick_due).
- Until then: 60 fps (or 30) keeps menus right.

### Mods folder + uncensored patch (hle_fs.cpp, tools/vcdiff.py)
- `<data>/mods/<name>/romfs/<path>` replaces romfs/<path> (file level, first match by sorted name; directory
  listings are the base only). `NX_MODS_DISABLED=a,b` (ini mods_disabled; launcher Mods page). Log: `fs: mod X on`.
- The user's uncensor mod (GameBanana 676474) = xdelta patches against the Switch cpks. tools/vcdiff.py is our own
  VCDIFF decoder (RFC 3284 default code table; the combined ADD+COPY entries are ordered mode, add size, copy size;
  xdelta Adler-32 per window checked). All 6 English patches (map, message, sound, movie, interface, lua) applied to
  our base with matching checksums -> private/tms/mods/uncensored/romfs/Pack (8.5 GB). Source archives in
  Uncensored/ (git-ignored); the Spanish set is not used.
- Verified: mod on, prologue -> first battle -> field (to_field.sh), no crash, no Lua errors. An earlier run with
  the Spanish set showed Spanish UI text, so the overlay works. The content changes themselves (outfits, hot
  springs) were NOT seen by the agent.

### Walk speed (hle_sys.cpp)
- Player move functions 0x40b594 (walk) / 0x40b6fc (run) step position by speed x scale x dt from their literals
  0x40b694 / 0x40b7fc (in DT_LITERALS). `NX_WALK_SPEED=k` (ini walk_speed, launcher Game slider 1.0-3.0) writes
  dt x k there; at fps 30 written once at the first interval set. NOT measured in game yet.

### UHD texture pack (vk_texture.cpp, vk.cpp recreate_image, tools/uhd_pack.py)
- `NX_TEX_DUMP=1` (ini tex_dump): each new 2D pool texture's level 0 -> <data>/textures/dump/<w>x<h>_<nvn fmt>_<hash>
  .dds (FNV-1a over the untiled level 0). <data>/textures/pack/*_<hash>.dds replaces it at upload (any size, own mips,
  BC1-5/7 or RGBA8 DDS; sRGB follows the original). `NX_TEX_PACK=0` (ini tex_pack) ignores the pack.
- uhd_pack.py: texconv decode (-srgb for sRGB formats) -> realesrgan-x4plus-anime x4 -> magick Lanczos to --scale
  (default 2) -> texconv BC7 (+ -srgb) with full mips. Only BCn colour formats: RGBA8 0x25 data/mask textures came out
  alpha-premultiplied (Itsuki turned grey), BC4/BC5 data skipped, normal maps skipped. About 3 s per 1024^2 texture.
- Tools (user approved the downloads 2026-10-27): private/tools/esrgan (Real-ESRGAN-ncnn-vulkan 20220424),
  private/tools/texconv/texconv.exe.
- Verified: one prologue -> field run dumped 474 textures (135 MB); a 24-texture pack replaced 20 (2048^2, 12
  levels), colours equal (channel means), 4K field shot correct (shots/tp.png). The pack of all 474 was built after.
  A full-game pack needs the user to play with "Collect textures" on, then run uhd_pack.py (hours of GPU time).

### Launcher redesign (runtime/launcher/launcher.cpp: Direct2D, DirectWrite, WIC, WinHTTP; no new dependency)
- Dark ink + magenta theme, Bahnschrift headings, sidebar pages Play / Graphics / Display & FPS / Game / Mods /
  Advanced, hero picture (<data>/launcher_hero.png|jpg|bmp, else the newest F12 shot, else drawn spotlights; the
  agent saved a 4K title-screen capture as private/tms/launcher_hero.png), quick settings, footer status + Save +
  PLAY, own dropdowns / toggles / slider, mod cards with toggles, dark title bar. `--page N` opens a page.
- Graphics page: resolution, native-size blur, UHD pack on/off, collect textures. Game page: walk speed, mute.
- Updates: GitHub releases/latest of ini update_repo or k_update_repo (empty now: "Updates not set up yet"). Update
  downloads the first .zip asset, unpacks it with Windows tar.exe, replaces the files next to the exe (files in use
  renamed *.old, deleted at the next start), never settings.ini / save / mods / romfs / link, restarts. NOT tested.
- Verified by window captures: all pages render; dropdown opens and picks; Save rewrote only the fps line (user ini
  backed up and restored). Test note: a non-DPI-aware sender's mouse coordinates get scaled by Windows (divide by
  1.5 on this 144 dpi screen).
- settings.h: k_version "0.9.0"; the default ini documents walk_speed, post_native, mods_disabled.

### Checks
- Saves md5 unchanged against the session start after all runs.

## Milestone 5, session 21 (2026-10-27 18:10-19:00, with the user: test report of the s20 build, new requests)

**NEXT (resume here, in this order):** (1) UI / menus / loading icon / right-stick camera / field radar too fast above
60 fps (user's #2 complaint; leads below); (2) Tsubasa face shadow in battle (user screenshot: dark band on her cheek /
neck when she turns; check shadow-map sampling at 3x, compare 720p vs 4K); (3) new features asked: PlayStation / Xbox /
Switch button icons by connected controller type, always first strike (player advantage) when touching a stunned
field enemy, in-game graphics/options menu (our own overlay, hotkey + pad combo); (4) offline full UHD texture
extraction from romfs (user asked "why wait to collect textures in game?"): parse the cpk texture containers, untile,
hash like vk_texture.cpp tex_hash, write dump/*.dds, then uhd_pack.py once.

### User report 2026-10-27 18:02 run (launcher, uncapped 4K, walk_speed 2.0, uncensored mod on, UHD pack on)
1. Launcher: user loves it. 2. Stutter much worse than before. 3. Menus, loading icon, right-stick camera, top-right
radar, party menu still too fast uncapped (battle + skill animations are right). 4. Tsubasa face shadow still there.
5. UHD pack makes Itsuki dark / grey. 6. Uncensored patch not checked (user asked what to look at). 7. Walk speed good.

### Stutter = UHD pack path (FIXED, commit a408862, verified)
- nx.log of the run: 62 hitches, 13.5 s total, all "texture uploads" (the 09:19 run without pack: 5 hitches).
- Measured (temporary log): tex_hash read 123 MB in 1472 ms = 83 MB/s, because it hashed level 0 inside the Vulkan
  staging buffer (HOST_VISIBLE|COHERENT = write-combined, uncached reads). Fix: untile level 0 of hash candidates into a
  thread_local cached vector, hash + dump from there, memcpy into staging. Also: 4-lane FNV (file names changed:
  existing dump/pack files renamed by a scratch script, tools do not need it), pack files read on a worker thread
  (texture shows its original data until then, `Image::pack_wait` + `pack_arrived` re-upload in vk_replay.cpp), pack
  images made once per hash and shared (`Image::own` keeps the texture's own image; the old recreate_image leaked an
  image per reuse; `new_image_2d`).
- Field replay to_field.sh at 4K: 26 hitches before (with the async read only), 3 after; no-pack baseline 2. 20
  replacements logged.

### Grey Itsuki = upscaler on alpha-masked textures (FIXED, verified)
- Original vs pack channel sums: textures with low mean alpha lost up to 1.9 of 3.0 RGB (realesrgan blackens RGB where
  alpha is low; the game uses alpha as a mask). uhd_pack.py now upscales RGB opaque and alpha separately (Lanczos),
  joins with CopyOpacity. Old pack kept in textures/pack_old_alphabug; new pack 425 files. 4K field shot: shirt white,
  skin normal ($TEMP shots, shots/live_00001.bmp).

### UI too fast: leads
- `watch *9f3738+10 4 r` (new syntax `*ptr+off`): in field nobody reads game manager +0x10 (only 0x246318 writes it),
  so the "make interval 0/1 per 60 Hz tick" idea does not work for field UI.
- Tween object (TM_MoveRoteSprite 0x45f824): +0x38 value, +0x54 start, +0x68 end, +0x90 counter (int 0), +0x94 frames
  (float), +0x98 ease. Static scan of [r,#0x90/94/54/68] gives ~30 candidate functions (useless). Next: add 0x45f824 to
  tools/recomp/names.txt (lift) and NX_PROBE it with the user in the Y menu, or `watch` +0x90 of the object it logs.
- Camera: orbit 0x5c4f84 already uses the dt literal; right-stick turn must be another per-frame add: find the camera
  yaw (watch while `rs` held).

### Small changes
- Mouse cursor hidden while a gamepad is connected (ui.cpp SDL_EVENT_GAMEPAD_ADDED/REMOVED); unplugged pad closed and the
  next one opened. Pad mapping is positional: EAST=A, SOUTH=B, NORTH=X, WEST=Y (PS: Circle=A, Cross=B, Triangle=X,
  Square=Y) -> needed for the icon swap.
- Smoke run OK. NOT user-tested: everything above.

## Milestone 5, session 22 (2026-10-27 19:00-20:05, agent, started by session 21; commit c88a5fc)

**NEXT (resume here, in this order):** (1) uncapped menu cursor over-steps: key repeat is frame-counted in the pad
manager 0x54d73c (one `down` of 150 ms moved 6 rows at ~1000 fps; 1 row at 60, verified); (2) right-stick camera,
field radar, loading icon still unchecked (leads below); (3) field countdown 0x4a5618 (30 Hz frames x30, task 0x7e6990)
and the bobbing map object 0x468884 (phase += constant per update) run 2x at 60 / faster uncapped; (4) then session 21
items 2-4 (Tsubasa shadow, pad icons / first strike / in-game menu, offline UHD extraction). Nothing of this session
is user-tested.

### Finding: the game counts 30 Hz frames, so 60 fps was also 2x for UI (verified by code + call counts)
- TM_* sprite tweens (Lua TM_MoveSprite 0x45f6b0, TM_MoveRoteSprite 0x45f824, TM_MoveScaleSprite 0x45f9ac,
  TM_FadeSprite 0x45fafc; counters +0x6c/+0x78/+0x84/+0x90) are fine: their updater 0x367894 (task 0x3675b0) adds the
  dt literal 0x367708 (in DT_LITERALS).
- UI widgets are not: the UI manager task update 0x246318 (also the one that stores the interval at +0x10) calls each
  widget's vt+8 once per frame; e.g. the yen panel (vtable 0x7d2a7c: update 0x24873c -> 0x248508, draw 0x2487d8)
  adds 1 to a slide counter +0x34 (done at 8) and fade +0x3c (4). On the Switch that is 8 updates at 30 fps. Draws
  run in another pass.
- Fix (hle_sys.cpp ui_manager_update): above 30 fps the manager runs only when tick_due (30 Hz) or when the latest
  pad read had a new press (ui.cpp pad_pressed_now; widgets see a press only in that frame). Call counts of 0x248508
  with the menu open: before 68 (60 fps) / 338 (240 fps) per window, after 34 / 42 (draws 68 / 338): 30 per second at
  any rate. First try latched pad buttons to ticks instead: menus lost presses (Chrom "Is this okay?" never accepted)
  and replays desynced; dropped.
- Uncapped stops at 1000 fps (ui.cpp pace_variable): dt is clamped to >= 1 ms, so the ~1800 fps menu ran game time
  1.8x fast.
- Verified: cut4416 replay reaches field control at the same position as before (-629.8 -240 -758.8); menu opens,
  1 `down` = 1 row at 60; no crash; saves md5 unchanged. NOT verified: other menus, party menu, battle menus at
  uncapped (by eye).

### New debug tools
- NX_CONTROL `dump lo hi file`: copies guest memory (uncommitted pages = 0) and logs `[dump] frames a-b`. The copy is
  fast; the file write blocks the game ~2 s per 128 MB (frames are counted, so fine).
- private/tms/agent_scripts/snap4.sh <tag> <prefix> (S0,S1 at 60, S2,S3 at 240) + framecount.py <prefix> <log>: words
  whose per-frame rate is the same at 60 and 240 = frame-counted (time-based ones run ~4x at 240). Ranges main
  0x900000-0x1400000 + heap 0xb8000000-0xc0000000. Oscillators with sign flips are false positives (TODO: same sign).
- coverdiff.py / coverfc.py (agent_scripts): NX_COVER=manual reports around an action; coverfc compares an action's
  call counts at 60 vs 240 (equal = frame-counted). Needs `lift.py ... --probe-range 200000:7d0000` (slow build).
- Pad: GetNpadState is called from 0x54d73c (pad manager, called 0x54d0fc <- 0x5be558 main loop); pad object fields
  +0x28..+0x34 = lx ly rx ry floats. Player stick history ring: 0x4113c0 (5 floats per entry) from 0x40eb48.
- Main loop: 0x4d9fa0 -> 0x5be5d4 (frame) -> 0x5be73c (render + present); tasks via task_run_phase 0x5bddd0.

### Leads for the rest
- Camera: field camera apply 0x3c5988 (map task 0x46713c) blends from a controller at +0x10c (virtuals +0x24 update,
  +0x14 get, +0x34 blend); the right-stick yaw code is in that controller's update (vtable not read yet). Camera
  direction floats at heap 0xbc926b08 (written by matrix code 0x5591c8). Reading the stick: watch the pad object
  0xbc504670 (rx) reads while `rs` held shows only the player ring (0x4113c0) -> the camera reads the ring or a
  getter; next: watch the ring entries' rx with the player code filtered out, or decompile controller vt+0x24.
- 0x3fa274 (map task) = cooldown timers adding a step from global +0x90 (not camera).
- Radar / loading icon: not found yet; check whether they are UI-manager widgets (now fixed) by eye at uncapped.

## Milestone 5, session 23 (2026-10-27 20:10-21:10, agent, user asked to continue s22; commits 549d8f2, 080e429)

**NEXT (resume here, in this order):** (1) NEW REPLAY BASELINE: `analysis/cut4416.rec` no longer reaches d002_01 at 60
fps (it was recorded with the old 2x camera; camera-relative walking now goes elsewhere: ends in Observatory Inside at
84.7 0 -116.6, field control, no crash). Record a new reference run (or ask the user for one) before using
to_field.sh as a regression check. (2) Verify the HUD spinner (0x3bf19c) in d002_01 at 60/uncapped (not visible in
Observatory Inside). (3) Loading icon still unchecked (not found; check by eye uncapped). (4) Field countdown
0x4a5618 (30 Hz frames x30, task 0x7e6990) still frame counted. (5) Then session 21 items 2-4 (Tsubasa face shadow,
PS/Xbox/Switch pad icons, 100% first strike on a stunned enemy, in-game graphics menu, offline UHD extraction).
Nothing of sessions 22/23 is user-tested.

### Key repeat (commit 549d8f2, verified)
- At the end of each pad read (0x54d73c, also 0x54e9e8) three functions count 30 Hz frames: pad_repeat 0x54c9bc
  (held mask +0x40 countdown +0x44: delay +0x48, interval +0x4c -> repeat bits +0x20), pad_repeat_bits 0x54ca24
  (+0x24 = presses +0x18 | buttons with (hold - delay) % interval == 0) and pad_hold_count 0x54ca78 (26 hold counters
  +0x5c + 4i, +1 per call while held). Pad fields: +0x10 held, +0x14 previous, +0x18 presses, +0x1c releases.
- Fix (hle_sys.cpp, names.txt): above 30 fps they count only on 30 Hz ticks (tick_due per pad); a new press still
  starts its counter at once; repeat bits only fire for counters raised in the last count.
- Verified uncapped (~1000 fps): 2 `down` = 2 rows (was 6 rows per press); stick held 700 ms from Skills lands on
  Analysis at 60 and uncapped, 3/3 trials each (500 ms gave 1 vs 2 rows once: delay is near 500 ms, borderline).

### Field camera (commit 080e429, verified 60 = uncapped by screenshots; 30 by code)
- Active controller in dungeons: vtable 0x7e0248, update vt+0x24 = 0x3c31c8 (cam_free_update). It calls 0x3c2cc4:
  smoothed stick +0x1c/+0x20 = keep*old + (1-keep)*stick, keep = settings(+8) +0xcc; yaw step at 0x3c3414 =
  settings +0x50 / 10 x +0x1c x -0.714 per update. Other controllers: 0x3c1930 (vt 0x7e0164), 0x3c1da0 (0x7e01b0),
  0x3c3c48 (0x7e0294) read the stick the same way (smoothing +0xcc / +0xec): NOT fixed yet, only if seen too fast.
- Fix: cam_free_update runs with keep^(dt*30) and +0x50 x dt*30, restored after the call.
- Found by: snap4.sh with `rs 32767 0 60000` held vs not, then `watch` on candidates. Camera matrices are written by
  0x5591c8 (bc926af0 etc. = matrix, not yaw).

### Step literals (commit 080e429)
- New STEP_LITERALS (hle_sys.cpp, x dt*30 in set_game_dt): 0x3bf320 (pi/30: sprite angle +0x36c in draw 0x3bf19c,
  callers 0x3bffd4 / 0x3c0324, map task 0x46bb1c; seen spinning only with rs held in d002_01, which element is
  unknown), 0x4689f0 / 0x468a0c (bobbing object 0x468884 phase +0x140, 20 / 16 degrees per update; its 0.75 decay
  per update is an immediate, not scaled).
- Another pi/30 literal 0x40f50c (0x40f1e8: player-object +0x330 += +0x334 x pi/30) is not scaled (use unknown).
- Saves md5 unchanged after all runs; 0 crashes.

## Milestone 5, session 24 (2026-10-27 20:40-21:30, agent, started by session 23; commit 5d64ad5)

**NEXT (resume here, in this order):** (1) 100% first strike on a stunned enemy symbol: decision code NOT found yet
(leads below); (2) Tsubasa face shadow; (3) PS/Xbox/Switch button icons by controller; (4) in-game graphics menu;
(5) offline full UHD texture extraction. Nothing of sessions 22-24 is user-tested.

### New replay baseline (verified)
- `private/tms/analysis/base60.rec` (recorded with agent_scripts/record_base.sh on the s23 build, 60 fps 720p):
  title -> load slot 2 -> north door -> d002_01 (-840,-240,-600) -> walk north -> goto (-659,-762) -> Chrom "Wait,
  Itsuki" + "Enemy Symbols and Sword Attacks" tutorial -> walk into the symbol -> battle (ends at battle start, read 11153).
  No right stick, so camera changes do not move the route.
- `agent_scripts/to_field.sh <tag>` now replays `$REC` (default base60.rec), presses through the battle and results:
  field control at (-494.1, -240, -760.0), HP 43 / 69 after the battle, ~5.5 min wall. Saves md5 unchanged.
- `analysis/d00201_60.rec` = base60 cut at read 4421: d002_01 field control at (-840,-246,-849) in ~75 s (quick
  field tests; the tutorial symbol is reached with goto (-659,-762)).

### HUD spinner (verified, no change)
- hud_pulse_draw 0x3bf19c (names.txt, probe only) = pulsing marker drawn while obj +0x20 is the current target;
  angle +0x36c wraps at 2 pi. Measured with `rs` held in d002_01 (dumps of obj+0x36c, obj bcc0efc0): 3.11-3.21 rad/s
  at 60 and uncapped (= pi rad/s = 30 Hz x pi/30). The STEP_LITERALS scaling from s23 is right.

### Field enemy respawn countdown (commit 5d64ad5, verified)
- 0x4a5618 (field_spawn_timer) = enemy respawn timer: counter at *(*0x9f3f1c) +0x10 +0x51dec (here bcaafdbc), 30 Hz
  frames, -1 per call (-3 while field global +8 == 0), at 0 respawns and reloads 30 x (91..600) (+ random 61..119 case).
- Fix: above 30 fps a plain decrement (1..3) is undone unless tick_due(counter); reloads stay. Measured: 121 / 4.03 s
  at 60 and 122 / 4.03 s uncapped (= 30/s); before, uncapped ran at the frame rate.

### Loading icon (verified, no change needed)
- "NOW LOADING" star ring (layout SYS_CMN_LOADING, anim setter 0x23f2e0; Lua OpenNowLoading 0x45d680). Frames at
  60 vs uncapped with sparse `shot` (log timestamps): ~0.33 s per star step at 60, ~0.37 s uncapped: not frame counted
  (probably fixed by s22's UI manager gating). Note: `shots N` writes BMPs at ~16 ms each, which throttles capped
  rates (a 144 fps capture ran at ~64 fps): use sparse `shot` + log times for rate checks above 60.

### First strike on a stunned symbol (NOT found yet)
- The tutorial text says touching a downed symbol "may" give the first action, so it is a chance. Not in
  EnemyServerParam (full field list: ghidra/parammap.py after Decomp 0x42edc0) and no Lua names (Advantage/Preemptive/
  Surprise only as facial anims).
- Looked at, NOT it: 0x3e9ae0 (symbol appear/pop), 0x3e7adc (enemy server reset, messages via 0x3e315c = server
  +100 handler table [type]->vt+8), 0x44c8dc (Lua setEnemyEncount = enable flag), 0x43f174/0x43f1ec (evtGetBattleResult
  / evtGetBattleTurn). Enemy symbol class code ~0x3c9460-0x3d2fec (ghidra/enemy_region.c); stun state anims set in
  0x3cb630 (fd_down_in_stun); getter callers decompiled in ghidra/encount_callers.c.
- Next: runtime. d00201_60.rec -> goto (-659,-762) -> b through tutorial -> `x` (sword) to stun the symbol -> walk
  into it; compare with plain contact: NX_COVER=manual + coverdiff.py (needs the probe-range lift) or watch the
  symbol's state word and log rand (thunk 0x2302894 callers in 0x3c9000-0x3f5000) at contact.


## Milestone 5, session 25 (2026-10-27 23:28 - 10-28, agent; user asked to continue + new list; commit 2778397)

**NEXT (resume here):** the request list below, items still open. Nothing of s22-25 is user-tested.

### User requests 2026-10-27 (verbatim intent, all to be done; status after this session)
Bugs / engine:
1. A press often ignored (worst at level-up, Chrom "Is this okay?" after picking a skill) -> FIXED by code (see below),
   not reproduced at that screen (needs a level-up with a full skill list).
2. Selecting Artists in the menu crashed -> FIXED (verified: Artists list, Stats, Skills pages open).
3. Exit item on the title menu -> DONE as an overlay: "(-) Exit Game" pill bottom-left on the title, minus opens
   "Exit the game?" (Yes / No, default No). Verified by window captures.
4. In-game graphics settings like AAA games (bloom, vignette, motion blur, DOF...) -> DONE first version: settings
   overlay (F1 or L3+R3) with frame rate, resolution, display, Bloom, Glow, DOF, Vignette, Fog, Outline, first strike,
   Exit. Not yet: motion blur (AtPSMotionBlur / PostEffectFBBlur*), SSAO, FXAA toggle, sharpening.
5. No VRAM leak / too-high VRAM -> OPEN (measure: VkMemory totals over a long run; s16 saw memory plateau 4.37 GB RAM).
6. DLSS / FSR (latest) option -> OPEN. Facts: DLSS 2+/FSR 2+/FSR 3 need per-pixel motion vectors + depth + jitter; the
   game renders none (Switch renderer). FSR 1 / RCAS (spatial) is possible but needs our own shader pass (no SPIR-V
   compiler on this PC: ask the user before adding glslang/shaderc). DLSS also needs NVIDIA's SDK (Streamline).
7. Everything paced to 60 game-speed; above 60 only smoother -> the design since s10; keep fixing anything too fast.
Mods / QoL (launcher or in-game):
8. Randomize battle music incl. bosses, except the final boss -> DONE by code (setting random_battle_bgm, menu
   "Random battle music", default off); not heard yet (the tutorial battle keeps the event music).
9. Detailed skill descriptions (real numbers, like the FF Resonance mod): read skill data + passives, rewrite the help
   strings in game -> OPEN.
10. Basic attack starts a Session when it hits a weakness (like skills) -> OPEN (gate not found, see below; a first
   patch wrote the wrong field and was removed before the user got it).
From the user's play test (10-27 21:53-22:09 run, fps 240, 4K): very little stutter (good); some effects still too
fast; Tsubasa face shadow (unchecked); PS/Xbox/Switch button icons by controller (open); offline UHD extraction (open).
New user rule: pause and write notes when the 5-hour limit reaches 99%; context can go to 80% before pausing.

### Artist menu crash (FIXED, lifter)
- FATAL "branch to unknown code 00347544 from 00347e60 fn_00347d1c+0x144" (user run 22:09): 0x34720c has an 18-case
  relative table (`add r2, pc, #0x1c; ldr r3, [r2, fp, lsl #2]; ... add pc, r2, r3`) whose ldr sits 7 instructions
  before the `add pc`; lift.py rel_table looked back only 6, so the whole table was unlifted. Now 12. Re-lift found 2
  tables (also one at 0x3a1360).

### A press ignored (FIXED by code)
- Lua event scripts resume once per 1/30 s (s10), but a press bit (pad +0x18) lives for one pad read. The skill-swap
  prompt (ScriptCommon/Result/ResultSkillSwap.lua) loops `Pad.Push(PadDef.OK)`; Pad.Push (0x4461f8) -> 0x25c970 ->
  input object (*0x9f37dc) vt+0x10 -> 0x54c7fc -> 0x54cc98 = `pad +0x18 & mask`. At 240 fps a press was seen ~1 in 8.
- Fix (hle_sys.cpp resume_scripts): pad_repeat logs each read's presses/releases; each script manager's resume ORs the
  ones since its last resume into pad +0x18/+0x1c/+0x20/+0x24, restored after.
- Checked: the d002_01 tutorial dialogue at 240 fps advanced on every single `a` (3/3). The tutorial info window
  (C++ widget 0x242574, closes on input_trigger(0x40)) only looked like it dropped the first B: it opens ~10 s after
  the line; presses before that cannot reach it (traced: UI manager ran, widget not created yet).

### First strike on downed symbols (DONE by code, not seen in a run)
- btl_setup_units 0x2c4108 (encount struct = static 0x9f3da8): flags +0x18 bit 0x20 = advantage contact. With it,
  btl_open_chance 0x2a0694 (only caller) >= 50 -> player first (|1), >= 85 -> |0x41; without it < 2 -> |0x42 and 2..5 ->
  |2 (enemy first). Hook: chance raised to 50 when bit 0x20 (setting first_strike, default 1). Log line
  "battle: opening chance N (contact flags F)". Plain contact measured: flags 0000 (chance 61 and 35 seen).
- Could not stun the tutorial symbol in a run (it rushes in; after a teleport it wandered off and vanished). Next
  user play: look for "contact flags 0020" in nx.log after touching a downed symbol.

### Settings overlay (runtime/src/overlay.cpp, NEW)
- Layered popup window owned by the game window (UpdateLayeredWindow + Direct2D/DirectWrite into a DIB; the
  swapchain is untouched; Windows components only). UI thread: poll_input -> overlay_update; while open the game gets
  no buttons (and not the closing press). F1 or L3+R3 opens; up/down select, left/right/A change, B/F1 close.
- Saves to settings.ini (save_setting rewrites "key = value", sets NX_KEY). Live: fps (60/120/144/165/240/uncapped;
  to/from 30 needs restart), display, effects, first strike. Restart: resolution.
- Post effects: manager *0x9f2904 (+0x18 DOF, +0x1c Fog, +0x24 Edge, +0x44 Glare, +0x48 Glow, +0x4c ToneMap, +0x60
  Vignette; effect +0x1c = enable, Lua PostEffect*SetEnable writes it). The manager calls effect vf5 only while
  enabled; hooks fx_*_render skip vf5 when the user turned it off. Verified: Bloom+Glow off in d002_01 removes the
  waterfall/light haze (frame diff), no crash. Keys fx_bloom, fx_glow, fx_dof, fx_vignette, fx_fog, fx_outline.
- Title: title_scene_update 0x4a1754 pings overlay_title_seen.
- NX_CONTROL: button names `l3`, `r3`, combos `l3+r3`. Window captures for overlay checks: the overlay is not in
  `shot` (game frame only); agent used a DPI-aware CopyFromScreen PowerShell script (scratch).
- The user's build/settings.ini was backed up and restored around the tests; saves md5 unchanged.

### Battle music randomizer (commit 2c9c7b1 + later)
- bgm_play 0x25fbe0: r2 = sound table index (table *0x9f3c48: 1568 entries of 0x90, +0 id name, +0x40 cue name; same
  order as ScriptCommon/Sound/SoundIdTable.lua). Battle tracks 55 b49_b_normal, 56 b50_b_boss, 57 b51_b_ganefu,
  59 b53_b_event, 60 b54_b_extra, 61 b55_b_quest; final boss 58 b52_b_medius, 47 b44_b_medius2 (kept). 62 = title,
  65 = victory, 1157 = env_battle (battle ambience at battle start). Log line "bgm: N (played M)" on each change.
  The d002_01 tutorial battle starts no battle track (event music continues), so a normal symbol battle is needed to
  hear it. Battle cue start: 0x2ddf24(this, index).

### Skill data (for the detailed descriptions and the attack Session request)
- Table/StSkillTable.dat (pack_030_etc.cpk): 952 records of 0x84, id = index, name label at +0x64 (CS_SWORD...) =
  SkillName.msbt / SkillInfo.msbt labels (msbt text is UTF-8; tools: agent scratch msbt.py, rewrite into tools/ when
  used). In memory (this build): bc9f624c; getter 0x27f280(*0x9f3d7c, id).
- Fields (u16, by comparing records): +0x6 type (1 phys, 2 mag/support), +0xa cost type?, +0xc cost (Dia 10 EP as the
  menu shows; Agi 6, Agilao 10, Cleave 5), +0x10 class (4 phys, 5 mag), +0x12 element (0 sword, 1 lance, 2 axe, 3 bow,
  4 fire, 5 ice, 6 elec, 7 force, 0xb support), +0x14 accuracy (Agi 110), +0x16 target (1 one, 2 all, 3 ally...),
  +0x20 formula (1 basic attack, 2 skill, 3 heal/support), +0x22 power (Agi 30, Agilao 68, Bufudyne 120, Dia 140),
  +0x52 session attribute/element (sword attack 0, lance 1, staff 0x12), +0x54 (1 attack skills, 5 support, 0 basic
  attack + CS_A_STR_SWORD_2), +0x56 tier, +0x5c effect id (ffff none), +0x60 (0 attack, 1 mag, 2 phys, 3 support).
- Battle reads (watch on the table during the tutorial battle): basic attack record fields +0x6 +0xa +0xc +0xe +0x16
  +0x1a +0x24 +0x2c +0x30 +0x36 +0x50 +0x62 +0x68; main reader 0x3014d8 (hit reaction class, uses +0x20 == 1 for basic
  attacks). Session start gate NOT found yet: next, watch the table while a Session starts (needs a party with a
  follow-up for the starting element, e.g. Tsubasa Elec-Lunge after an Elec hit on a weakness) and diff with an Attack.
- Detailed descriptions plan: find the loaded SkillInfo.msbt in guest memory (MsgStdBn + labels), build new UTF-8 texts
  from the record fields, put them in a guest allocation and point the TXT2 offsets at them (32-bit wrap makes any
  address reachable); help bar is one line (~95 characters at 720p).

### Detailed skill help (hle_sys.cpp skill_help_update, setting skill_details default 1, verified)
- Runs from the ui_manager_update hook every 120 frames until done (done ~4 s after boot). Skill table = *0x9f3d7c +
  0xc (getter 0x27f280: +0xc + id x 0x84). Finds every loaded SkillInfo.msbt by Agi's text "(Mag/Fire) Light attack."
  over the whole guest space: 6 copies (languages) at 7e880f40..7fbedf00 (below 0x80000000!). For each: rebuilds all
  952 texts + suffix into one operator new (0x5a8720) block and points TXT2 offsets + section size at it.
- gcall from inside an HLE hook clobbers the hook's registers: save/restore c->r around it (first try crashed in
  ui_manager_update).
- Suffix: formula 3 -> "[Heal power P, target]"; type 1/2 with power -> "[Power P, hit H%, target]"; target 1 one foe,
  2 all foes, 3 one ally, 4 all allies (3/4 assumed from Dia/Tarukaja). EP cost +0xc confirmed (Zio 6 EP in menu).
- Test hazard: menu navigation by blind presses once landed on the SAVE screen (killed, saves md5 unchanged). Navigate
  with a screenshot after each step. Menu order: Skills, Items, Wardrobe, Artists, ???, Analysis, System.

### Session end (2026-10-28 ~01:40): stopped at 5-hour usage ~85% / weekly ~95% (user rule: pause near the limit)
Next, in order: (1) user play test of everything above (look for "contact flags 0020", "bgm:", "skills:" lines);
(2) attack Session gate (see skill data notes); (3) PS/Xbox/Switch button icons; (4) Tsubasa face shadow; (5) VRAM
audit (log VkDeviceMemory totals over a long run); (6) offline UHD extraction; (7) motion blur / FXAA / sharpen toggles;
(8) FSR 1 needs a shader compiler (ask the user about glslang); DLSS / FSR 2+ need motion vectors the game lacks.

## Milestone 5, session 26 (2026-10-29 ~02:00-, agent alone; user asleep, said continue without asking)

**NEXT (resume here):** the open items at the end of this section. Nothing of s22-26 is user-tested.

### VRAM leak (FIXED, commit 8d6bcf9, verified by log)
- Cause: textures the game finalizes (nvnTextureFinalize, or nvnTextureInitialize again at the same address) dropped
  the host Texture but never the VkImage, views or memory; vk.cpp alloc() was a bump allocator with no free. Every
  map/battle/menu texture stayed in VRAM for the whole run.
- Fix: backend_texture_finalized queues the Image with serial gpu_recording_serial()+1; begin() (each submit slot)
  destroys queued images whose serial is done (pack-replaced images destroy their own image, never the shared pack
  image); alloc() is first-fit over per-block free ranges, free_mem() coalesces. NX_FREE_IMAGES=0 = old behaviour.
- Log every 10 s: "frames: VRAM N MB in blocks, M MB used; K images freed (F MB)". Measured: to_field replay 720p
  678 images / 204 MB freed after the first battle; 4 instances uncapped 4K battle 140-154 MB freed each, 0 crashes
  (uncap_batch 4x150 s), saves md5 unchanged.
- agent_scripts/batch.ps1 now replays analysis/base60.rec (cut2110.rec no longer reaches a battle since s23).

### FXAA toggle (commit b6e8812, verified by screenshots)
- Settings menu "Anti-aliasing (FXAA)" (key fx_fxaa). FXAA fragment constants (logged once): 0.5/w 0.5/h 2/w 2/h 1/w
  1/h 0 8 0.01 0.01 0.75 0 (w, h = 1280x720). Off = words 8 and 9 set to 100 (the pass passes pixels through).
  4K d002_01: off changed 42% of pixels, sharper, no artefacts. fxaa_rescale now runs at every scale (finds the pass).
- Motion blur: the game has no motion blur post effect (PostEffect* list: ColorBalance, ColorScreenBlend, Dof, Edge,
  FBBlur (scripted screen blur for transitions), Fog, Glare, Glow, Hls, Sepia, ToneMap, ToneReversa, Vignette).

### Button icons by controller (first part, commit b905569)
- Interface/_US/common/icon/button_icon.gtx = BNTX 256x256 RGBA8 atlas, runtime hash 34c763427410e392: Switch faces
  in two sizes (26 px row y 2/33/64, 22 px rows y 129/154/179; cell table in pad_icons.cpp). pad_icons.cpp draws
  PlayStation (coloured symbols) or Xbox (coloured letters) faces, L1/R1/L2/R2 or LB/RB/LT/RT, menu/view/share over a
  copy before upload (vk_texture.cpp upload_from_pool; check_pool_texture re-uploads when the style changes).
  Setting pad_icons auto|switch|playstation|xbox (menu "Button icons"); auto from SDL_GetGamepadType (log line
  "input: pad ... -> X button icons"; the user's pad is a DualSense). Mapping is positional: Switch A = PS circle /
  Xbox B, B = cross / A, X = triangle / Y, Y = square / X. NX_TEX_DUMP=1 also writes textures/dump/padicons_N.dds.
- BUT most prompts the player sees do not use that atlas (drawlog: atlas 988c02a0 not bound in the battle HUD, Stats
  screen or battle submenu). Seen: battle "(+) Stats / (X) Auto-Battle", tutorial "(B) Close" = white disc + grey
  letter (likely a disc sprite + Alps font letter), Stats "Other Info (X)" yellow, L/R tabs, "SELECT (A)", "Close (B)",
  "(X) Details" baked into the big RGBA8 UI atlases (2048x2048_25_ea576a96..., 7ada3bc9..., 1024x1024_25_94e020b4...,
  a4c81da5...; contact sheet method: texconv dumps -> PNG). Full coverage needs a cell table per atlas (and per
  language folder) or the text path for disc+letter prompts. Not started.
- Later (commit 47c6bdb, verified in a 720p battle): the prompt sprites ARE atlas sprites (plain white disc, grey
  letter): HUD atlas 2048 (hash ea576a96a510fd6e, row y 1236: A B X Y + -, y 1284: L R; large A at 1696,188), the
  same atlas at 1024 (74557bfcf56aafe0, y 618/642; A at 848,94) and the ringed - / Y of menu atlas 94e020b4e4e95ccd.
  pad_icons.cpp has a table per atlas (k_atlases; plain look = no ring, grey ink). Battle HUD shows "(menu) Stats /
  (triangle) Auto-Battle" with PlayStation, "(Y) Auto-Battle" with Xbox; switching in the settings menu re-uploads
  live. Still Switch: coloured or black-background variants (Stats "Other Info (X)" yellow, black A/B on black,
  "SELECT (A)" combos) and atlases of screens not in the dumps. tools/padicons: find_discs.py (white disc finder over
  RGBA8 dumps), sheet.py (numbered contact sheet), crop.py (zoom). Hashes are of the modded pack_080_interface
  (uncensored mod); button_icon.gtx is identical in the base pack.

### Button icons, more atlases (commit ec69f2d)
- tools/padicons/find_discs.py over textures/dump_all (offline dump) -> 1884 white-disc candidates; filtered to
  grey glyphs -> 571; labelled by eye with cells_sheet.py crops. Added: 9fd0da0c8aec7663 (the 1024 HUD atlas as in the
  packs; 74557 is the play-dump variant), b18094e4c410f0aa (ringed + - A B X Y, big X/Y on a white panel),
  16f810b5373bff80 (2048x1024: Y, big thick-ring X), 171a1c16c51d09c9 (512: X, Y on a panel). Drawing is now
  composited over the original (panels around discs stay) and a cell can override the atlas look.
- NX_PAD_ICONS_TEST=<dir> tms.exe: draws both styles over every known atlas found as a dump in <dir>
  (padicons_<style>_<hash>.dds) and exits: check new cell tables without playing. Verified all 8 atlases.
- classify.py (template match against labelled glyphs) works for large sprites only (27 of the set); kept for later.
- Not covered: coloured prompts (Stats "Other Info (X)" yellow), black-background discs, "SELECT (A)" combos.

### Offline texture dump (commit 7bf15fe)
- tools/texextract/texextract.py <data> [--packs ..] [--out DIR]: parses every BNTX in every pack file (CRILAYLA,
  untile and hash in fasttex.dll, built with `clang -O2 -shared -o fasttex.dll fasttex.c` in tools/texextract), mods
  applied as tms.exe does. Full run ~10 min: 29647 textures, 10560 unique, 4.6 GB in private/tms/textures/dump_all;
  495 of the 513 play dumps are among them (same hashes), so pack files built from it replace in game.
- Build a full UHD pack: `python tools/uhd_pack.py private/tms --dump private/tms/textures/dump_all` (hours of GPU;
  not run by the agent: the user decides).

### Leads checked, not the cause
- Tsubasa face shadow: polygon offset is never enabled (polygon state words 0x14-0x16 only: cull, front face, fill),
  so the no-op nvnCommandBufferSetPolygonOffsetClamp is not it. Still needs a user screenshot / save near the scene.

### UHD pack images freed when unused (commit 199f3c0, verified by log + batches)
- Pack images were kept for the whole run (fine for 425 files, not for a full-game pack). Now PackTex.refs counts the
  images showing it (pack_swap_in / pack_swap_out / image destroy -> pack_released); at 0 it joins an unused list;
  over NX_PACK_CACHE_MB (default 1024) the oldest are freed (vk::defer_destroy, serial-deferred like images) and
  their file is read again on the next use (state 0). Views made for a pack image are freed on swap-out (were leaked);
  a re-swapped texture keeps its own views. Verified: NX_PACK_CACHE_MB=8 replay logs "1 unused pack images freed",
  4x150 s batch with 8 MB 0 crashes.

### Launcher (commit 147cd4f): Game page "Button icons" (pad_icons), Display & FPS page "Anti-aliasing (FXAA)".
  Checked by window captures (PrintWindow, DPI aware; scratch cap.ps1 clicks pages with WM_LBUTTON messages).

### Session 26 end state
- Final batch (uncapped 4K, 4x180 s): 0 crashes; VRAM used 2.2-2.3 GB per instance at 253 s; saves md5 unchanged;
  user's build/settings.ini restored after every overlay/launcher test (backup compared).
- Nothing of s22-26 is user-tested. For the user to try: PlayStation icons should show automatically with the
  DualSense (battle HUD "(menu) Stats / (triangle) Auto-Battle", tutorial "(cross) Close"); F1 menu has "Button
  icons" and "Anti-aliasing (FXAA)"; nx.log "frames: VRAM ..." every 10 s.
- Next, in order: (1) user play test; (2) coloured / black-background prompt sprites (Stats "Other Info (X)" yellow,
  "SELECT (A)" combos) - extend find_discs.py to non-white discs; (3) attack Session gate; (4) Tsubasa face shadow
  (needs the user's save/screenshot); (5) full UHD pack from dump_all (user's call, hours of GPU); (6) FSR 1 needs a
  shader compiler (ask the user).

### Sharpening (commit 68cae8b, verified by A/B screenshots + batches)
- No GLSL/HLSL -> SPIR-V compiler here (Windows SDK dxc.exe has no SPIR-V codegen), so the shader is built with
  Ryujinx's MIT SPIR-V builder: tools/spvgen (own project, references private/third_party/ryubing Spv.Generator)
  -> runtime/src/sharpen_spv.h (committed; regenerate with `dotnet run --project tools/spvgen --
  runtime/src/sharpen_spv.h`). Shader source tools/spvgen/Sharpen.cs: contrast-adaptive, cross neighbours, weight
  peak x sqrt(clamp(min(mn, 1 - mx) / mx)), peak = -1 / (8 - 3 s). First build crashed the driver: the builder's
  Function() needs AddFunction() (no OpFunction emitted); a python opcode dump of the header found it.
- Present path (vk.cpp): staging images are R8G8B8A8_UNORM storage images with a view; present_async runs the
  compute pass (src frame sampled, staging written) instead of the copy when sharpen > 0 (descriptor set per staging
  slot + one for screenshots). shot / F12 dump the sharpened frame (shot_source). Setting sharpen 0/35/65/100
  (settings menu "Sharpening" Off/Low/Medium/High, launcher Display & FPS page), default 0.
- 4K field A/B (to_field replay, same position): visibly crisper floor/jacket, no halos; 60.0 fps both.
  uncap_batch NX_SHARPEN=65 4x150 s: 0 crashes.
- IMPORTANT: rebuilding tools/shaderc (NxShader.dll) restamps it and throws away the user's shader translation cache
  (cache/shaders.bin header = dll size + mtime). This session rebuilt it once by mistake and restored it: same source,
  same size 11264, LastWriteTimeUtc set back to FILETIME 134372452221816453 (read from the cache header).
- agent_scripts: batch.ps1 takes any number of env k=v (was only the first); uncap_batch.sh forwards extras.

### Button icons: coloured discs
- Yellow "(X)" (Stats "Other Info (X)") = atlas 16f810b5373bff80 at 1274,904 and 1274,972 (32x31 + 2 px black ring);
  found by a yellow-disc scan of dump_all (only these two). Cell.fill = disc colour (0xFED128); with a fill every
  glyph is black. Self-test checked both styles.

### Final check (session 26)
- uncap_batch 4 x 600 s, NX_SHARPEN=65 NX_PAD_ICONS=playstation, 4K: 0 crashes, battle cues 80/47/17/4; VRAM used
  2.24-2.31 GB at 673 s (same as at 250 s: no growth); saves md5 unchanged; user's settings.ini unchanged.

## Milestone 5, session 27 (2026-10-29 afternoon, with user; commits a397e7a, 0ed3c45)

**NEXT (resume here):** user play test of the items marked "verified by agent"; then the open list at the end.

### User report 2026-10-29 (240 fps run, launcher) and status
1. FPS / pacing: great (user). 2. PS icons partly; "SELECT (A)" still Switch -> DONE (below). 3. UHD pack: later (user
asks). 4. F1 menu pad button: it was already L3+R3 (now also closes it; footer says so). 5. Walk speed in F1 -> DONE.
6. Random battle music never played -> FIXED. 7. First strike works (user). 8. F1 menu works (user). 9. No motion
blur is fine (user). 10. Tsubasa face shadow still there; user thinks material shader; hard to see in screenshots,
visible in game -> OPEN. 11. Effects too fast at 240: a camp menu circle + cursor circle, b Artists NEW / "check it
out", c battle green circle / ROUND Action / COMMAND, d enemy target circle, e "SELECT (A)", f level-up/RESULTS
screen effects, g topic map (above HELP) -> a-f gated (below), g OPEN. 12. Skill descriptions work (user).
New requests: autosave after every battle (F1 option) -> OPEN (see below); Return to Title / Quit inside the game's
own menu -> DONE as camp-menu (-) dialog.

### Random battle music (commit a397e7a, verified by agent: batch logs "bgm: 55 (played 57)" / "(played 61)")
- Battles start their music by NAME, not through bgm_play: battle start 0x2c6388 -> 0x2ddd0c(mgr, encount BGM name)
  -> bgm_play_name 0x25fce0 (s0-s2 floats, r0, r1, r2 = cue name, r3; name -> index 0x42e694). Hook: with the setting
  on, look the name up (gcall inside the hook: save/restore the whole Cpu, it clobbers s0-s2) and, for a pooled
  battle track, call the bgm_play hook with the index (it picks the random one). Lookup only when the setting is on.

### Walk speed in F1 (commit a397e7a): walk_speed()/set_walk_speed() in hle_sys.cpp (atomic, live: rewrites the two
walk dt literals with g_game_dt x k). Menu 1x..3x, saved as walk_speed.

### Speech-bubble (A) prompts (commit a397e7a, self-test verified)
- Camp "SELECT (A)" = atlas a4c81da53e4659cc (1024) grey disc 858,544 48x48; Artists "check it out! (A)" = atlas
  df5661e8b0521c20 (2048) grey disc 980,1978 32x32 inside a white ring. Bubble look (Cell look 3): grey 0xA6A6A6 disc,
  white glyph (the game tints the bubble green). Found with a grey-disc + white-ring scan (scratch greydisc.py; add
  to tools/padicons if more are needed). L/R dotted page discs (menu atlas 9addc8475d0d1011 etc.) still Switch.

### UI speed above 60 fps (commit 0ed3c45, verified by agent with coverage counts at 60 vs 240)
- Same rule as ui_manager_update (s22): run on 30 Hz ticks (tick_due) + frames with a new press (pad_pressed_now).
  ui_skip(key) helper; control `uigate N` (0 off, 1 ticks+press, 2 ticks only) for A/B tests.
- camp_update 0x313ac8 (camp menu manager; top menu 0x34d760 counts +0x1c/+0x8c, draw 0x34ddf8 animates from them):
  0x34d760 92/3 s at 60 and 91/3 s at 240 (was 723).
- btl_ui_update 0x2e9540 (battle UI task: command wheel 0x2ea044/0x2eb924, timeline 0x2edea0, ~20 parts): parts 90/3 s
  at both rates. party_hud_update 0x24e5b0 (portrait HUD, blink animator 0x24aad8; ticks only).
- btl_wheel_input 0x2b21c8: wheel hold-scroll counter +0x195ac (step every 10 calls) ran per frame: one 150 ms press
  = 3 steps at 240 (also with the gates off: pre-existing). Gated (key obj+0x195ac): 1 step per press, hold rate =
  60 fps (22-23 steps / 3.3 s). Other 0x25c950 (held) users: 0x31bef4 (now gated), 0x26fff8, 0x25a510, 0x332c08,
  0x33d964, 0x41f2fc, 0x44627c (Lua Pad?), 0x46a69c, 0x483b1c (gated) - unchecked.
- Post-battle screens (GATED_TASK macro, own tick key obj+1+line because tasks share objects, skipped frames return
  the last real return value): result_update 0x483120, result_parts_update 0x483b1c, levelup_update 0x31b7dc,
  levelup_parts_update 0x31bef4, skill_learn_update 0x26ebfc, result_flow_update 0x318010, result_bg_update 0x47f964,
  result_bg_parts_update 0x47fc5c. RESULTS parts 91/3 s at 240; battle -> results -> field at 240 OK.
- NOT done: topic map (g). TOPIC map tab = automap draw task 0x4a4cc4 (+ 0x4a9708 -> 0x4c0b94 renderer); no int frame
  counter found (framecount found only player counters); the moving part may be a float that wraps.
- Field task 0x4a338c writes per-frame counters bc9c38xx (field enemy manager region; still runs in battle). Unchecked
  whether that is visible (symbols?).

### Camp menu Return to Title / Quit (commit 0ed3c45, verified by log: new process started)
- camp_update pings overlay_camp_seen; while the camp menu is open a "(-) Title / Quit Game" pill shows bottom-left;
  minus opens "Leave the game?" Return to Title / Quit Game / Cancel (default Cancel). Return to Title = restart the
  exe (same command line, folder, environment) - no engine teardown. Caveat: the child reopens the same log files.
- A real item inside the game's System submenu (Save / Load / Mode / Settings sprites in menu atlas 9addc8475d0d1011)
  would need the camp menu code + label sprite; not attempted.

### Autosave after battle (superseded: DONE, see "Autosave (session 27 later)" below; findings kept)
- Lua save API: evtSaveCreate (0x4364d0 -> 0x2691b0 creates the save object 0x268e74, tasks 0x26900c), evtSaveIsRun
  (0x4364f0), evtSaveGetExec, evtSaveDelete; SetGameDataState 0x43bc24 -> 0x354a80 (state at save +0x52514).
  ScriptCommon/Utility/SaveUtility.lua SaveWakeUp uses them ("MIDDLE_SAVE" dialogs). The save object runs a full
  save-screen flow (0x266a7c: loads resources 41000/0xa029, fades; 0x266b88 UI) = slot picker, not silent.
- Silent autosave needs the inner slot writer (find who writes save_N.bin through our fs HLE during a manual save:
  log the fs write call chain) and a decision on which slot (user: dedicated slot?). Ask the user.

### Debug additions
- control `actors` (every actor: handle, tag, vtable, position; no enemy symbols were near the base60 field end).
- NX_ANIM_PROBE resolves member-function tasks (0x3134f4 and byte-identical copies 0x318c98, 0x320c10, 0x2794e8,
  0x47fe1c, 0x488fb0, ...) to the bound function.
- Replay base60.rec needs NX_WALK_SPEED=2 (recorded with the user's ini walk_speed 2) and NX_RES=4k to reach the
  tutorial battle (~181 s); at 720p / walk 1 it ends in the field without a battle. Battle then waits at the
  command wheel (Escape selected) after "replay finished".
- shot helpers used: scratch shot.sh / strip.ps1 (crop strips of several shots) - simple, rewrite when needed.

### Checks
- uncap_batch 4 x 240 s 4K, NX_WALK_SPEED=2 NX_RANDOM_BATTLE_BGM=1: 0 crashes, battle cues 17/53/35/47, VRAM 2.2-2.3 GB
  used. Saves md5 unchanged; user's settings.ini restored (tests ran with it moved aside; a default one reappeared and
  was replaced). textures/dump restored (test dump moved back).

### Open, in order
1. User play test (camp menu, battle HUD/wheel, RESULTS at 240; SELECT/check-it-out icons; random music; walk
   speed in F1; camp (-) Title/Quit; autosave slot 20). 2. (autosave done) 3. Topic map
   animation (g). 4. Tsubasa face shadow (user: maybe material shader; needs a save near the scene). 5. Other held-
   counter users listed above. 6. Attack Session gate. 7. UHD pack when the user asks.

### Autosave (session 27 later, commit e5b66a6, verified by agent: written, listed, loaded)
- User decision 2026-10-29: autosave goes to its own slot. The game has 20 slots (save list built 1..20 in 0x26a394);
  Load scans save:/ and shows every save_N.bin -> autosave = slot 20.
- Save state machine 0x2694ec(mgr 0x9f3d38 = *0x9ef5fc, slot): alloc 0x535c0, 0x352dd4 (0x4aad6c syncs the player,
  then memcpy of game data *global+0x10), 0x269708(mgr, buf) header (reads buffer from mgr+4: date, play time,
  episode/scene), file job 0x5cf7fc -> 0x5cf4dc (nn::fs write), then 0x26a804 (save-screen slot widget: mgr+0x14 list
  is NULL outside the save screen -> do not call), gamedata+0xa6b94 = last slot, system.bin = gamedata+0xa6b90 (0x200).
- Ours (hle_sys.cpp autosave_try): btl_open_chance arms; btl_ui_update / GATED_TASK hooks stamp battle_ui_seen; the
  first player_walk 0x40b594 / player_run 0x40b6fc probe >= 3 s later: operator new 0x5a8720, mgr+4 = buf, 0x352dd4,
  0x269708, mgr+4 = 0, host write save/save_20.tmp -> MoveFileEx save_20.bin, delete 0x5a87f8. Skips if mgr+4 or
  mgr+0x2c (game save running). system.bin and the last-slot byte untouched. Setting autosave (default 1), F1 item.
- Verified: battle -> results -> field -> walk: "autosave: slot 20 written"; header like a menu save (state 0, date
  2026/10/29 21:26); title LOAD shows slot 20 (Prologue / I. Daitama Lower Lv / 0:34); loading it puts the party at the
  same spot with post-battle HP (83 / 55). Test file removed afterwards; user saves md5 unchanged; ini restored.
- Risk (unverified): a battle followed by an event where the script walks the player could save mid-event. Launcher
  has no autosave item yet (F1 only).


## Milestone 5, session 28 (2026-10-29 ~22:40-23:15, with user; PAUSED at 5-hour usage 98%, WIP commit)

### User report 2026-10-29 (after the s27 build) and decision
- USER DECISION: UI must NOT run at 30 Hz. Reference speed = 60 fps: at 60 every frame updates; above 60 never faster
  (smoother where the game allows); only fps 30 runs like 30. -> all UI gates now use a 60 Hz clock (below).
1. Camp menu opening transition still fast / not paced like 60 -> 60 Hz gates (NOT re-checked by eye).
2. Level-up screen blinks white (REGRESSION from s27) -> FIXED by code (below), not seen in a run (no level-up repro).
3. Title LOAD "SELECT (O)" bubble fast -> save_screen_update gate (below); rate NOT measured yet.
4. F1 menu text cut off at the bottom -> rows scroll with the selection (overlay.cpp), NOT checked on screen yet.
5. Return to Title opened a new window -> now in-process (below), NOT verified yet.
- User has not tried autosave yet.

### Changes (source; tms.exe in private/tms/build was built WITH a temporary "TMPRATE" log line in save_screen_update,
removed from source: rebuild before handing over)
- hle_sys.cpp: g_tick60 (frame_begin; at most one per frame) + ui_tick_due (own map g_ui_tick). ui_manager_update,
  ui_skip (camp, battle HUD, wheel input, GATED_TASK), party_hud_update, pad key repeat (pad_repeat) use 60 Hz.
  Battle process/task timers, field spawn countdown, Lua resume stay 30 Hz (game-timing sync, not UI).
- Level-up blink root cause (decompiled): the "parts" tasks are draw-only: levelup_parts_update 0x31bef4 ->
  0x31c898/0x31cb84/... immediate sprites (0x5754e8 begin .. 0x5757cc submit), 0x4890a0 fill, 0x489568 button
  prompt; counters +0x68/+0x318 are stepped by levelup_update 0x31c2a0. Same for result_parts_update 0x483b1c and
  result_bg_parts_update 0x47fc5c. Gating them dropped the drawing on skipped frames. Now DRAW_TASK (every frame).
  GATED_TASK keeps its last return per key (all these tasks return 1 anyway).
- names.txt: 0x266b88 save_screen_update (save/load screen: 0x266cbc list/input, 0x26cb64 star field +0x124 per call;
  returns 1 when done -> skipped frame returns 0). 0x47146c field_play_update (field play state, vtable 0x7e6454).
- Return to Title: Lua ChangeTitle = 0x44911c -> 0x46c274 sets flag *0x9f52a0, but only the event-end state 0x47203c
  reads it (tested: flag set from the camp hook did nothing). The game leaves the field with 0x46c1a0(next scene;
  4 = title, 6 / 3 other) + 0x46ed90(state obj, 8). Hook field_play_update: on the overlay request call those two
  and return 0. UNTESTED: whether the field play update runs while the camp menu is open (if not, the exit happens
  when the menu closes; may need closing the menu first).
- overlay.cpp: F1 rows window (vis rows fit the window, top follows sel, arrows when rows are hidden).

### Boot abort (pre-existing, seen 10-26 once, 2 of 4 starts tonight - both the FIRST run after a fresh build)
- "FATAL: guest abort '' ... WaitSystemEvent+0x3c" ~1.9 s after start, right after "vi: vsync event ... state 2".
  Next run boots fine. Lead: WaitSystemEvent on the vsync event (ui.cpp vi_VsyncEvent: attach_system_event, then the
  event is pushed to g_vsync_events) vs kernel wait_sync result; maybe a startup race when the new exe starts slowly
  (Defender scan?). Not investigated further.

### Next (in order)
1. Rebuild (TMPRATE removed). Measure save screen rate: uigate 0 vs 1 at 240 (temp log or coverage).
2. Test Return to Title from the camp menu (log "field: return to title", title appears, same window); if the camp
   menu blocks it, close the menu first.
3. F1 menu on screen (desktop capture: overlay is a separate window; $TEMP/desk.ps1 style CopyFromScreen).
4. Level-up screen at 240 (needs a battle with a level up; autosave risk: save_20.bin exists - user's? keep md5).
5. Boot abort race. 6. Older open list (topic map anim, Tsubasa shadow, held-counter users, Session gate, UHD pack).
- Saves: md5 before tests in %TEMP%/claude_s28_save_md5.txt; this session only loaded slot 2 (no save written).


## Milestone 5, session 29 (2026-10-30 00:05-, agent alone after the usage reset; commits e7c4d46, 150c1eb, ...)

### Done (agent-verified, NOT user-tested)
- Rebuilt without s28's temporary TMPRATE log. First run after each fresh build booted fine (no boot abort in ~20
  starts this session).
- Title LOAD screen pacing (s28 item 3). save_screen_update 0x266b88 is only the camp Save screen: on the title LOAD
  screen it never ran (NX_COVER). Title LOAD = title menu state class (vtable address point 0x7e6934): update
  0x4a07e8 (case 4 calls load_screen_update 0x2621b8), draw 0x4a0b18 -> 0x263768 (0x2637a0 star field draw,
  0x263840 slot list + SELECT bubble: pulse = +8 % 18, 0x263d94). load_screen_update steps +8 once per call and runs
  the star field 0x26cb64: hooked with the same ui_skip gate (skipped frame returns 0 = not done). Measured with a temp
  counter: 60 updates/s at 240 and at 60 fps, 30/s at 30 fps. Camp Load (0x337c58) uses the same function.
  Method that found it: `watch <addr> 4` on a float the frame-count dump flagged -> writer chain -> title draw task.
- Return to Title (s28 item 5), commit 150c1eb. Verified by run: camp menu -> (-) -> Return to Title -> menu closes,
  title screen, A -> LOAD -> slot 2 loads and plays (camp opens/closes, walking). Findings:
  - camp_update 0x313ac8 runs EVERY field frame; camp state short at 0x7dd8f0 (pointer slot 0x9efb40): 0 = closed,
    6 = open (dumped). overlay_camp_seen now only pings while it is non-zero (pill / dialog only with the menu open).
  - field manager (ctor 0x46b45c) holds state objects at +0x28.. (index n at +0x28+4n): 0 = map load (vtable 0x7e6408,
    +8 = 0x46ee28 opens the "now loading" widget via 0x247d74(1)), 1 = free roam (vtable 0x7e654c, update 0x47345c =
    NEW hook field_roam_update), 5 = camp open (field_play_update 0x47146c: state 1 opens the camp, 2 waits for camp
    mgr *0x9f3dfc +0x14 == 0, then resumes or, for a Load from the menu (mgr +0x10 == 2), cleans up + 0x46c1a0(6) +
    0x46ed90(obj, 8)). 0x46ed90(obj, n) only sets obj+4 = next state; 0x46c1a0(n) sets the next scene.
  - Failed tries (all reached the title scene, title movie decoding): leaving from field_play_update with the menu open
    left the camp menu drawn over the title; leaving in its state 2 after the menu closed (ChangeTitle mimic, or the
    game's Load exit + scene 4) left the now-loading circles over the title; closing it with Lua CloseNowLoading
    0x45d744 on the title's first update did not help.
  - Working: overlay presses B (150 ms on/off) until the camp state is 0 for 300 ms, then sets the request;
    field_roam_update does 0x46c1a0(4) + 0x46ed90(obj, 8) like the event-end state 0x47203c. Input injection:
    overlay_buttons() ORed into the pad in ui.cpp poll_input. Gives up after 10 s ("camp menu did not close").
- F1 menu (s28 item 4) on screen (desktop capture of the window; overlay is a layered window): 13 rows visible in a
  1280x720 window, list scrolls with the selection, ▲/▼ shown when rows are hidden, wrap from last to first works.
- Level-up screen at 240 (s28 item 2): NOT verified. base60.rec (replay at 60 - it desyncs at 240: replays are
  keyed by pad reads, so replay at the recorded fps, then control `fps 240`) reaches the tutorial battle; that battle
  gives no level-up, only skill inheritance ("NEW SKILL!" via skill_learn_update) -> field; no white blink in stills.
  The "Skill Inheritance" tutorial popup after it needs B (A alone does not close it; to_field.sh also sends b).
- Boot abort (s28 item 5): not reproduced (0 in ~20 starts, several first-after-build). kernel.cpp wait_sync now logs
  "kernel: wait on bad handle <h> (i of n) in '<thread>'" before returning R_BAD_HANDLE (the SDK's WaitSystemEvent
  aborts on it): the next occurrence names the handle/thread. Other candidate: R_CANCELLED from a stale
  CancelSynchronization flag (t->cancel is set even when the thread is not waiting).
- Checks: saves md5 unchanged (%TEMP%/claude_s28_save_md5.txt) after every run; user's build/settings.ini was moved
  aside for tests and restored (copy %TEMP%/claude_s29_settings.ini). Tests ran with NX_AUTOSAVE=0 for battles.
- Test helpers (scratchpad, rewrite when needed): rate.sh (boot, title LOAD, temp counter), rtt.sh (slot 2 -> camp ->
  (-) -> Return to Title, shots), desk.ps1 (capture the game window from the desktop incl. the F1 overlay; L3+R3 in
  one control write opens F1: printf "l3\nr3\n" >> ctl).

### Next (in order)
1. User play test of s28 + s29: camp menu opening speed at 240, title LOAD SELECT bubble, Return to Title, F1 menu,
   level-up screen (needs a battle with a level-up), autosave slot 20.
2. Level-up screen check by agent needs a save before a battle that levels up (ask the user for one).
3. Boot abort: read the new "wait on bad handle" line if it happens again.
4. Older list: topic map animation, Tsubasa face shadow, other held-counter users, Attack Session gate, L/R page dots
   still Switch icons, launcher autosave option, UHD pack when asked; GitHub only after the user's full test.

## Milestone 5, session 30 (2026-10-30 05:30-, with user report; commits 53ffe71, f78f6f1)

### User report (test of s28 + s29 at 240 fps, run logs/nx_20261030_013158.log, 8 battles)
1. More stutter than usual. 2. Camp menu open (white circle) still fast. 3. No crash. 4. Level-up screen works.
5. Level-up skill inheritance "SELECT (A)" still Switch A. 6. Enemy skill banner ("Bufu / Enemy Dark Mage") missing
sometimes (regression). New: battle voice subtitles (asked if possible), Guard recovers 10% HP/EP (toggle), settings
inside the game's own menu like the BotW PC port (asked if possible; keep L3+R3), full UHD upscale (start it).

### Done (agent-verified unless noted)
- Stutter = pipeline creation: user run 6079 ms in all (hitches 330-584 ms) vs 738 ms in the 10-29 runs with the same
  ~28k pipeline requests. cache/pipelines.bin had shrunk 19.6 -> 10.8 MB (a run saved only its own VkPipelineCache over
  the file; s29 test runs most likely). Fix (vk_shader.cpp): every save (10 s, present thread) now runs on a worker:
  file -> fresh cache, merge ours into it (vkMergePipelineCaches; dst is private, so no sync with live creation), write
  tmp + rename. The file can only grow. Not user-verified; the first user run refills what the shrink lost.
  Median fps 160 in field/battle at 4K/240 is the same as 10-29 (not a regression).
- Autosave file write (write-through) moved to a worker thread (was on the game thread after battles).
- Camp open/close wipe = its own task camp_wipe_update 0x318e40 (draw 0x318ef8; +0xe wipe steps, +0x10 ring angle,
  +1 per call; camp_update waits on it via 0x3199ec). Gated with ui_skip (60 Hz). Shots: 60 vs 240 same length.
- Level-up SELECT (A): HUD atlas m_window003 (ea576a96a510fd6e, 2048) cell {1890,226,32} and its 1024 copy
  (9fd0da0c8aec7663) {945,113,16}: white disc with the A knocked out (game draws it dark over a green disc). New cell
  look 4 (cut-out): disc painted white, glyph black, copied back as white with alpha = luminance. Self-test checked.
  Found via tools/texextract --list (new: hash -> pack, file) + contact sheets of the _US Interface atlases.
- Guard recovery (setting guard_regen, default 1, F1 item): hook btl_apply_action 0x304664 (after the call): skill 6 =
  Guard; unit = 0x2b4c2c(battle = **0x9ef428, actor id rec+4); data = unit vt+0x14c: +2 party slot (enemies 10), +0xc
  HP, +0x10 max HP, +0x14 EP, +0x18 max EP (u32, matched with HUD). +ceil(10%) each, clamped. Verified: HP 110 -> 128 /
  178, then an enemy hit 25 -> HUD 103. NX_DEBUG_BATTLE=1 logs every action with the actor data.
- UHD: full run started 06:13 in the background (python tools/uhd_pack.py private/tms --dump .../dump_all --sources
  private/tms/textures/sources.txt > textures/uhd_full.log). 9577 textures (BCn colour + RGBA8 Interface atlases),
  ~16/min -> ~10 h, ~23 GB. Old pack moved to textures/pack_s21 (425 files). uhd_pack.py now: chunks of 40 (resumable:
  done files are skipped), realesrgan-x4plus for pack_000_map, anime model for the rest, alpha upscaled by the model
  (crisper UI edges), 4x for textures <= 256, 2x otherwise; pad-icon atlases are skipped at runtime anyway.

### Not done / open
- Enemy skill banner: NOT reproduced. Tutorial battle at 240: ally banners (Zio, Attack, Soft Drink) and enemy
  "Attack / Enemy Blob" show. Slot 20 floor had no enemies left. Needs the user's case (fps, enemy, how often, save).
  Battle HUD = btl_ui_update 0x2e9540 -> 18 parts (setup 0x2e9290; draw task phase 0x21); +0x58 = double update mode.
- Battle voice subtitles: feasible (answered user, not started): CRI log already names the wave per play
  (SoundPlayer_SetWaveId, ACB) -> transcribe JP battle voice AWBs with faster-whisper (C:\Users\user\Tools\whisper-venv,
  as for FFR), translate, show in the overlay; toggle. Big job.
- Settings inside the game's own menu: feasible, big (game's camp System/Settings screen + its msbt texts + hooks).
  Awaiting user go-ahead. L3+R3 overlay stays.
- Test hygiene: tests ran with the user's settings.ini in place this session (only env overrides), NX_AUTOSAVE=0; save
  md5s unchanged (/tmp/s30_md5_before.txt).

## Milestone 5, session 31 (2026-10-30 06:30-, with user; commits e530319, 5d21017)

### User input (reply to s30)
- Enemy skill banner missing: SOMETIMES only, at 240 fps; both Dark Mage (Bufu) and enemies that use a basic attack.
  User had not tested the s30 build yet.
- UHD: keep the full run going; the pack must be toggleable (people should see the difference) and must NOT cost
  stutter/lag (preload, caches, whatever it takes) - give people a reason to install it.
- Go: battle voice subtitles first, then settings inside the game's own menu. Keep the rules, record notes/memory.

### Done (agent-verified, NOT user-tested)
- Battle voice subtitles (setting voice_subs, default 1, F1 item "Battle voice subtitles").
  - Voices are loose files Sound/Voice/Jp/<name>.adx in pack_040_sound.cpk (17069 files; BTL_* = 3168 battle lines).
    The CRI trace line "#CRIATOM, ..., ExPlayer_SetFile, player, binder, Sound/Voice/Jp/BTL_....adx" names every line
    played; CRI builds its trace format at run time, so game_log (hle_sys.cpp) checks the formatted text (with
    NX_GAME_LOG=0 only formats starting with '#' or '%' are formatted).
  - Pipeline (tools/subs): transcribe.py (vgmstream-cli -> wav, faster-whisper large-v3 in Tools/whisper-venv, ~1/s;
    output private/tms/subs/transcripts_jp.json, all 3168 done) -> hand translations tools/subs/en/<GROUP>[_n].txt
    (key|English) -> build.py -> data/subtitles_en.tsv (stem, seconds, speaker, text; CMake copies it next to tms.exe).
    show.py <json> <GROUP> prints untranslated lines (grunts filtered). 2101 lines translated: all party / Mirage /
    boss lines with words. Left out: grunts, generic soldiers em20xx (non-verbal; whisper hallucinates "thanks for
    watching"), np2312 (noise), unclear audio.
  - Speakers: pc1001 Itsuki, 1002 Tsubasa, 1003 Touma, 1004 Maiko, 1005 Barry, 1006 Eleonora, 1007 Mamori, 1008 Yashiro,
    1009 Kiria, 1010 Tiki; mr1051 Chrom, 1052 Caeda, 1053 Cain, 1054 Tharja, 1055 Virion, 1056 Draug; em1057 Navarre,
    em1008 Yashiro (as enemy); em2307/2308/2309 Dark Tsubasa/Kiria/Yashiro (their own lines). Other bosses unnamed
    (names in Message/USen/Common/BtlName.msbt + CharacterName.msbt, but not which em id is which).
  - *_mix clips = party member + Mirage in one file: build.py composes "A // B" from the two single lines (order from
    the transcript); subs.cpp shows two rows (stem#2). Max 2 rows on screen (a third would reach the action banner).
  - Drawing: runtime/src/subs.cpp worker thread draws with DirectWrite on a WIC bitmap (Segoe UI semibold, black
    outline, speaker coloured: party lime, Mirages blue, others red); vk.cpp overlay_subs blends it over the staging
    image with a compute shader (tools/spvgen/Overlay.cs -> overlay_spv.h; `dotnet run --project tools/spvgen --
    overlay runtime/src/overlay_spv.h`). Screenshots (F12, control shot) include it. Position: bottom strip
    (y = 0.99 h - height), under the battle action banner. Verified in 4K shots ("Itsuki: Strike, lightning!").
  - Lesson: OpSelectionMerge must come right before its branch (condition computed before) or the driver crashes in
    vkCreateComputePipelines (no spirv-val here; tools: write a dump like the s31 scratch one).
- F1 "UHD textures" On/Off (tex_pack -> NX_TEX_PACK, applies after a restart). Not live.
- Test hygiene: saves md5 unchanged, cache/pipelines.bin 16.6 MB before and after.

### Not done / next (in order)
1. User test: subtitles in battle (position, wording, missing lines), F1 toggles.
2. UHD: full run in background (textures/uhd_full.log; started 06:13, ~10 h). When done: measure hitches with the full
   pack (hitch log "texture uploads"), consider pre-reading pack files of a map at load (file cache), live A/B toggle
   (swap pack images out: im->own keeps no original data, so the originals need a re-upload -> mark written=false).
3. Settings inside the game's own menu (big RE job). Leads found s31:
   - Camp > Settings texts: Message/USen/Camp/Camp.msbt labels CAMP_SETTING_* (BGMVOL, SEVOL, VOICEVOL, MSGSPEED,
     PLAYRECORD, CAMMOVELR/UD, CAMLRBUTTON, BATTLECURSOR, GLASSES, DIFFICULTY; HELP_* = help line; SELECT_* options;
     CONFIRM "Apply these settings?").
   - Item table in main rodata at 0x7ddd98: 11 records of 40 bytes {u32 kind (0x4e6a = volume slider, 0x4e6b = choice),
     label ptr, help ptr, u32 flag (1 = difficulty), u32 option count, 5 option label ptrs (0x74f436 = empty)}; ends at
     0x7ddf50. Words just before (0x7ddd80..0x7ddd94 = 0x33bea4, 0x33beb4, 0x33bff4, 0x33c030, 0x33c0a0, 0x33cb14) and
     after (0x33d5a4, 0x33d754) look like the settings screen's methods. No absolute pointer to the table: found by
     PC-relative code -> decompile 0x33c0a0 / 0x33cb14 (Ghidra headless private/tms/ghidra) to find the loop + count 11.
   - Plan: hook the screen to use our own table (guest heap copy + our items: max 5 options, so fps as a choice of 5 or
     a slider), resolve our labels ("TMSR_*") in the msbt text lookup hook, apply/save through settings.ini on the
     screen's confirm. F1/L3+R3 overlay stays as it is (user).
4. Enemy skill banner (sometimes, 240 fps, Dark Mage + basic-attack enemies): battle HUD btl_ui_update 0x2e9540 ->
   18 parts, +0x58 double update mode; suspect a banner part whose show/hide timer runs on the 60 Hz UI clock while the
   action ends on battle ticks (short enemy actions at 240 fps). Needs a repro: enemy-heavy battle save.

## Milestone 5, session 32 user report (2026-10-30 07:55, user tested s31 build; user asleep, work resumes 10:00 by scheduled task tms-recomp-s32-resume)

User results:
1. Guard regen WORKS, but the HP/EP bar refill animation shows only on that character's next turn. Must show at once when guarding.
2. Voice subtitles WORK, but the bottom strip collides with the command wheel and the skill-help ticker ("...ed weapon..."). User wants them just BELOW the turn-order UI (top).
3. Enemy "!" icon before a skill is selected animates too fast (not 60 pacing); after selecting a skill it is correct 60 speed -> two code paths, gate the pre-select one (UI reference = 60, g_tick60).
4. Camp -> Load in a dungeon: "This will load the save data... Proceed?" Yes/No still shows Switch "SELECT (A)" bubble.
5. Autosave: CONFIRMED working.
6. Stutter: CONFIRMED gone (s30 pipelines.bin merge fix).

User asks next: fix 1-4; finish open work (in-game settings menu, enemy banner, UHD check/live toggle); LAST: everything must work WITHOUT the uncensor patch (no breakage from patched vs unpatched data), VRAM leak + stutter check, optimization; then ZIP the program + launcher (no ISO/game files/uncensor patch/saves/caches) and a SEPARATE optional UHD texture ZIP. Do not ask the user; record everything here.
## Milestone 5, session 32 (2026-10-30 10:00-, scheduled task, user asleep)

### Done (agent-verified by run/log/screenshot, NOT user-tested)
1. Guard recovery bar refill at once (commit "Guard recovery: tell the party HUD..."): the party HUD (portrait gauges)
   only re-read the unit on its next turn. Now after the HP/EP write the hook calls the game's own HUD setters:
   HUD = ld32(ld32(ld32(ld32(0x9ef770)) + 0x18)); entry = 0x24d1e8(HUD, s16 unit+0x818) (0xb4-byte entries from
   HUD+0x28; +0x48 HP shown, +0x50 max, +0x68 EP, +0x70 max EP); hud_set_hp 0x24cf2c / hud_set_ep 0x24cf84 (value up =
   refill animation, type 2). Verified: base60 replay, Itsuki Guard -> HUD shows 128 0.3 s after the action (log
   "guard recovery: HP 110 -> 128 / 178 ... (hud bc99ea00 entry bc99ea28)").
2. Subtitles moved just below the battle turn-order bar (y = 0.145 h), 2/3 screen width (clear of the party
   portraits on the right), long lines wrap (DirectWrite layouts measured first). Verified 720p shot: "Tsubasa: Leave
   it to me!" under the bar, nothing overlapping. Wrapped (long) lines not seen in a run yet (54 of 2101 lines > 70 chars).
3. Enemy "!" while the Skills list is open = btl_weak_mark_draw 0x303290 (per unit, per frame, draws sprites
   0x1ad2768a / 0x1ad2768f-90 over the projected unit; pulse counter u16 unit+0xaca +1 per call, loops 4..0x13). It is
   a draw function, so it ran per frame. Hook keeps the counter on frames that are not a 60 Hz tick (game resets to 0
   stay). Found with the probe-range coverage build (wheel vs skills list, 60 vs 240: per-unit functions). Measured
   (NX_DEBUG_BATTLE log "weak marker N steps/s"): 60 at 60 fps, 60 at 240 fps; ungated (uigate 0) 240 fps = 120+.
   The post-select (target) marker 0x2f2c60 was already gated through btl_ui_update (182/3 s at both rates).
4. Camp Load "Proceed?" Yes/No: the black "SELECT (A)" disc is HUD atlas ea576a96 (1254,1866 32x32; 1024 copy
   627,933 16x16), look 1 (plain white disc). Also TOPIC menu atlases 512x512 (JP 2ebbd8bb, zh 31bb1f04 / 71afab7f, fr
   dc05f6d4; no English variant in dump_all) "Close (B)" 26,122 18x18 and "SELECT (A)" 100,281 16x16. Found by a
   dark-disc scan over textures/dump_all (scratch darkdisc.py: dark opaque disc with light glyph, contact sheet).
   Verified: self-test PS/Xbox crops and in game (720p shot: yellow bubble with PS circle).
- Test hygiene: cache/pipelines.bin 17402513 bytes before and after every run; save/* md5 unchanged.
- UHD full run still going: 2027 / 7942 at 10:05 (textures/uhd_full.log).

### In-game settings: RE so far (session 32, not implemented)
- Camp > System > Settings screen object S (methods at 0x7ddd80..: dtor 0x33bea4, 0x33beb4 = load its resources
  (layout 0x14, 2, fonts 0x4e21/0x4e22/2000), 0x33bff4 ready?, 0x33c030 release, 0x33c0a0 = update, 0x33cb14 = draw,
  0x33d5a4/0x33d754 dtor).
- Update 0x33c0a0: S+4 state (2 = browsing, 3 closing, 4/5 confirm dialog "Apply these settings?" (S+0x134 = 1 when
  leaving with B), 6/7 after); cursor row S+0x124 (11 rows hard-coded: `% 0xb`, last = 10); input code from
  0x34eaf8(S) (0 = A/confirm, 1 = B, 2 = ?, 8/0xe up, 9/0xf down, 10/0x10 left, 0xb/0x11 right).
  Row i state at S+0x1c+i*0x18: +0 label text object, +4 option text object (0 for the 3 volume sliders), +8 value,
  +0xc has arrows, +0x10 min, +0x14 max. Value change -> 0x586818(option text obj, font, option string ptr from the
  item table 0x7ddd98 (row*40 + 0x14 + value*4)); help line 0x319d54(.., 7, 0, help ptr). Rows 0-2 = volumes: live
  preview 0x25e37c(vol*k, .., channel). Row 10 uses another font (S table +8).
- Draw 0x33cb14: 11 rows (loop to 0x108 = 11*0x18), positions from layout parts 0xbebebf3+i, text objects drawn by
  0x20ccc4, sliders for rows < 3, arrows 0xbebec40/41 when +0xc.
- Apply: 0x33c7e8(S, config) writes rows into the game config bytes (+0..+0xe) then 0x3c169c + 0x26124c (save);
  0x33c8a8 = "restore defaults" path (0x3535a4 defaults -> 0x33b9e8 fills rows, refreshes texts).
- Plan (unchanged idea, refined): a second page in the same screen ("PC settings", toggled by a button shown in the
  help line): swap the 11 rows' label/option texts for ours (needs our strings through 0x586818: check whether it takes
  msbt labels or text), keep our values in S rows with our min/max, after every game update re-set the option text,
  and on the confirm/close path write our page to settings.ini (apply_* in overlay.cpp) and restore the game's rows
  so 0x33c7e8 never sees our values. Effort: several hours; risky. NOT started.

### Without the English/uncensor mod (session 32, agent-verified with NX_MODS_DISABLED=uncensored)
- The mod (mods/uncensored: pack_000_map, 031_message, 040_sound, 050_movie, 080_interface, 999_lua) ships the _US
  Interface atlases at 2x size; the game's own ones are half size with other hashes (texextract over the base pack
  with NX_MODS_DISABLED, now honoured by texextract too). Mapping (mod -> base): m_window003 ea576a96 -> 74557bfc (1024,
  already in the table), topic_window 94e020b4 -> 25e96f94, drc_tv b18094e4 -> 90b79255, status_drc001 16f810b5 ->
  57febd3b, saveload001 a4c81da5 -> ea81556a, camp002 df5661e8 -> 43e7b49d; button_icon 34c76342 and the other
  languages' atlases are the same in both. pad_icons.cpp: ATLAS_HALF entries reuse the cell tables at div 2. The topic
  table now also covers the (X) Details / Timeline pills (yellow 0xFBD130, ringed) and the topic ringed - / Y.
  Self-test contact sheet of every cell (PS + Xbox, mod and base atlases): all drawn in place.
- Runs without the mod: English text, base60 battle (skills list "!", subtitles "Itsuki: Strike, lightning!", PS
  icons in the HUD, detailed skill help), field -> camp -> System -> Load -> "Proceed?" bubble with the PS circle.
  Voice file names are the same (pack_040_sound), so subtitles match either way.
- UHD pack: replacements are by hash; textures the mod changed simply have no replacement without it (silent).
  The pack is built from the modded dumps, so unmodded _US Interface atlases stay original resolution. Not measured.

### Release packaging (session 32)
- tools/package/package.ps1 [-Out dir] [-Uhd]: TMSRecomp-<date>.zip = tms.exe, launcher.exe, SDL3.dll,
  subtitles_en.tsv, shaderc\ (no pdb/nupkg), README.txt (tools/package), LICENSE, THIRD_PARTY.txt (SDL3, libvpx,
  Ryujinx, Spv.Generator). No game files, mods, saves, caches, logs or settings.ini. -Uhd: TMSRecomp-UHD-<date>.zip
  of textures\pack via a junction (the script unlinks a leftover junction before any recursive delete).
- tms.exe now prefers <exe dir>\shaderc\NxShader.dll (release layout), else <data>\shaderc. The translation cache
  stamp compares the dll time in whole seconds (ZIP drops sub-second times; exact compare would have thrown the
  user's shaders.bin away). Verified: zip extracted to %TEMP%, tms.exe --data <user data>: "shader cache: 665
  translations loaded", title movie, caches unchanged (pipelines 17402513, shaders 22969084).
- Desktop: TMSRecomp-20261030.zip (15.7 MB). Note for a public release (user decision): tms.exe contains the
  translated game code (as every static recomp does); data must come from the user's own dump (README). The UHD ZIP
  waits for the full upscale run (2027/7942 at 10:05; ~500/h -> done around 22:00-23:00 10-30).
- NOT tested: launcher.exe from the extracted ZIP (GUI), a PC without .NET 10.

### Enemy skill banner (session 32, code reading only, no repro yet)
- Battle action banner ("Bufu / Enemy Dark Mage", "Zio / Artist Itsuki Aoi") = btl_ui_update part, update 0x2f0750
  (called from 0x2e95e4; so it runs on the 60 Hz UI ticks): state +0x14 (1 slide in, 5 steps; 2 shown, +0x18 up to
  +0x1c = duration+0x1a; 3 slide out, 5 steps; 0 idle), +0xc/+0x10 anim floats. 0x2f0238 starts the next queued
  banner (queue of 0x34-byte entries from +0x148, shifted down) when idle / sliding out / shown longer than +0x20
  (= duration+0x15): sets the skill text (0x27a8ec(skill id) or special cases -1..-5) and the actor line (+0x15c).
- 0x2efdb0 (start of the update) turns pending requests (+0x28: 24 x {unit id, kind 1..0x20, ?}) into queue
  entries, but only for units where 0x304298(unit, 1) == 0 and !(unit+0x84 & 2); others stay pending.
- Hypothesis to test with a 240 fps repro: an enemy request is added and the action ends before a 60 Hz UI tick
  (requests cleared or the unit check fails), or the queue entry is overwritten. Next: log enqueue (writes to +0x28)
  and 0x2f0238 starts with NX_DEBUG_BATTLE at 240 in base60 (Dark Mage Bufu + Blob attacks).

### In-game PC settings page (session 32, commit 026a6a1; agent-verified by run + screenshots, NOT user-tested)
- Camp > System > Settings: L or R switches between the game's page and "PC settings" (runtime/src/camp_settings.cpp).
  Rows: Sharpening, Walk speed, Frame rate (the 3 slider rows: one choice per press, the value is in the help line),
  Resolution, Display, Button icons, UHD textures, Battle voice subtitles, Guard recovers HP / EP, First strike on
  downed symbols, Autosave after battles (choice rows, max 5 options = the game's option slots). The other overlay
  items (bloom, glow, DOF, vignette, fog, outline, FXAA, skill help, random music, exit) stay in F1 / L3+R3.
- Each change applies at once through the overlay's own apply (overlay_setting / overlay_apply_setting by name;
  writes settings.ini like F1). Leaving the screen's browsing state (B, Defaults, confirm dialogs) first puts the
  game's rows back (values, ranges, label/option texts by label), so the game's apply 0x33c7e8 never sees our values.
- Texts: labels/options = the text objects' direct UTF-8 text (0x586488(obj, str)); the help bar is Lua (0x319d54 ->
  0x5ac3e0) and takes msbt labels, so Camp.msbt's TXT2 is replaced by a whole new block (count, offsets, texts) that
  the section table entry points to (+0 block, +8 size): our help for the row's CAMP_SETTING_HELP_* entry, and the
  hint "(L / R: PC settings)" appended to every game Settings help line (shown on open).
- Two failures on the way (recorded so nobody repeats them): (1) hooking msbt lookups (0x5c210c returns an INDEX,
  not text; hooking 0x5c22e8/0x5c23dc/0x5c2414 was not the cause of the stall below but was dropped); (2) the stall
  "frames stop when Settings opens" (busy loop in text layout 0x588d08/0x589d2c) = appending the hint after the FIRST
  0 byte: help texts hold button-icon tags with 0 bytes inside; now only the trailing terminator is stripped.
- Verified: PC page shows all 11 rows with current values; Sharpening slider -> settings.ini sharpen 65; subtitles
  Off -> voice_subs 0 (both restored afterwards); B leaves cleanly; reopen + L/R twice: hints shown, no stall, frames
  60/s. Not checked: changing game values and PC values in one visit then "Apply these settings?" Yes (code path:
  game rows restored first), difficulty option text after switching back inside one visit (no crash seen).
- Row 2 (Frame rate) is the game's voice-volume row: changing it plays the game's voice preview sample (harmless).

### UHD full pack, hitch + VRAM checks (session 32, agent-verified)
- Full upscale finished 10-30 11:56: textures/pack = 9540 files, 24 GB (log textures/uhd_full.log; old pack_s21 kept).
- Hitches (to_field.sh replay, 4K/60, two parallel runs): pack on 3 hitches (741 + 75 ms at boot, one 53 ms with 14 ms
  texture uploads), pack off 4 (756 + 108 at boot, one 64 ms). Frames 60/s, 0 gaps > 40 ms with the pack. VRAM used
  2570 MB with the pack vs 1725 MB without. So no per-map prefetch needed now (pack reads stay async).
- VRAM leak check: field + 15 camp open/close cycles: VRAM used 1780 -> 1868 MB then flat for 4 min while "images
  freed" kept rising (300 MB freed); working set 4.9 GB. No leak seen.
- Packaging fixes: package.ps1 calls Windows tar.exe by path (Git Bash's GNU tar cannot write ZIP), forces --format zip
  (bsdtar -a picks the format from the extension; ".zip.part" made a plain tar), writes to .part and renames (a failed
  run had already removed the previous Desktop ZIP). The UHD ZIP adds textures/pack in place (-C data) - no junction.
- Found by checking the ZIP: vk_shader's exe-dir translator path used "\/" (the backslash was lost in an edit), so a
  ZIP install never found its own shaderc\ (fell back to <data>\shaderc). Fixed; the cache log line now names the
  translator path.

### Session 32 end state (2026-10-30 ~13:30)
- Desktop: TMSRecomp-20261030.zip (program, 15 MB, real ZIP, verified extract + start against the user data, own
  shaderc used) and TMSRecomp-UHD-20261030.zip (pack, ~23 GB; see the check line below).
- User's settings.ini restored from the pre-test copy; saves md5 unchanged; cache/pipelines.bin 17402513 and
  shaders.bin 22969084 unchanged after every test.
- Built tms.exe in private/tms/build = HEAD (normal lift, no probes; NX_DEBUG_BATTLE logs only when set).
- Awaiting user (test list): (1) guard: HP/EP bar refills at once; (2) subtitles under the turn bar (wrapping of
  long lines); (3) skill-list "!" at 240; (4) camp Load "Proceed?" + TOPIC "Close"/"SELECT" icons; (5) Settings
  screen L/R PC page (values, help line, leaving with B, Apply dialog after changing game values too); (6) the
  program ZIP on another folder / PC, the UHD ZIP extracted into the data folder.
- Open: enemy skill banner (no repro in base60 at 240: the tutorial battle ends in ~8 s of auto-battle; the debug
  hook btl_banner_requests 0x2efdb0 logged nothing there - check that it is reached before relying on it); live UHD
  toggle (not started; restart toggle works); remaining overlay-only items could get a second PC page.
- Decisions for the user: public release scope (tms.exe holds translated game code; data from the user's dump).
- UHD ZIP check: TMSRecomp-UHD-20261030.zip = 11.48 GB (deflate from 24 GB), listing = README_UHD.txt + textures/pack/
  with all 9540 .dds (tar -tf, exit 0). Not extracted in full (24 GB); the program ZIP was extracted and started.

## Milestone 5, session 33 user report (2026-10-30 afternoon, user tested the s32 build)

User results:
1. Frame time + no stutter: CONFIRMED, user "genuinely impressed".
2. UHD pack: user cannot see a difference; wants the UHD toggle LIVE (no restart) to compare.
3. Field interaction prompts "(A) Talk" (Tsubasa NPC) and "(A) Exit" (door) still show the Switch (A), not the PS icon.
4. In-game PC settings page: user says "AWESOME, feels native" (CONFIRMED working). Missing: bloom, glow, DOF, fog,
   vignette, outline, FXAA etc. (still only in F1). Wants them in the game menu too.
5. Pressing A/circle on the PC page opens the game's "Apply these settings?" dialog and leaves the PC page (minor).
6. Some PC page help lines are cut off at the right (e.g. Sharpening). Wants a scrolling ticker or shorter texts.
7. Enemy skill banner still missing sometimes (Dark Mage Bufu).
User asked: do all open milestone work now; no GitHub upload yet. Question: Ryujinx files - needed? credit/licence?


## Milestone 5, session 33 (2026-10-30 16:15-, with user; agent-verified by runs + screenshots, NOT user-tested)

### Done
1. Field interaction prompts "(A) Talk" / "(A) Exit" / "(A) Check" ... (report 3): NOT in a UI atlas. Each prompt pill
   is a pre-rendered 512 x 128 BC3 texture of the effects Effect/map_0086..0095.ptcl (10 prompts x 5 languages = 50
   hashes, k_prompt_hashes in pad_icons.cpp). Found by drawlog with / without the prompt on screen (only 3 textures
   differ: the pill + two 64x64 ring arcs), then textures/sources.txt. Fix: vk_texture.cpp decodes BC3 level 0
   (decode_bc3), pad_icon_prompt finds the green (A) disc (leftmost round blob of opaque green; the pill border is
   wide) and paints the controller face (look 2: disc colour from the blob, black ring + glyph), and the result is
   swapped in as an RGBA8 image with a box-filtered mip chain through the pack swap path (g_prompts, key = hash +
   style * golden ratio, never freed: 50 x ~340 KB max). Offline check of all 50: disc found at x 43 / 89 / 135
   (3 pill widths), 54 x 54. Verified in game: Tsubasa "Talk" shows the PS circle (720p shot).
   A UHD pack file of a prompt is ignored while PS/Xbox icons are on (it would show the Switch A).
2. Live UHD toggle (report 2): pack index always loaded; rt::set_tex_pack / tex_pack_on (vk_texture.cpp) flip
   g_pack_on and bump g_pack_gen; images whose data has a pack file (Image::pack_file, pack_gen) upload again at
   next use (check_pool_texture). F1 item + PC page row switch at once. Verified: On -> 3 pack textures swapped in
   18-40 ms after the switch, Off -> back, frames 600/10 s throughout, no crash.
3. PC settings pages (reports 4-6): L / R steps game -> PC 1 -> PC 2 -> game (R; L reverse). PC 2 = Bloom, Glow,
   Depth of field (slider rows 0-2 as Off=MIN / On=MAX), Vignette, Fog, Outline, FXAA, Detailed skill help, Random
   battle music, 2 empty rows (no arrows). A on a PC page = next choice (wraps) via the new hook
   camp_settings_input 0x34eaf8 (A code 0 -> right 0xb, or at max: row = min + code 0x7f = no-op); the "Apply these
   settings?" dialog no longer opens from our pages. Help texts are our own short ones (k_pages, <= ~75 chars after
   "PC n/2 (L / R: pages)"). Verified: both pages render, A Bloom On -> Off (wrap), A Vignette On -> Off, B leaves.
4. Enemy skill banner (report 7): code read, NOT fixed. btl_banner_requests 0x2efdb0 queues pending requests only for
   units with u16 +0x838 != 1 and !(u8 +0x84 & 2) (unit = ld32(ld32(ld32(0x9ef428)) + 0xd8 + id*4); 0x304298 =
   "+0x838 == arg") and then CLEARS ALL pending requests: a request whose unit fails the check at that UI tick is lost.
   Hypothesis: at 240 fps the 60 Hz UI tick sees the unit in state +0x838 == 1 more often than the 30 Hz original.
   The base60 tutorial battle makes no banner request at all (its enemy action is a basic attack, skill 197), so no
   repro here. The request log is now ALWAYS on ("battle: banner request unit U kind K: unit+0x838 V +0x84 F"): the
   user's next run that misses a banner shows whether this drop is the cause. Second banner-like panel: 0x2f1cac
   (skill name panel, skill 0x18b closes it, 0xdc special) - not checked.
5. README Credits section (Ryujinx/Ryubing MIT shader translator + Spv.Generator, SDL3, libvpx, Vulkan-Headers).
   Answer to the user: the Ryujinx code is needed (it is the shader translator; without it nothing renders), it is MIT
   (compatible with GPL-2.0-or-later), and the MIT notice must ship with binaries (package.ps1 already writes it into
   THIRD_PARTY.txt); credit in README added.
- Tools: private/tms/ghidra/DecompRange.java (decompile all functions in [lo, hi) -> out.c; g.sh DecompRange lo hi);
  btlui_all.c = 0x2e0000-0x310000.
- Test hygiene: saves md5 = save_bak_s33/md5.txt (OK after all runs), settings.ini restored from save_bak_s33,
  cache/pipelines.bin 17402513 + shaders.bin 22969084 unchanged.
- Awaiting user: (1) field prompts with the DualSense; (2) UHD On/Off live in the PC page; (3) PC 2 page + A press;
  (4) a run where an enemy banner is missing: send the log time (issues/live log has the banner lines).

## Milestone 5, session 34 user report (2026-10-30 evening, user tested the s33 build)
1. PC page 2: works (bloom, vignette...). Asked: the 2 empty rows, intentional? (yes: 11 game rows, 9 items).
2. Camp menu (square) background: Itsuki/Tsubasa on the grass look blurry / not 4K, grass not sharp.
3. Guard regen: CONFIRMED. 5. Skill-list "!": CONFIRMED. 6. Field prompts Talk/Door show PS circle: CONFIRMED.
7. Live UHD toggle: CONFIRMED.
4. Enemy skill banner still missing: "when Blob attacks, no banner".
8. O on a PC page changes the value like Right; user expects the game's "Apply these settings?" dialog (native).
9. Tsubasa (and Itsuki) face: dark shadow still there; user is convinced it is the character material shader.
10. Attack Session gate: not done.
New requests: DLSS 4.5 + FSR (launcher, L3+R3/F1, in-game menu); FPS/VRAM/shader cache "ready for other users";
list everything not done since the project start; random battle music from external P5R ADX files with a matched
victory theme (example: 1 Last Surprise -> 300 P5R Victory).

## Milestone 5, session 34 (2026-10-30 ~17:20-, PAUSED at 5-hour usage 95% before any code change; nothing built)

### Findings (code reading, not yet tested)
- Enemy banner: the s32/s33 hook 0x2efdb0 (btl_banner_requests) is the WRONG panel: in the user's 17:07 run (battle +
  victory) it logged nothing (+0x24 never set). The skill-name banner is the panel at 0x2f1cac (open(panel, unit+0x278
  or action+0xc, skill id, ?, flag)), panel = ld32(ld32(*0x...)+0x20). Callers: 0x29049c (once per action, flag
  action+0xa8; enemy path, action record +0x48) and battle state machine 0x2a5c50 case 0x11 (player). 0x2f1cac
  RETURNS EARLY when panel +0x28 == unit and +0x20 == skill id (same unit + same skill as the last banner): check
  whether the close path (skill 0x18b -> state 2, +0x1c = 5) clears +0x20/+0x28 at 30 fps but not at 240. Panel update
  = 0x2f13b8 (from btl UI update 0x2e9540, 60 Hz gated), draw 0x2f157c. Next: names.txt entries + probes on 0x2f1cac /
  0x29049c, base60 replay at fps 30 vs 240 (Blob basic attack = skill 197), compare panel fields.
- BGM: bgm_play 0x25fbe0 = (s0-s2, r0, r1 = player slot, r2 = sound index, r3 = push sub-slot); both it and
  bgm_play_name call 0x25f2fc(s0-s2, r0, slot, acb, cue, push, ...). Index -1 (r2 < 0) = stop that slot WITH the push
  bookkeeping (designed path). 0x25f7c8 = restore a pushed cue (r0 slot, r1 from, r2 to): field music after battles
  (no bgm_play line after victory in logs). 0x25fdf8(slot, sub) clears a pushed entry. Logs: battle start = by name
  (+ 1157 env_battle, another slot presumably), victory = bgm_play(65).
- External music plan (not written): runtime/src/ext_bgm.cpp = own ADX decoder (v4 header: 0x24 loop flag, 0x28 loop
  start sample, 0x30 loop end sample; 18-byte frames x ch, 32 samples; flags 9 = scale XOR, P5R key9
  <keycode> (no longer in the code, s98: setting custom_bgm_key), start/mult/add as P5RAudioTools/to_adx.py key9_to_xor, xor advances per frame in interleaved
  order; save hist + xor at loop start) on a second SDL stream bound to the game's audio device (expose the device from
  hle_audio.cpp), gain = setting. Battle pool track (55,56,57,59,60,61) in custom mode: start ext battle track, call the
  game's bgm_play with r2 = -1; bgm_play(65) while ext battle active: r2 = -1 + paired victory; any other bgm_play on
  the same slot or restore 0x25f7c8: fade ext out. Pairing: file "<id>_<series>_<title>.adx", victory = name contains
  "Victory"; series exact match, alias P4 -> Persona 4, else one series a prefix of the other or >= 9 equal chars
  (Persona 2 InnocentSin -> Persona 2 EternalPunishment), else random victory. "356_Persona_Name Entry" would land in
  the battle pool. Setting random_battle_bgm: Off / Game / Custom / Mixed; bgm_dir (user: C:\Reloaded\Mods\
  persona5royalreimagined\FEmulator\AWB\BGM_42.AWB = loose ADX files, 200 tracks, 1.6 GB), custom volume.
- PC page plan: drop the A override in camp_settings_input (game opens its dialog); during the dialog restore only the
  row VALUES (keep our texts), back in state 2 on the same screen -> re-enter the PC page. Fill PC 2 rows 10/11
  (custom music volume; upscaler if FSR 1 is built) instead of empty rows.
- FSR / DLSS: Windows SDK dxc.exe has no SPIR-V codegen (tested), so FSR 1 EASU = hand-written Spv.Generator shader
  like Sharpen.cs (~1 session). DLSS SR / FSR 2+ need per-pixel motion vectors, depth and sub-pixel jitter; injectors
  (OptiScaler, DLSS Enabler, Streamline) only reuse inputs a game already produces. Here: camera-only motion vectors
  from depth + the game's view/projection matrices + a jitter hook in the projection setup (characters would ghost
  without object vectors) + NVIDIA DLSS SDK download (ask; licence vs GPL to check). Multi-session. USER DECISION.
- Camp menu blur, face shadow: not started (camp background probably a fixed-size render target not scaled by
  NX_RES, check with `rt`/drawlog in camp; face: compare NX_RES=720p vs 4k shots of the same frame first).

## Milestone 5, session 35 user report (2026-10-30 ~18:00, user played the s33 build to the end of the prologue)
User rule repeated: pause near the 5-hour limit (99%) and write everything down; remember everything done, miss nothing.
Items (all to be done or answered; status in "session 35" below):
1. PC page 2: Depth of field and Bloom are min/max sliders; should be On/Off buttons.
2. Vignette is also a min/max slider; toggling it on the native PC page triggers an Itsuki voice line (bug).
3. NEW: battle speed toggle 1x / 2x / 3x in battle (manual, like the game's auto-battle speed-up, but not tied to auto).
4. Chapter title card ("Chapter 1 A Star is Born", load save 20) runs too fast: not 60 fps paced.
5. Stutter grows as the story goes on ("stutterfest"). Analyse + prevent. Shader compiling?
6. User disagrees with "4K = 160+ fps": big areas 90-100 fps. Optimisation still needed; DLSS/FSR optional.
7. Continue DLSS/FSR. 8. Continue external random battle music (P5R ADX). 9. Tsubasa/Itsuki dark face shadow: visible
   in battle, NOT in cutscenes (cutscenes look right). 10. Attack Session. 11. Optimise more, also with UHD textures.
12. Launcher: first-time help - how to add game files, how to apply the uncensored patch, how to add the UHD pack.
13. Question: why do SavageWind (BotW recomp, C:\Users\user\Desktop\SavageWind-0.3.1-alpha.3-windows,
    github.com/Revivedx/SavageWindRecomp) and totk-pc-recomp (github.com/valentderah/totk-pc-recomp) not ship Ryujinx
    files? How do they differ from ours?
14. Subtitle: Itsuki "Roar" seems wrong (user hears "todoroke").
15. Some subtitles do not show (e.g. a boss fight).
16. Quick Session banner in battle ("Quick Session (Y) OFF") still shows the Switch Y, not the PS icon.
17. Question: Linux support / playable? 18. Question: needs runtimes / VC++ redistributable?
19. Question: odds of running well on many AMD/NVIDIA cards with no stutter / no crash.
20. NEW: option to hide field enemies (no field encounters, free exploration).

## Milestone 5, session 35 (2026-10-30 ~18:00-, with user; commit c443585; PAUSED: 5-hour 69% + weekly 88% in ~1 h)
Weekly usage went 79% -> 88% in one hour of work: next sessions must be short and targeted.

### Done (built, agent-checked as stated, NOT user-tested)
- Item 5 stutter, ROOT CAUSE (user run logs/nx_20261030_181056.log, 52 min): 73 of 81 hitches = pipeline creation
  (11 s in all); cache/pipelines.bin grew 17.4 -> 27.7 MB and shaders.bin 23 -> 32 MB = new areas compile new
  pipelines on first sight (classic shader stutter; not translation: 2 hitches, 0.7 s). Fix (vk_replay.cpp PipeJob,
  pipe_worker, pipe_wait): async pipeline compiles on 2-6 worker threads (half the cores); the draw waits at most 6 ms
  per 16 ms window, else it is skipped until its pipeline is ready (pop-in for a few frames instead of a freeze).
  Driver cache hits finish inside the wait, so known places look as before. NX_ASYNC_PIPELINES=0 = old sync path.
  Verified: 4K replay, "6 pipeline compile threads", no crash, 3 hitches, caches not shrunk. NOT verified: a new area.
  Still open for stutter: shader TRANSLATION is still sync (sidecar NxShader.dll); other users start with empty caches
  -> later: record pipeline keys + precompile at start (SavageWind/TotK precompile all shaders at setup).
- Item 3 battle speed (hle_sys.cpp battle_dt/apply_game_dt, ui.cpp, overlay, PC page 2 row 1): setting battle_speed
  1-3; in battle (btl_ui_update seen in the last 250 ms) the game step = frame time x k (cap 1/30 s: 3x needs 90+ fps,
  at 60 fps 3x acts as 2x; not at fps 30). UI 60 Hz ticks use the unscaled step (acc60 += g_base_dt). anim_update now
  scales by dt*60 at fixed 60 too (k in fast battles). F3 or DualSense TOUCHPAD cycles 1x/2x/3x with a 1.5 s note in
  the subtitle spot (subs_notice). The game's own "high speed mode" (battle +0x5c0, btlGetHighSpeedMode Lua -> 0x3ae2cc,
  read in 0x289854) only skips animation frames in auto battle: NOT used. Verified: base60 replay at 2x ran, no crash
  (replay desyncs after the battle as expected); fast battle look/sound NOT checked by eye.
- Item 20 hide field enemies (hle_sys.cpp hook field_enemy_spawn 0x4a7088: every symbol spawn - area load 0x4a6c74,
  respawn timer 0x4a5618, 0x4a7564 - returns -1). Setting hide_field_enemies (F1 + PC page 2), from the next area.
  NOT verified: base60's battle is scripted; no spawn call happened in the 150 s test. Risk: if a story symbol is
  spawned through it, that fight is skipped (user to watch).
- Items 1/2 PC pages (camp_settings.cpp): the game draws rows 0-2 as sliders always (draw 0x33cb14 `row < 3`, no
  option text) -> only stepped items there. Page 1: Frame rate, Resolution, Sharpening | Button icons, UHD, FXAA,
  Bloom, Glow, Depth of field, Vignette, Fog. Page 2: Walk speed, Battle speed, (row 2 empty: planned custom music
  volume) | Battle voice subtitles, Random battle music, Hide field enemies, Guard regen, First strike, Autosave,
  Detailed skill help, Outline. Display only in F1 now. Itsuki voice = the Settings screen's voice preview: update
  0x33c0a0 plays sound_play_cue 0x25fed4(0, cue) when ROW 2 (voice volume) changes; hooked: skipped on our pages.
  NOT verified in game (page layout, no voice).
- Item 16 Quick Session icon (pad_icons.cpp k_battle4096_cells): pills "Quick Session (Y) OFF/ON" are in the 4096
  battle atlas battle_02/battle_003.gtx hash 37357058a189ec59 (English mod's copy), white discs at (462,580) and
  (462,672) 32x32, look 1. Self-test verified (PS square / Xbox X drawn). The game's own half-size atlas (no mod):
  hash not found yet (ATLAS_HALF entry needed).

### Findings, not done
- Item 4 chapter card ("Chapter 1 A Star is Born", 1280x720 VP9 movie? not proven): movie input pts are ALWAYS 0
  (logged), so timestamp pacing cannot work (tried + reverted). The game's player thread 0x6df4e8 queues frames
  (+0x38c ring, 50); the consumer that shows them decides the speed - find it (or prove the card is a layout anim):
  repro = load slot 20 at 240 fps; use NX_COVER with a probe range or a probe on movie::Decoder vtable calls per frame.
- Item 14 "Roar": Itsuki's line is probably "Todoroke!" (轟け = "Roar / Thunder!", imperative of todoroku, to roar
  / resound). Check data/subtitles_en.tsv entry text before changing (not checked).
- Item 15 missing boss subtitles: subtitles_en.tsv only has the clips whisper transcribed; boss voice files not in
  the table are silent. Next: list BTL_*.adx played (game log ExPlayer_SetFile) without a table entry.
- Item 9 face shadow: battle only (cutscenes fine) -> battle lighting/shadow-map path, not the material itself.
  Compare battle vs cutscene drawlog of Tsubasa's face draw (shadow sampler/cbuf). Not started.
- Items 6/7/11 optimisation + FSR/DLSS: plan unchanged from s34 (FSR 1 = hand Spv.Generator shader ~1 session; DLSS
  needs motion vectors). Big-area 90-100 fps at 4K: profile with NX_PROFILE in such an area (user save needed).
- Item 8 P5R music: plan in s34 notes (ext_bgm.cpp), not started. Item 10 attack Session: not started.
- Item 12 launcher first-time help (game files, uncensored patch folder, UHD pack folder): not started (text page).

### Answers given to the user (items 13, 17, 18, 19)
- SavageWind (BotW) and totk-pc-recomp ship NO Ryujinx files because they wrote their own Maxwell shader translator
  (SavageWind: own translator to GLSL, then Google's libshaderc_shared.dll to SPIR-V; Ryujinx only as reference for
  instruction fields). They also recompile the game code ON THE USER'S PC at setup (bundled zig/clang + swgen), so
  the download holds no translated game code, and precompile all ~14,000 shaders at setup (no first-visit stutter).
  FFmpeg for video. Ours: Ryujinx (MIT) translator as a .NET sidecar (needs the .NET runtime) + prebuilt tms.exe.
- Linux: not supported now (Win32 window/overlay/launcher, Direct2D/DirectWrite, Windows file APIs); the core
  (SDL3 + Vulkan) is portable; a port is possible later (several sessions).
- Runtimes: tms.exe is built with clang against the MSVC runtime -> VC++ 2015-2022 redistributable needed unless
  linked statically (check CMake /MT before release); the shader sidecar needs .NET (version per shaderc build).
- GPU odds: Vulkan 1.3 everywhere; tested only on the user's NVIDIA. AMD/Intel risk: driver differences (SavageWind
  had a black window on AMD/Intel in 0.3.0). "No stutter at all" on first play is not possible without shader
  precompilation; async compile turns stalls into brief pop-in.

### Test hygiene
save_bak_s35 (saves md5 OK after tests, settings.ini same), cache/pipelines.bin 27723096, shaders.bin 32062692 unchanged.

## Milestone 5, session 36 (2026-10-30 ~20:30-, with user)
User: ignore the weekly limit, pause only at 5-hour 99%. Asked: make first play stutter-free like SavageWind (shaders ready
before they are needed); question only (no work yet): can we do what SavageWind/TotK do (own translator, build on the
user's PC, translate all shaders at setup)?

### Done (agent-verified as stated, NOT user-tested)
- Pipeline recipes + prewarm (vk_replay.cpp recipe_record / pipeline_prewarm; vk_shader.cpp make_module, module_hash,
  translation_by_hash, make_layout): every new pipeline appends a recipe to <data>/cache/pipelines.recipes ("TPR1",
  records [u32 len][RecipeFixed + RecipeStage[] + vertex attribs + bindings]; shaders named by an FNV hash of their
  SPIR-V, looked up in shaders.bin). At start (first pipeline job) a thread rebuilds every recipe as a warm PipeJob
  (pipeline destroyed at once, only fills the VkPipelineCache); game jobs go to the FRONT of the queue. NX_PREWARM=0 off.
  Recipes only exist from this build on (pipelines.bin is opaque): they grow as the user plays.
- Seed folder <exe dir>/cache_seed/{shaders.bin,pipelines.recipes}: read-only, loaded before the data cache (shaders.bin
  needs the same NxShader.dll stamp: package copies keep it). package.ps1 -Seed copies private/tms/cache files there.
- Measured (base60 replay 4K, 202 recipes, __GL_SHADER_DISK_CACHE=0 had NO visible effect: NVIDIA's own driver cache
  still hits, so true cold compiles were not measured): empty pipelines.bin without prewarm = 208 ms in-game pipeline
  creation + 1 skipped draw; with prewarm = 36 ms, 0 skipped; prewarm 202 pipelines 0.3 s. Simulated new user (empty
  data cache + cache_seed) = 0 sidecar translations, 202 prewarmed. Saves md5 OK; caches restored from cache_bak_s36.

### For a stutter-free release (open)
1. The seed must cover the whole game: the user plays through once with this build (recipes record automatically), then
   package.ps1 -Seed. The current recipes only cover base60 (202). shaders.bin already has 899 translations from play.
2. With a full seed, .NET + shaderc are only a fallback (a shader missing from the seed) -> could become optional.
3. Shader translation of a shader NOT in the cache is still synchronous (100+ ms): async translation = next step if
   needed.

### Answer given (SavageWind-style, question only)
- Own Maxwell->SPIR-V translator: possible (only the instructions TMS uses, ~900 shaders), several sessions; removes
  .NET + Ryujinx files. Cheaper path now: full cache_seed makes the translator a fallback only.
- Build game code on the user's PC at setup: possible (ship tools/recomp + a compact compiler such as zig/clang,
  lift the user's own main NSO); download then holds no translated game code. Cost: big setup step + compiler download.
- Translate ALL shaders at setup from game files: needs the location of the shader binaries in the romfs (not researched).
- Item 14 DONE: BTL_ACT_0013_pc1001 whisper had 驚け; user hears 轟け (todoroke, thunder rumbles) -> "Roar, thunder!"
  (tools/subs/en/BTL_ACT.txt + data/subtitles_en.tsv, copied to build; commit 1a06225). Not checked in game.
- Item 15 analysed (user run logs/nx_20261030_181056.log): 63 played clips have no subtitle. Most are grunts (OK).
  Real gaps: (a) boss em2301 BTL_OPEN_0002, BTL_ACT_0031/0032, BTL_REACT_0014/0015/0017/0033/0037 and em2001/em2049
  lines: whisper gave empty text or hallucinations ("ご視聴ありがとうございました", "BAKER", "キューブワールド");
  (b) BTL_TURN_01/02/03_* (turn voice lines): never transcribed (not in transcripts_jp.json at all); (c) no transcript:
  BTL_ACT_0014_pc1002/pc1003, BTL_ACT_0054_pc1002, BTL_OPEN_0007_pc1003; garbled BTL_SESSION_0022_pc1001.
  Next: re-run tools/subs/transcribe.py on those files (language ja, no condition on previous text, VAD off for short
  clips), add BTL_TURN group, hand-translate, build.py. List command: grep -o "BTL_[A-Z]*_[0-9]*_[a-z]*[0-9]*" <log>
  | sort -u, comm -23 against cut -f1 data/subtitles_en.tsv.
- Item 15 follow-up: re-ran whisper (3 settings, scratch retrans.py) on the 24 non-grunt battle clips without English.
  Boss em2301 / em2001 / em2021 / em2049 / np1101 clips are roars, laughs and monster noises (whisper: empty, "ご視聴
  ありがとうございました" hallucination, long "うおおお"): nothing to subtitle, so "missing boss subtitles" is expected.
  EVT_* clips (event voices) have the game's own text boxes. Added 6 spoken lines: BTL_CALL_0008_pc1001 "This might be
  tough.", BTL_OTHER_0002d_mr1051 "Don't let this chance slip!", BTL_OTHER_0003_mr1053 "A weak point!",
  BTL_OTHER_TALK_1014_pc1001_mix "Itsuki, can you stand? // Not yet!", BTL_SESSION_0022_pc1001 "Don't mess this up!"
  (whisper "のじるなよ", read as しくじるなよ: UNSURE), BTL_REACT_0007_em2049 "Adieu!". Table 2107 lines.
- Item 12 DONE (agent-verified by window capture, NOT user-tested): launcher page 7 "Setup help" (game files: nstool +
  prod.keys -> exefs/romfs, link.py -> link\image.bin, Browse; English patch: mods\<name>\romfs + tools\vcdiff.py;
  UHD: extract ZIP -> textures\pack, toggle). Opens on start when no valid data folder (unless --page). GAP for a real
  release: the program ZIP has no link.py/vcdiff.py/Python -> setup must be done from the source repo today; a release
  needs tms.exe (or the launcher) to link exefs itself or ship the tools.

## Milestone 5, session 37 (2026-10-30 night, with user, short: 5-hour budget 13% at start)

User: do PLAN_SETUP_PRECOMPILE.md (legal-risk-free release, precompile all shaders, no full playthrough); do NOT write
our own shader translator. Phase 1 started.

- **Where the shaders are (measured).** BNSH blobs in every pack, not only pack_030_etc Shaders/: effects
  (pack_020_effect, inside .ptcl) hold most of them. A BNSH stage record = control offset u64, code offset u64, then two
  u32 sizes (offsets from the BNSH start). The game reads control +0x6fc/+0x700/+0x748 past the stated control size,
  so the scan slices control and code to the BNSH end (as they lie in guest memory). Mods do not touch shaders (no mod
  replaces pack_030/020; the uncensor mod only has map/message/sound/movie/interface/lua).
- **New tool `tools/shaderscan/shaderscan.py <data>`**: finds every BNSH stage, keys it exactly like vk_shader.cpp
  translate() (prefix fnv of inputs + 256 code bytes, full hash over the translator's code_size + constants), runs the
  same sidecar (dotnet NxShader.dll, same protocol), appends to <data>/cache/shaders.bin. Only appends; refuses a cache
  of another translator build; skips entries already there. `--check` = no translation, only counts cache hits.
  Vertex shaders: float inputs only (integer-attribute variants still translate at run time; seen in the user cache).
  Pipelines still need the s36 recipes + prewarm (they are only known at run time).
- **Key check (measured, --check against the user's cache, 899 entries):** pack_030 alone reproduced only 86 of the
  899 (813 had no code in pack_030), so effect shaders matter. All packs: 21,413 BNSH stage blobs (many duplicates,
  e.g. one shader in many .ptcl), 8,043 of them already in the cache. Scan of all packs, no translation: 3 min 20 s.

- **Full run (measured, into a scratch cache, user cache untouched):** 6,737 unique translations, 0 failed, 3 min 45 s
  total, shaders.bin 290 MB. Covers 780 of the 849 distinct entries in the user's play cache; the other 69 are most
  likely vertex integer-attribute variants (run-time only, cheap). NOT yet tested in game: next = run shaderscan into a
  fresh <data>/cache, play a new area, hitch log should show ~0 translations.
- Next (needs user answers, plan "Open questions"): Phase 2 (lift + build on the user's PC from their own game files),
  toolchain bundled vs downloaded, NSP+keys vs extracted folder, UHD pack. shaderscan needs Python today; for release
  it must run from the launcher setup (port to C++ in tms.exe or ship with Phase 2 tooling).

## Milestone 5, session 38 (2026-10-31 ~00:30-02:30, with user; commits 138a17b, 730f2e3, 9e63a23)
User answered the plan questions (PLAN_SETUP_PRECOMPILE.md "User decisions"): bundle the toolchain, NSP + own prod.keys,
UHD pack stays a separate ZIP, Phase 1 done. Phase 2 built. Everything agent-verified as stated, NOT user-tested.

- **game.dll split.** tms.exe = runtime only (1.7 MB, was 41.9 MB), exports guest.h NX_API functions + g_cover (tms.lib).
  game.dll = lifted code + tables (game.def exports; dispatch.cpp game_load() binds them right after mem_init). Gen is
  compiled with clang only (guest.h NX_GAME_DLL: own stdint/math/setjmp declarations, -nostdinc), linked by lld-link
  /NODEFAULTLIB against tms.lib + import libs from our own tools/setup/nx_crt_math.def / nx_vcruntime.def (`_setjmp ==
  __intrinsic_setjmp`). Names start nx_: a "vcruntime.lib" in the build dir shadowed Microsoft's and broke the launcher.
  game.dll imports: 12 runtime symbols, ceil/floor/round/sqrt[f], __intrinsic_setjmp. .text within 0.1% of the old objects.
  Crash log names tms.exe+off / game.dll+off; NX_PROFILE knows both modules.
- **tools/setup/build_game.py**: the one build script (CMake calls it for dev, setup.py for players); incremental;
  `compile i/n` progress. Full compile 1 min on 16 threads.
- **tools/setup/setup.py**: NSP (largest NCA via nstool --fstree, -x /0 exefs, -x /1 romfs; temp NCA removed) or an
  extracted folder (becomes the data folder, nothing copied) -> SHA-256 check of exefs main/sdk (SUPPORTED) -> link ->
  lift -> build_game -> shaderscan --set-aside. Markers in <data>/setup/*.done make it resumable. NSP MODE UNTESTED (J:
  not mounted). nso.py: own LZ4 block decoder (byte-identical to the lz4 package on all 15 segments).
- **shaderscan now also scans link/image.bin** (169 BNSH in the executables: boot/movie/system). In-game proof (fresh
  data folder, base60 replay, 4K/60): scanned cache without image.bin = 28-47 translations in play (25 at boot, 393 ms);
  with it = 5 (4 integer-attribute vertex variants, 1 float vertex shader consts 6608+12, key d9732a36717afb21: open).
  tms.exe logs every miss ("vk: shader cache miss: ...").
- **package.ps1**: ships setup\ (python, llvm\clang.exe + lld-link.exe, nstool.exe, sdk\ guest.h + libs + game.def,
  tools\), refuses to package game code/data (name/extension list + tms.exe size check). -Seed removed. -StageOnly for
  tests. Staged size 188 MB uncompressed (without Python).
- **Launcher "Setup" page** (page 6, was Setup help): game NSP/folder, prod.keys, target, shader toggle, progress bar,
  Cancel (job object), errors, saves data= when done. PLAY + first start need game.dll. `--setup <folder>` starts at once.
- Measured: setup from the staged package, folder mode: 5 min 24 s (lift + compile ~1.5 min, shaders ~3.5 min);
  gen/ and image.bin byte-identical to the dev tree; base60 replay on split builds = same end state, 0 crashes.
  Caches only grew (backup private/tms/cache_bak_s38), saves md5 unchanged.
- Test leftovers: private/tms/setup_test (romfs = junction to private/tms/romfs, shaderc junction), install_test,
  build_dll (old split test dir). Safe to delete; romfs junction: remove the junction only, never its contents.

### Open (release)
1. Downloads needed (ask user): Python 3.12 embeddable ZIP + capstone wheel -> private/third_party/python-embed;
   LLVM LICENSE.TXT -> private/third_party/llvm-LICENSE.TXT; nstool LICENSE -> private/third_party/nstool/LICENSE.
   Then package.ps1 (no -StageOnly) and a test on a clean Windows account/VM.
2. NSP mode test with the user's NSP (J:).
3. Updater: a new runtime changes tms.lib/guest.h -> game.dll must be rebuilt (launcher should run setup after an update).
4. Remaining shader misses: integer-attribute vertex variants (need attr types: could be recorded as recipes).

## Milestone 5, session 39 (2026-10-31 ~02:30-03:00, with user; commit bb34ebb)
User: J: mounted, downloads approved. Downloaded (private/third_party/dl_s39): python-3.12.8-embed-amd64.zip (python.org),
capstone-5.0.9 win_amd64 wheel (PyPI), LLVM llvmorg-23.1.4 llvm/LICENSE.TXT, nstool v1.9.2 LICENSE (GitHub raw).
private/third_party/python-embed = embed ZIP + wheel in Lib/site-packages, python312._pth adds Lib\site-packages.

- NSP mode bug: nstool `-x /<name>.nca <file> <nsp>` fails on Windows paths (path not found / access denied). Fix:
  `-x / <data>/setup/nca.part <nsp>`, renamed to nca when complete; program NCA = biggest; temp folder removed after.
- Release ZIP Desktop/TMSRecomp-20261031.zip: 84.9 MB, 260 entries, no game code/data (checked by package.ps1 and by
  listing). Extracted with Windows tar into private/tms/release_test, launcher `--setup <nsp> <keys> <target>`:
  Done in ~8 min (02:36:56 -> 02:44:52), bundled Python only. gen/ + image.bin identical to the dev tree. tms.exe from
  the release folder: base60 replay 0 crashes, same end state, 6886 precompiled shaders, same 5 misses as s38.
- Launcher path boxes show long paths as "…" + the last 63 characters.
- Test folders (delete when done): private/tms/nsp_test (13 GB, a real data folder), release_test, setup_test (romfs is a
  JUNCTION to private/tms/romfs: remove the junction only), install_test, build_dll.
- Open: user play test of the release flow (fresh extract of the ZIP); updater must re-run setup after a runtime update;
  clean-account/VM test (no VS/LLVM/Python installed); the 5 remaining shader misses.
- Later s39 (commit 3db2126): updater -> rebuild. setup\built.txt = signature of build inputs (tms.exe, setup\sdk|
  tools|llvm, shaderc\NxShader.dll; path|size|time). Launcher start: signature differs -> setup re-runs on the data
  folder (incremental), PLAY blocked meanwhile. Verified: plain restart no rebuild; touched tms.exe -> re-run ~1 s, Done.
  Older installs without built.txt get one quick rebuild. Test folders all deleted (junctions removed first).
  Release ZIP rebuilt (Desktop, 84.9 MB).

### OPEN LIST (2026-10-31, everything not finished since s32; s = session it came from)
Release / setup: (a) user test of the fresh ZIP flow; (b) clean Windows account/VM test (no VS/LLVM/Python);
(c) 5 shader misses in play (4 integer-attribute vertex variants, 1 float vertex key d9732a36717afb21).
Game bugs: (1) enemy skill-name banner missing, e.g. Blob attack (s34: real panel 0x2f1cac, early return when same unit +
skill; probes + fps 30 vs 240 replay); (2) chapter title card too fast at high fps (s35 item 4: movie pts always 0, find
the consumer of player ring +0x38c); (3) Tsubasa/Itsuki dark face shadow in battle only (s35 item 9); (4) camp menu
background blurry at 4K (s34 item 2: fixed-size render target?); (5) O on PC settings page should open the game's
"Apply these settings?" dialog (s34 item 8, plan in s34 notes); (6) Quick Session icon for the game's own half-size
atlas (no English mod: hash not found).
Features: (7) Attack Session gate (s25, not found); (8) external P5R ADX battle music + matched victory theme (plan s34,
ext_bgm.cpp); (9) FSR 1 (hand Spv.Generator shader, ~1 session) / DLSS + FSR 2 (motion vectors: USER DECISION);
(10) optimisation of big areas at 4K (90-100 fps; needs a user save there + NX_PROFILE).
Unverified by the user (s35): battle speed 1x/2x/3x by eye, hide field enemies, PC page layout/no voice preview.

## Milestone 5, session 40 (2026-10-31 ~03:10-03:50, with user; commit a3e7603) - open list item 1 (enemy banner)
- ROOT CAUSE (measured): skill-name panel = open 0x2f1cac (panel, &skill, unit, ?, flag), show 0x2f2118 (returns if
  +0x18 visible != 0; sets +0x18 = 1, +4 = 1), update 0x2f13b8 (state +4: 1 open, 2 closing: +0x1c counts down, at 0 resets
  +0x28 = -1, +0x20 = -1, +0x18 = 0, 0x2f9980 on +0x34/+0x50/+0x6c/+0x88, +4 = 0). Enemy path 0x29049c (once per action,
  +0xa8) = open + show. An open while CLOSING sets the text, show is ignored, the close then hides it -> no banner.
  base60 battle: 60 fps 0 of 12 enemy opens in the closing window, 240 fps 2 of 12.
- Fix (hle_sys.cpp PROBE_FN btl_skill_panel_open): closing panel + a new open -> run the update's reset first, then the
  open/show proceed. Every open logged: "battle: skill panel open unit .. skill .. from ..: panel state .. timer ..
  visible ..[ -> close finished first | -> SKIPPED (same unit + skill)]". The player's second open per action
  (btl_enemy_action_banner+0xb8 for player units too) is SKIPPED by design (menu path already showed it).
- Verified: 240 fps battle, fix path taken (enemy unit 8 skill 197 and player units), 0 crashes in 3 battle runs. NOT seen
  by eye (screenshot runs desynced: base60 sometimes never reaches the battle after the replay; agent_scripts/
  banner_shots.sh <tag> <fps|-> presses A to drive it, still flaky). User playtest: missing banner -> send log time.
- names.txt: btl_skill_panel_open/update/show, btl_enemy_action_banner (re-lift done, 20595 hooks).
- New scripts: agent_scripts/banner_shots.sh, wincap.ps1 (window capture), thumb.ps1 (downscaled PNG).
- Release ZIP rebuilt (Desktop/TMSRecomp-20261031.zip). Usage 03:50: 5-hour 33%, weekly 96%.

## Milestone 5, session 41 (2026-10-31 ~03:55-04:20, with user; NO code change kept) - open list item 4 (camp blur)
- Repro: agent_scripts/to_field.sh <tag> NX_WALK_SPEED=2 NX_RES=4k, then control `x` opens the camp menu (worked in
  run s41, NOT in s41b: timing), `shot` / `rt` / `drawlog`.
- Measured (s41, 4K, camp open): `rt` dumps only 3840x2160 targets (bc502910 d28, bc502b10 d2): the grass + characters
  are drawn LIVE at 4K, not a captured 720p picture. All texture copies of the run are 4K -> 4K (no capture copy).
  The camp passes also sample two linear pool textures, flags 0x14: bcfdcc90 1280x720 nvn fmt 0x1 and bcfdd010 640x360
  fmt 0xd (stage 5, into bc502910). Likely blur/mask inputs; who writes them is NOT found (not a COPY_TEX_TEX).
- Tried + REVERTED: render-scaling full-frame copy targets (never triggered). User settings have fx_dof = 0, so DOF
  is probably not it either (unless camp ignores fx_dof). Next: find the writer of bcfdcc90 (drawlog of the frame the
  camp opens; NX_LOG_IMAGES=1), compare a 720p vs 4K camp crop of the same spot (agent_scripts/crop.ps1 bmp png x y w h).
- Seen in passing (4K field, tex_pack = 1): fern plant leaves in the d002_01 hall drawn BLACK around the leaves (crop of
  shots, near the red chair). Probably the UHD pack alpha problem (s21: realesrgan blackens RGB under low alpha) on
  that texture: check with tex_pack = 0. NEW open item.
- Usage 04:20: 5-hour 39%, weekly 97%. Stopped here (weekly).


## Milestone 5, session 42 (2026-10-31 ~11:45-12:10, with user; weekly 97-98%: short)

### User report 2026-10-31 (play test of the s41 build)
Bugs: 1. Hide field enemies does NOT work: an enemy still spawns while exploring. 2. After a battle, Itsuki/Tsubasa's
victory animation before the level-up screen: transition a bit too fast (analyse). 3. Boss-area cutscene: Tsubasa's
hair + clothes glitch a little (user will send a picture).
New features: 4. Level-up refills HP + EP to full. 5. Mod support: make it easy for people to mod the game.

### Done
- Item 1 (FIX built, NOT user-tested): s35's hook field_enemy_spawn 0x4a7088 is NEVER called in d002_01 (NX_PROBE
  field_enemy_spawn: 0 calls in d00201_60.rec and base60.rec runs; field_spawn_timer runs). Symbols come from the enemy
  server, driven by EnemyServerParam (map: ghidra/parammap.py after Decomp 0x42edc0): AddSymbol_* = wild symbols that
  pop near the player, FixSymbol_* = placed ones that appear inside FixSymbol_AppearDistance. New enemy_hide_apply
  (hle_sys.cpp, before enemy_param_store): with NX_HIDE_FIELD_ENEMIES on, table +0x10c..0x118 (AddSymbol_NormalPercentA-D)
  = 0, +0x140 FixSymbol_AppearDistance = 0, +0x130/+0x13c karma thresholds = 0x7fffffff; off restores loaded values.
  Called from enemy_param_store (map load; the game keeps the table pointer: only 1 enemy_param_get call in 76 s) and
  enemy_param_get. Log "field: hide field enemies on" seen at 16.8 s. NOT seen by eye that symbols are gone (the replay
  end position shows none either way). s35 hook kept. Risk: a story symbol placed by layout may not appear -> story
  fight skipped; Lua appearEnemyImmediate / mapCreateEnemy probably bypass the distance (unverified).
- Leads seen: Lua setEnemyEncount -> 0x3e47ec writes server +0x7c (only used for push-out radius in 0x3e723c, not
  spawning); 0x3e9ae0 = scripted appear list (messages 0x3e315c type 4).

### Not started (weekly limit)
- Item 2 victory pose speed: s27 gated RESULTS/level-up tasks; the pose before RESULTS is probably battle sequence/
  camera time. Repro: base60.rec at 60 then `fps 240`, shot timings of the victory pose vs 60.
- Item 4 level-up refill: needs the persistent party HP/EP (battle unit data +0xc/+0x10/+0x14/+0x18 is the battle copy;
  write-back order after RESULTS unknown, see FFR lesson: setter can hit a stale battle copy). Hook point candidate:
  levelup_update 0x31b7dc first call. Needs a user save right before a battle that levels up.
- Item 5 mod support: user chose "loose files + textures" (not Lua/DLL plugins). DONE (see below).
- Item 3: waits for the user's picture.
- Build: private/tms/build has this session's tms.exe. Saves intact (md5), cache/pipelines.bin 27834776 unchanged.

### Item 5 mod support (later in s42)
- Loose files already worked (hle_fs.cpp rom_roots: <data>/mods/<name>/romfs, first name wins, NX_MODS_DISABLED).
- New: texture mods <data>/mods/<name>/textures/**/*_<hash>.dds (vk_texture.cpp pack_index): scanned after the UHD
  pack, so a mod wins over the pack; between mods the first name wins (same as romfs); NX_MODS_DISABLED skips them;
  log "textures: mod <name>: N textures (M new)". They follow the tex_pack switch (ponytail: separate switch later).
  Verified: temp mod with 1 copied pack file -> "textures: mod _textest: 1 textures (0 new)" (removed after).
- Launcher Mods page now lists texture-only mods too (romfs or textures folder). Not checked by window capture.
- "Making mods" guide in README.md and tools/package/README.txt (release ZIP): paths, tex_dump to find hashes, DDS
  formats + mips (texconv -m 0), order, mods_disabled, log lines in <data>/nx.log.


## Milestone 5, session 43 (2026-11-01 ~05:00-, SCHEDULED RUN, user asleep: backlog run, no user input)

### User playtest log 2026-10-31 21:39-21:41 (private/tms/nx.log + issues.log, s42 build, 240 fps, 4K, DualSense)
- Run: title -> d002_02 -> d002_01 (prologue). User turned hide_field_enemies on (line 2853), played event EVM_0009
  (flags 0009_04 gimmick, 0009_04, 0009_02), one battle, results (FLG_SYS_RESULT_TTL_CHROM_TALK, _FIRST_01 = the
  first results tutorial), back in d002_01, event 0009_03, camp item Performa unlocked. Window closed normally, NO crash.
- Hide field enemies: "field: hide field enemies on" logged; the s35 spawn hook 0x4a7088 IS called here (5x "enemy
  spawn skipped", 4 at once during event 0009_02 at 0:59). The battle after it ("opening chance 56, contact flags
  0000" = no symbol contact) is the scripted first battle of the prologue (first results tutorial) -> correct to keep.
  Risk seen: the 4 skipped spawns came from a story event; the story still went on (battle + next event happened).
  Not proven that no wild symbol showed (user did not report).
- Battle speed: user switched 2x, 3x, back to 1x in the battle (settings lines 11634/11667/14036): feature used, no
  crash, no complaint in the log.
- Enemy banner (s40 fix): enemy unit 0x42 skill 8 opens shown twice from state 0 and once "close finished first"
  (frame 12240) = fix path taken in the user's play. Player second opens SKIPPED by design.
- Perf: 3 hitches only (705 ms + 74 ms at boot/loading = game code, 57 ms first battle: pipelines 11 + uploads 13);
  0 shaders translated, all from cache; 125-236 fps.

### Item 4: A / O on the PC pages opens the game's "Apply these settings?" dialog (built, compile-checked only)
- Game update 0x33c0a0 states (decomp ghidra/set1.c): 2 browsing; A -> 4 (+0x134 = 1), 5 = dialog up: Yes -> apply
  0x33c7e8 -> 6 -> 3 (screen closes); No / B -> 7 -> 2. Y -> 4 with +0x134 = 0 (defaults dialog). B -> 3.
- camp_settings.cpp: the camp_settings_input hook (A = next choice) is REMOVED, so the game opens its dialog. When the
  state goes to 4 with +0x134 = 1 from a PC page: only row values/arrows/min/max go back to the game's (labels stay),
  g_pending = page. When the dialog is gone: state 2/7 (No/B) -> enter_pc(page) again; else (Yes, closing) the help
  texts are restored. Y / B from a PC page: full leave_pc as before. Our settings are still applied live on change.
- NOT tested in game (needs camp > System > Settings navigation). User check: PC page, O -> dialog; No -> PC page
  back with its values; Yes -> screen closes, settings kept.

### Item 10: FSR 1 upscaler (built; run-checked at 720p -> 4K, NOT user-tested)
- DECISION (made for the user, scheduled run): FSR 1 only. DLSS / FSR 2+ need per-pixel motion vectors + jitter the
  game does not produce (s34 analysis); not built.
- tools/spvgen/Upscale.cs -> runtime/src/upscale_spv.h (`dotnet run --project tools/spvgen -- upscale
  runtime/src/upscale_spv.h`): our own SPIR-V of the EASU idea (AMD FidelityFX FSR 1, MIT, credited): 12 taps,
  luma gradient + edge strength mixed bilinearly at the 4 inner pixels, Lanczos-like kernel rotated along the edge
  and stretched by strength, clamped to the 4 nearest pixels. RCAS half = our existing Sharpen pass, run after the
  upscale at screen size when sharpen > 0.
- vk.cpp: image_pass()/run_image_pass() shared by sharpen + upscale; present_async: setting upscaler = fsr1, RGBA8
  frame smaller than the swapchain -> staging image at swapchain size, upscale (+ sharpen) into it, present blit 1:1.
  Otherwise unchanged (bilinear blit). Staging storage images now also SAMPLED (upscale -> sharpen).
- Setting `upscaler = bilinear | fsr1` (NX_UPSCALER), F1 menu "Upscaler", PC page 2 row 10 (replaces "Outline",
  which stays in the F1 menu: DECISION, page 2 was full), launcher Graphics page.
- Verified: replay d00201_60.rec at NX_RES=720p borderless 4K: "vk: upscaling pass ready (FSR 1 style)", no
  crash/VK error; window captures FSR vs bilinear (scratch crops): FSR edges visibly sharper, no artifacts.

### Item 9: custom battle music from the user's P5R ADX files (built; decoder verified offline, NOT in game)
- runtime/src/ext_bgm.cpp (own code): file scan of custom_bgm_dir (default <data>\music; the user's settings.ini now
  has custom_bgm_dir = C:\Reloaded\Mods\persona5royalreimagined\FEmulator\AWB\BGM_42.AWB), victory pairing by series
  (exact, P4 alias, longest common start if prefix or >= 9 chars, else random), own ADX v4 type-9 decoder (P5R key),
  loop points, linear resample 44.1 -> 48 kHz (most files are 44100), mixed into a copy of each game audio buffer in
  the hle_audio feeder, gain custom_bgm_volume/10 (default 7), 1 s fade out.
- random_battle_bgm: 0 off, 1 game tracks (old "on"), 2 custom, 3 mixed (coin per battle). bgm_play hook: pool battle
  track with custom -> game call with index -1 (stop with the push bookkeeping), remember slot; bgm 65 victory while
  custom active -> paired victory theme, game stops its jingle; any other track on that slot or new hook bgm_restore
  0x25f7c8 (names.txt; re-lift done, 20596 hooks) -> fade out. bgm log lines now show the slot.
- Verified: tools/tests/adx_check.cpp (includes ext_bgm.cpp) = byte-identical output to an independent Python
  decoder on 300_P5R_Victory.adx (3000 frames), loop wrap continues exactly at the loop start, all 200 user files
  parse (header, loop). NOT verified: in a real symbol battle (replays only have the tutorial battle, which starts no
  battle track). Risks: the game's 1157 env_battle ambience on the same slot would stop the custom music (assumed a
  different slot); bgm_restore args assumed (slot not used).
- UI: F1 menu "Random battle music" Off/Game/Custom/Mixed + "Custom music volume" 0-10; PC page 2 row 2 = Custom
  music volume (slider), row 4 = Random battle music (4 choices); launcher Game page AUDIO row; settings.h comments.

### Item 12: PC page 2 empty row filled (row 2 = Custom music volume, row 10 = Upscaler). Built, not seen in game.

### Item 1: chapter title card too fast at high fps (FIX built, NOT seen in game)
- Cause (static RE): CRI Mana 2.18's timer object (ctor 0x6c72a0, vtable 0x9ee570; strings CriManaSystemTimer /
  CriManaTimer found by a PIC-reference scan, scratch picrefs.py). GetTime 0x6c74e4: manual mode (+0x10 == 1) time =
  count (+0x48 u64) x unit (+0x38 / +0x40); count++ in 0x6c7634 (vtable slot 8) = once per game frame. Movies on the
  manual timer (no audio clock: the chapter cards) therefore run fps/30 times too fast; the opening movie (audio
  clock) was fine.
- Fix: names.txt 0x6c7634 mana_timer_advance (re-lift, 20597 hooks); hle_sys.cpp hook: above fps 30 the count
  follows real time (x control speed), whole units, remainder carried, max 8 units per call, a gap > 0.5 s = new
  movie (one step). fps 30: the game's own code. Log "movie: manual timer .., unit .. s, paced by real time" once per
  timer object. Not verified: needs the chapter card (user's save 20 era); user check = card at 240 fps plays as at 30.

### Item 5: Quick Session PS / Xbox icon without the English patch (built, self-test verified)
- texextract over pack_080_interface with NX_MODS_DISABLED=uncensored: the game's own _US battle_02/battle_003.gtx =
  9a884b596879859b, 2048 x 2048 (half of the mod's 4096 atlas 37357058a189ec59). pad_icons.cpp ATLAS_HALF entry
  with k_battle4096_cells. NX_PAD_ICONS_TEST on the dump: PS square / Xbox X drawn exactly on both Y discs (OFF/ON).
  _JP battle_003 (765f4692cfd8004a) not added (other layout, not checked).

### Level-up refill (user request s42 item 4; built)
- Persistent party records in the game data (**0x9ef37c + 0x10, = save file layout): record k at +0x350ac + k x
  0x360: +0 id/slot, +4 level, +8 HP, +0xc max HP, +0x10 EP, +0x14 max EP (u32). Found in save_20.bin by the user's
  HUD values (Itsuki 60/178 77/83 at 0x350b8, Tsubasa 67/162 119/119 at 0x35418). The battle unit data (unit +0x818)
  is a copy written back after the results.
- hle_sys.cpp: levels_snapshot() at btl_open_chance; levelup_refill() at the first field step >= 3 s after the
  battle (autosave_try, before the autosave writes): level went up -> HP = max, EP = max; log "level-up refill: party
  record k level a -> b: HP .. -> .., EP .. -> ..". Setting levelup_refill (default 1), F1 menu item.

### Item 6: black fern leaves with the UHD pack (cause found; tool fixed; 76 pack textures redone)
- Cause: BC1 cut-out textures decode their transparent texels as black (and many BC3 ones have black under alpha 0);
  uhd_pack.py upscales RGB as an opaque picture, so the black ran into the leaf edges, then the separately upscaled
  alpha shows it. Scan of 4089 decoded map textures: 76 pack textures with alpha-0 texels whose RGB is dark (< 40)
  next to bright edges (> +40).
- tools/uhd_pack.py: new bleed() (pull-push fill of RGB under alpha < 16, alpha untouched, numpy) before the RGB
  upscale. Verified on 256x256_46_169b5d6bceb5987b (cut-out windows: black -> window colour).
- Pack repair: the 76 old files moved to private/tms/textures/pack_pre_bleed (backup), redone with
  `python tools/uhd_pack.py private/tms --dump <scratch>/redo_dump --sources private/tms/textures/sources.txt`.
  The fern itself was not identified (route to the Fortuna Office not in a replay); user check: Fortuna Office fern.
  The separate UHD ZIP must be rebuilt (package.ps1 -Uhd) for other users: NOT done (user decides, large).
- Level-up refill test: base60 replay via to_field.sh desynced this run (no battle reached: no "opening chance",
  no bgm 1157) -> refill NOT verified. Next: rerun to_field.sh lvl (it reached the battle in s41) and walk; look for
  "level-up refill" in the log.
- Pack redo of the 76 textures: DONE (76/76, pack back to 9540 files). Release ZIP rebuilt:
  Desktop\TMSRecomp-20261101.zip (84.9 MB).

### Session 43 end state (PAUSED at the 5-hour limit; continues by scheduled task tms-recomp-backlog-run-2)
Backlog status (2026-11-01 list; NOTES wins):
- DONE this session (built, NOT user-tested): 1 chapter card pacing (manual Mana timer), 4 PC page A -> Apply dialog,
  5 Quick Session icon (game's own atlas), 6 fern black edges (uhd_pack bleed + 76 pack textures redone), 9 custom
  P5R ADX battle music + matched victory, 10 FSR 1 upscaler (DECISION: FSR 1 only, no DLSS/FSR2), 12 PC page 2 rows
  (Custom music volume, Upscaler; Outline only in F1 now), level-up refill.
- OPEN, next session in this order: (a) victory pose before level-up too fast at high fps (s42 item 2: replay
  base60 at 60 vs `fps 240`, shot timings); (b) 2 face shadow Tsubasa/Itsuki battle only (drawlog of the tutorial
  battle vs a cutscene, compare the face draw's shadow-map sampler/cbuf); (c) 3 camp blur at 4K (writer of the
  1280x720 / 640x360 pool textures bcfdcc90 / bcfdd010); (d) 8 Attack Session gate; (e) 7 shader misses (DECISION
  proposal: leave 4 integer-attribute variants + 1 unexplained, ~ms each, async pipelines hide most; record attr types
  in recipes only if cheap); (f) 11 big-area speed at 4K (no save in a big area: profile statically / NX_PROFILE on a
  replay area); (g) Tsubasa hair/clothes glitch in the boss cutscene (waits for the user's picture).
- Release: 13 user ZIP-flow test and 14 clean VM test are for the user (no VM here). 15 GitHub: NOT touched (user rule).
- UHD ZIP not rebuilt (pack changed: 76 files). Build it with package.ps1 -Uhd only if the user asks.
- Continuation task could NOT be scheduled (create_scheduled_task needs a person's approval in a scheduled run). User: start the next run by hand (same prompt as tms-recomp-backlog-run, open list above).

## Milestone 5, session 44 (2026-11-01 ~18:00-, user asked to continue the s43 backlog)

### Level-up refill: FIXED + verified in a run
- s43 code read the party record 4 bytes too low (+4 "level" = 0x10001 = id word). Layout from save_2/save_20 and
  the live record: +4 id (u16) | ? (u16), +8 level (2 for both after the prologue battles; 0 for Touma, not joined),
  +0xc HP, +0x10 max HP, +0x14 EP, +0x18 max EP. Fixed in hle_sys.cpp (commit 26b26a8).
- New log lines: "level-up refill: battle start / first field step, record 0 level .. HP ../.. EP ../..".
  Test switch NX_LEVELUP_TEST=n lowers the battle-start level snapshot by n (pretends a level-up).
- Verified (base60 via to_field.sh, NX_LEVELUP_TEST=1, NX_AUTOSAVE=0): battle start HP 60/178; first field step HP
  110/178 (the game had already written the battle copy back) -> "party record 0 level 1 -> 2: HP 110 -> 178" and
  record 1 110 -> 162; next battle start shows 178/178 (kept, not overwritten by a stale battle copy).
  Real level-ups not seen (no battle in the replays levels up), the write-back order is now proved.
- New log: "post-battle: <task> first update (frame N)" for each gated post-battle task (result_flow/levelup/
  skill_learn/result_bg/result_update): markers for the victory timing.
- Replay note: base60 via to_field.sh now often ends at (160.7, 50, -795.4) without a battle; ~1 in 3 runs reach one.
- Incident: killing the stale s43 `to_field.sh fern0` loop let its parent script run its own taskkill tms.exe and it
  killed a test run at 68 s. Before starting runs: check `ps -ef | grep to_field` for old loops and kill the parents too.

### Victory pose before level-up (s42 item 2): measured, NOT fixed (no difference found yet)
- New rig private/tms/agent_scripts/victory.sh <tag> <fps> (SHOTS=1: 20 shots every 0.4 s after each enemy death ->
  shots/<tag>_v + times.txt): base60 replay, then `fps N`, `setpos -494 -240 -760` (the desynced end 160.7 50 -795.4
  has no symbols near), walk back and forth + A until a battle, no input for 8 s after each kill, prints the timeline.
  Battles still not certain (one run got stuck mid-battle after a B press on the skill list).
- Timeline (game time, "post-battle: .. first update" + cues):
  - 240 fps, no input after the kill: enemy dead (cue bpro_dead_enemy) -> victory bgm 65 1.38 s -> result_flow_update
    (RESULTS/level-up tasks) 2.58 s later.
  - 60 fps (A presses continued, may skip): dead -> bgm 65 1.38 s (2 runs), bgm 65 -> result_flow 1.28 s / 1.60 s.
  -> the waits are NOT shorter at 240. result_bg_parts_update 0x47fc5c only calls the sub-object's draw (vt+0x10);
  its update (vt+0xc) runs in result_bg_update (gated, 60 Hz) -> not the cause.
- Still open: a clean 60 fps run without input (rig ready), then compare the shot series (pose animation / camera
  speed) at equal times; ask the user which part looks fast (pose, camera, the wipe into RESULTS) and at which fps.
- Harness lesson: background `for` loops of run scripts kept relaunching tms.exe after TaskStop/kill (two instances
  at once). Run victory.sh in the foreground, one at a time.

### Session 44 end state (paused at 5-hour 77%+ for notes/ZIP)
- Done: level-up refill fixed + verified (above). Open list from s43 otherwise unchanged: (a) victory pose (above),
  (b) face shadow, (c) camp blur, (d) Attack Session, (e) shader misses, (f) big-area perf, (g) Tsubasa glitch.
- User's build/settings.ini now has fps = 120, random_battle_bgm = 0 (user changed them; left as is).

### User answer 2026-11-01 (after s44): the fast part is THE WIPE INTO RESULTS (not the pose, not the camera)
- Next session, item (a) first. Leads: the wipe starts near cue `sm_info` (~0.02 s before bgm 65) and ends at
  result_flow_update (2.58 s at 240). Candidates: (1) a battle-side wipe/fade object driven per frame, not one of the
  GATED_TASK hooks (s30 found the camp wipe task 0x318e40 counting frames; look for a sibling used by the battle end:
  find who plays cue sm_info / bgm 65 -> log symbol_at(lr) in the bgm_play hook, hle_sys.cpp:402); (2) result_bg's
  sub-object (result_bg_update 0x47f964 case 4 vt+0xc, objects built in case 3: kind 2 = 0x18c bytes, 10 parts with
  ids 0x13ab66dd.., kind 1 = 0x74 bytes) - its draw vt+0x10 runs every frame from result_bg_parts_update 0x47fc5c:
  check the draw for its own counter (decompile the vtables at DAT_0047fc54+0x47fae0 / DAT_0047fc50+0x47fbac).
- Check: victory.sh v60 60 / v240 240 with SHOTS=1, compare shots/<tag>_v at equal times after bgm 65.

## Milestone 5, session 45 (2026-11-01 ~22:50-, with user)

### User report 2026-11-01 (playtest of the s44 build, run 19:52, 240 fps, random_battle_bgm 3)
1. "Level up does not increase HP MP at all."
2. Custom battle music (incl. victory) TOO LOUD: match the original volume.
3. Answer to s44: the fast part is the wipe into RESULTS.

### 1. Level-up refill: the data was refilled, but late -> now refilled the frame the level rises
- User log: record 0 level 2 -> 3 refilled 73 -> 184 at the first field step, next battle start 184/184. So the data
  path worked; what the user saw was most likely the camp menu / HUD before the first walk step (the refill waited for
  the first step >= 3 s after the battle).
- Battle main 0x2c6ca8 (state before victory bgm 65, call 0x2c9614) writes the battle copies' HP/EP back to the party
  records (0x352f2c(id) -> +8 HP, +0x10 EP); the level-up itself lands in the records later, in the result screens.
- Fix (hle_sys.cpp): levelup_poll() from rt::frame_begin (every frame) while armed (battle start -> first field step):
  any record whose level is above its battle-start level and HP/EP below max is refilled at once. The first-field-step
  pass stays (log line + disarm). Verified (w240c, NX_LEVELUP_TEST=1): refill at battle start (test), then the
  write-back at the battle end (HP 36) refilled in the same frame, before bgm 65 (230.630 s).
- Real level-up not seen in an agent run (no replay battle levels up); user check: level up, open camp at once.

### 3. RESULTS wipe: 2x the Switch speed (60 Hz UI pace) -> 30 Hz
- The wipe is result_bg kind 1 (set by 0x47fdbc(rbg, 1) from 0x318a30 = result flow start, called by battle main
  state 0xd); object vtable 0x7e671c: update 0x47dfc8 (8 + 10 + 10 eased steps, +1 per call), draw 0x47e290 (pure).
  result_flow case 3 waits for it (0x47fd88). s44's guess (wipe before result_flow) was wrong: the wipe IS the time
  from result_flow first update to result_update first update.
- Measured: 0.535 s at 60 fps (lvl/fld/rmsC logs), 0.52 s at 240 (w240c): our 60 Hz gate was right, but 60 Hz is twice
  the Switch's 30 fps (~1.07 s). Fix: result_bg_update in state 4 steps on 30 Hz ticks (tick_due, game time) instead of
  the 60 Hz UI gate (GATED_TASK_SKIP + result_bg_skip). DECISION (agent): only this animation; menus stay 60 Hz (s28).
  Kind 2 (0x18c object, other screens) also uses state 4 -> same 30 Hz.

### 2. Custom music loudness: per-track normalisation to the game's level
- Audio log now prints RMS of the game's buffer and of the custom music per 10 s ("rms game N custom M").
- Measured: field music output RMS ~750; game battle (music + SFX) 1700-2200; the game's BGM files (Common.awb, 518
  plain ADX, 101 longer than 60 s) raw RMS quartiles 3384 / 4286 / 6384 -> the game plays them at ~0.175; P5R files
  4800-12300 raw, played at 0.7 = 3400-8600: 10-18 dB too loud.
- Fix (ext_bgm.cpp): RMS of each track's first 60 s at load (on a copy of the decoder), gain = min(1, 1100 / rms) x
  custom_bgm_volume / 7 (default 7 = game level, 10 = +3 dB). Log line shows "rms .., gain ..".

### Incident: test replays rewrote the user's settings.ini
- Desynced base60 replays wander into the F1 menu and toggled settings (levelup_refill = 0, battle_speed 3,
  custom_bgm_volume 8 appended). Restored by hand (battle_speed = 1, the two lines removed). Fix: save_setting()
  (overlay.cpp) never writes settings.ini while NX_REPLAY is set (setting applies to that run only).
- victory.sh needs timeout >= 590 s (the replay alone runs ~190-320 s).
- Root cause of most "desync" chaos this session: SDL gives the real gamepad to background windows; the user's
  DualSense reached the minimized test instances (touchpad = battle speed toggles, L3+R3 = F1 menu, A = "Exit" -> a run
  quit at 198 s). Fix (ui.cpp): with NX_REPLAY set the real pad is never opened. Keyboard only reaches a focused window.

### Verification (w240g, 240 fps, after the pad fix; cache/pipelines.bin 27901427 B unchanged, saves md5 unchanged, ini intact)
- Custom battle: game buffer (SFX + voices, music stopped) RMS 1391-1687; custom music 940-1129 ("830_P5R_Shido Phase 1",
  raw rms 5188 -> gain 0.212; victory "300_P5R_Victory" rms 7399 -> gain 0.149). Game-music battles (rmsC, w240c) total
  1682-2232 -> the game's music alone ~sqrt(1900^2 - 1550^2) = ~1100 = BGM_RMS. Matched by log, not by ear.
- RESULTS wipe at 240: result_flow -> result_update 0.904 s (was 0.52 s; 60 fps was 0.535 s; Switch ~1 s).
- User checks: (1) level up, open the camp menu right after the battle: HP/EP full; (2) custom music volume like the
  game's; (3) wipe into RESULTS speed.

### Session 45 end state
- Open list unchanged otherwise: face shadow, camp blur, Attack Session, shader misses, big-area perf, Tsubasa glitch.

## Milestone 5, session 46 (2026-11-02 ~00:10-00:45, with user)

### User notes 2026-11-02
- "Weapon LEVELUP is different from character level up": the refill is for Itsuki / Tsubasa character level-ups.
  Weapon (Carnage) Mastery = the "Skill Inheritance" screen, a different thing.
- "Load SAVE 2 to try battles, not save 20."

### Replays were loading save 20 (root cause of most replay desyncs since s27)
- save/system.bin byte 5 = last used slot: 2 in save_bak_1023b (when the .rec files were recorded), 20 now (autosave).
  The title Load cursor starts on it, so base60 replays loaded slot 20 (HUD showed Lv 3 HP 111 EP 74 = save_20).
- Fix: NX_SAVE_DIR (hle_fs.cpp mount + autosave write in hle_sys.cpp). agent_scripts/run.ps1 sets it to
  private/tms/testsave/<tag>, a fresh copy of save_bak_1023b (slots 1, 2, system.bin). The user's save/ is never
  touched by test runs now. First run with it reached the base60 battle at once (was ~1 in 3).

### Level-up refill: verified with a REAL character level-up from save 2 (screenshot)
- Record +8 = character level (stats +0x28..+0x30 rise with it); +0x64 = EXP (20 in save 2 at Lv 2, 66 in save_20 at Lv 3,
  same for both members). Weapon mastery data is elsewhere (+0x190 / +0x1a4 change too).
- New test switch NX_LEVELUP_EXP=n: at battle contact sets the joined members' EXP to n; the game's own results then
  level them up. NX_LEVELUP_EXP=60 from save 2: "party record 0 level 2 -> 3: HP 67 -> 184, EP 77 -> 89", record 1
  "HP 38 -> 174". Field HUD after the Skill Inheritance screen: Itsuki Lv 3 HP 184 EP 89, Tsubasa Lv 3 HP 174 EP 125
  (full; battle start was 110/178, 110/162). Saves md5, settings.ini, cache/pipelines.bin unchanged.
- Commit 9fd1212.

### Session 46 end state (paused at 5-hour 88%)
- Open list unchanged: face shadow, camp blur, Attack Session, shader misses, big-area perf, Tsubasa glitch (picture).
- User checks still pending from s45: custom music volume, RESULTS wipe speed, level-up refill in own play.

## Milestone 5, session 47 (2026-11-02 ~01:30-, with user)

### User report 2026-11-02 (playtest of the s46 build)
1. Level-up HP/EP refill: CONFIRMED working.
2. Custom battle + victory music: CONFIRMED, volume good.
3. Wipe into RESULTS: still too early - it starts before the victory pose animation has finished.

### New requests (all in the F1 / L3+R3 overlay AND the native PC settings page)
1. EXP multiplier up to 5x (all battle EXP x N).
2. Money multiplier, same.
3. Resistance badges as icons like SMT V (toggle): Rs = half shield, Wk = red warning, Nu = purple, Dr (absorb) = green,
   Rp (repel) = blue. User gave P5R Reimagined sprites C:\Reloaded\Mods\persona5royalreimagined\FEmulator\SPD\INIT\
   P5CAMP_00SPD.SPD\spr_329..333.dds as the icon source.
4. Camp menu background still not upscaled (s41 open item).

### 1+2. EXP / money multipliers (built, verified by run + RESULTS screenshot)
- btl_add_reward 0x2cb2d4 (battle, enemy level, EXP, money): once per defeated enemy (and Lua btlSetExpMoney 0x429fa4);
  adds to battle +0x528 (EXP total), +0x568 (money x float +0xa0), +0x52c.. per-member EXP (level-gap rule). Hook
  (hle_sys.cpp) multiplies r2 / r3 by settings exp_rate / money_rate (1..5). Lua AddResultParamExp/Money (event rewards,
  globals 0x9f4f44 / 0x9f4f7c) are NOT scaled (quest/event rewards, not battle).
- Verified (v47, 240 fps, x5): log "battle: reward level 2 EXP 5 x5 money 100 x5" per enemy; RESULTS showed 50 EXP and
  1,000 Yen for 2 Blobs (game: 10 / 200); both members leveled 2 -> 3.
- Settings: F1 "EXP multiplier" / "Money multiplier" (1x..5x), PC page 3 rows 0-1 (sliders). camp_settings.cpp now has
  3 PC pages (PC 3/3: EXP, Money, empty slider row, Resistance icons, Level-up refills HP / EP).

### 3. Resistance icons (built; Stats screen verified, battle panel dim)
- Badges = white letter sprites over a separate grey disc sprite. Atlases (letters at the same cells): camp/status001
  (266e32dcca881b44 / own 6e6254f0ac17ee63), status_drc/status_drc001 = the Stats screen ((+) in battle; 16f810b5373bff80
  / own 57febd3b87911115; also a button-icon atlas: both repaints stack, resist first into level0), battle_02/battle_002
  (7ada3bc97c0dd991 / own f7914dfb3c6f343d; small badge set + larger Rp/Nu/Dr at y ~982). Own = no English mod, half size
  (texextract with NX_MODS_DISABLED=uncensored).
- pad_icons.cpp resist_icon_atlas: each letter cell (44 px square at 2048 scale, 60 for the big set) cleared and filled
  with <data>\resist_icons\{weak,resist,null,absorb,repel}.png (WIC, Fant scale) or a coloured disc if missing. Setting
  resist_icons (default 1), live toggle (Image::resist, check_pool_texture re-upload). F1 + PC page 3.
- The user's icons (P5R Reimagined spr_329 absorb, 330 repel, 331 null, 332 resist, 333 weak) copied as PNG into
  private/tms/resist_icons. NOT shipped (third-party art): the release shows coloured discs unless the folder exists.
- Verified: Stats screen (4K crop) red "!" for Wk, half shield for Rs, full colour, not clipped. Battle target panel
  (analysis row): icons drawn but DARK - the game tints the badge letter sprite dark grey there (multiply). Texture
  cannot undo it; needs the draw colour (layout data is not in the .gtx = plain BNTX; no rect table found in main.bin
  for the badge cells). Nu / Dr / Rp not seen yet (no such enemies in the test battle).

### 4. Camp menu background: it is a MOVIE, not a texture
- c47 runs: camp at 4K, crop soft like a 3x stretch. Replacing the camp scene texture (zz_campTop d3a9f9f4d8c4058e) with
  a 4x ESRGAN version changed nothing (restored the 2x pack file after). Log: "movie: VP9 1280x720" when the camp opens.
  Background = Movie/camp/camp_00..10(g).usm (pack_049_movie_camp, 20 files, ~12 MB each), 1280x720 VP9. s41's
  R8 1280x720 + 640x360 linear IMAGE textures = its NV12 planes.
- Options (NOT started, user decision): (a) offline: decode each camp movie, Real-ESRGAN every frame, encode VP9 at
  2560x1440 or 4K, our movie HLE plays the replacement stream and the NV12 planes become larger Vulkan images (UV
  sampling, like the UHD pack) - hours of GPU time, needs an encoder (ffmpeg/libvpx vpxenc download); (b) runtime:
  sharper upscale filter (FSR1 EASU-style) of the planes at upload - cheap, sharper edges, no new detail.

### Victory wipe (user: wipe still starts before the pose ends): FIXED by timing, user check pending
- Battle main 0x2c6ca8 (names.txt btl_main) state 0xb sets state 0xc with timer +0x18 = 30; 0xc counts it down per
  call, then waits for button 0x20 (0x25c970) or the victory sequence done (**0x9ef790 vt+0xc), then 0xd = result
  flow start. Counted per frame: 0.125 s at 240 fps instead of the Switch's 1 s; the "done" check passes ~0.7 s after
  the victory music, so the wipe came ~0.3 s early. Hook: on frames without a 30 Hz tick the timer is put back.
- Measured 240 fps: bgm 65 -> result_flow 0.73 s (v47) -> 0.92 s (v47c, log "battle: victory wait over (timer 0)").

### Session 47 end state
- Commits 90d30a4, b377275. Saves md5, settings.ini, cache/pipelines.bin (27901427) unchanged by test runs.
- User checks: EXP / Money multiplier, resistance icons (Stats + battle), victory wipe at your fps.
- Open: battle badge tint (icons dark in the target panel), camp movie upscale (decision a/b), plus s46 list (face
  shadow, Attack Session, shader misses, big-area perf, Tsubasa glitch).
- Harness: in this shell `cmd /c build.cmd` fails (current dir not searched): use the full path
  C:\Users\user\Projects\TMSRecomp\build.cmd.

## Milestone 5, session 48 (2026-11-02 ~05:25-05:40, with user; PAUSED at 5-hour 97%)
User answers to s47: camp background = **AI re-encode offline**; resistance icons are the USER'S OWN art -> ship them.
- Resist icons: data/resist_icons/*.png in repo; CMake copies to build/resist_icons; package.ps1 copies to the ZIP;
  pad_icons.cpp load_icon: <data>\resist_icons first, else <exe>\resist_icons. Built, not run-checked, ZIP NOT rebuilt.
- Camp movies: USM video chunks already hold an IVF stream (tools/camphd/usm2ivf.py just concatenates). 20 movies x 500
  frames, 30 fps. tools/camphd/camphd.py <data> <esrgan dir>: ffmpeg frames -> realesr-animevideov3 x3 (3840x2160;
  0.33 s/frame, x4plus was 1.8 s and no better) -> libvpx-vp9 crf 24 -> <data>/movie_hd/camp/<name>_<hash>.ivf
  (~20 MB each; hash = FNV-1a 64 of frame 0's first 4096 bytes). Resumable (skips done files). ffmpeg was already
  installed (C:\Program Files\FFmpeg), no download. RUNNING in background at pause (camp_00 done 05:37, ~4 min/movie);
  log private/tms/camp_hd/run.log. If it died: rerun `cd private/tms; python -u ../../tools/camphd/camphd.py . ../tools/esrgan`.
- Runtime (built, NOT run yet): hle_movie.cpp hd_index/hd_open/hd_next: first packet hash -> HD stream decoded in step
  (one HD frame per visible low-res frame), planes registered by rt::movie_fp; vk_texture.cpp movie_replace swaps a
  4K image into linear 1280x720 / 640x360 textures whose bytes match. NX_MOVIE_HD=0 off.
- NEXT: (1) run to camp (agent_scripts/to_field.sh + control `x`), log must show "movie: 4K stream camp_.. playing"
  and "textures: movie plane ... -> 4K"; if no "playing", log the game's first packet hash (assumption: packet = IVF
  frame payload) and compare; 4K crop vs s47 crop. (2) commit, rebuild ZIP (package.ps1), HD movies are derived game
  data -> NOT in program ZIP (like UHD pack; ask user: separate ZIP or setup step). (3) update memory.
- UPDATE 11-02: upscale batch FINISHED, all 20 movies in private/tms/movie_hd/camp (631 MB). Runtime swap still untested.

## Milestone 5, session 49 (2026-11-02 ~08:15-, user asleep: "keep going, pause at 5-hour 99%, new session after reset")

### User report 2026-11-02 (s48 build)
1. Resistance icons work, BUT in the battle target panel they are too DARK and do not fill the circle.
2. New: Weapon EXP (Carnage Mastery) multiplier, in L3+R3 / F1 and the native PC settings page.
3. Camp HD batch finished: finish the runtime swap. Then the rest of the backlog.

### 1. Resistance icons (FIXED, verified by 4K screenshots: shots/s49_resist_battle.png, s49_resist_skill_inherit.png)
- Target panel drawlog (agent_scripts/target.sh: base60 to the battle, then `a` = Attack -> target panel): each badge
  is its own 4-vertex sprite, shader vs 009e4000, stride 36 = pos 3 + colour 4 + uv 2 floats (attribs [3]=05c00640,
  [8]=02c00e40), tinted 0.263 grey (white letters on the white disc), quad 24 px at 720p = 48 atlas texels.
- Fix: vk_replay.cpp draw(): when the draw samples a resist atlas drawn with icons (Image::resist_hash, set in
  bind_resources) and the quad's uv centre is in an icon cell (rt::resist_icon_cell) and the tint is grey, the guest
  vertex colours become 1.0 (alpha kept; the game rewrites them every frame).
- Fit: the user's PNGs are 192 px canvases with the art top-left (~135-155 px): load_icon crops to a square around
  the alpha bounds (WIC clipper) before scaling; cells are now 48 (= the whole sprite) in both cell tables.
- Skill Inheritance screen showed letters: its atlas = result/result_001 (3c5e643864ee95df, own 7fd8beb4e7f14b1a);
  fusion/fusion001 (688fc06ddecf3eb3, own 133f164b20932f02) has the same cells (pixel-matched to status001 with numpy
  over dump_all). Added to k_res_atlases. Own hashes from texextract --packs pack_080_interface with NX_MODS_DISABLED.
- Commits acc6f82, dbae2e5.

### 2. Mastery multiplier (built, verified by run)
- Battle Mastery = u16 battle +0x548 + 2 * member (7), added per action in the damage routine 0x2b8bc8 (several
  sites) and by Lua btlSetForceMastery (binding 0x429870 -> 0x2c3c1c); btl_main 0x2c6ca8 clamps them to 50000 each
  call; the results then add them to the weapon entries in the game data (e.g. Itsuki's Falchion gd+0x368a0:
  70 -> 305). Found with the new debug NX_GD_DIFF=1 (logs every game-data word changed from battle opening to the
  first field step) and the Lua binding table (name/function pairs at 0x7e3bxx: AddResultParamExp 0x4404f4,
  AddResultParamMastery 0x44064c = event rewards).
- Hook: hle_sys.cpp mastery_scale() in btl_main: the rise since the last call x mastery_rate (1..5, NX_MASTERY_RATE),
  capped 50000; shadow copy per battle object. Settings: F1 "Mastery multiplier", PC page 3 row 2 (was empty).
- Verified (x5): log "battle: mastery member 0 +900 x5 -> 4500" per action; Itsuki's Skill Inheritance after the
  first battle lists Cleave + Lance-Slash + Rakukaja (x1: Cleave only), shots/s49_mastery_x5.png.
- NOT checked: the PC page 3 row by eye.

### 3. Camp 4K movies (runtime swap VERIFIED)
- New fast rig agent_scripts/to_camp.sh <tag> [env]: no replay, title -> Load slot 2 -> field -> Y = camp in ~21 s.
- Log: "movie: 4K stream camp_01_fc9f455be46abee8.ivf playing", "textures: movie plane 1280x720 -> 4K 3840x2160";
  4K crop is sharp line art (shots/s49_camp4k.bmp). Pacing: 601 presents / 10 s, gaps 16.1-17.1 ms over a full loop
  (NX_PROFILE run). One earlier long replay session showed ~505 / 10 s in camp: not reproduced in a fresh start.
- Distribution: movies are derived game data -> NOT in the program ZIP; built as a separate ZIP like the UHD pack
  (see end state). User decides how other players get them.

### 4. Face shadow in battle (looked at, NOT fixed)
- Battle shadow maps: depth fmt 0x35, 1024x2048 + 1024x1024 (two cascades, 2 textures each), sampler 261 = compare
  LESS, linear (PCF), clamp to border 1.0. Command-wheel frames (battle start + 1.5-4 s, agent_scripts/target.sh,
  RES=720p env for 720p) at 4K and 720p: Itsuki's face has the hair shadow under the fringe in both; the replay picks a
  different character / camera each run, so no identical-frame comparison yet (shots/s49_face4k*.bmp, s49_face720.bmp).
- Next: an identical frame needs NX_REPLAY to the same turn (fps 60, same opening chance) or a live `res` switch;
  then compare the face draw's shadow-map sampling at 1x vs 3x (theory: shader PCF / bias constants in shadow-map
  texels while the maps are scaled with the render scale, like the FXAA case).

### Release
- Desktop\TMSRecomp-20261102.zip (85 MB, program + resist_icons, rebuilt after all code commits) and
  Desktop\TMSRecomp-CampHD-20261102.zip (661 MB, movie_hd/camp/*.ivf, extract into the data folder). README: 4K camp
  section. The user's own data folder (private/tms) already has movie_hd.

### Session 49 end state
- Commits acc6f82, dbae2e5, 529b0ec, README commit. Saves (user save/), settings.ini, cache/pipelines.bin untouched by
  tests (testsave copies; NX_EXP_RATE=1 env in rigs because build/settings.ini has exp_rate = 5).
- Scheduled one-time task tms-recomp-s50-resume (2026-11-02 07:12 UTC). NOTE: cfb-recomp-resume-s8 also fires 07:16 UTC
  (both share the 5-hour budget).
- User checks: battle target panel icons (bright, fill the disc), Skill Inheritance icons, Mastery multiplier (F1 +
  PC page 3), camp menu background at 4K (needs movie_hd in the data folder), victory wipe timing (s47).
- OPEN (order): face shadow (above), Attack Session gate, 5 shader misses (proposal: leave), big-area perf (needs a
  user save), Tsubasa boss-cutscene glitch (needs the user's picture).

## Milestone 5, session 50 (2026-11-02 ~07:15-09:10 UTC, SCHEDULED run, user asleep; commits 3df2e30, 83e6890)

Worked the s49 open list in order: face shadow, then Attack Session. Neither is fixed; both narrowed down.
5-hour usage at the end ~65%; stopped to leave room for notes + ZIP (no continuation scheduled: limit not hit).

### 1. Face shadow in battle: shadow-map scale is NOT the cause (verified by run)
- Shadow maps (battle depth 0x35, 1024x2048 + 1024x1024, power-of-two) were created at res_scale() x like every
  compressible target. New debug switch NX_SHADOW_NATIVE=1 (vk.cpp image_of) keeps power-of-two depth targets at the
  game's size (log "vk: shadow map 1024x2048 kept at game size").
- Compared at 4K, 30 consecutive frames each (agent_scripts/face2.sh, NX_SHADOW_NATIVE=1 vs 0), best-matched frame pair
  (shots/s50_face_matched.png, left native / right scaled): native maps show fine diagonal acne stripes on Itsuki's
  cheek, scaled ones are clean; no dark band on Itsuki in either. Default stays scaled (switch off by default).
- Still open: the user's case is Tsubasa (and Itsuki) "dark band on cheek / neck when she turns", battle only. Not
  reproduced in the tutorial battle frames. Needs the user's screenshot or a battle where Tsubasa faces the camera
  (save_20 battles now work, see 2). Next idea: drawlog the face draw in battle vs a cutscene (shader constants,
  which shadow cascade it samples, light direction).

### 2. Attack Session gate: mechanics found, gate NOT found
- Test setup that works (no user save touched): testsave/s20 = copy of the user's save/save_20.bin as slot 2 (Lv 4
  Itsuki + Tsubasa, Daitama, Sessions unlocked; Tsubasa knows Elec-Lunge). Rigs (agent_scripts):
  tobattle.sh <tag> [env] (title -> slot 2 -> walk loop at 980 50 -760 until a symbol battle, ~200 s),
  weak.sh <tag> <element> [value] (finds Caspar's affinity bytes in the heap dump and pokes them: 0 = sword weak),
  v.sh <tag> (screenshot -> shots/s50_v.png 1280x720), field.sh. Enemies there: Dark Mage, Caspar (Elec weak), Blob
  (Sword/Fire/Elec weak).
- The save's party records: skill list at record +0x18c (u16 per slot; Tsubasa save_20: 107 Dia @0x18c, 324
  Elec-Lunge @0x1a4). Slots from +0x18e..0x1a2 are NOT used by the battle (Lunges written there in s50 tests were
  inert: no Lineup) -> write test skills right after the last real one (testsave/s20M: 318 Sword-Lunge @0x1a6).
- StSkillTable record +0x44 (u32) = Session TRIGGER element mask of a follow-up skill: bit (1 << element of the
  previous hit). Sword-Lunge 1, Lance-Lunge 2, Axe 4, Bow 8, Fire 16, Ice 32, Elec-Lunge 64, Wind 128.
  Verified: NX_SKILL_POKE=144:44:41 (Elec-Lunge mask 64 -> 65) and Cleave on sword-weak Caspar shows the Lineup
  "Cleave -> Elec-Lunge" (shots/s50_cleave_lineup_mask.png).
- Lineup preview: built by 0x2acc4c (partner skill scan: unit +0x60 slots, skill +2 == 1 = Session-capable, copies
  +0x12 element and +0x44 mask) called from the action/damage evaluator 0x2ad86c at 0x2afd20 when its 7th argument
  (callee sp+0x364) is non-zero. Both target-select call sites (0x2a6904, 0x2a885c) pass 1; 0x2a8444 passes 0.
  The executed Session = 0x2ab480 (reads the slot list), from the state machine 0x2a5c50 at 0x2a95f0.
- Ruled out with a VALID setup (testsave/s20 + NX_SKILL_POKE=144:44:41): Attack record +0x54 = 1 -> still no Lineup.
  The other Attack pokes (+0x12/+0x52 = 6, +0x56 = 2, +0x58 = 9, +0x5a = 1, +0x0a, +0x20 = 2, +0x5c, +0x60, +0x22)
  ran on testsave/s20L whose Lunges were inert (unused slots), so they prove NOTHING: retest them with s20 + the
  mask poke (cheap: one tobattle.sh run each, Lineup shows during target select). Note +0x12/+0x52 = 6 made Attack
  show the Elec icon but the hit stayed Sword (weak on sword-weak Caspar). The state-machine branch at 0x2a92b4 (skill_get +0x20 == 1 -> state 2 else 5/8) is
  NOT on the Attack path (a skill_get hook on return address 0x2a92c4 never fired; hook removed).
- Attack target-select DOES call skill_get from 0x2ad8c0 (= the evaluator) like Cleave, so the gate is inside
  0x2ad86c / 0x2acc4c before the Lineup is filled: next, watch (NX_CONTROL `watch addr 0x84 r`) Attack's record
  (table *0x9f3d7c + 0xc + 1*0x84) during Attack target-select vs Cleave's and diff the read offsets; or compare the
  unit/wheel state (command kind byte r8+0x9e3 / +0x9e0 skill id) between the two.
- Action record (btl_apply_action r1, now logged with NX_DEBUG_BATTLE): +0 = 1 for a Session follow-up (0 own
  action), +4 actor, +8 target, +0xc skill, +0x10 result (1 normal, 2 weak; 0x100 / 0x2xx seen), +0x18 damage.

### 2b. Attack Session: GATE FOUND = formula +0x20 == 1 (verified by run, not shipped)
- NX_SKILL_POKE=144:44:41,1:20:2,1:22:19,1:54:1,1:56:2,1:58:9,1:5a:1,1:a:1,1:60:2 (testsave/s20): Attack shows the
  Session Lineup ("Start Attack", shots/s50_attack_lineup.png); Attack on sword-weak Caspar -> WEAK -> Tsubasa's
  Elec-Lunge follows: "SESSION 01 COMBO GOOD", cue bt_session00_tsubasa (shots/s50_attack_session.png).
  The same pokes WITHOUT 1:20:2 / 1:22:19: no Lineup -> the gate is formula +0x20 == 1 (basic attack).
- But formula 2 = skill damage formula: the Attack did 6 HP (power 0x19) instead of ~16 -> not shippable as a poke.
- Readers of Attack's +0x20 during target select (watch on record + 0x20, chains):
  skill_is_basic 0x27f854 (= +0x20 == 1 || +0x24 == 1) from 0x2b5268 (in 0x2b5178, the command state before the
  evaluator) and 0x2ad924 (in the evaluator 0x2ad86c); 0x27f290 (lifted as F_022d4a38 +0x5bf / +0x5cb) from
  0x302024 (target cursor) and 0x2b8bc8 (damage routine); 0x2fab84 / 0x3014d8 (skill panel / hit reaction, UI).
- Tried: hook skill_is_basic returning 0 at return addresses 0x2b526c and 0x2ad928 (fired, logged) -> still NO
  Lineup. Reverted (not in the build). Next: also make 0x27f290's +0x20 read (from 0x302024, return 0x302028?) see
  a non-basic formula, e.g. hook 0x27f290 like skill_get with a record copy whose +0x20 = 2 only for the target-cursor
  caller, and keep the damage routine 0x2b8bc8 on the real record (damage stays basic). Disassemble 0x27f290 first
  (takes (table, ?, id); reads +0x20 twice). Then check the Session follow-up damage and that Attack without a
  weakness / without a partner Lunge behaves as before.

### Debug tools added (commit 83e6890)
- NX_SKILL_POKE=id:off:val,... (all HEX: 144 = skill 324) u16 writes into the loaded skill table once it is up
  (inside skill_help_update; skipped when NX_SKILL_DETAILS=0). Log "skills: poke record ...".
- NX_CONTROL `poke addr byte` (hex): one guest byte write, logged.
- NX_DEBUG_BATTLE also logs the raw action record ("battle: action record").
- NX_SHADOW_NATIVE=1 (commit 3df2e30).

### Session 50 end state
- Built and run-verified: the two debug commits only (no player-visible change this session).
- User save/ untouched (save_20 md5 cc11562e... unchanged; tests used testsave/s20, s20L, s20M copies), settings.ini
  untouched, cache/pipelines.bin only grew (28.1 MB).
- OPEN (order): Attack Session (gate found, see 2b: finish the 0x27f290 read), face shadow (needs a Tsubasa frame / user picture),
  5 shader misses (proposal: leave), big-area perf (needs a user save in a big area), Tsubasa boss-cutscene glitch
  (needs the user's picture). User checks from s49 still pending (target-panel icons, Skill Inheritance icons,
  Mastery multiplier, 4K camp, victory wipe).

## Milestone 5, session 51 (2026-11-02 ~19:00-, with user)

### User report 2026-11-02 (s49/s50 build)
CONFIRMED working: resistance icons (battle panel + Skill Inheritance), Mastery multiplier, camp 4K background.
New: (1) random battle music must not hit story bosses (e.g. Gojuin), as an option; (2) Itsuki / Tsubasa look bad in
the dungeon field (dark areas: Itsuki's trousers black with blue edges, glowing outlines) but fine in cutscenes;
(3) Tsubasa's ribbon "glitches uncontrollably" while she walks in a cutscene (user picture: both walking on dark tiles).

### 1. Bosses keep their music (built; normal battle verified by log)
- bgm_play (hle_sys.cpp): only track 55 BATTLE_NORMAL is replaced (random or custom); 56 BOSS / 57 GANEFU / 59 EVENT /
  60 EXTRA / 61 QUEST keep theirs unless setting random_bgm_bosses = 1 (F1 "Random music for bosses", PC page 3 row 5,
  settings.h comment). Log bg1.log: "bgm: 55 (played 59, slot 0)" with NX_RANDOM_BATTLE_BGM=1. Boss battle not run.

### 2. Field look: UHD PACK MIPS were the cause (FIXED, verified by 4K crops)
- Repro: agent_scripts/pants.sh <tag> [env] (testsave/s20 -> Daitama Lower Lv, 4K crop of Itsuki -> shots/s51_<tag>.png).
  Reference: Switch footage (YouTube 1080p frames): trousers smooth grey-green, no black patches.
- Ruled out: Maxwell FMUL/FFMA .FMZ (0 x inf = 0; Ryujinx decodes Fmz but never uses it). Implemented it in the
  translator: NO change -> reverted (translator dll + caches restored from cache_bak_s51 / shaderc_bak_s51, md5 + mtime
  checked). NX_TEX_PACK=0 -> clean => the pack.
- Bisect with new debug NX_PACK_SKIP=<hash,...> and NX_PACK_LOG=1 (logs every pack texture loaded): the culprit set is
  Character/player/pc000/skin/04 (Itsuki's current outfit), e.g. 1024x1024_48_e53aeac3e12c3a2f (BC3: RGB = shade colour
  everywhere, alpha = mask).
- Root cause: tools/uhd_pack.py ran texconv without -sepalpha: mip generation weighted RGB by alpha, so RGB under
  transparent texels went black in every mip but level 0. The shader reads that RGB with alpha as a mask; at field
  distance the trousers sample mip 2-3 -> black with blue fringes. (Level 0 compared fine: my first numpy check resized
  RGBA with PIL, which premultiplies - beware.)
- Fix: uhd_pack.py builds mips with -sepalpha; no bleed() for BC2/BC3/BC7 (only BC1 cut-outs store black under alpha);
  new `uhd_pack.py <data> --remip` rewrites the mips of existing pack textures with min alpha < 0.9, level 0 byte for
  byte, header/size checked, resumable (textures/remip_done.txt, log textures/remip.log). Verified: remipped e53aeac3 via
  a test mod -> clean trousers with the pack on (shots/s51_pG.png vs s51_pA.png). Full remip of the user's pack running
  (~3.5 h, ~15% of textures need it). Backup of the old pack: Desktop\TMSRecomp-UHD-20261030.zip.
- After it: rebuild the UHD ZIP (package.ps1 -Uhd); check Tsubasa (pink outline, user picture 4) with the pack.

### 3. Tsubasa ribbon: NOT reproduced (no save near a walking cutscene)
- Physics: model+0x81c = 0x20c-byte object (ctor 0x56a034, vtable 0x7e8940): +0x20 = phys_update 0x56bd00 (s0 dt,
  uses dt x timescale +0x120 = actSetPhysicsTimerParam / cutSetPhysicsTimerParam binding 0x3a61ec / 0x3aa984), +0x10
  solve iterations. Called from phys_step 0x21929c (s0 dt, node) <- character update 0x3cf374. Names added; NX_ANIM_PROBE
  logs their dt: field at 60 fps = 0.016667 (correct dt, not a fixed 1/30).
- Idle Tsubasa in the Observatory: 16 consecutive frames stable (shots/s51_ribbon_idle60.png).
- Theory (unverified): cut scripts run on 30 Hz ticks, so script-moved characters jump every other frame at 60 fps and
  the chain physics gets alternating impulses. Needs: user save before such a cutscene + whether 30 fps also glitches.
- Attempt to reach the prologue with newgame scripts landed on Load (title cursor) instead: scripts need "up" first.

### Session 51 end state
- Commit 2f8d8d9 (BGM option, uhd_pack fixes, NX_PACK_SKIP/LOG) + probes commit. Test runs used testsave/ copies.
- Full remip DONE: 9540 checked, 3585 rebuilt, 0 errors (textures/remip.log). In game with the whole pack:
  Itsuki's trousers clean in Daitama (shots/s51_pH.png); Tsubasa in the Observatory has no dark patches, a thin pink
  rim remains on her outline (shots/s51_after_remip.png) - probably the game's edge light, not compared to Switch yet.
- UHD ZIP rebuilt from the fixed pack: Desktop\TMSRecomp-UHD-20261102.zip (old 20261030 kept as backup).

## Milestone 5, session 52 (2026-11-02 ~21:55-23:00, with user; PAUSED at 5-hour 96%; commit d2cbb86)

### User report 2026-11-02 (s51 build)
1. Boss battle music works, not randomized (CONFIRMED).
2. Tsubasa / Itsuki in the dungeon field (walking) still look ugly (after the s51 UHD remip).
3. Tsubasa's ribbon still glitches in the cutscene. Save in slot 20: walk forward to the door -> boss scene.

### 3. Ribbon: ROOT CAUSE FOUND + FIXED (verified by numbers + frames, not by the user)
- Rig: agent_scripts/ribbon.sh <tag> <nshots> [env] (testsave/b20 = user save_20 as slots 2 + 20; title cursor is on 20
  via system.bin; stick up + A at the door, `shots N` from the door; HOLD=s keeps the game open). The walk-in shot is
  ~frames 240-290 of the capture (camera close on both walking towards it). Crops: ribbon_metric.py / ribbon_track.py.
- Physics per frame was already right (new NX_PHYS_LOG=1: one phys_update per frame, dt 1/60, timescale 1, 76 chains).
- NX_PHYS_DUMP=<file> (chain array +0x134, 0x150 bytes x chains per call; agent_scripts/phys_dump.py -> .npy): chain
  record +0x2c/+0x30/+0x34 = anchor position, +0x50.. matrix. The anchor x moved 0.33, 0, 0.33, 0 ... per frame.
- Watch on Tsubasa's actor +0xc: the cut script (Lua resume 0x5acac0 -> binding 0x41a894 -> actor_set_pos 0x3c853c)
  sets the position on each 30 Hz resume (scripts resume at 30 Hz by design, s11). actor_move_update 0x3c8d90 (job,
  every frame) integrates the move delta +0x6c/+0x70/+0x74 - that delta stays 0 in cutscenes.
- Fix (hle_sys.cpp HLE actor_move_update, names.txt, re-lift 20602 hooks): a position change made outside the job that
  comes after exactly gap-1 calm frames (gap 2..8) and is < 4 units is pulled back and replayed evenly over the gap
  frames (done before the next resume). Per-frame motion untouched (field walk: 0 hits in the log). NX_SMOOTH_MOVE=0 off,
  NX_MOVE_LOG=1 logs steps. 30 fps: hook bypassed.
- Verified: anchor deltas 0.15-0.19 every frame at 60 (direction flips 35% -> 1%), 0.08 at 120 (gap 4); same shot
  before/after: tails no longer swing left/right per frame (shots/s52m_before_after.png, top = before).
- Also smooths Itsuki and any script-walked NPC (they stepped at 30 Hz too).

### 2. Field look: NOT fixed, narrowed
- agent_scripts/door4k.sh <tag> [env] (b20 save, standing at the boss door, Itsuki crop; DRAWLOG=1 / RT=1 options).
- Trousers are clean now (no black). What remains: a pale blue/teal rim along Itsuki's silhouette (sleeves, trousers)
  and a harsh dark face. Same at 720p and with NX_TEX_PACK=0 (shots/s52_door_cmp.png: 4K / 720p / no pack) -> not the
  pack, not render scale. Skipping shader range a7900000-a7a00000 removes the environment only, rim stays.
- RT dump (shots/s52_rt_it.png): scene target bc502910 has only a faint rim; the final target is lighter with a clearer
  teal edge -> probably the post pass (640x360 blur targets bc9772d0/bc977990 composited back) or the game's edge light.
- NEXT: get the user's picture of "ugly" (which part), or Switch footage of the same spot; then drawlog the post pass
  (NX_POST_NATIVE=0 test; skip the composite shader) and compare.

### End state
- Commit d2cbb86. Saves untouched (tests used testsave/b20). Usage 5-hour 96% at pause.
- User checks: ribbon in the boss-door cutscene at 60 fps; Itsuki/Tsubasa walking in cutscenes look smoother.

## Milestone 5, session 53 (2026-11-03 ~00:15-01:25, with user)

### User report 2026-11-03 (s52 build, 240 fps 4K)
1. Tsubasa's ribbon fixed in the boss cutscene (CONFIRMED), maybe not in other cutscenes (save 3: walk on, cutscene).
2. Itsuki's body pose changes at once in the save-3 cutscene before the battle.
3. EXP / Mastery x5: escaping at once still gives Mastery.
4. Field look (pale outline glow) still there, worst in dark areas (save 2). User pictures: Observatory door + dungeon.

### 3. Mastery from escapes: FIXED (verified by replay log)
- The user's run (logs/nx_20261103_001527.log) was the d002_01 tutorial battle: "mastery member 1 +5500 x5 -> 27500"
  before any action, then the escape tutorial (bpro_pcescape) and RESULTS with 3 skills. The 5500 is the tutorial
  script's btlSetForceMastery (binding 0x429870 -> 0x2c3c1c; r1 = character id, r2 = amount x 100); EXP was not
  touched (no btl_add_reward call, EXP 20 before and after).
- Fix: names.txt btl_force_mastery 0x2c3c1c; hook scales earned Mastery first, runs the grant, resyncs the shadow copy.
  Log "battle: script mastery char 2 +55 x100 (not scaled)"; actions still x5 (+900 -> 4500).

### 1. Ribbon / script walks at varying frame rates: FIXED (verified by numbers)
- Save 3 (Daitama Upper Lv, elevator, 380 50 -760): walk 1 s west -> m0009_02 (both walk to the red tent, TOPIC,
  then the Mirage battle). s52's smoothing fired (gap 2 at 60) but counted frames: at 4K/240 (~120 fps here) the gap
  varied 3/4/5 and shown speed jumped (step/dt std/mean 0.19, frame ratios 0.47..2.33).
- Order: the step appears in the frame of the script manager's resume (script_resume_all runs before actor updates).
- Fix (hle_sys.cpp): script_resume_all records g_resume_frame / g_resume_left (game time to that manager's next
  resume); actor_move_update spreads a step seen in a resume frame (after >= 1 calm frame, < 4 units) linearly in game
  time until the next resume. Result: speed std/mean 0.001 at 60, 240 (4K) and uncapped (agent_scripts/move_speed.py on
  NX_MOVE_LOG=2 traces). New debug NX_MOVE_LOG=2 = every frame's shown position.

### 2. Pose snaps: action blends counted frames: FIXED (verified by log)
- _chrPlayAction 0x41ebfc: blend seconds (default 0.5) x 30 -> 0x3ce298 sets step +0x11fc = 1 / frames; chr_motion_update
  0x3ce438 adds the step to weight +0x11f8 once per call (per frame). s0 there is a speed factor (1.0); dt = literal
  0x3ce588 x s0. Walk -> stand: 0.23 s at 30, 1/8 of that at 240 (pose "changes directly").
- Fix: hook chr_motion_update, step x dt*30 for the call. NX_BLEND_LOG=1: [blend] start/done. Measured 0.234 s (30),
  0.25 (60), 0.26 (240).
- cutPlayAction (0x5bcef4, virtual +0x4c with a blend arg) not checked: cut-only actors may still blend fast.
- base60.rec now desyncs (battle opens 5 s later: walk-start blends take Switch time); flow after is the same, 0 crashes.

### 4. Field look: the pale outline is the game's outline SHELL (setting added)
- agent_scripts/rim.sh <tag> [env]: user save 2 (system.bin byte 4 = title Load cursor, not byte 5) -> Observatory door,
  4K crop shots/s53_<tag>.png. Same with every post effect on (shots/s53_* base / edge / allfx).
- Drawlog: every character mesh is drawn 5x (2 shadow, depth, colour, then a 5th pass with front faces culled, colour
  blend src alpha / one minus src alpha = inverted-hull outline; vs 801c2600 Itsuki, 801bd300 Tsubasa). Skipping it
  removes the rim. Its FS: colour = VS attr3^2.2 x c13[0].z x c6[20] x c13[2] (all 1 here); attr3 = vertex colour RGBA8
  (NVN 0x25 = unorm, mapping right), data e.g. 9d9fb0 / a4a4bb / 808080: light grey-lavender by the game's own data.
  An official Switch screenshot also shows a light edge on Itsuki's hair. So: not a translation bug (assumed: not
  compared to Switch footage of the same spot).
- Added setting fx_char_rim (F1 "Character rim", default on = game look): off skips draws with cull front + that blend
  (only the shells use it in the drawlog). Verified shots/s53_rim_on_off.png. Not on the PC settings page.
- Not done: Itsuki's harsh dark face (s52 note).

### End state
- Commit (this session). Tests used testsave/c2, c3 (copies of the user's save/); save/ md5 unchanged, pipelines.bin
  28.1 MB unchanged. Usage 5-hour ~45%, weekly 92%.
- User checks: save 3 cutscene ribbon + Itsuki's stop pose at 240; Mastery x5 escape; F1 "Character rim" off in save 2.

## Milestone 5, session 54 (2026-11-03 ~04:35-05:10, with user)

### User report 2026-11-03 (s53 build)
1. Mastery multiplier: "levels up again after escaping".
2. Tsubasa's ribbon better in another cutscene; "Itsuki cutscene" (save 3, pose snap before the battle) still not fixed.
3. Character rim setting works but the rim was not what the user meant (keep it as an extra setting). Asked: continue
   the dark face (s52 note) and body; add Character rim to the native PC settings page.

### 1. Mastery after escape: game behaviour, no change (verified by the user's log)
- The user's run (private/tms/nx.log 04:31, s53 build) is again the d002_01 tutorial battle: "battle: script mastery
  char 2 +55 x100 (not scaled)" = the tutorial script's btlSetForceMastery (5500 to Tsubasa), escape tutorial
  (FLG_SYS_BTL_TU_ESC), RESULTS with skill_learn. No action Mastery and no multiplier in that battle: the same happens
  at 1x. Asked the user whether to drop that scripted grant (would differ from the original game).

### 2. Save-3 cutscene: no snap found (blends + frames match 30 fps)
- Rig agent_scripts/tent.sh <tag> <nshots> [env] (testsave/c3 copy; setpos 380 50 -760, stick up 1 s -> m0009_02
  red tent cutscene -> TOPIC chat -> dialogue -> `shots N` from the 2nd "action 200 <- 128" blend = the Mirages
  appear, Itsuki turns and shields Tsubasa -> battle). Frames in shots/tent240, shots/tent30; sheets
  shots/tent_sheet2.png (240) and shots/tent30_sheet.png (30).
- NX_BLEND_LOG: every Itsuki blend in the cutscene starts at the same relative time and lasts the same at 30 and 240
  (e.g. 131 <- 128 0.13 s both; 128 <- 131 then 200 0.40 s both). The turn + arm motion spans ~0.4-0.5 s in both
  frame sequences, no single-frame jump seen. Needs the user's exact moment (time / video) to go further.

### 3. Dark face / body = self-shadowing: shadow-map STENCIL views were read as depth (FIXED, verified by 4K crops)
- NX_SKIP_SHADOW=1 (new debug: drops draws into power-of-two depth-only targets) removed the dark hatched shading on
  Itsuki's face -> it is shadow-map shading on the character itself.
- Face FS (drawlog stages line, analysis/code_a2a12f30_5_28d0_18.bin -> analysis/glsl_face): per tap
  lit = (depth <= shadow depth) OR (texel of handle 0x26 == c7[2].x). Handle 0x26 / 0x18 = the shadow maps' second
  pool entries, read with point samplers and I2F: STENCIL reads. The game writes character ids into the shadow maps'
  stencil so a character never shadows itself. We sampled those entries as depth -> id never matched -> every
  character got self-shadow acne (diagonal stripes on cheeks) and a dark face / neck under hair and chin.
- NVN texture view layout: +0x1c = depth-stencil mode (0 depth, 1 stencil); pool ids 278 / 280 (1024x2048, 1024x1024
  D24S8) have 1. nvn::TexView.ds_mode + has; vk::sampled_view makes a VK_IMAGE_ASPECT_STENCIL_BIT view for them (shader
  still declares float sampler2D; the raw uint comes through floatBitsToUint on NVIDIA).
- Verified: shots/s54_face_fix_cmp.png / s54_face_fix_zoom.png (left before, right after: stripes and dark patches
  gone), environment shadows still there (s54_full_cmp.png), battle Chrom face clean (s54_battle_crop.png). Probably
  also the old "Tsubasa / Itsuki dark band in battle" report (s20-s50): same shader path, not checked with Tsubasa.
- Rig agent_scripts/face.sh <tag> [env] (door4k with RSMS ms of right stick so the camera faces Itsuki).
- drawlog now prints "stages (ryujinx stage:code)" per draw (the old "fs" field stays 0).

### 4. Character rim on the native PC settings page (verified by screenshot)
- camp_settings.cpp PC 3/3 row 6 "Character rim" (shots/s54_pc3_rim_row.png). Not toggled in the test (would write
  the user's build/settings.ini).

### End state
- Tests used testsave copies; save/ md5 unchanged, pipelines.bin 28.1 MB unchanged.
- User checks: faces / bodies in field + battle (dark face, cheek stripes gone?), PC 3/3 Character rim toggle,
  answer: drop the tutorial's scripted Mastery? which moment in the save-3 cutscene snaps?


## Milestone 5, session 55 (2026-11-05 ~09:30-, user asleep; scheduled resume 12:21 = task tms-recomp-s55-resume)

### Reddit reports (2026-11-03, user forwarded 11-05)
1. TrishaMeower: background crowd in battle "flashing a lot" (framerate?); only FXAA, asks for MSAA / SMAA.
2. BigheadSMZ: still sped up at high fps: file-select "Select" circle button, Enemy Radar flashing diamonds, spinning arrow
   around the attack icon, arrow above ATTACK, stars next to ATTACK, battle portraits, menu transition effect. Compares
   with Eden's 60 FPS patch (same speed-up), wants the original speed.

### 1. UI speed: setting ui_speed, default 30 = Switch speed (FIXED, verified by frame diffs)
- Cause: since s28 (user decision 10-29) every UI gate (ui_manager_update, camp_update, camp_wipe_update,
  save/load_screen_update, btl_ui_update, btl_wheel_input, party_hud_update, post-battle GATED_TASKs, weak marker, pad
  repeat) used 60 Hz ticks: the widgets count 30 Hz frames, so 60+ fps = 2x the Switch. Every item in the Reddit list is
  one of these gates.
- Fix (hle_sys.cpp): UI clock g_tick_ui30 (30 Hz of real time, base dt, not battle speed); ui_tick_due uses it when
  rt::ui_speed() == 30 (default; NX_UI_SPEED / ini ui_speed = 60 brings back the 60 Hz clock). F1 item "UI animation
  speed" (Original / 60 fps, applies at once) + PC settings page 3 row 7. settings.h documents ui_speed.
- Verified (new debug control `fixdt N` = every frame steps 1/N s, so captures are deterministic; agent_scripts/
  radar.sh, btlui.sh, regdiff.py): Enemy Radar region changes every 8th frame at fixdt 240 (= 30 Hz) and every frame at
  fixdt 30; command wheel / ATTACK region and portraits the same (8-frame steps). Not checked by eye: file select,
  camp wipe (same ui_skip gate).

### 2. Crowd flashing (NOT fixed yet, root cause narrowed)
- Repro: agent_scripts/crowd2.sh <tag> (base60 -> tutorial battle, fps 240, consecutive frames at fixdt 240 / 60 / 30,
  mean brightness of the stands, regmean.py). Stands brightness: fixdt 30 = 85 every frame (crowd visible, the correct
  look); fixdt 60 = ~20-25 every frame (crowd BLACK); fixdt 240 = ~25 with spikes ~65 every 16 frames (= the flashing).
  So above 30 fps the upper stands' crowd goes dark and flashes in.
- Not the cause (tested): UI gates (uigate 0), all 31 dt literals kept at 1/30 (new control `dtkeep <hex mask>`),
  shadow maps (NX_SKIP_SHADOW), async submits (NX_SYNC_SUBMIT=1).
- Drawlog (new `drawlog N` = N frames; NX_LOG_UBO_FULL=<slot> dumps a whole big UBO): lit and dark frames have the same
  486 draws, same per-draw fragment counts, same textures and same small-UBO values (only camera/material values that
  change every frame). The crowd is drawn in both; it is only shaded black. Stage shaders use tiled lighting: compute
  80357ee0 builds a 16x16-tile light list in the 4 MB guest buffer 73d8d000 from the light table at 76296000 /
  77496000 (double-buffered, = fragment ubo slot 14; light count 1, identical in lit and dark frames); fragment shaders
  (e.g. analysis/code_aa584530_5_fd0_4.bin -> private/tms/glsl_crowd) add ambient c5 + grid lights x texture.
- CROWD DRAWS FOUND: the 30 draws with fragment code 89915a30 (vs 7fc74e30). NX_SKIP_CODE=89915a00-89915b00 at fixdt
  30 took the stands from 85 to 28 (crowd gone). Their FS is unlit: colour = texture (512x512 pool, fmt 0x46) x c6[20]
  x c13[2], alpha = tex.a x c13[5].x. The VS UV = attr8 x c6[0] + c6[1].xy (texture SRT). Between lit and dark frames
  the ONLY input that differs is c6[1].y (ubo slot 6 word 5, V offset): e.g. 0.8687 / 0.8594 / 0.8438 (lit) / 0.8437
  / 0.8452. Lit = 0.84375 = 27/32 exactly: the crowd texture is a FLIPBOOK of rows (cells 1/32 high) and the material
  texture-SRT animation is evaluated at fractional frames, so between keys the V offset is interpolated half way to the
  next cell and samples the transparent gaps (black stands). The Switch (30 fps, frame steps of 2) only ever hits keys.
  Vertex data, textures, states, fragment counts, light table: identical lit vs dark (verified).
- Anim callers seen in the battle (NX_ANIM_PROBE=1, ap1.log): model_anim_update+0x2e0, model_skel_update +0x40 /
  +0x1e4 / +0x2b0, and unnamed 0x5541fc (FUN_005541dc: controller = *(obj+0x10) = {frame, start, end, ?, policy fn,
  step}; sets obj+0x6c = 1; frame 106.146 of 0..120 at 182.5 s), 0x554ff8 (0..2200), 0x555668 / 0x5556d4 / 0x55571c /
  0x5557f0 / 0x555860 (FUN_00555638(model): +0x44 skeletal, +0x48 (+0x14), +0x4c count of +0x50[] (+0x10) = probably
  material anims, +0x70 count of +0x74[] (+0xc)). Decompile: ghidra/g.sh Decomp <addr> -> out.c.
- FIX PLAN (next session): find the material anim evaluation (the reader of those controllers' frame for the
  texture-SRT / shader-param curves; candidates: callees of 0x5541dc / the +0x50[] list), and evaluate it at the frame
  rounded DOWN to the Switch grid (even 60 Hz frames = 30 Hz steps), keeping the controller's true frame. Verify with
  crowd2.sh: stands ~85 at fixdt 240 and 60 in every frame. Risk: smooth scrolling materials (water) then step at 30
  Hz (= Switch look). Alternative if the eval is not found: per-call-site rounding in the play-policy hook with a shadow
  true frame per controller (needs the controller address).

### 3. Anti-aliasing (SMAA / MSAA): NOT started (answer for the Reddit user)
- The game renders forward + MRT (colour, two extra targets) and its own post chain; MSAA would need multisampled targets
  for every pass and resolves before each post effect: large, risky. SMAA = own 3-pass shader (edge detect, blend
  weights with precomputed area/search textures, blend): ~1-2 sessions, our own code (no copied SMAA source per the
  user's rule). Cheaper now: render at a higher internal res than the screen (res 4k on a 1440p / 1080p display =
  supersampling) should work through the present scaling path (NOT verified this session). Ask the user which to build.

### Debug added this session
- NX_CONTROL `drawlog N`, `fixdt N` (0 = off), `dtkeep <hex>`; env NX_LOG_UBO_FULL=<slot>. sheet.ps1 takes CW (cell width).

## Milestone 5, session 56 (2026-11-05 ~12:20-, scheduled resume, user asleep; commits 3f61520, d8c1263)

### 1. Crowd flashing in battle: FIXED (agent-verified by drawlog + frame stats, NOT user-tested)
- s55's measurement was CONFOUNDED: crowd2.sh's fixdt 240 / 60 / 30 phases run seconds apart and the battle idle camera
  orbits, so the "stands brightness 85 vs 20" compared different views (screenshots: crowd visible in both). The real
  symptom: 1-frame flashes (stands region 25 -> 47) every ~16-28 frames at 240 fps, where the UPPER stands (normally
  black) fill with crowd for one frame. Shots in shots/cgC_240 (frames 12, 28, 56).
- Root cause (agent_scripts/crowdfl.sh = shots + drawlog of the same N frames; crowdparse.py, flashdiff.py): one draw,
  fs aa584530 (upper stands crowd), texture V offset c6[1].y = a 4-cell flipbook 0 / .25 / .5 / .75 held ~16 frames,
  with CUBIC steps between keys 2 frames apart (overshoot: 0.4979 0.4816 0.5243 0.6682 0.7630 0.7603 0.75). The
  Switch only evaluates even frames (30 Hz updates, step 2 from the start) = only cell values. Above 30 fps the
  in-between frames show half cells = the flash.
- Path: model_obj_update 0x3a4410 (vtable 0x7dea9c, info+0xc = dt x model speed) -> model_mat_update 0x555c40 (dt /
  (1/60) frames, policy step) -> mat_anim_eval 0x4e51c0 (per material, skips if frame == +0x2c) -> mat_eval_a_cached
  0x4e8c74 -> anim_curve_float 0x4e768c (s0 frame, curve, cache -> s0; curve +0x10 flags, +0x18/+0x1c range, +0x20
  scale, +0x24 offset). 0x4e77d0 = anim_curve_int (bone visibility). All in names.txt.
- Fix (hle_sys.cpp, before NX_ANIM_PROBE): mat_anim_eval sets a thread-local "in material eval" + controller start;
  anim_curve_float evaluates p, a, b, n at the Switch frames g-2, g, g+2, g+4 (g = start + even floor): a JUMP (|b-a| >
  2x max(|a-p|, |n-b|)) or a HOLD (b == a) returns a (the Switch value); anything else returns the true frame value, so
  scrolls stay smooth. 5 curve evals instead of 1 for material float curves only; only when fps != 30. NX_MAT_GRID=0
  turns it off. First version (whole material anim on the 2-frame grid, 3f61520) made the field WATERFALL step at 30 Hz
  (regdiff 6.0 every 8th frame) -> replaced by the per-curve test (d8c1263): waterfall changes every frame again.
- Verified: 64 frames at fixdt 240: aa584530 V offset only 0 / .25 / .5 / .75 (before: 22 in-between values), stands
  brightness max 24 (before: spikes 47-49). Field d002 waterfall smooth (agent_scripts/campw.sh wf1).
- NOTE: today's 2x material step (dt 1/30 at fixdt 60) is the user's battle_speed = 2 in build/settings.ini, not a bug.
- Debug: NX_MAT_LOG=N (+ NX_MAT_FROM=frame): [mat] / [matupd] / [objupd] lines; NX_CURVE_LOG=N: smooth-path samples
  that differ from the Switch value by > 0.05.

### 2. UI speed (s55) checks by eye/diff
- File select (Load screen) SELECT bubble: region changes every 8th frame at fixdt 240, every frame at fixdt 30 = 30 Hz
  (agent_scripts/loadscr.sh <tag> testsave/b20, KEYS="a"). Camp wipe NOT checked: 'x' in the field = Sword Strike;
  the camp key is another one (try 'y' / NX_CONTROL key list).

### 3. AA
- Present = linear blit (vk.cpp present_async / present): at the default res = 4k on a 1080p display it is an exact
  2:1 = 2x2 box filter = 4x SSAA; 1440p display = 1.5:1 bilinear (partial SSAA). 4K displays: only FXAA;
  NX_RES_SCALE=4 renders 5120x2880 (clamp is 4) = 1.78x SSAA (heavy). SMAA (own code) / MSAA still need a user decision.

### 4. Later in s56 (commits af76e48, d3576d2)
- Perf of the curve test: battle 4K uncapped (agent_scripts/btlperf.sh) hook off 1520/1488/1271 presents per 10 s,
  first per-curve version 1504/1385/1140 (-3..7%); now the test runs once per curve and Switch window (thread-local map
  curve -> {g, start, signature of +0x18..+0x24, a, jump}, cleared at 65536): 1521/1467/1220 = hook-off level.
  Re-verified after the cache: crowd only 0/.25/.5/.75 in 64 frames (cfq), waterfall changes every frame (wf2).
- NEW Resolution 8K (res = 8k / NX_RES=8k, render scale 6 = 7680x4320, clamp 4 -> 6): supersampling for 4K screens
  (present blit 2:1 = 2x2 box). Battle at 8K: ~136 fps here, VRAM 5.0 GB (4K: 2.4 GB), image correct
  (shots/r8k_240). F1 "Resolution" 5 choices (help text explains SSAA), PC page slider follows the item, launcher
  choice + status line, settings.ini comment. NOT checked by eye on a real 4K screen.
- UI speed checks (all = 30 Hz steps at 240, every frame at fixdt 30): file-select SELECT bubble (loadscr.sh), camp
  open wipe (campw.sh, KEY=y; x = Sword Strike), loading spinner "NOW LOADING" (loadicon.sh <tag> testsave/b20 [fixdt],
  region 1782,1252 145x150 at 1080p setting). So the s34 "loading icon too fast" item is fixed too (by s55's UI clock).
- Perf look (open item 10): Daitama Upper field (b20) at 4K uncapped = ~130 fps, min frame gap 6.6 ms; NX_PROFILE:
  32% innermost guest F_004fadb8 = a wrapper around NVN command-buffer calls (= our nvn HLE), host side heap alloc /
  SRW locks / vector<nvn::Cmd> inserts ~25%. Possible later work: reserve nvn::Cmd vectors / avoid copies. Not touched.

### Session 56 end state
- Commits 3f61520, d8c1263, (notes), af76e48, d3576d2. Saves untouched (tests: testsave/b20 copies, base60 replays).
- User checks: battle crowd no longer flashes at 60/120/240 (any battle with the stands, e.g. idol stage); waterfalls
  / scrolling textures still smooth; Resolution 8K on a 4K screen (AA quality, fps); UI speeds (s55).
- Still open: SMAA / MSAA (user decision; 8K and 4K-on-1080p SSAA exist now), OPEN LIST (s39) items needing the
  user's saves / pictures.

## Milestone 5, session 57 (2026-11-05 ~19:00-, with user; commits 978fdd0, ef304d7)

User: "implement the SMAA MSAA, then continue what has not been done".

### 1. SMAA: DONE (agent-verified by crops, NOT user-tested)
- Own code, no SMAA source: tools/spvgen/Smaa.cs -> runtime/src/smaa0..3_spv.h (dotnet run --project tools/spvgen --
  smaaN runtime/src/smaaN_spv.h). Pass 0 edges: luma (Rec. 709) delta to left / top neighbour > 0.05 and >= half the
  largest delta around (local contrast). Pass 1 weights: per top / left edge, walk both ways along the edge (max 32
  px, NX_SMAA_STEPS; stops at crossing edges), each end's crossing edge = silhouette step +-1/2, line from each end's
  half step to 0 at the segment centre (MLAA Z/U/L shapes), the pixel's share of the area = blend weight for the pixel
  on that side (no area / search textures). Pass 2 (rgba8) / 3 (R11G11B10 float, StorageImageExtendedFormats, device
  feature shaderStorageImageExtendedFormats now enabled): neighbour blend, weights scaled down when they sum > 1.
- Where: vk_replay.cpp draw() at the game's FXAA draw (fxaa_frag() = the old fxaa_rescale detection): end rendering,
  copy the FXAA input (3840x2160 B10G11R11_UFLOAT at 4K, measured) to a work image, 3 dispatches write it back in
  place via its storage view, FXAA thresholds -> 100 (pass-through). So SMAA is under the UI like FXAA.
- Setting: fx_fxaa = 0 off / 1 FXAA (default) / 2 SMAA (NX_SMAA=1 also). F1 "Anti-aliasing" Off/FXAA/SMAA, PC page 1
  same row (name-matched), launcher Display page drop-down (launcher NOT checked by eye).
- Verified: field Observatory 4K, shots none / FXAA / SMAA (private/tms/shots/aa_none, smaa_off, smaa_on): SMAA smooths
  Itsuki's shoulder and Tsubasa's skirt / leg silhouettes, textures stay sharper than FXAA. 200 s run, no device
  fault. Uncapped: 1519-1521 presents / 10 s with SMAA and FXAA (display cap here, no measurable cost). Battle with
  SMAA NOT run (tobattle.sh needs the Daitama save; field.sh loads slot 2 = Observatory). pipelines.bin size unchanged.

### 2. MSAA: assessed, NOT built (needs a user decision)
- What it takes here: per render target used with depth (the 3D scene: colour + 2 MRT + depth at render scale) a
  multisampled twin; begin_rendering into the twin with resolve attachments (colour average, depth SAMPLE_ZERO, integer
  MRT SAMPLE_ZERO); every pipeline gets a samples variant (pipeline cache keys, recipes, prewarm); a target written by
  a copy / clear / compute / single-sample draw must be re-expanded into its twin before the next MSAA pass; shaders
  that read the scene depth (DOF, outline, fog, soft particles) see the resolved depth. Memory at 4K x4: ~400-600 MB.
- Value: the default already renders 4K internally (= SSAA on 1080p / 1440p screens), 8K SSAA exists for 4K screens,
  and SMAA now handles the remaining jaggies. MSAA would not smooth alpha-tested foliage / hair cards (no
  alpha-to-coverage in the game's shaders) or shader aliasing. Estimate 2-3 sessions + regressions in every post
  effect. Recommendation: do not build unless the user still wants it after trying SMAA.

### Session 57 end state
- User checks: Anti-aliasing = SMAA in F1 (applies at once) in field and battle (crowd stands, idol stage, hair);
  launcher Display page drop-down; fps.
- Still open: MSAA (user decision), OPEN LIST (s39) items needing the user's saves / pictures, perf idea from s56
  (nvn::Cmd vector reserves).

### Session 57 part 2: MSAA BUILT (user changed mind: "just implement msaa too"; commit aaae656; agent-verified, NOT user-tested)
- Setting msaa = 0 (default) / 2 / 4 / 8 (NX_MSAA), F1 "MSAA" Off/2x/4x/8x (applies at once), PC page 3 row 8. Not in the
  launcher (pages full). Clamped to the GPU's colour/depth/stencil sample counts.
- vk_replay.cpp MsTwin: a pass is MSAA when it has a depth target at render scale (res_scale) and colour targets of the
  same size (single layer/level): the 3D scene. Shadow maps (no colour), post and UI passes stay 1x. Attachments draw
  into multisampled twins; pipelines get the sample count (key only grows for MSAA: 1x cache entries unchanged; MSAA
  pipelines are NOT in the recipes/prewarm, so they compile on first use = brief pop-in).
- Resolve is lazy (ms_flush: empty dynamic rendering with resolve attachments; colour AVERAGE, integer formats and
  depth/stencil SAMPLE_ZERO) at: a pass with other targets, copies, ClearTexture, dispatch, sampling a dirty image
  (bind_resources), the SMAA pass, end of replay().
- The scene colour (B10G11R11 4K) is written at 1x before each scene pass, so a stale twin is refilled by ms_expand:
  full-screen triangle drawing the 1x image into the twin (tools/spvgen/MsExpand.cs -> msxv/msxf_spv.h). First try =
  compute imageStore to a multisampled storage image: the NVIDIA driver HUNG in vkCreateComputePipelines (no error) ->
  dropped. Stale depth with content and no clear ahead -> that pass is 1x. Clears after OP_RENDER_TARGETS are looked
  ahead (g_clear_ahead); ClearTexture clears the twin too. Copies into an image mark its twin stale.
- Verified (field Observatory 4K, private/tms/shots/msaa4.bmp with FXAA, msaa4_only.bmp without): image correct,
  silhouettes (legs, skirt hem, shoulder) anti-aliased; uncapped 1503-1521 presents / 10 s = display cap here (same as
  off); 60 fps run 600/10 s; no device fault. NOT checked: battles, cutscenes, DOF/outline/fog with resolved depth,
  8x, 8K + MSAA (VRAM: 4K 4x adds ~0.4 GB colour+depth twins), memory over a long run.
- Debug: NX_MSAA_LOG=N logs N pass decisions (why 1x).
- Shortcut: twins keyed by Image*, never freed when the image goes away (replaced when a new image at that address
  differs); upgrade if VRAM grows.

## Milestone 5, session 58 (2026-11-06 ~09:00-, user asleep after the report; user: at 5-hour 99% pause, write notes, schedule a resume at 10:21 AM, no questions)

### User report 2026-11-06 (s57 build, Reddit items seem fixed)
1. REGRESSION: "everything slow, even dialogue". USER RULE (again, firm): 60 Hz is standard for 60 fps; fps cap 30 -> 30 Hz; every UI speed thing at 60 Hz;
   uncapped must be SMOOTHER, not speedier. Never default anything UI to 30 Hz again.
2. Dark faces / bodies in battle (shots 1, 3): compare Tsubasa in Artists menu (clean) or YouTube (clean skin).
3. Crowd: black stands with only arm tips; should be a full crowd (YouTube shot).
4. Then continue the open list.

### 1. UI speed: FIXED + smoothing above 60 fps (agent-verified, NOT user-tested)
- rt::ui_speed() default 60 (NX_UI_SPEED=30 / ini ui_speed=30 opt-in, F1 "UI animation speed": Switch / 60 Hz). s55's 30 default was the regression.
  Measured: file select at fps 240 = screen changes every 4th frame (= 60 Hz; loadscr.sh + per-frame count; before smoothing).
- RESULTS wipe still on 30 Hz game ticks (user asked for that in s45: "too fast"). Kept on purpose.
- UI smoothing (setting ui_smooth, default 1, F1 "UI smoothing", ui_sprite_smooth in vk_replay.cpp): every UI sprite = one OP_DRAW of 4 vertices, stride 36, attribs [0]=04400040 [3]=05c00640 [8]=02c00e40,
  fresh in the frame's ring near its UBO (vertex ubo INDEX 1 = "slot 4"; words 0-7 matrix rows, word 16 = 2/1280 ortho). rt::ui_clock gives UI tick + fraction. Sprites of the previous tick matched by key (texture
  handle + uv of corners 0, 3), in order; corners + colours are lerped and written back into the guest vertices, in the sprite's local space (inverse 2x2). Moves > 320 px, no match, unmoved: as drawn.
  Only while frames are < 0.75 tick. Cost: shows the UI up to one tick (16 ms) late. uv steps (scrolling, flipbook) stay at 60 Hz.
- Verified: file select at 240: every frame changes (9000 px sub-steps, 23000 at ticks); battle wheel: ATTACK label + ring grow in sub-steps, 90 sprites, 90 matched, 14 glided (shots/bu1_c). NX_UI_SMOOTH_LOG=1 prints stats.

### 3. Crowd: FIXED, ROOT CAUSE = hardware alpha test never implemented (agent-verified by 4K shots, matches the YouTube look; commit "Hardware alpha test")
- s56's note "upper stands normally black" was WRONG.
- NVN ColorState bits 24-27 = AlphaFunc (driver 0x21bcc74; default 8 always), nvnCommandBufferSetAlphaRef was an empty hook, the sidecar translates AlphaTestOp.Always.
  The crowd cards (mesh 1440 indices, 240 quads ~141 x 35 units, RGBA8 sRGB 512x512 flipbook of 4 cells, textures/dump_all/512x512_38_*) use func 5 GREATER, ref 0.50196, in the depth
  pre-pass (fs 008b4030, ds 0x43, no colour writes) and the main pass (ds 0x31 = depth EQUAL). Without the test every card wrote depth over its transparent
  part, so nearer rows' cards hid rows behind: front row complete, only tips above it.
- Fix: OP_ALPHA_REF, alpha_module() (vk_shader.cpp) patches the fragment SPIR-V: before each OpReturn of main, load output location 0, compare alpha, OpKill. Pipelines with a test
  add the ref to the key; all other pipelines keep key + driver hash. Variants are not in shaders.bin, so recipes cannot prewarm them (compile on first use).
- Likely helps every other alpha-cut mesh with func != 8 (none else checked).

### 2. Dark faces + bodies: FIXED (agent-verified: 4K crops + frame flip diff, NOT user-tested). Four separate bugs on one path
- Method: control `skipshadow 2` flips casters off / on per frame, `shots 6`, agent_scripts/bmpdiff.py = per-frame diff with almost no camera motion (agent_scripts/shdiff.sh, WAIT=1). fixdt does NOT freeze the battle camera.
- The game's rule: a fragment counts as lit if shadow depth passes OR the shadow map's stencil id == c7[2].x, so a character never shadows itself. Chrom + Tsubasa ref 2, enemies 18 / 19.
- Bug A: replay never applied stencil ops (passOp stayed KEEP), stencil stayed 0. NVN word1 layout from driver 0x21bcdf4: func 0-3, fail 4-7, depth PASS 8-11, depth FAIL 12-15, back = +16;
  enum 1 keep 2 zero 3 replace 4 incr 5 decr 6 invert 7 incr wrap 8 decr wrap. Casters = 0x1318 = replace on pass. Applied only with the stencil test on (other pipelines keep their driver hash).
- Bug B: SetStencilMask / ValueMask overwrote the REF (same OP). Now only logged when != 0xFF ("nvn: stencil write/value mask ... ignored"); masks stay 0xFF.
- Bug C: float samplers over stencil data never give the id (Vulkan: undefined). integer_samplers() in make_module (vk_shader.cpp): samplers whose result reaches OpBitcast + OpConvertU/SToF become uint samplers; each sample's
  uvec4 is bitcast back to the vec4. Static, so spirv_hash and recipes keep working (hash is the sidecar's); prewarm rebuilds these pipelines once. Log: "vk: N integer sampler(s) in a shader".
- Bug D (the one that made A-C look useless): each surface has TWO NVN textures at the same GPU address (depth bc960310 + stencil-mode bc960690, shadow maps 1024x2048, 1024x1024). image_of made one image each, so the
  shader read ids from an empty image. Now depth / stencil textures at the same gpu address + size share an Image (g_ds_by_gpu, Image::share counts, freed with the last).
- Dead end, removed: compute copy of stencil into an R32 image (R32_SFLOAT flushed denormal ids to 0, and it copied the wrong image's reader anyway because of Bug D).
- Result: shdiff on / off shows NO change on Chrom's body or face (only camera edges), face clean. Field Observatory: flip diff shows ONLY the floor shadows of Itsuki + Tsubasa, no shading on bodies.
- User's build/settings.ini has bloom / glow / DOF / vignette / fog / outline all OFF: their choice, but it changes the look vs YouTube (fog on tints the scene teal). Told the user.

### Checks after all fixes
- MSAA 4x + alpha test in battle: full crowd, no fault (ms1). uncap_batch.sh 4 x 420 s: 0 crashes, saves md5 unchanged. pipelines.bin grew 28.1 -> 32.7 MB (only grows).
- Reddit crowd flashing (s56) still applies: flipbook cells now visible as a full crowd.

### Session 58 end state
- Commits: UI default, alpha test, stencil / integer samplers, UI smoothing. All agent-verified, NOT user-tested.
- 5-hour window reset at 10:20 (next 15:20); never reached 99%, so no resume task was scheduled. An extra safety resume task was refused by the permission classifier.
- User checks: dialogue + menus at 60 and uncapped; battle faces; crowd; F1 "UI smoothing" on / off.

### Attack Session: DONE (open list item 7; agent-verified, NOT user-tested)
- Attack's record (table + 1 * 0x84) gets the fields s50 found (attack_session_patch in hle_sys.cpp): +0x20 = 2 (the Session gate: 1 = basic attack), +0x22 = 0x19, +0x54 = 1, +0x56 = 2, +0x58 = 9, +0x5a = 1, +0x0a = 1, +0x60 = 2.
- skill_copy hook (0x27f290, 35 callers, copies the record + weapon stats; new names.txt entry, needs `python tools/recomp/lift.py private/tms/link private/tms/gen` before build.cmd): callers in the damage routines 0x2b8bc8..0x2c1000 get formula 1 + the original power 0 back.
- Verified (agent_scripts/asdmg.sh, testsave/s20, Caspar made sword-weak, NX_SKILL_POKE=144:44:41 because Tsubasa only knows Elec-Lunge): Session Lineup "Start Attack", SESSION 01 GOOD, Elec-Lunge follows (shots/as2). Damage equal with / without: 58 HP enemy -16 both, 68 HP enemy -31 / -32.
- Skill help: no [Power ...] on Attack (the record's value is not the real one); " (Session won't occur.)" blanked in the loaded text (English only, found at the same scan as Agi's text; NOT checked on screen).
- Setting attack_session (default 1, F1 row, restart). Not in the launcher / PC pages. NX_DEBUG_BATTLE also logs "battle: target hp".

### Performance try: reverted
- b20 Daitama field, 4K uncapped: 115 fps (agent_scripts/fieldperf.sh; flat profile). Inline 48-byte Cmd payloads + thread-local cmdbuf lookup cut heap from 8.8% to ~5% but Cmd copies grew: 110-115 fps, no gain. Reverted. The real lever would be CallCommands without deep copies (needs OP_CALL + clear look-ahead across lists); not done.

### Open after s58
- User checks above + Attack Session in play. Shader misses (5, harmless), clean VM test (needs user), s54 questions (drop the tutorial's scripted Mastery? which moment of the save-3 cutscene snaps?).
- Final crash batch on the final code: 4 x 420 s, 0 crashes, saves md5 unchanged. ZIP Desktop\TMSRecomp-20261106.zip 85.1 MB.

## Milestone 5, session 59 (2026-11-06 ~17:50-, with user)

### User report 2026-11-06 (s58 build; plays uncapped ~150 fps, battle_speed 1)
CONFIRMED by user: Attack Session works; Tsubasa + Itsuki faces clean; audience full, no black. Tutorial Mastery grant: KEEP (s54 question closed).
Still fast: 1. Topic menu open (green diamonds, white background); 2. green marker under turn-order portraits; 3. target spotlight + "?" panel; 4. SESSION / COMBO / GOOD text. 5. Victory poses cut by RESULTS. 6. "MSAA not available".

### Method: measure against Switch frame logic
- `fixdt 30` in variable mode (fps 240) = every frame is a Switch frame (fixdt is ignored in fixed mode: `fps 60`, and live `fps 30` does not exist; NX_FPS=30 runs do not find a battle in tobattle.sh). Compare bursts at fixdt 120 vs 30.
- NX_UI_STEP_LOG=1 (needs ui_smooth or NX_UI_SMOOTH=0): sprites changing between UI ticks. The replay thread lags the guest by a frame, so 60 Hz sprites show 60 hits / 240 frames: only > 70 means ungated. Battle HUD: none.
- Rigs: agent_scripts/topic.sh (Topic bursts), tgt.sh (target pick), sess.sh (SESSION text burst at the 60 fps cap, real frames; WAIT / N set the window), vict.sh <tag> <fps> <fixdt|0> (NX_ENEMY_HP1 + A until bgm 65; prints the timeline), uistep.sh, topcov.sh, uifrz.sh + frzcmp.py (freeze experiment, camera noise made it useless).

### 1. Topic: root cause = no gate at all (FIXED, agent-verified, NOT user-tested)
- Probe build (--probe-range 200000:4b0000, topcov.sh): map manager update 0x4a338c (names map_mgr_update) runs every frame and counts frames: Topic state +0x1b0, open / close +0x1b4 0..4, diamond strip scroll +0x8d4, 12 icon flipbook timers +0x8dc + 8 i. At 150 fps = 5x the Switch.
- Fix: Topic open (+0x1b0 != 0): whole update on 30 Hz ticks of real time (press frames pass). Closed: runs every frame (minimap follows the player), only the strip / flipbook counters are put back on frames without a UI tick.
- Verified: at fixdt 120 the bottom strip changes every 4th frame with the same step sizes as every frame at fixdt 30 (before: every frame).

### 2-4. Battle HUD: were gated at 60 Hz = 2x the Switch (FIXED, agent-verified, NOT user-tested)
- Chevron region at fixdt 120 stepped at 60 Hz ticks; nothing ungated. SESSION text is drawn by a btl_ui_update part: pop-in ~16 frames at 60 fps before, ~32 frames with the 30 Hz mask.
- Every part of btl_ui_update got a hook (names btlui_p24 .. p54, BTL_UI_PART). rt::g_ui_part30 mask: all parts on 30 Hz real-time ticks except bit 9 = command wheel 0x2ea044 (stays 60 Hz: input feel). control `uipart <hex>` changes it, `uifreeze <part + 1>` stops one part.
- DECISION (agent, from the report): this is an exception to the s58 rule "every UI at 60 Hz", only for what the user called too fast. Dialogue, menus, wheel stay 60 Hz. Report it to the user.
- UI smoothing: rt::ui_clock switches to 30 Hz ticks + g_ui_frac30 while 30 Hz widgets ran in the last 200 ms, so these sprites glide for the whole 33 ms (also at 60 fps). Sprite pairs now = nearest sprite of the same key (order pairing slid a scrolling strip back at each wrap).

### 5. Victory: FIXED (agent-verified by timeline + shots, NOT user-tested)
- btl_main state 0xc waits for the victory process (vtable 0x7d55dc, child of **0x9ef790 +0x20). Switch frames: 129 (timer -99). 60 fps: 58 ticks = 1.9 s, 240 fps: 1.0 s (timer 0): its sequence tasks without a delay run per frame. s47's timer fix only protected the 1 s minimum.
- Fix: while state == 0xc, btl_seq_update runs on 30 Hz game ticks. Measured 240 fps: timer -97, bgm 65 -> wipe 4.16 s, shots/vj_sheet.png shows the camera shots + poses complete. A still skips (game's button 0x20 check).
- NX_VICTORY_LOG=1 logs the process words.

### 6. MSAA
- Works by env / ini (s57, s58 checks); the launcher had no row, likely why the user saw none. Launcher Graphics page: new MSAA row (Off / 2x / 4x / 8x, key msaa); Blur effects moved down, "Collect textures" moved to Advanced. Frame-rate help text updated.
- Verified: launcher Graphics page by window capture (shots/lg.png, agent_scripts/launcherpage.ps1 <sidebar y> <png>); NX_MSAA=4 battle target pick at 4K: correct image, full crowd, no fault (shots/ms.png).

### Checks + end state
- Crash batch on the commit: 4 x 420 s uncapped 4K, 0 crashes, battle cues present, saves md5 unchanged.
- User checks: Topic open at uncapped; chevrons + target "?" + SESSION text pace; poses finish before RESULTS (A skips); launcher MSAA row, then a battle; dialogue + wheel unchanged. If a HUD part now feels slow: `uipart` clears its bit in the mask (hle_sys.cpp g_ui_part30).
- Not changed: Topic / HUD were not compared with real Switch footage, only with the game's own 30 Hz frame logic.
- Still open: 5 shader misses (harmless), clean VM test (user), save-3 cutscene moment that snaps (user), Tsubasa hair glitch picture (user), big-area fps (s58: flat profile, CallCommands without deep copies is the real lever).


## Milestone 5, session 60 (2026-11-08 ~07:15-, with user)

### User report 2026-11-08 (s59 build; uncapped 240, 4K; video D:\OBS VIDEO\OBS\2026-11-08 07-11-29.mp4)
1. Target spotlight (yellow beam) still too fast, "speed up uncapped". 2. Battle skill list feels 30 Hz. 3. Topic chat feels 30 Hz
(should be 60 Hz, smoother uncapped). 4. Sparkle stars on the Action portrait glitchy uncapped. 5. Field "CALL" ring text far too fast.
6. Itsuki glitch in the save-3 cutscene (video).

### 6. Itsuki: turn action looped forever (FIXED, log-verified, NOT user-tested)
- Video: "That must be it." (m0009_02, before the red tent). Itsuki snaps from back view to side view, turns back, snaps again (every
  2.65 s in the video, 1.3 s in our 720p run). At 30 fps: action 132 then 128 (idle) 1.0 s later; at 240: 132 never ends.
- Script: chrRotTo (ScriptCommon/Utility/ActorUtility.lua closure 49) -> _chrRotTo 0x41cbd4 plays TURN_LEFT/RIGHT (0x83 / 0x84)
  and starts thread _chrActorRotThread, which calls _chrActorRot 0x41d28c each resume: yaw from the turn clip's frame, and at
  frame >= end it plays idle 0x80 (0x412580(4.0, actor, 0x80)) and returns false. Binding table: names at 0x7e1dcc.. (pairs).
- The clip's frame record {cur, start, end} (via action table chr +0x530 + id*4 + 8 -> +0x1c8 key, list *(chr +0x11c8) +0xe4 nodes
  {+4 next, +8 key, +0xc ->anim}, anim +0x44 -> +0x10 ...; 0x555734 / 0x5558c8 / 0x555950). The end frame lasts ONE update, then
  the action chains to its next clip (60-frame turn -> 160-frame look loop) even with speed 0. 30 Hz resumes at 240 fps miss it.
- Fix (hle_sys.cpp turn_frames + chr_motion_update): a turn clip on its end frame gets no motion update for up to 0.1 s game time
  (pose stays), so the next resume ends the turn; a wrap without an end frame puts the frame on the end. NX_TURN_LOG=1 holds /
  wraps, =2 every turn update. Verified (agent_scripts/itsuki.sh <tag> <fps>, S= shots, N= A presses; headdiff.py): 132 -> 128
  after 1.03 s at 240 (30 fps: 1.0 s), no snap spikes in 200 frames.

### 1. Spotlight: it was the battle speed-up (FIXED, log-verified, NOT user-tested)
- User log logs/nx_20261108_070910.log: "battle speed: 2x", then 3x in that battle (screenshot note "speed up"). At 1x the beam
  steps on 30 Hz game time (tgt.sh bursts: fixdt 120 changes every ~4 frames, fixdt 30 every frame).
- Fix: battle_dt() stays 1x while the player chooses: btl_wheel_input sets g_btl_input_ms (it runs during wheel, skill list and target
  pick). Log "battle speed: 1x while choosing" / "back to the set speed". Verified NX_BATTLE_SPEED=2: 1x from the wheel through target
  pick, 2x from the attack, 1x again next turn.

### 2. Skill list: btl HUD part bit 2 (btlui_p1c 0x2f4688) back to 60 Hz (agent-verified by freeze test, NOT user-tested)
- uifreeze per part with the list scrolling: only p1c (and the wheel input, bit 9) stop the list. p1c does not hold the target panel.
  g_ui_part30 default = 0x1ffff & ~bit 9 & ~bit 2.

### 3 + 5. Topic chat 60 Hz, CALL ring 30 Hz (map_mgr_update rewritten; NOT user-tested)
- CALL ring = field top-left ring ("1", portrait, "CALL" text running along the arc) shown ~4 s before the Topic opens in save 3.
  s59 stepped its counters on 60 Hz ticks while the Topic was closed (2x the Switch) and the whole open Topic on 30 Hz ticks (chat 30 Hz).
- Now: open = update on UI ticks (60 Hz); closed = every frame; in both, counters +0x1b4, +0x8d4, +0x8d8, +0x8dc + 8 i (12) step only on
  30 Hz real-time ticks. Verified: CALL text travel per game time equals fixdt 30 frames (agent_scripts/callring.sh <tag> <fixdt|0>).
  Chat 60 Hz: by code only (shot rate ~35 fps could not separate 30 / 60).

### 4. Sparkle stars: no glide farther than the sprite's own size (NOT verified against the user's glitch)
- ui_sprite_smooth pairs the nearest sprite of the same texture + uv; sparkles appear at new spots, so a star could slide from another
  star's spot. Glide only when moved <= max(sprite size, 4 px). Frames after the change show no sliding stars; the original glitch
  was not reproduced on purpose (needs the user's eye).

### End state
- Rigs: itsuki.sh, callring.sh, headdiff.py (crop diff per frame). Tests used testsave copies (c3, s20); save/ md5 unchanged.
- Crash batch uncap_batch.sh 80 420 NX_WALK_SPEED=2: 4 x 420 s, 0 crashes, battle cues present; pipelines.bin 32.8 MB unchanged.
- User checks: save-3 "That must be it." (Itsuki still), battle speed 2x/3x target pick at normal pace, skill list feel, Topic chat,
  CALL ring pace, Action sparkles.

## Milestone 5, session 61 (2026-11-08 ~08:20 +07, user asleep; PAUSED at once: WEEKLY 99%)

User request (verbatim intent): "add DLAA or DLSS 4.5 and FSR 3 above. Possible at all without causing any issue?
Make sure no legal issue." User asleep, said do not ask, just do it. Session 60 build is still NOT user-tested
(Itsuki "That must be it." scene, target pick at 2x/3x, skill list, Topic chat, CALL ring, Action icon stars).

Nothing built this session (weekly limit 99% at start). Scheduled resumes: tms-recomp-s61-noon (12:01 +07, after
weekly reset 11:59:59 +07) and tms-recomp-s61-evening (17:01 +07).

### What exists already
- FSR 1 (EASU+RCAS, own SPIR-V via tools/spvgen Upscale.cs), s43. CAS sharpen s26. SMAA/MSAA s57. 8K SSAA s56.
- s25/s34/s43 finding: DLSS, DLAA, FSR 2/3 all need per-pixel MOTION VECTORS + depth + jittered projection.
  The game renders none. s43 DECISION was "FSR 1 only, no DLSS" -> user now asks again, so build it.

### Technical plan (assumed, not measured yet)
1. Motion vectors, phase A (camera only): from the scene depth buffer + current and previous view-projection
   (find where the game uploads camera matrices: cbuf data of the main 3D pass; NX_LOG_UBO_FULL helps) ->
   compute pass writes RG16F MVs = reproject(depth). Correct for static world, wrong for moving characters.
2. Phase B (objects): characters are skinned on GPU from bone palettes. Keep the previous frame's palette/
   model matrix per draw (keyed by draw identity) and run a second vertex variant that outputs prev clip pos
   (SPIR-V variant like alpha_module), or mark character pixels via the shadow stencil ids (s54) and let the
   upscaler treat them as reactive (FSR3 reactive mask / DLSS bias mask) as a cheaper first step.
3. Jitter: add sub-pixel Halton offset to the projection of the main 3D pass only (not UI), pass jitter to SDK.
4. Insert point: where FSR 1 runs now (before UI; scene at render res, output at display res). DLAA = DLSS at
   scale 1.0. UI stays native (already composited after).
5. Settings: upscaler = off/fsr1/fsr3/dlss; quality preset; F1 + PC page + launcher. DLSS only on NVIDIA RTX
   (NGX init fails -> fall back to FSR 3, log it). User GPU NVIDIA (4K 160 Hz).
6. Skip FSR 3 FRAME GENERATION first (UI interpolation artifacts, pacing work just finished); upscaling/AA only.
7. Verify: 4K crops vs 8K SSAA reference, fps at 60/uncapped, moving Itsuki ghosting check, 0-crash batch,
   caches never shrink, saves md5.

### Legal check (from memory of the licences, MUST be re-read from the actual licence files before shipping)
- FSR 3 / FidelityFX SDK: AMD, MIT licence -> fine with our GPL-2.0-or-later; vendor sources under
  private/third_party, add licence text to release + README Credits. Download needs a pinned release from
  GPUOpen GitHub (user pre-approved downloads? NOT for this one: s38 rule = ask before downloads... user said
  "do not ask, just do it" this time -> download the official release only, record URL + hash here).
- DLSS: NVIDIA DLSS SDK (github NVIDIA/DLSS) or Streamline. Licence = NVIDIA RTX SDK licence (proprietary,
  allows shipping nvngx_dlss.dll with an app, requires attribution/notice, forbids reverse engineering of it).
  GPL-2.0 issue: our code is GPL; linking a proprietary non-system library is a GPL grey zone. Safe pattern:
  load nvngx_dlss.dll at RUNTIME only if present (LoadLibrary, optional), DO NOT bundle it in our release;
  user drops the DLL in (or it is found from NVIDIA driver/another game), like other open-source projects do.
  Also add a GPL linking exception notice in README for the NVIDIA runtime if we keep any NVIDIA header.
  "DLSS 4.5" = newer DLL/presets (transformer model); the SDK API is the same, newer DLL = drop-in.
- Do not use NVIDIA/AMD logos or trademarks beyond plain names ("DLSS", "FSR" as feature names, with
  "NVIDIA DLSS is a trademark of NVIDIA" line in README).
- Re-verify all of the above from the licence files after download; write findings here.

### Order for next session
1. Read licences (download FidelityFX SDK MIT + DLSS SDK) -> record exact terms.
2. Camera matrices + depth -> camera MVs (debug view of MVs, check by screenshot while turning camera).
3. FSR 3 upscaler (MIT, can ship) first, then DLSS/DLAA runtime-optional.
4. Character MVs (phase B).

## Milestone 5, session 62 (2026-11-08 12:01 +07, scheduled run tms-recomp-s61-noon, user asleep)

### 1. Licences: read from the downloaded files (2026-11-08)
Downloads (official GitHub only, kept in private/third_party, never in the repo):
- AMD FidelityFX / "FSR SDK" v2.4.0 (tag v2.4.0, 2026-10-28), raw.githubusercontent.com/GPUOpen-LibrariesAndSDKs/FidelityFX-SDK/v2.4.0/...
  -> private/third_party/FidelityFX-SDK-2.4.0/: api/include headers, upscalers/include/ffx_upscale.h, docs/license.md,
  3rdpartynotice.md, docs/techniques/super-resolution-upscaler.md, signedbin/amd_fidelityfx_loader_vk.dll
  (sha256 38a56a01fb3565c0757d9f5c1e4e69de4b65e5f2e5769b323b200dc1f142bab9, 39184 B) and amd_fidelityfx_upscaler_vk.dll
  (sha256 4a7e895af6e0b615d40a84d59eb8c2b1054ad91cdd0c739567940270d51bdab7, 36135696 B; FSR 3.1.6 + FSR 4.1.2 inside).
  Release notes: FSR 3.1.6 upscaler "Vulkan support at feature parity with DX12".
- NVIDIA DLSS SDK v310.9.16 LICENSE.txt and NVIDIA Streamline v2.14.16 license.txt -> private/third_party/NVIDIA-licences-s61/.
  The DLSS SDK binaries/headers were NOT downloaded (not needed to decide, see below).

AMD SDK 2.4.0 licence (docs/license.md): CORRECTION of s61's memory: the DEFAULT licence of the SDK 2.x is NOT MIT. It is a
binary-only redistribution licence ("distribute copies of the Software, in binary form only", "No reverse engineering,
decompilation, or disassembly", copyright + notice + disclaimers must be reproduced in the documentation). BUT a long list
of files is "subject to the following license" = the MIT text, and that list INCLUDES: api/include/*.h (ffx_api.h,
ffx_api_types.h, ffx_api_loader.h, vk/ffx_api_vk.h), upscalers/include/ffx_upscale.h, all upscalers/fsr3 sources and
signedbin/amd_fidelityfx_loader_vk.dll + amd_fidelityfx_upscaler_vk.dll (license.md lines 37-983 list, 425-436, 649-672).
=> Shipping the two Vulkan DLLs with our GPL-2.0-or-later program is fine (MIT is GPL-compatible): put the MIT text +
"Copyright (C) Advanced Micro Devices, Inc." in THIRD_PARTY notices of the ZIP. Files NOT on the list (samples, other
kits) stay binary-only: do not copy them. No RE of the DLLs (we only call the documented API).
Trademarks: "AMD FSR" / "FidelityFX" are AMD marks: use plain text "AMD FSR 3" as a feature name, no logos.

NVIDIA RTX SDKs licence (DLSS SDK, v. March 14, 2024), the parts that matter for us:
- 4(e) "You may not use the SDK in any manner that would cause it to become subject to an open source software license"
  (examples: must be disclosed in source form / licensed for derivative works / redistributable at no charge).
- 2(c) distribution "subject to the terms at least as protective as this license"; 4(a) no reverse engineering.
- Supplement 1: DLSS only for systems with NVIDIA GPUs. Supplement 4: notify NVIDIA before a COMMERCIAL release.
- Supplement 7.1(b): "For applications that incorporate the DLSS SDK ... you must attribute the use of the applicable SDK
  and include the NVIDIA Marks on splash screens, in the about box ... and in credits", and 7.2(c): every use of the NVIDIA
  Marks must be sent to NVIDIA for written approval 2 weeks before (no answer in 10 business days = NOT approved).
- Streamline (NVIDIA's wrapper): its own source is MIT (license.txt), but the DLSS feature DLLs it loads are under the
  RTX licence above.
=> Our project is GPL-2.0-or-later and free: linking the NGX static lib (nvsdk_ngx_s.lib) or shipping nvngx_dlss.dll would
   put the SDK into a GPL, free, source-available release = conflict with 4(e) and 2(c), plus a marks-approval duty we
   cannot meet. NOT a lawyer's opinion; it is the plain text.
   Only shape with no clear conflict: our release contains NO NVIDIA file (no headers from the DLSS SDK, no .lib, no DLL);
   a DLSS path would load NVIDIA's own DLLs that the PLAYER supplies, through MIT Streamline headers. Even that leaves the
   7.1(b) marks duty unclear (whether "incorporates" covers a user-supplied DLL). DECISION for this session: build FSR 3
   (incl. "Native AA" = DLAA-like, scale 1.0); DLSS NOT built and NOT in any ZIP until the user decides with this text.

### 2. Camera motion vectors (DONE, agent-verified by numbers, commit 5bfa3a4)
- Scene camera = the 3D draws' VERTEX uniform 1 (NVN index 1 -> slot 4), 736 bytes (drawlog + NX_LOG_UBO_FULL=4, 11-08):
  floats 0-3 = target size in game pixels (1280 720), near 1, far 10000; 4-7 view dir; 8-10 camera position; 12-23 view
  3x4; 28-43 inverse view; 56-71 projection (row-major, GL style: [2][2] -1.0002, [2][3] -2.0002, [3][2] -1); 61 =
  cot(fov y / 2) (2.414 = 45 deg); 72-87 inverse projection; 88-103 VIEW-PROJECTION (row-major); 104-119 its inverse.
  Shadow maps bind the same block with their own size (1024x2048 / 1024x1024) -> picked by size == colour target.
  Check: row 3 of VP . camera position = 0. NDC: NVN +Y = top (our viewport flip), depth = (z + 1) / 2 (depth clip control).
- tools/spvgen/Motion.cs (our own): per pixel NDC from depth (jitter removed) -> M = VP_prev x inverse(VP_cur) (CPU,
  double, invert4) -> previous pixel; mv = previous - current in PIXELS (FSR scale 1, 1). Also copies depth to R32F.
- Verification rig: NX_MV_CHECK=s replaces the frame by 4 x |frame - previous frame at (pixel + s x mv)| (bilinear,
  MvCheck in Motion.cs). Region means (720p, c3 save, camera yaw with rs 20000 0; regmean.py in the s62 scratchpad,
  same as agent_scripts/regmean.py idea): s=0 buildings 90 / wall 100 / all 82; s=0.9 54 / 65 / 51; s=1 30 / 32 / 39;
  s=1.1 54 / 68 / 51 -> 1.0 is the clear minimum (right scale and sign). Pitch (rs 0 -32767): s=0 47, s=1 29, s=1.1 29.
  Residual at s=1 = animated textures (waterfall), moving Itsuki, sub-pixel texture detail. FSR's own debug view:
  NX_FSR3_DEBUG=1 (FFX_UPSCALE_ENABLE_DEBUG_VISUALIZATION).

### 3. FSR 3 (DONE as native AA = "like DLAA", agent-verified, NOT user-tested; commits 5bfa3a4, 6336af2)
- Setting: Anti-aliasing (fx_fxaa) 3 = "FSR 3" in F1, PC page row "Anti-aliasing", launcher ("AMD FSR 3 · temporal").
  Runs at the game's FXAA draw (after tone mapping, under the UI) like SMAA: vk_replay.cpp fsr3_in_place -> MV pass ->
  vk_fsr3.cpp fsr3_dispatch (FidelityFX API: ffxCreateContext upscale, Vulkan backend, render size = output size,
  no HDR flag: input is the tone-mapped B10G11R11 frame, depth = R32F copy, state UNORDERED_ACCESS = GENERAL) -> output
  copied back into the FXAA input, FXAA a pass-through. Provider picked by the DLL on the user's NVIDIA: "3.1.6".
- Jitter: FSR's sequence (ffxQuery jitter phase count / offset, 8 phases at 1:1), applied as a viewport offset to draws
  that bind the scene camera block (not post / UI / shadows); verified non-zero in the log (-0.250 0.167, 0.250 -0.389).
- History reset: first frame, a missed frame, or camera moved > 200 units in one frame.
- Fallback: no DLL / context failure -> SMAA, log "fsr3: ... SMAA instead" (tested by renaming the loader DLL).
- Cost: 4K uncapped field (fieldperf.sh) SMAA 1332 vs FSR 3 1335 presents / 10 s: both at the display cap, no loss seen.
- Look (4K crops, shots q2 = SMAA, q3 = FSR 3): still scene equal or smoother edges; Itsuki's sword while walking is less
  smoothed than the background (no per-object vectors: FSR drops history there) but NO ghost trails seen.
- Debug env: NX_FSR3_DEBUG=1, NX_FSR3_NOJITTER=1, NX_FSR3_SHARPNESS=0..1 (RCAS in FSR, default 0), NX_MV_CHECK=s.
- Release: package.ps1 ships amd_fidelityfx_loader_vk.dll + amd_fidelityfx_upscaler_vk.dll (CMake copies them next to
  tms.exe from private/third_party/FidelityFX-SDK-2.4.0/Kits/FidelityFX/signedbin) + THIRD_PARTY.txt entry from
  private/third_party/FidelityFX-SDK-2.4.0/LICENSE-shipped-MIT.txt (the MIT text + which files it covers). README credits
  with the AMD trademark line. Nothing from NVIDIA anywhere.

### Not done (next)
- FSR 3 UPSCALING (render below output, Quality/Balanced/Performance): needs the 3D scene targets at a lower scale than
  the post/UI targets (today every render target uses one rt_scale). Plan: per-texture scale for the targets the scene
  camera draws into (colour + depth + the passes before the FXAA draw), viewport/scissor from the target's scale, FXAA
  input at render size -> FSR output at display size. Big; measure which targets the pre-FXAA passes touch first.
- Character / object motion vectors (phase B): per-draw previous bone palette (vertex uniform 6 = slot 9, 12288 B) + model
  block (uniform 5 = slot 8) kept per draw identity, a second vertex variant writing previous clip position. Only needed
  if the user sees aliasing / ghosting on moving characters with FSR 3.
- DLSS / DLAA: NOT built (licence, section 1). Needs the user's decision.

### Checks + end state (s62)
- Crash batch: uncap_batch.sh 80 420 NX_WALK_SPEED=2 NX_FX_FXAA=3 (4K, battles uncapped, FSR 3 on): 4 x 420 s, 0 crashes,
  battle cues 45 / 69 / 49 / 19, FSR 3 context + frames logged in all four. pipelines.bin 32822405 B before and after;
  user save/ md5 unchanged (all tests used testsave copies).
- User checks: F1 -> Anti-aliasing -> FSR 3 (or launcher "AMD FSR 3 · temporal"): edges in the field / battle / cutscenes,
  shimmer on the city and fences, any smearing or ghosting on moving characters and effects, fps at 4K.
- ZIP: DesktopTMSRecomp-20261108.zip 115.8 MB (+30 MB = the AMD upscaler DLL).
- Decision for the user: DLSS / DLAA (licence section 1). FSR 3 upscaling modes and character motion vectors are next.

## Milestone 5, session 63 (2026-11-08 17:01 +07, scheduled run tms-recomp-s61-evening, user asleep; commit 8d09732 + later)

### FSR 3 upscaling (DONE, agent-verified, NOT user-tested)
Setting fsr3_quality (ini, launcher Graphics row "FSR 3 upscaling", F1 row): 0 Native (default, s62 behaviour), 1 Quality 1/1.5, 2 Balanced
1/1.7, 3 Performance 1/2, 4 Ultra Performance 1/3. Only with Anti-aliasing = FSR 3. Read at start (restart). Scene scale = floor(res_scale / ratio x 80) / 80,
min 1.0 (k / 80 keeps 1280x720 x scale whole pixels); 4K: 2560x1440 / 2256x1269 / 1920x1080 / 1280x720. At 720p there is nothing to upscale: off.
- Measured frame graph (NX_LOG_IMAGES + drawlog 11-08, Daitama field 4K): scene colour bc502b10 (B10G11R11, flags 0xc) + depth bc502450 -> tone map into
  bc502910 -> FXAA draw bc502910 -> bc502b10 (in the Observatory the two swap roles) -> bloom small targets (native 640x360) -> UI on the same
  texture -> copy to the display texture (flags 0xd). So ONE NVN texture is scene before the FXAA draw and full-size UI after it.
- Solution (vk.cpp "FSR 3 upscaling", struct Twin): every screen-size render target (flags & 8, not display flag 1, 2D 1280x720, 1 level) gets a lo twin image;
  vk::scene_phase(lo) swaps t->host of all twin textures. Phase: frame starts lo when the previous frame had a 3D scene camera (upscale_frame_end, vk_replay.cpp,
  after g_present_no++), FSR's dispatch at the FXAA draw copies its output into the full-size FXAA input and switches everything to full size
  (fsr3_in_place). Menus / UI-only frames never go lo. First 3D frame after a menu is one full-size SMAA frame (also tests the DLLs, g_up_ok); a menu right
  after a scene is one low frame at most. Switching Anti-aliasing away from FSR 3 in F1 returns to full size at once (twins stay, ~+135-250 MB VRAM at 4K).
- Image::scale is float now (viewport, scissor floor/ceil, copy regions lround, w/h lround, support buffer already float). twin_register in image_of, freed
  through g_dead on backend_texture_finalized.
- After the FXAA draw the game binds depth but with depth test off (ds 0x80 in field and battle, drawlog 11-08), so full-size depth is left unwritten on purpose.
  If a scene ever shows 3D drawn over the UI wrongly after FXAA, this is the first place to look (would need depth lo -> hi nearest blit at the phase switch).
- MSAA does not apply on lo phase passes (ms check dimg->scale == res_scale). Not a crash: MSAA + FSR upscaling simply renders the scene 1x.

Verified 11-08:
- Field at 4K Quality vs native FSR: side-by-side crops equal except tiny stair-stepping on the sword (idle animation, no per-object vectors); UI full size (crops).
- Camp menu at 4K Performance + battle field shots (shots/r1_s, r2_s, b1b_s, c1_s): correct, UI sharp, scene upscaled.
- Crash batch uncap_batch.sh 100 420 NX_WALK_SPEED=2 NX_FX_FXAA=3 NX_FSR3_QUALITY=3: 4 x 420 s, 0 crashes, battle cues 23 / 141 / 37 / 54, FSR 3 frames logged.
- Default settings regression: uncap_batch.sh 200 180 NX_WALK_SPEED=2: 4 x 180 s, 0 crashes.
- Performance, GPU-limited 8K field (fieldperf.sh, NX_RES=8k, FSR 3): native 65-66 fps -> Performance 113-120 fps (render 4K of 8K). At 4K the game sits at the
  display cap so the gain cannot be seen there.
- pipelines.bin 32822405 B before and after every run; user save/ md5 unchanged (all tests used testsave copies).
- Launcher Graphics page: 6 rows, section titles removed for room, layout by screenshot.
NOT verified: cutscenes at each mode, Balanced mode by eye (Performance and Quality were), user's real play.

### Decisions and open items
- DLSS / DLAA: still NOT built (s62 licence text: GPL conflict plus NVIDIA marks approval). User must decide; nothing of NVIDIA is in the repo or ZIP.
- Character motion vectors (phase B) NOT built: waits for a user report of ghosting or shimmer on moving characters with FSR 3 (measure first).
- Next: user test of FSR 3 modes, then the OPEN LIST (session 39 + later).

## Milestone 5, session 64 (2026-11-08 evening + 2026-11-09 morning, with user, then scheduled runs tms-recomp-s64-1021 / -1521; commit e5a831d + later)

USER DECISION (2026-11-09, verbatim intent): "Finish the open list, DLSS too", do not ask, keep polishing. So the s62 "user decides" on DLSS is settled.

### DLSS / DLAA (BUILT, agent-verified, NOT user-tested)
Setting fx_fxaa 4 (F1, PC page, launcher "NVIDIA DLSS"); fsr3_quality 0 = DLAA, 1-4 = DLSS modes (same twin images as FSR 3 upscaling).
- runtime/src/vk_dlss.cpp: own code, no NVIDIA header/lib compiled in. Loads the driver's _nvngx.dll (registry NGXCore\FullPath), NVSDK_NGX_VULKAN_* by GetProcAddress, parameter object through its vtable with a layout self-check (TMS.Check). Device/instance extensions asked from NGX only when nvngx_dlss.dll is next to tms.exe: nobody else's device changes.
- nvngx_dlss.dll: NOT in repo or ZIP (package.ps1 refuses nvngx*/nvsdk_ngx*). Setup page tick / "Get DLSS" -> setup.py --dlss / --dlss-only downloads NVIDIA's signed file from github.com/NVIDIA/DLSS tag v310.9.16, size + sha256 pinned, RTX GPUs only, never fails the setup. README has a GPL additional permission for the NGX core + DLL, plus the trademark line.
- Fallback chain: DLSS -> FSR 3 -> SMAA. Without the DLL the game logs "dlss: nvngx_dlss.dll is not next to tms.exe" and runs FSR 3.
- Verified: 4K field picture correct, UI sharp, Performance mode, fallback without the DLL, crash batch 4 x 420 s DLAA 0 crashes (m1/m2 stayed capped at 60: their replays never logged "replay finished", waiters hung; uncap_batch.sh now bounded at 150 s).
- Moving character check 11-09 (agent_scripts/dlwalk.sh, shots/wcmp.png = SMAA, FSR 3, DLAA, DLSS Performance while walking, 1:1 crops): DLAA and DLSS Performance CLEAN, no ghost or speckle on Itsuki. FSR 3 native shows white speckle along character edges (camera-only vectors are wrong on a character the camera follows).
- Rig: agent_scripts/dl.sh, dlwalk.sh. Save checks: save/ mtimes unchanged by test runs, pipelines.bin 32822405 B before and after. The old rule "md5 of save/* equals save_bak_1023b" is stale: the user has played since (save_3, save_20 newer).

### s64 state at 2026-11-09 ~09:40 (this session stops before 10:15 so the 10:21 scheduled run has the tree alone)
- DLSS verified 11-09: Performance 4 x 300 s 0 crashes (only m4 reached a battle: the then-new 150 s bound in uncap_batch.sh switched m1-m3 to uncapped during their replay and desynced them; bound now = batch length and only after "replay finished"). Field at DLSS Quality by eye (shots/bd_s.png) correct. Launcher Setup page row by screenshot (shots/ls_setup.png) correct.
- NOT verified by eye: DLSS in battle and cutscenes (tobattle.sh did not reach a battle: no "opening chance" in 60 walk steps at NX_FPS=60).
- FSR 3 white speckle on followed characters: main-scene draws have NO stencil (agent_scripts/sten.sh: field frame, main depth ds 41/43/31/80 with ref 0; stencil refs 2/8/14 only on the shadow maps). So no character mask exists yet.

### s64 update 09:50: more measured
- DLSS Quality in a battle by eye (agent_scripts/dlbat.sh, shots/db_s.png): 3D, crowd and UI correct. Cutscenes still not seen by eye.
- 4-instance DLSS batches STARVE the GPU: m1 at 1.3 frames/s, present blocked 1.2 s, about 3 GB VRAM per instance (uncap_batch 400 420: m1-m3 never finished the replay, 0 errors). Test artifact, not a game bug. Use agent_scripts/dlsolo.sh (one instance + mash; single instance reaches the battle at ~190 s).
- Main scene depth = fmt 126 D32_SFLOAT, no stencil aspect. So the stencil-mask plan for the FSR 3 speckle needs a depth format change (all FSR pipelines): not worth it; lower priority (DLSS clean, FSR 3 row text already says moving characters are smoothed less).

- Solo soak 09:55 (dlsolo.sh ds1 501 330, DLSS Quality, mash, uncapped after the replay): 55 battle cues, 0 crashes, 93.9 frames/s at the end, pipelines.bin 32822405 B unchanged. Release ZIP Desktop\TMSRecomp-20261109.zip 115.8 MB (09:40, no code change after it; no NVIDIA file inside, package.ps1 refuses them).

### Next, in order (scheduled runs)
1. DLSS by eye in a cutscene (save-3 boss cutscene replay or base60 story beats).
2. Shader misses (s39 item c): 4 integer-attribute variants + 1 float key: only if attribute types can be recorded in recipes cheaply; s43 proposal was to leave them.
3. Big-area perf with NX_PROFILE on the b20 Observatory save; MV pass and DLSS cost per frame.
4. FSR 3 character speckle only if cheap: mask draws need another route than stencil (depth has none).
Waiting on the user: FSR 3 / DLSS by eye in real play, ZIP flow, clean VM test, GitHub (not before the full game test).


## Milestone 5, session 65 (2026-11-09 10:21 +07, scheduled run tms-recomp-s64-1021, user asleep; commits d9fe8cf, FSR/NGX start commit, 75da38b + notes)

Everything below is agent-verified only. Nothing here is user-tested.

### Done
- DLSS in a cutscene by eye (s64 next item 1): boss-door cutscene, 4K, DLSS Quality vs SMAA, 1:1 crop (private/tms/shots/dc_cmp.png): same picture. Rig agent_scripts/dlcut.sh. Banding seen on contact sheets is the downscaled sheet, not the render.
- MSAA is now off while FSR 3 / DLSS is active (vk_replay.cpp ms_wanted, g_temporal_bad). Reason: the user's ini has msaa = 8; upscaling modes already skipped it by the scale check, but native DLAA / FSR 3 ran 8x under the temporal pass, and the 8x twins were allocated at the title and never freed. DLAA cutscene run: 0 twins, 2085 MB used (was 3281 MB at DLSS Quality with twins, 3010 MB SMAA + MSAA). If FSR 3 / DLSS cannot start, MSAA comes back. SMAA + MSAA unchanged (4 twins, verified). F1 and PC page help texts say so.
- NGX / FidelityFX start at the first FXAA draw (title screen) at native size too. Was a 2.9 s freeze on the first in-game frame with DLAA (spike frame 2859 ms at 18.2 s -> NGX up at 4.1 s, largest spike after it 148 ms).
- Resolution matrix, DLSS, field by eye (shots/mx_sheet.png), 0 errors: 720p q0/q2, 1080p q0/q1, 1440p q2/q4, 4k q4, 8k q3. NX_RES=1080p means an internal 2560x1440 scene target. 720p modes above DLAA fall back to DLAA (lo >= hi); 1440p Ultra Performance clamps at 1280x720 = Performance.
- Live AA switching with msaa = 8 in the ini: DLSS, FSR 3, SMAA, DLSS, FXAA, 0 errors, pictures correct (agent_scripts/aaswitch.sh, new debug control `aa N`, shots/as1_sheet.png).
- Soak, DLAA, one instance, msaa 8 ini, uncapped after the replay: ds2 seed 601 (battle won by 212 s, then field), ds3 seed 501 (47 cues, 20 skill panels), both 0 errors. Saves, build/settings.ini md5 and pipelines.bin (32822405 B) unchanged after all runs.

### Measured, not changed
- Big-area perf (s64 item 3): b20 Daitama field uncapped, SMAA no MSAA 115 fps, DLSS Quality 115, DLAA 83-85. 720p = 117 fps, so this area is CPU-bound and DLSS modes do not raise fps here. Profile flat (heap, SRW locks, vector<nvn::Cmd> ~25%). s58 inline-payload try gained nothing. Remaining lever = CallCommands without deep copies (OP_CALL + clear look-ahead across lists): core replay risk for at most ~15%, NOT attempted.

### Left on purpose
- Shader misses (s64 item 2): 0 translations in this session's runs, s43/s58 call them harmless. Not touched.
- FSR 3 white speckle on followed characters (s64 item 4): needs a character mask; main depth has no stencil. Not touched. DLAA / DLSS do not show it.

### Rig notes
- agent_scripts/run.ps1: empty <rec> now uses analysis/none.rec (missing file on purpose), so live-control runs also count as replays: no real pad, no settings.ini writes. Before this, rigs passing "" (dl.sh, fieldperf.sh, ribbon.sh, ...) ran without that guard.
- dlsolo.sh no longer waits for mash.py (run took twice as long and left strays). 8 stray `analysis/mash.py` processes (m1.log, m2.log, m3.log) from s64 batches are still running: this run did not touch them (task rule: only tms.exe processes). They poll those logs once a second; do not reuse tags m1-m3 until they are gone (uncap_batch.sh uses m1-m4), or close them.
- Battle cue counts vary by mash seed: check where the battle ended before reading a low count as a failure.

### Waiting on the user
FSR 3 / DLSS by eye in real play, ZIP flow, clean VM test, GitHub (not before the full game test).


## Milestone 5, session 66 (2026-11-09 15:21 +07, scheduled run tms-recomp-s64-1521, user asleep; commits ea8ef5d, e159dfd + notes)

Everything below is agent-verified only. Nothing here is user-tested.

### Done
- FSR 3 / DLSS history reset at camera cuts (vk_replay.cpp, MV pass). The old test only reset on a frame gap or a jump over 200 units, and cuts inside a room move less: the boss-door cutscene (dlcut.sh, DLSS Quality) logged 16 cuts that moved 17-99 units and turned 25-170 degrees, all of which kept stale history. New test: also reset when the view direction (VP row 3) turns more than 15 degrees in one frame (dot < 0.966). New log line "vk: temporal history reset (frame gap, moved, view dot)", first 200 only. The picture at cuts was NOT compared by eye before / after, only the reset log.
- False-positive check: DLSS Quality battle soak (dlsolo.sh ds7 701 330, uncapped after the replay, 112.7 frames/s): 56 resets in 330 s, about 20 per 30 s during the battle and 1-3 per 30 s outside it. Assumed real battle camera cuts (15 degrees per frame at 112 fps is not a pan); not checked shot by shot. 54 cues, 0 crashes, saves / build/settings.ini md5 unchanged, pipelines.bin only grew (32822405 -> 32885370 B).
- Release flow retest from a fresh ZIP extract in scratch, environment scrubbed (only System32 + dotnet on PATH, bundled Python), folder mode on a copy of exefs + romfs: setup done in 230 s (first attempt without dotnet on PATH stopped with the expected .NET message at step 6), game boots to the title from the copy, 0 shader translations, game.dll built.
- REAL BUG FOUND: tms.exe, launcher.exe, game.dll and both AMD DLLs import msvcp140 / msvcp140_atomic_wait / vcruntime140(_1). The ZIP did not carry them, so on a PC without the VC++ redistributable even launcher.exe cannot start and cannot say why. package.ps1 now copies the 4 DLLs from the newest VC Redist folder installed (14.51) next to the exes, with a THIRD_PARTY.txt notice. Verified by the process module list: all 4 load from the app folder. NOT tested on a PC that really lacks them (no VM here; Windows Sandbox would need a system feature change, not done).
- Fresh-install default frame rate 60 (was 30 in the ini template, the launcher and the no-ini default; 30 also refuses live fps changes in F1). Verified: a new settings.ini says fps = 60. Existing inis are untouched (user's stays 240).
- pinned nvngx_dlss.dll: sha256 of the local file equals setup.py DLSS_SHA256. The download itself was not re-run.

### Not confirmed
- FSR 3 start from the ZIP layout: the 18 s run stayed before the first 3D scene, log shows no "FSR 3 frames" line. Same DLLs and code path as the dev build.

### Left on purpose (unchanged from s65)
Shader misses, FSR 3 speckle on followed characters, big-area CallCommands rewrite. Stray analysis/mash.py from s64 were not touched (task rule: only tms.exe).

### Waiting on the user
FSR 3 / DLSS by eye in real play, ZIP flow on another PC / clean VM, GitHub (not before the full game test). Before publishing: decide whether shipping the Microsoft runtime DLLs in a GPL release ZIP is fine (they are Distributable Code; alternative = link the CRT statically, game.dll would still need its import libs changed).


## Milestone 5, session 67 (2026-11-10 ~09:00 +07, user asleep after a play test; commits c0394f0 + later)

### User report 2026-11-10 (s66 build; uncapped 240, 4K, FSR 3 / DLSS tried; videos D:\OBS VIDEO\OBS\2026-11-10 08-53-01 / 08-54-07 / 08-54-38.mp4)
"Super impressed, most issues fixed." Still open: 1. DLSS / FSR upscaling quality not in the native PC settings page. 2. Glitch in the
transition after a level-up (stripe wipe into NEW SKILL). 3. Session "GOOD" text still too fast. 4. "CALL" text still too fast.
NEW FIRM RULE: portability (see "PORTABILITY RULE" at the top): must not only work on the user's machine.
Scheduled one-time runs: tms-recomp-s67-1121 (11:21 +07) and tms-recomp-s67-1621 (16:21 +07) continue this list.

### 1. Upscaling row on PC page 3 (DONE, build-verified only)
camp_settings.cpp page 3 row 9 "FSR 3 / DLSS upscaling" (overlay item fsr3_quality: Native / Quality / Balanced / Performance /
Ultra perf.; restart). NOT seen on screen yet (rig: to_camp.sh, then Settings, R x3).

### 2. Level-up stripe wipe glitch (FIXED by code, NOT reproduced)
- User video 08-53-01 frames 94-141: the stripes of the wipe after the level-up screens cover / uncover the screen on alternate
  frames (152 fps), and the screenshot shows bands shifted up / down with the level-up screen between them.
- Cause (by reading ui_sprite_smooth): the stripes are equal sprites (same texture + uv) in several rows sliding in fast; the glide
  paired each with the NEAREST equal sprite of the previous tick, which could be a stripe of another row (moved < 320 and < its width),
  so stripes glided vertically between rows.
- Fix (vk_replay.cpp ui_sprite_smooth): a pair is only taken when per axis the move is within the sprite's own width / height
  (both ticks, min 4 px); the nearest is chosen among those. Camp run with NX_UI_SMOOTH_LOG: glides still happen, 0 crashes.
- NOT verified on the wipe itself (needs a NEW SKILL after a level-up: mastery x5 battle in a later area). If the user still sees it:
  NX_UI_SMOOTH=0 (F1 UI smoothing off) is the test.
- Also seen in the video, not changed: "NEW SKILL" text doubled for 2 frames (likely the game's own trail effect), and ~0.4 s grey
  screen between the stripes and NEW SKILL (unknown if the Switch has it).

### 3. Session COMBO / GOOD (FIXED by code, NOT verified by eye)
- User video 08-54-07 frames 139-141: "1" -> "01 + small GOOD" -> full GOOD in 2 frames at 60. s59 shots (shots/st_s, 30 Hz mask) took
  4 frames. s60 put HUD part bit 2 (btlui_p1c) back to 60 Hz for the skill list: p1c also draws the combo counter -> regression.
- Fix: g_ui_part30 default has bit 2 again; part_skip keeps p1c at 60 Hz only while battle_choosing() (btl_wheel_input ran in the last
  150 ms: wheel, skill list, target pick). Session plays with no input -> 30 Hz.
- Verification failed 3 times (sess.sh WAIT=0: battles ended or no Session triggered: gd1-gd3). Next run: sess.sh until a Session
  shows, count GOOD pop frames (expect 4 at 60, as shots/st_s), and check the skill list still scrolls at 60 Hz.
- Tools added: agent_scripts/sessgood.sh (Session at 240 with NX_UI_STEP_LOG; GATES="0 1 2 3" sweeps debug control `gate30 <mask>`:
  1 = btl_ui_update, 2 = party_hud_update on 30 Hz ticks). Findings: top-left turn-order sprites (y < 100) step at 60 Hz, NOT under
  btl_ui_update / party_hud_update (gate30 3 changed nothing); the GOOD sprites never show in NX_UI_STEP_LOG.
- NX_UI_WLOG=1 logs UI-manager widget vtables; NX_UI_W30=<hex vt,...> steps those widgets on 30 Hz ticks (vtable swap to a copy whose
  update is guest "return 1" 0x201d24). Battle has no UI-manager widgets of its own. Field: 7d2308, 7d29f0, 7d2ab4, 7d2c00, 7d2378 at
  load, 7d2d8c ~6 s after the CALL ring area loads.

### 4. CALL ring (NOT fixed; one real gate bug fixed on the way)
- Ring text laps in ~0.35 s at 240 fps (user video 23 frames at 60; cr1 shots ~12 shots per right-edge pass).
- map_mgr_update 0x4a338c: +0x8d4 drives the strip scroll (F_004a9004: x = -(n % (w*20)) * 1.5) and Topic schedule keyframes
  (F_004aa354, table 0x789614, periods 1350-5400 frames); NOT the ring spin. Gating 7d2c00 / 7d2378 / 7d2d8c at 30 Hz (cr3) did not
  change the ring speed. s60's oracle (fixdt 30 equal) means the spin is game-time driven = Switch speed.
- Real bug fixed: flipbook timers +0x8dc + 8 i call 0x4a2270 (next cell + reset) when +1 reaches their limit; the hook's post-update
  rollback let that reset through on frames without a tick (cells one tick early, 2x for 2-tick cells). Now pre-decremented on
  non-tick frames. cr1 run: ring + icons draw, 0 crashes.
- Next: find the ring draw (search lifted code for the ring texture / a rotation from dt) or ask the user for Switch footage. If it
  is dt-driven, it is Switch speed and the honest answer is "same as Switch"; offer a slower option only if the user wants it.

### Other
- User log: "vk: skipped ... other" grows to 1M = Character rim off (fx_char_rim 0 skips the shell draws). Not a bug.
- User's 3rd battle (the Session clip) ran at battle speed 1x (log), so GOOD was not the speed-up.

### Portability audit (PORTABILITY RULE; code done, NOT tested on other GPUs: none here)
- Vulkan device creation asked for ~20 features unconditionally (wideLines, logicOp, pipelineStatisticsQuery, dualSrcBlend, ...): a GPU
  missing ONE failed vkCreateDevice and the game died. Now (vk.cpp) features are queried: required ones (Vulkan 1.3, dynamicRendering,
  timelineSemaphore, scalarBlockLayout, BC textures, depthClipControl, swapchain / external_memory_host / depth_clip_control extensions)
  give a clear "update the graphics driver" message naming what is missing; the rest are switched off with a log line ("vk: X not
  supported by this GPU: off"). Line width is always 1 and logic ops are unused, so those cost nothing. Without
  shaderStorageImageExtendedFormats, SMAA / FSR 3 / DLSS fall back to the game's FXAA (log line), pipeline statistics (debug) off.
- Fresh-install resolution: template / launcher default was 4k for everyone (iGPUs and 2-4 GB cards). New `res = auto` (default for new
  inis, launcher first option): integrated GPU -> 720p, discrete under 4 GB VRAM -> 1080p at most, else the screen height (1080p /
  1440p / 4k). Log "vk: res auto -> ...". Existing inis keep their value.
- Checked, fine: present mode falls back to mailbox / fifo; no -march / AVX flags (baseline x86-64 SSE2) in CMake or build_game.py;
  VC++ runtime DLLs ship app-local (s66).
- Still open for portability: a real non-NVIDIA test (AMD / Intel), a 4 GB VRAM run (NX_RES=4k + DLAA used ~3 GB here), first-run
  shader / pipeline compile stutter on a clean cache (s36 prewarm exists; measure on a clean data folder), CPU-bound big areas
  (s65: 115 fps on this PC; slower CPUs may drop below 60: CallCommands deep copies are the lever).

### s67 checks + end state (~10:20 +07)
- Crash batch uncap_batch.sh 90 240 NX_WALK_SPEED=2 (before the Vulkan / res changes): 4 x 240 s, 0 crashes, BUT no instance reached a
  battle in 240 s (battle cues 0): battle coverage of this build is weak. Next run: uncap_batch.sh with 420 s.
- res auto run (to_camp.sh ra1 NX_RES=auto): "res auto -> 4k (screen height 2160, discrete GPU, 15995 MB VRAM)", no feature dropped,
  camp reached. pipelines.bin 32885370 B unchanged; user save/ not used (testsave copies).
- Release ZIP Desktop\TMSRecomp-20261110.zip 116.2 MB.
- NOT verified: PC page 3 upscaling row on screen, GOOD pop pace, level-up wipe, skill list still 60 Hz.
- Next (scheduled runs): (1) verify the 3 items above (sess.sh until a Session shows; Settings screen via camp System); (2) longer
  crash batch; (3) CALL ring: find the spin's driver; (4) portability items still open (list above).


## Milestone 5, session 68 (2026-11-10 11:21-~14:00 +07, scheduled run tms-recomp-s67-1121, user asleep; commits d9c8db4, 4a49d3a, ed5f801, f0c1090 + notes)

### s67 items checked
- PC page 3 "FSR 3 / DLSS upscaling" row: SEEN on screen (shots/s68_pc3_upscale_row.png, rig: to_camp.sh, up + a = System,
  up + a = Settings, R x3). Not toggled (would write settings.ini).
- Test rigs field.sh / to_camp.sh: their `tail -20 log | grep [pos]` never matched because the game log carried CRI's per-frame
  "soundvoice_parameter_update_on_changed" trace (60+ lines/s): that is why s67's Session runs never reached a battle. Game log now
  drops that line (NX_GAME_LOG=2 keeps it; also less disk writing for players) and the rigs grep the whole log.
- New rigs: sessloop.sh <prefix> <tries> (repeats a Session rig until a Session cue shows; SCRIPT=, EXTRA= env, PRE= / POST= control
  lines before / after the attack in sess.sh), sessrt.sh (real-time fps, no fixdt), sesswatch.sh (watch a HUD part's memory),
  sesspop.sh + popdiff.py (heap dumps around the GOOD pop), ringsnap.sh + framecount2.py (ORDER= dump order), ringsig.py (CALL text
  green-pixel signal per shot), sh1.sh (shot -> png).
- IMPORTANT rig fact: under `fixdt N` the UI clocks (g_tick60 / g_tick_ui30) follow the REAL frame time (g_base_dt), the game runs
  slow motion. So "steps per shot" under fixdt measures UI pace against real fps, not game time. For UI pacing use real fps + logs.

### 4. CALL ring (FIXED, measured)
- callring.sh with fixdt: at 240 the "CALL" text pass took the SAME frames as at true NX_FPS=30 (30 frames; identical per-frame
  green-pixel sequence) = 8x the Switch. s60's oracle compared fixdt 30 at fps 240 (gates on), not true 30 fps.
- Memory snapshots (ringsnap.sh, framecount2.py) + `watch`: counter written by 0x4accf0 (names.txt notify_anim_tick), called once
  per frame from map_mgr_update via 0x4acdc4; fields +8, +0xc, +0x10, +0x14 (120..238 loop = ring text), +0x20, +0x24, +0x2c, +0x374.
- Fix: hle_sys.cpp notify_anim_tick steps only on 30 Hz ticks. Measured: 8 frames per step at 240 (cr10), same sequence as 30 fps.
- Other per-frame counters under map_mgr_update seen, NOT changed (unknown use): bc9c2f5c by 0x4d7408 (via 0x4b734c / 0x4b8f60),
  bcc9c4d0 by 0x4cced8 (countdowns ~1/frame). If something in the field still runs fast at high fps, look there first.

### 3. Session COMBO / GOOD (measured; one fix)
- The pop is HUD part p3c (btlui_p3c 0x2ea1d8, object btl_ui +0x3c): state +4 = 1 while it runs, step +8 0..15 (+1 per update),
  draw 0x2ea218 lerps the GOOD scale 1.5 -> 1.0 over steps 0..3. NOT p1c (uifreeze 3 changed nothing; s67's guess was wrong).
  Found by: task30 on btl_ui draw 0x2e9664 (GOOD flickers), then uidraw30 bisection over the 19 part draws (parts 9/10), then
  `watch` on part +0x3c +8.
- Real-time measurement (sessrt.sh, NX_DEBUG_BATTLE "battle: GOOD pop p3c ..." lines): steps 33 ms apart = Switch, 16 steps in
  0.48 s (Switch 0.53 s). BUT the Session code sets step 1 itself and the shared 30 Hz tick came 0-33 ms later (8 ms seen), so the
  GOOD reached full size up to a Switch frame early.
- Fix: btlui_p3c hook steps on its own 1/30 s clock from the moment the pop starts (gu5: first step +43 ms, then 33 ms, 0.51 s).
- If the user still finds it fast: the timing now equals the Switch's 30 fps frames; only Switch footage could show otherwise.
  The "01" / COMBO number may belong to part 9 (+0x38, draw 0x2ea068): not measured.
- New debug: btl_ui_draw hook (0x2e9664 reimplemented: the same 19 part draws in order) with control `uidraw30 <mask>` (bit i =
  draw i on 30 Hz ticks only, order in k_btl_draws); `task30 <update fn>` / NX_TASK30 (scheduler tasks on 30 Hz ticks, vtable swap).

### 2. Level-up stripe wipe: not reproduced (needs a NEW SKILL after a level-up). s67 code fix stands; user check.

### Portability (PORTABILITY RULE)
- Low VRAM: vk::alloc ended the game when a 256 MB device-local block failed. Now: retry with the exact size, then any other memory
  type the resource allows (system RAM; slower but running), log "vk: video memory full ...". NX_VRAM_LIMIT_MB=<n> simulates a full
  GPU: 768 MB at 4K reached camp and rendered correctly (shots/s68_vram768_camp.png).
- AMD: D24_UNORM_S8_UINT is not supported by AMD's Windows driver (NVIDIA / Intel have it): the depth image failed at the first 3D
  frame. vk_format now checks D24S8 / S8 support and uses D32_SFLOAT_S8_UINT. NX_NO_D24=1 forces it: field + battle correct
  (shots/s68_nod24_battle.png).
- 3-component 8/16-bit vertex formats: support checked, 4-component fallback (NX_NO_RGB_VERTEX=1 test; field / battle use none).
- Prewarm: seed recipes from another GPU now get the same depth / vertex conversions (NVIDIA recipes on AMD would have built
  pipelines with D24S8). Forced-fallback run: 1981 prewarmed, 0 failures.
- Checked: ASTC formats unmapped-only (never created on desktop), present-mode fallbacks, no AVX flags (s67).
- Still open: a real AMD / Intel run; log noise "vk: skipped ... / vk: N draws" ~8 lines/s (harmless, could be rarer);
  CPU-bound big areas on slow CPUs.

### Checks + end state
- Crash batch uncap_batch.sh 91 420 (after the log/VRAM change): 4 x 420 s uncapped 4K, 0 crashes, battle cues 2/56/150/128.
- Final crash batch uncap_batch.sh 96 420 (final build f0c1090): 4 x 420 s uncapped 4K, 0 crashes, battle cues 2/43/79/151.
- Tests used testsave copies (s20, c3); user save/ not used; settings.ini not written (replay mode); pipelines.bin 32.89 -> 33.65 MB
  (grew: D32 prewarm variants).
- Release ZIP Desktop\TMSRecomp-20261110.zip 116.2 MB (13:44).
- Next (scheduled 16:21 run): level-up wipe (needs NEW SKILL), "01"/COMBO number part 9 timing, map_mgr countdowns 0x4d7408 / 0x4cced8, log noise, OPEN LIST (s39).

## Milestone 5, session 69 (2026-11-10 16:21-~17:15 +07, scheduled run tms-recomp-s67-1621, user asleep; commits 8e44aec, 1912031 + notes)

State of the 4 user items (report 11-10): 1 upscaling row DONE (s67, seen s68); 4 CALL ring DONE (s68, measured); 3 GOOD DONE (s68) and
the COMBO number below (s69); 2 level-up wipe: s67 code fix, still not reproduced (needs a NEW SKILL after a level-up) -> user check.

### Session COMBO number "01" (FIXED, measured)
- HUD part 9 (btl_ui +0x38, update 0x2ea044 / widget update 0x2eb924, draw 0x2ea068) is the COMBO counter, NOT the command wheel:
  0x2ea0ac adds a combo (+4 count), 0x2eb7a0 writes the ones / tens digits (layout ids 0x1ad27611 / 12) and restarts their pop.
  names.txt called it the command wheel (early RE), so s57 left bit 9 out of g_ui_part30 -> the "01" pop ran every frame.
- Fix (hle_sys.cpp btlui_p38): own 1/30 s clock, phase restarted when the combo count (widget +8 -> +0x1c -> +0x10) changes (like p3c);
  every frame while battle_choosing() (in case the wheel shares it). g_ui_part30 default 0x1ffff; uifreeze 10 still stops it.
- Measured (sessrt.sh via sessloop, cb1, NX_DEBUG_BATTLE "battle: COMBO p38" lines): digit slide +0x24 = float 30 -> 22.5 -> 15 -> 7.5
  -> 0 in 4 steps, ~33 ms apart (Switch pace). shots/cb1_combo.png: "01" pops in over ~4 steps, then GOOD; draws correctly.

### Log noise (portability: disk writes, readable logs)
- CRI per-sound housekeeping trace (~28 #CRIATOM lines per sound: ExPlayer_Create / AttachFader / SoundVoice_Allocate / ...) dropped from
  the game log (hle_sys.cpp k_noise list); ExPlaybackId (Cue:) lines, file / ACB loads, Pause / Stop and anything else stay;
  NX_GAME_LOG=2 keeps everything. vk draw stats ("vk: skipped ..." + "vk: N draws") once a minute (were every 20000 draws, ~7 pairs/s).
- Result: 500 s batch logs ~2000 lines (s68: ~24000).

### CPU (portability: slower CPUs in big areas)
- Profile b20 Daitama 720p uncapped (fieldperf.sh fp69): heap alloc / free + SRW locks + vector<nvn::Cmd> copies ~25%. Cause: every
  Cmd's blob was a std::vector, and CallCommands deep-copies whole recorded lists into the calling buffer each frame.
- Fix (nvn_hle.h Blob): copies share the bytes (shared_ptr), a write copies first if shared (writes only happen while recording);
  EndRecording reserves the buffer's last length for the next recording. fp69 120 fps -> fp69b 131 fps (+9%).
- Tried + REVERTED: per-thread cache in nvn::pool_of (5% in the profile): fp69c same fps.
- Still in the profile: "vkGetInstanceProcAddr" ~11% = unsymbolised Vulkan loader / driver time on the game thread (nvn::begin,
  make_image), NtGetWriteWatch 3.5%, guest-side SwitchToThread polling (svc SleepThread < 1 ms, by design). Next lever is still OP_CALL
  instead of copying (s64 note), not attempted.

### Checks + end state
- Crash batch uncap_batch.sh 97 420 (final build 1912031): 4 x 420 s uncapped 4K, 0 crashes, battle cues 56 / 0 / 71 / 0 (the 0s:
  replay finished, seed never met a battle; logs end normally at ~496 s).
- testsave copies only; user save/ untouched; build/settings.ini unchanged (08:51); pipelines.bin 33651233 B unchanged.
- Not done: level-up wipe repro, map_mgr countdowns 0x4d7408 / 0x4cced8 (no symptom known), a real AMD / Intel run (no hardware).
- Next: user play test of the s67-s69 builds (GOOD + COMBO pace, CALL ring, level-up wipe, PC page upscaling row, fps in big areas);
  OPEN LIST (s39) items left need the user's saves / pictures (face shadow, Tsubasa glitch).

## Milestone 5, session 69 part 2 (2026-11-10 evening, with user)

User: "the GOOD and CALL text, I thought I told you to make it 60 Hz not 30 Hz." + "Tsubasa face shadow is already good" (OPEN LIST
s39 item 3 CONFIRMED fixed by the user).
- The UI rule (s58, firm): UI steps on 60 Hz ticks (the UI clock: g_tick60; fps 30 or ui_speed 30 -> 30 Hz); above 60 smoother,
  never faster. The 11-10 "too fast" reports were per-frame stepping at 240, NOT a request for Switch 30 Hz pace. s67-s69 wrongly put
  GOOD (p3c), COMBO number (p38), p1c (Session) and the CALL ring (notify_anim_tick) on 30 Hz.
- Fix: g_ui_part30 default 0x1ffff minus bits 2, 9, 10 (those parts step with btl_ui_update's UI-clock gate); p3c / p38 own 1/30 s
  clocks removed (plain BTL_UI_PART); notify_anim_tick on the UI clock. Other HUD parts stay 30 Hz (s59, USER 11-06 report).
- Measured (sessrt g60_2, 240 fps target): GOOD steps 1..15 in 0.21 s (~15 ms each = 60 Hz pace). CALL ring: build only, not measured.

## Milestone 5, session 70 (2026-11-13 06:40-, with user; user report on the s69 build, 240 fps cap, 4K, 160 Hz G-SYNC display)

User report (videos D:\OBS VIDEO\OBS\2026-11-13 06-02-37 .. 06-36-59.mp4, run log nx.log 06:01-06:38, a new game from the start;
saves in save/ = slots 1-5 + 20 of that run, copied to save_bak_1113 (md5.txt) and testsave/u13; title "a" opens Load at slot 5,
up = slot 4 (end of prologue, next event = Chapter 1 card m1016_01), up up = slot 3 (Gojuin boss door, Daitama Upper Lv)):
1. Prologue title card "Reincarnation" too fast, fades out fast. 6. Same for "Chapter 1 A Star is Born".
2. Dialogue text far slower than the original (YouTube). 3. Phone ringtone (Topic urgent call, prologue) far too fast.
4. FPS drops hard in the prologue stage scene (Gojuin, crowd). 5. Attacks / skills not smooth ("like a camera shutter").
7. Office Records screen (above Awards): UI effects (green bubbles column) sped up. 8. Carnage Unity menus: UI effects sped up.
9. Gojuin boss: fades to white too early, should wait for the death animation (save 3).
User's words on pace: "60 Hz speed and smoother when fps is higher, not sped up" = the ORIGINAL speed, smooth. For the text the
user compared with YouTube (Switch) footage. Read together with s58 / s69: "60 Hz" means correct speed, never faster.

### 2. Dialogue text 4x slow at 240 (FIXED, measured)
- Message window = UI-manager widget (vtable 0x7d2d44, update 0x25a510; Lua AddMessageWindow 0x459934 etc. -> 0x246f64(0) finds it).
  It types by a timer +0x128 += dt literal 0x25ae8c (also 0x259d9c in 0x259a88, 0x25b5f4). The UI manager is gated to 60 Hz ticks
  (s22), but the dt literals hold the frame step (1/240): per tick 1/240 s instead of 1/60 -> 4x slow (user video: 7.7 chars/s).
- Fix (hle_sys.cpp UiDt): while a gated UI update runs (ui_manager_update, camp_update, camp_wipe_update, save/load screens, open
  Topic map_mgr_update, GATED_TASK post-battle screens) the dt literals hold the real time since that update's last run (UI time,
  g_ui_time += g_base_dt: 1x in fast battles), then the frame step again. Not on btl_ui_update / party_hud_update (no dt literal
  in that code; battle literals 0x2e101c / 0x2e18e0 are actor animation code). NX_UI_DT_LOG=1 logs the values.
- Measured (textshots.sh t240 / t30, slot 4 path, event m1016_02 "Welp, here we are."): 240 and true fps 30 both ~30 chars/s.

### 1 + 6. Chapter title card 2x fast (FIXED, measured)
- Card = Lua UI.OpenIntermission (0x45d574) -> widget kind 0xc, vtable 0x7d29b8, update 0x2433f4: counts frames, +0x3c to 120 then
  closes itself (state 3 -> 4). On 60 Hz UI ticks 120 frames = 2 s; Switch 4 s. TimingWaitIntermission = WaitForTimer(5) then
  CloseIntermission (UIMessage.lua).
- Fix: default g_w30_vts = {0x7d29b8} (the s67 30 Hz widget mechanism: vtable swapped to a "return 1" copy on non-30 Hz ticks;
  g_ui30_ms set -> sprites glide over the 30 Hz steps). Log "ui: 30 Hz widget ... shown".
- Measured (cardshots.sh c240 / c30, shots 0.25 s apart, m1016_01 Chapter 1 card): text gone after ~3.25 s at 240, ~3.5 s at fps 30
  (one shot of jitter); the user's video (old build) 2.3 s.

### 3. Ringtone 8x fast (FIXED, measured)
- TopicUrgentOn (Lua 0x43e608 -> 0x4ab13c) arms the urgent call; map_mgr_update 0x4a338c: +0x8b8 counts updates to 60, then
  restarts the ring cue (sound 0x11, tp_emergencycall) and +0x8c8 = 30 stops it 30 updates later. Topic closed = map_mgr_update every
  frame -> user log: cue every 250 ms at 240.
- Fix: both counters step on 30 Hz ticks in the map_mgr_update hook (+0x8b8 pre-decremented, +0x8c8 pre-incremented on non-tick
  frames, undone if the game did not count). Switch: ring every 2 s, 1 s long.
- Measured (ringtest.sh r240, NX_RING_TEST=1 forces the urgent state in the field): cues 2.000 s apart at 240. (+0x1e0 900-frame
  cooldown and +0x1b8 / +0x1bc countdowns are also per frame when closed: NOT changed, no symptom known; look there if Topic timing
  is reported.)

### 5. Attack "camera shutter" judder (FIXED by pacing, measured)
- NOT the animation: slow motion (fps 60 + fixdt 240, mv240) shows character and camera moving every frame; only the crowd flipbook
  steps on Switch frames (s56 design). The dash ghosting is the game's own blur (Lua PostEffectFBBlurStart, shader
  post_blur_feedback, 8 samples; the same discrete copies at fps 30 in the a30 shots).
- Real cause: presents were capped at ~152/s (exactly 6.6 ms apart; also with minimized test windows; matches NVIDIA's G-SYNC /
  low-latency limit refresh - refresh^2/3600 for 160 Hz) while the game made 240 frames/s: present_thread shows the newest staged
  frame, so shown frames advanced 4.2 or 8.3 ms of game time in turn = judder on fast motion. User log: "frames: 240/s",
  "present: 1521 in 10 s".
- Fix (vk.cpp vk_wait_present_taken, ui.cpp pace_variable): fps 0 / N > 60 wait (at most 2 frame times of the cap, 33 ms uncapped,
  not under fixdt) until present_thread has taken the previous frame. Measured on the title screen: fps 240 and fps 0 -> frames
  152.0/s = presents 152/s, gaps 6.6 ms. NX_PRESENT_BACKPRESSURE=0 = old behaviour. Where presents never block nothing changes.
- The user's FPS overlay already showed ~150 (presents), so the counter does not drop.

### 9. Gojuin boss white fade (NOT fixed; see the end of this section for the rig result)
- Death cut = Battle/Dead/em200/d000/dead.lua (cutStartTemplate): sound bpro_dead_gojyuin frame 0, effect BTL_EFT_BASS_002_ST10A at
  60 Hz frame 90, ST10B at 346, function at 500 = cutActorFadeOutB(actor, 120/60 s) (ParamEdit2 alpha tween += info.delta), all via
  cutDelay* -> cutCreateCoroutine (0x5bd418, same script manager) + WaitForTimer(info.delta).
- User log: bpro_dead_gojyuin -> BTL_WIN 10.9 s with battle speed 1x: the cut's total length matches the script, so the early
  white is something inside it (effect ST10B? the actor fade?). btl_finish_cut.lua FinishCut3 also fades to WHITE after 55/60 s.
- Battle action / entry cue timings are equal at 240 and fps 30 (a240 / a30 logs).
- Rigs: agent_scripts/bossfight.sh <tag> <fps> (save 3 copy, enter the door, A through the intro, X = auto-battle; the intro needs
  more A presses than the script gives) + deadwatch.sh <tag> (130 shots 0.1 s apart from Cue:bpro_dead_camera).

### 7 + 8. Records / Unity menu effects (NOT fixed; leads)
- Both are office facility scenes (FacilitySceneID.lua OFFICE_SCENE_RECORD; Bloom Palace). Records screen object ctor 0x47ad04
  (loads Facility/RecordCategoryName.msbt). User video 10: the bubble column moves ~50 px per 1/60 s at 4K.
- Next: open them from save 5 (office) with NX_UI_WLOG=1 (new widget vtables) and NX_COVER=manual at fps 60 vs 240 (functions that
  run per frame only while the menu is open), then the 30 Hz vtable list (like the card) or a task gate.

### 4. Prologue crowd scene fps (NOT fixed; measured from the user's video)
- Video 4: 53-96 fps, GPU 43 %, CPU 31 % (one core saturated) = game-thread bound (draw replay of the many crowd models). Same lever as
  s64 / s69: CallCommands copies -> OP_CALL; profile with NX_PROFILE in a crowd scene (needs a save before m0002 = new game).

### Tools added this session
- agent_scripts: newgame.sh, cardshots.sh, textshots.sh, ringtest.sh, atkshots.sh, bossfight.sh, deadwatch.sh.
- NX_SHOT_TAG=<tag>: control-file shots named <tag>_NNNNN.bmp (parallel rigs); NX_RING_TEST; NX_UI_DT_LOG.
- Ghidra decompiles in private/tms/ghidra: msgwin.c, msgrange.c, tm.c, tmrange.c, inter.c, interrange.c, notify.c, mapmgr.c, fbblur.c.
- Commit 1bd32f5: items 2, 1+6, 3, 5.

### Checks + end state (s70, ~08:05)
- Crash batch uncap_batch.sh 98 300 NX_RES=720p (final build; 2 boss rig instances ran beside it): 4 instances, 0 fatal lines, all
  reached the replay end and ran uncapped to the kill at ~375 s. Battle coverage low (2-4 battle cues each).
- Boss rig (k240 / k30, save 3, auto-battle): reached the fight, then stalled at Gojuin's "Find! That! Mirage!" phase
  (Cue bpro_reinforcements, needs real choices); no death cut captured. Item 9 still needs a run through the boss by hand
  (or the user's video of the white fade).
- User save/ md5 unchanged (save_bak_1113/md5.txt), build/settings.ini md5 unchanged, cache/pipelines.bin 41699008 B unchanged.
- Release ZIP Desktop\TMSRecomp-20261113.zip 116.2 MB.
- Next: user test of items 1/2/3/5/6 at 240; item 9 (fade) with a video or a hand run; items 7/8 (open the office menus from
  save 5); item 4 (crowd scene CPU).
- Items 7/8 probe (of rig, save 5 + NX_UI_WLOG=1): office loads next to Maiko; "Talk" starts a story event (Touma / Tsubasa scene),
  not the Records menu. Widget vtables at load: 7d2308, 7d29f0, 7d2ab4, 7d2c00, 7d2d44 (message window). Records / Bloom Palace
  entry point still unknown: ask the user where "Records (above Awards)" is opened, or follow the office map gimmicks.

## Milestone 5, session 70 part 2 (2026-11-13 ~08:40, user videos; PAUSED at once: 5-hour usage 88% at start)
User played the s70 build and sent 3 videos (D:\OBS VIDEO\OBS\2026-11-13 08-31-30.mp4, 08-31-45.mp4, 08-34-35.mp4). Frames at
1 fps + contact sheets: private/tms/user_video_1113 (v1_*, v2_*, v3_*, sheet_v1/2/3.jpg). USER (going to sleep): no questions,
fix the open items, polish, big crowd optimisation that also helps other / future areas. Scheduled one-time tasks
tms-recomp-s71-1051 (11-13 10:51 +07) and tms-recomp-s71-1551 (15:51 +07) continue this list.

### How to open items 7 + 8 (from the videos)
- 7 Records (video 1, 9.8 s): Fortuna Office (field), walk to the back wall with the FORTUNA ENTERTAINMENT shelves (left of
  the desk) -> "The WALL of FAME" menu: View Play Records / Admire Trophies / Watch Videos -> View Play Records = RECORDS list
  screen. The fast effect = the green bubble / ring circles on the left and right edges of the RECORDS screen.
- 8 Carnage Unity (video 2, 16.9 s): Bloom Palace (field, Tiki's stage; reached from the office / map) -> talk to Tiki
  ("Welcome to the Bloom Palace...") -> CARNAGE UNITY: Mirage select (Chrom / Caeda / Cain cards) -> weapon list. Fast effect =
  the faint concentric ring circles in the background behind the cards / list.
- Next: save 5 is in the office: walk to the shelf wall (not Maiko) with NX_UI_WLOG=1, open View Play Records, find the
  bubble widget / sprite task (per frame at 240?) and step it on 60 Hz UI ticks (UI rule: 60 = reference speed, smoother
  above). Same for the Unity rings. Compare the bubble speed at fps 60 vs 240 by shots (rig like cardshots.sh).

### Item 9 boss white fade (video 3, 28.7 s)
- After the killing Session (Touma), the WHOLE screen is pure white from ~t=14 s to ~t=20 s (6+ s), then the Overkill
  tutorial pops on a grey (white dimmed) background, then the victory scene ("Touma: The big boss is down!", confetti).
- So it is a full-screen white (not the boss model): suspects = btl_finish_cut.lua FinishCut3 fade to WHITE (55/60 s), a
  screen fade whose alpha is stepped per frame (reaches full early and holds), or the dead.lua ST10B effect. Check at fps 30
  vs 240 how long the white lasts (Switch: a short flash?). Rig bossfight.sh stalls at "Find! That! Mirage!" -> needs a
  better input script, or force the death cut (btl debug / HP poke) to reach it.

### Item 4 crowd fps: still open (see session 70 item 4).

## Milestone 5, session 71 (2026-11-13 10:51-~14:20 +07, scheduled run tms-recomp-s71-1051, user asleep; commits e832c67, 758af83 + notes)

### Item 9: Gojuin boss white screen after the kill (FIXED, measured)
- Measured first: user video 3 = pure white (255) from ~14 s to ~23 s. Rig k240 (agent_scripts/bosskill.sh: save 3 copy,
  NX_ENEMY_HP1=1 + NX_DEBUG_BATTLE=1 (HP1 needs both), A presses + B every 13th) = 9 s white after bpro_dead_gojyuin; true fps 30
  and fps 60: no held white (only the ST10A glow, mean ~115). Live "fps 60" during the white did NOT clear it = a stuck state.
- What is white: draw log of a white frame: the last draw is a full-screen quad with vertex colour (1,1,1,1) = the screen fade
  manager (fade_update 0x20ba14: t += rate, colour = lerp(from +0x10, to +0x20, t)); rt dump: the scene itself renders normally.
- Order of fades (new log line "fade N: state .. t .. to alpha .. rate"): btl_finish_cut.lua FinishCut3 = Flash (FadeOut
  WHITE_HALF 0, FadeIn 2/60) + a thread WaitForTimer(55/60) then FadeOut(WHITE, 55/60). Lua FadeOut binding 0x430570 -> 0x20bed8,
  FadeIn 0x430514 -> 0x20c184. The death cut start does a FadeIn. At 240 (f240): the 3 finish flashes 0.17 / 0.23 s apart, the
  death cut 0.38 s after the last flash, the Lua FadeOut(WHITE) on time 0.97 s after = AFTER the death cut's FadeIn: nothing
  faded it back -> white through the whole death animation (the user's "fades to white too early").
- Cause: the finishing-blow sequence 0x2d37cc (battle task tree) waits 25 / 35 / 55 frames in pure wait tasks (ctor 0x2d6804,
  vtable 0x7d83ec, length in +0x14, per-step action vt+0x38 = 0x2d682c "bx lr"). btl_task_step (0x2d0268) counts the +0x10
  delay and the +0x14 length per update; our hook gated only the delay to 30 Hz ticks (s12), so the length ran per frame
  (2x fast at fps 60 too).
- Fix (hle_sys.cpp btl_task_step): tasks whose vt+0x38 is a bare "bx lr" also step their +0x14 on 30 Hz ticks.
- Measured x240 (fixed build): flashes 0.835 / 1.163 s apart (25/30, 35/30 s), FadeOut(WHITE) 0.94 s after flash 3, death cut
  1.82 s after (55/30 s) = the white builds over 0.9 s and the death cut fades it in (the designed transition); brightness
  through the death cut 56-113 (no held white), then the normal short finish flash.
- Not checked: other bosses' finish sequences (same code path, should now match fps 30).

### Item 4: crowd / big-area CPU (part done, measured)
- New stat on the 10 s frames line: "frames: replay + submit X ms per frame (Y% of the time)" (game-thread draw replay cost).
- Profile b20 4K uncapped (fieldperf.sh + NX_PROFILE_SPIKE): pool_of ~10% (global mutex + map walk per buffer binding), SRW
  locks (cb(): mutex per recorded command), driver recording ~8.6%, CallCommands copies ~5%, write-watch syscalls ~3.6%,
  sampler_of building a 72-byte std::string key per binding.
- Fixes (nvn_hle.cpp, vk_replay.cpp): pool_of per-thread 4-entry cache with exact validity ranges + generation counter (bumped
  on pool init / finalize); cb() per-thread last buffer (generation bumped on Finalize); sampler_of unordered_map on the words.
- Measured (720p, uncapped, NX_PRESENT_BACKPRESSURE=0, 2 runs each, A = before, D = after): 143 -> 151-156 fps (this display's
  present cap is 152/s, so D is capped; the real gain is higher), replay + submit 2.64 -> 2.23 ms per frame (-16%).
  Screenshots A vs D differ only as much as A vs A (animated flames).
- Tried + dropped: OP_CALL (replay the called list in place instead of copying it in CallCommands): 4% SLOWER (many small
  lists cost more than the copies). Do not retry in that form.
- Still in the profile: driver recording (vkCmd*), write-watch per texture per submit (check_pool_texture), CallCommands
  copies, guest waits. Big next lever: replay on a worker thread (pipelining game logic and replay); needs: syncs pending until
  replayed, drain before texture finalize / write_texels / CPU waits, present ordered after the replays. Not started (risky).
- Rig notes: fieldperf.sh now kills only its own PID; renamed exes can not run (game.dll imports from module tms.exe): A/B by
  copying exes over build\tms.exe while nothing runs; use NX_PRESENT_BACKPRESSURE=0 for CPU numbers (else capped at 152).
- Not measured: the prologue crowd scene itself (no save before it; boss arena crowd is the nearest).

### Items 7 + 8: Records / Carnage Unity bubble rings (NOT fixed; findings)
- Rig: agent_scripts/records.sh <tag> <fps> (save 5 office -> walk left "ls -32767 0 1800" -> A Check -> A View Play Records).
- WLOG: opening it adds UI widgets 0x7d2d44 (message window) and 0x7d2c90 = the WALL of FAME 3-item menu (update 0x252cf0),
  both UI-manager widgets (60 Hz gated + UiDt). The RECORDS screen itself is NOT a UI widget: singleton object (ctor 0x47ad04,
  made by 0x47aff8, vtable 0x7e66dc = destructors only; loads Facility/RecordCategoryName.msbt), and it starts the shared
  facility background singleton 0x48afdc -> ctor 0x4897a8 (9 callers: every facility screen, Carnage Unity likely too), which
  registers two tasks: update 0x489a38 (frame-counted state machine, slide-ins over 4 / 8 frames) and draw 0x48a094 (phase 0x1a,
  sprites 0xc8458xx), plus layouts +0x34 / +0x3c (0x5c1dd0 + 0x5c200c; anims started by 0x2457bc(.., layout, name, -1, 0)).
  Which of these steps the bubbles per frame is NOT known yet.
- Measuring speed is the problem: every shot / dump stalls the game and the next variable dt = the stall (capped 1/30), so shot
  pairs and memory snapshots can not tell per-frame from per-time (snapshot rates looked "per frame" for model anim counters
  whose dt NX_ANIM_PROBE showed correct; consecutive-shot diffs were equal at 60 and 240 for the same reason).
  Ideas: (a) gate candidate tasks live with "task30 <fn>" and look for stepping; (b) a no-stall measure: log a ring sprite's
  position from its draw each frame for 1 s at fps 60 vs 240 (find the draw via drawlog textures, then a probe);
  (c) compare the user's 08-31-30.mp4 ring speed (px/s) with an fps 30 capture.
- Tools fixed: snap4.sh / framecount.py counted every log line twice (plain + timestamped copy) -> timestamped lines only.

### Tools added this session (private/tms/agent_scripts)
- bosskill.sh (kills Gojuin with NX_ENEMY_HP1), bosswhite.sh (live fps switch at the white), bright.py (mean / min luma per
  shot), records.sh, vshift.py, snaprt.sh + ratert.py (per-real-second snapshot rates). Ghidra decompiles in private/tms/ghidra:
  fade.c, fadelua.c, finish.c, waitnode.c, nodebase.c, actmgr.c, recw.c, recctor.c, recscene*.c, bgctor.c, bgupd.c, bgdraw.c, dof.c.

### Checks + end state (s71, ~14:15)
- Crash batch uncap_batch.sh 99 420 NX_RES=720p (final build 758af83): 4 x 420 s, all "ok", logs end at ~495 s, no fatal
  lines (only the usual startup import note), battle cues 58 / 0 / 0 / 29.
- User save/ md5 = save_bak_1113/md5.txt (all 7 files equal); build/settings.ini unchanged (mtime 08:34 = the user's session,
  md5 64e0d45a...); cache/pipelines.bin 41699008 -> 42583224 B (grew, never shrunk).
- Release ZIP Desktop\TMSRecomp-20261113.zip rebuilt 14:13 (116.2 MB) with both fixes.
- Next (s71-1551): items 7+8 (measure first, see ideas), then the item 4 big lever (async replay) only with a solid plan + A/B;
  user test of items 1/2/3/5/6/9 at 240 fps.

## Milestone 5, session 72 (2026-11-13 15:51-~17:30 +07, scheduled run tms-recomp-s71-1551, user asleep; commits 31ae58f, 3c71e12 + notes)

### Measuring frame-counted effects without stall noise (new method, use it from now on)
- Control "fixdt n" (existed) makes every frame step exactly 1/n s, so a shot stall no longer changes the next dt. Rig
  agent_scripts/ringrate.sh <tag> <fps> <opener.sh> (env PRE="fn fn" = task30 gates first): fixdt 60 + "shots 8", then
  fixdt 240 + "shots 32" = the same game time. agent_scripts/fixshots.sh <tag> does the same on a running game.
  agent_scripts/stripdiff.py <tag> <first> <last> [step] [x0 x1]: mean abs luma change of a screen strip between shot i and
  i+step. Per-time (correct): 240 with step 4 = 60 with step 1. Per-frame (bug): 240 step 4 ~ 2.5-4x the 60 value.
  The diff metric saturates for faint / repeating patterns (Unity weapon list): use it as larger / equal, not as a ratio.

### Items 7 + 8: Records bubbles + Carnage Unity rings (FIXED, measured)
- Records: tasks new at the open (NX_ANIM_PROBE): 0x47a7e8, 0x47ab48 (phase 0), 0x47ab74 (phase 23), 0x48a094 / 0x489a38
  (facility bg). task30 bisect: 0x47ab48 = the bubbles (task -> singleton manager 0x47b05c: counters +0x50..+0x6c +1/+2 per
  call, rings lerped by 0x23f904 over 0x3c0 / 0x780 frames). Gating draw tasks (0x48a094 etc.) blanks the screen: never.
- Carnage Unity: rig agent_scripts/unity.sh (save 5 office -> "setpos 146 0 -60" = the blue Bloom Palace door, A ->
  "setpos -9 2 -506" = Tiki, A x4 -> Mirage cards). Tasks made when Tiki's menu opens: 0x372284 / 0x3722f8 (vt 0x7de6f0)
  and 0x386ec0 / 0x386fc8 (vt 0x7de7e8); 0x372284 = the Unity screen (state +0xc 1 -> 0x386868). Bg 0x489a38 and 0x386ec0:
  no effect on the rings.
- Fix: names.txt records_task_update 0x47ab48 + unity_task_update 0x372284 (re-lift 20636 hooks), hle_sys.cpp hooks with
  the camp-menu gate (ui_skip: 60 Hz UI ticks, press frames pass, UiDt). Both always return 1.
- Measured (fixdt shots): Records 240 step 4 = 13.8 before -> 5.6 after (60 step 1 = 5.3-5.7); Unity cards 3.7 -> 2.1
  (60: 2.3); Unity weapon list: uigate 1 at 240 <= the 60 value (uigate 0 above it). Screens look normal at 240.
- Lead (not done, not reachable from save 5): task pair 0x38fe58 / 0x38fe84 runs manager 0x39a444, which builds two more
  facility screens (ctors 0x390818, 0x39bc40: same widgets as Unity, shared bg 0x48afdc) = probably shops or a later
  Bloom Palace menu; likely the same per-frame bug. The other bg users (ctors 0x320c34, 0x322ce0, 0x332194, 0x33cf24) sit
  in the camp-menu code (camp_update is gated already); 0x3885c8 is under the Unity screen. Gate 0x38fe58 the same way
  once a save reaches it (verify with fixshots first).

### Item 4: CPU (part 2, measured)
- Profile b20 720p uncapped (NX_PROFILE_SPIKE=0 gives guest / runtime caller / leaf per frame; aggregate with a script):
  SRW locks from get<T> (nvnBufferGetAddress / Map took the global lock twice per call), per-draw heap allocations in
  bind_resources (descriptor lists, tex scales, support key), support_buffer map walk, pipeline() key string.
- Fix (nvn_hle.cpp, vk_replay.cpp): get<T> per-thread 64-entry cache checked against a generation bumped on destroy /
  replace; thread_local lists in bind_resources; support_buffer last-key fast path; thread_local pipeline key.
- Measured (2 runs each, NX_PRESENT_BACKPRESSURE=0): 162.0-163.5 -> 188.6-190.2 fps (+16%), replay + submit 2.12 -> 1.49 ms
  per frame (-30%). Image check: A vs A and A vs B shots at fixdt 60 differ only in animated areas (flames, radar sweep,
  idle pose); static areas identical. Unity screens render normally on the new build.
- Together with s71: replay + submit 2.64 -> 1.49 ms per frame (-44%) in this scene.
- Remaining in the profile: NtGetWriteWatch (one syscall per texture per submit, check_pool_texture, ~5%), driver
  recording (vkCmd*, ~10%), NtFreeVirtualMemory (big frees, ~2%, caller not found), the main thread waiting for its AtJob
  workers (guest job system, 50 us yields). Idea for write-watch: one GetWriteWatch per pool per submit without reset; skip
  the per-texture calls when the pool has no written page (only a gain if texture pools hold no CPU-written data: count
  first). Async replay stays a big, risky change (syncs, UI smoothing reads game state at replay time): not started.

## Milestone 5, session 73 (2026-11-13 ~19:00-, with user away: "polish and finish the backlog, I will playtest later")

### Write-watch per-pool snapshot (s72 idea): MEASURED, NO GAIN, REVERTED
- Tried: check_pool_texture takes one GetWriteWatch (no reset) per pool per submit and skips a texture's own call when
  none of its pages is listed (4-slot cache, then a per-submit map per pool).
- Measured (fieldperf.sh b20 720p uncapped, NX_PRESENT_BACKPRESSURE=0, A = NX_WW_PER_TEXTURE, 4 runs each): replay +
  submit 1.59-1.80 ms (new) vs 1.54-1.65 ms (old) per frame. Counters: ~29000 pool snapshots and ~36000 skipped checks
  per 10 s with both cache forms = textures sit about one per pool, so a pool snapshot IS the per-texture syscall.
- Code reverted (no change kept). Do not retry in this form; the remaining lever is fewer checks (e.g. only textures
  that ever got a CPU write), not a coarser call.

### Other Bloom Palace facilities: same 60 Hz UI gate as Carnage Unity (BUILD ONLY, not measured)
- Lead 0x38fe58 resolved by xrefs: Bloom Palace facility switch 0x36cf64 (called from 0x4365f0) reads a type from a
  table: type 1 = Carnage Unity (0x3720a4 -> task 0x372284, fixed in s72); types 2-5 = 0x38fc84, which registers tasks
  0x38fe58 / 0x38fe84 and runs manager 0x39a444 -> 0x39a10c builds screen 0 (0x39eea4), 1 (0x390818) or 2 (0x39bc40):
  same widgets + facility bg as the Unity screen = the later Unity menus (Radiant Unity etc.).
- 0x38fe58 just calls 0x39a444 when its singleton is set and returns 1 (decompiled). Fix: names.txt unity2_task_update
  + hle_sys.cpp hook with the same ui_skip / UiDt gate (re-lift 20637 hooks).
- Not reachable from save 5 (Tiki offers only "Perform Carnage Unity" + "Unity Q&A", shot tk_00003). USER CHECK: at
  240 fps, open Radiant Unity (or any later Tiki menu) and compare the background ring speed with fps 60.
- New rig agent_scripts/tiki.sh <tag> <fps> (office -> Tiki, shot per A press).

### Fern black edges (s41 / s43 item 6)
- Save 5 Fortuna Office at 4K with the pack (9540 files): no fern in the default view (camera turn by control "rs" did not
  move it). Still a USER CHECK (s41 saw it in the d002_01 hall near the red chair).

### Checks + end state (s73, ~19:50)
- Crash batch uncap_batch.sh 99 420 NX_RES=720p (build with unity2 gate): 4 x 420 s, all "ok", logs end at ~497 s, only
  the usual boot "unimplemented import" line; battle cues 60 / 0 / 0 / 0.
- User save/ md5 = save_bak_1113 (all equal); cache/pipelines.bin 42583224 B (not shrunk).
- Next: user test at 240 (s70-s73 items); async replay only with a solid plan + A/B.

## Milestone 5, session 74 (2026-11-13 ~21:15-, with user; branch fix/movie-hle-leak, commits 074f166, 028c4db + notes)

User report (played prologue -> Chapter 1 on the s73 build at 240 fps, 4K; videos D:\OBS VIDEO\OBS\2026-11-13 20-46-12.mp4
(prologue crowd / big areas ~100 fps), 20-50-40.mp4 (battle target pick, Blob), 21-04-19.mp4 + 21-05-07.mp4 (Shibuya);
contact sheets + crops in private/tms/user_video_1113b; run log private/tms/nx.log ends 21:09 with the crash):
- CRASH entering Shibuya ("The game crashed", nx.log). 1. crowd / big areas drop to ~100 fps at 4K. 2. enemy target
  highlight (Blob body) looks sped up. 3. boss white fade now correct (s71). 4. Shibuya not smooth (frame pacing), NPCs
  walk too fast, cars too fast. 5. Play Records + Performa fusion now good (s72).
- User saves backed up first: private/tms/save_bak_1113b (+ md5.txt; save 6 = Shibuya, last slot). testsave/u13b = copy.

### Crash (FIXED, verified)
- nx.log: "CRASH: code c0000005 ... access 100ffc0f000 (guest ffc0f000)", guest lr 0x6ddb3c = right after
  __aeabi_memcpy4(movie::Buffer::Base(), src, n) in the game's movie input path (r2 = 0x1199 bytes left), just after
  "movie::Decoder(bdd0a1c0...)" for camp_04 (camp menu background). The log has exactly 16 decoder creations.
- Cause: hle_movie.cpp Configure took 4 input buffers x 4 MB (hle_alloc, a never-freed bump allocator) per decoder;
  destructors dropped them. 16 decoders = 256 MB = the whole HLE region (0xf0000000 + 0x0fff0000). The 16th decoder's
  4th buffer end passed 4 GiB: `a + size` wrapped in 32 bits, the bound check passed, nothing was committed, the buffer
  came back at 0xffc0xxxx and the game's copy hit the first uncommitted page 0xffc0f000. Any 16th movie (camp menu opens,
  shop movies) crashed; Shibuya was just where the count ran out.
- Fix: destroyed decoders put their input buffers in g_in_pool, Configure takes from it first; hle_alloc checks the end in
  64 bits (fatal "HLE region exhausted" instead of a silent bad pointer). No other hle_alloc user allocates per use
  (all one-time: callbacks, NVN device, audio scratch).
- Verified: agent_scripts/campcycle.sh cc1 24 (to_camp.sh, then B / Y 24 times): 26 decoders, no CRASH / fatal, 26 "first
  frame", 25 "4K stream ... playing", 0 decode errors. (Old build not re-run; the arithmetic matches the log exactly.)

### Item 4: Shibuya cars + walking NPCs too fast (FIXED, measured)
- Measure: fixdt shot pairs were too scene-dependent (traffic varies run to run); numbers instead: NX_TOWN_LOG (car pos per
  call) and NX_MOVE_LOG=2 "[movef]" + agent_scripts/movef_speed.py (units/s of game time, share of frames without motion).
  Rig agent_scripts/shibuya.sh <tag> <fps> [env] (save 6 via testsave/u13b; player at 488.4 1.0 169.4).
- Cars: Lua ScriptVehicle bindings (Vehicle_GetCurrentSpeed 0x461548 reads +0x34) -> car object; car update 0x3df4fc
  (virtual; ~50 cars, every frame): speed +0x34 eased to target +0x94, pos +4 += speed x dir (no dt), steering, then
  actor_set_pos 0x3c853c on the car actor +0xb4. Measured 1.25 units per call = ~130 units/s at ~105 fps; Switch 30 Hz =
  37.5. Mob creation 0x3d5968 / vehicles 0x3db0c8 found from "Character/mob/%s" / "Character/vehicle/%s".
- Crowd: walkers are actors moved by their job (actor_move_update 0x3c8d90 adds delta +0x6c/+0x74; cleared after unless
  +0xd8). The crowd manager 0x3d6e2c (from field task 0x46b7f0, after singleton 0x3d6724) spawns one walker per call,
  steps each walker (0x3d64b0: delta = target - pos, actor_set_dir 0x3c8734), avoidance (0x3d5bd4), placement (0x3d53dc
  -> actor_set_pos). Step 0.441 units per call = Switch 13.2 units/s; at ~100 fps it was ~44.
  (0x3da594 = a path-follower class not used in Shibuya; the watch tool missed most job-thread writes.)
- Fix (hle_sys.cpp, names.txt vehicle_update / mob_mgr_update / actor_set_pos / actor_set_dir, re-lift 20641 hooks):
  both run on 30 Hz ticks per object above 30 fps (town_tick_due on g_tick30).
  Cars: the hook shows each car between its last two tick positions (alpha = 1 - g_tick30_left*30, via actor_set_pos), puts
  the true position back before the next tick (the update starts from the actor position), restarts the blend when other
  code moved the car (x/z differ from what we showed) or it jumped > 20 units. Car actors skip actor_move_update's script
  spread (it fought the blend: 8600 jitter steps in 20 s before that change).
  Walkers: actors marked by actor_set_pos / actor_set_dir while mob_mgr_update runs (g_town_placed, active within 2 ticks)
  go through town_actor_update: true position kept for the game, the step (delta) applies once per placement and is held
  off between, the shown x/z glide from the shown position to the new true one ending at the next tick (glide starts one
  frame back so no held frame); y always the job's own (the job changes y every frame: comparing all 3 floats restarted
  the glide every frame = walkers frozen then 4-unit snaps). Jumps > 4 units snap.
- Measured 240 fps 720p (tz5): walkers 11.8-14.4 units/s, 0% frames without motion; cars even per-frame steps (e.g.
  0.7-0.8 per 10 ms frame), "kept" jitter steps 0 (was 0 with the gate off too). CPU A/B (pf, 720p uncapped,
  NX_PRESENT_BACKPRESSURE=0): 100-103 fps gate off vs 103-110 gate on; replay + submit 3.6 -> 3.4 ms.
- Same code also fixes 60 fps (was 2x there). NX_TOWN30=0 (all off), NX_MOB30=0 (crowd gate off), NX_TOWN_LOG=N,
  NX_TOWN_DBG=<actor hex | 1> (per-frame placement / delta trace), NX_MOVE_LOG=3 ("[movej]" in-job moves).
- NOT done: yaw (actor_set_dir) of walkers and car rotation still step at 30 Hz (small; looks fine in shots).
  Other towns' crowds (Harajuku etc.) use the same manager: not checked (no save there).

### Item 2: enemy target highlight (NOT fixed, findings)
- User log: battle speed 3x, "1x while choosing" active in target pick, so not the s52 battle speed-up.
- User video 20-50-40.mp4: Blob (cup-shaped) inside the yellow spotlight; its body brightness pulses (blob_v2.jpg).
- Rig: agent_scripts/tgt2.sh (tgt.sh + wheel left, A, A) is NOT deterministic: the s20 battle opens on a different member /
  cursor each run (Items, Escape, Skills, Tsubasa's wheel). Next: make the rig wait for Itsuki's turn (log line) and pick
  Attack by its cursor, then fixdt 120 vs 30 bursts of the target body; candidates: the target flash (btl material colour,
  per call) next to btl_weak_mark_draw (s38, 0x303290) and the post-select marker 0x2f2c60.

### Items 1 + 4: crowd / Shibuya fps (NOT fixed)
- Shibuya 720p uncapped: ~100-110 fps, replay + submit ~3.4 ms of ~9.5 ms per frame; the rest is game logic (crowd, cars,
  field) on the game thread; worst gaps 18-23 ms per 10 s. At 4K the user saw 106-122 fps and uneven pacing. Lever left
  (s71/s72): async replay (pipelining replay with game logic); also the crowd jobs themselves.

### Tools added (private/tms/agent_scripts)
- campcycle.sh, shibuya.sh, sbrate.sh (fixed-step strip diff; too noisy for traffic), movef_speed.py, tgt2.sh.
- Ghidra decompiles in private/tms/ghidra: vehmob.c, traffic_range.c (0x3d5000-0x3e0000), mob_range.c (0x3cf000-
  0x3d5000), trafmgr.c.

### Checks + end state (s74, ~23:40)
- Crash batch uncap_batch.sh 99 420 NX_RES=720p (final build): 4 x 420 s, all "ok" (battle cues 2 / 0 / 0 / 2).
- User save/ md5 = save_bak_1113b/md5.txt (all equal); cache/pipelines.bin 42583224 -> 46318885 B (grew: Shibuya).
- Release ZIP Desktop\TMSRecomp-20261113.zip rebuilt 23:29 (116.2 MB) with both fixes.
- Branch fix/movie-hle-leak (not merged into claude/changes). Next: user test in Shibuya at 240 (crash gone after many
  camp opens, car / walker speed + smoothness); item 2 rig; Shibuya CPU.

## Milestone 5, session 75 (2026-11-14 ~00:05-01:30, with user; branch fix/shibuya-cars-fps from fix/movie-hle-leak; commits adbd6da, be7a25a + notes; PAUSED at 5-hour 95%)

User report (s74 build, 240 fps 4K, video D:\OBS VIDEO\OBS\2026-11-14 00-01-21.mp4, frames in private/tms/user_video_1114):
walkers fixed, CARS NOT (shake), movie crash gone ("all good"). Asked: fix items 1+4 low fps (important; backup before
risky work, break nothing), then a QoL fast travel (native port menu or L3+R3) to visited shops / accessory places in
Shibuya: ANALYZE FIRST, respect visited flags, never break story scripts. Saves backed up: private/tms/save_bak_1114 (+md5,
same as save_bak_1113b). Backup before fps work: git tag backup/pre-fps-1114 (adbd6da) + private/tms/build_bak_1114
(note: an exe outside build\ does not start, A/B by env switch instead).

### Cars shaking (FIXED, measured)
- Video: cars stopped at the light jump ~15-25 px back and forth every frame. Logged positions (vehicle_update time) were
  smooth: the shake is after it. Cause (0x3deb84 decompiled, ghidra/actorpos.c): a VISIBLE car (actor +0x4a8 == 0) does not
  move itself; it sets the actor move delta +0x6c..+0x74 and the actor job (actor_move_update) applies it. s74 blended cars
  inside vehicle_update, before the job, so the job added the delta on top of the blend and the next frame pulled it back.
- Fix (hle_sys.cpp): cars go through town_actor_update like walkers (vehicle_update runs on 30 Hz ticks from the true
  position, its actor_set_pos / actor_set_dir mark the actor; delta applied once per tick, shown position glides).
  g_town_cars / car blend removed. town_log("car") now logs the ACTOR address.
- Measured 240 fps 720p (agent_scripts/carshown.py on NX_MOVE_LOG=2 + NX_TOWN_LOG): 0 back-steps in 5424 moving car frames
  (24 hits were all 8 frames after spawn = metric window). Speed vs true 30 fps (agent_scripts/cartick.py): units per tick
  p90 3.10 / p99 3.24 at 240 vs 3.22 / 3.24 at 30 (s74's "1.25 per tick" was slow cars only).

### Items 1 + 4 fps (Shibuya 4K, MSAA 8x = the user's settings): big GPU waste FIXED, measured
- New stats: frames line "GPU waits X ms per frame"; NX_GPU_TIME=1 "GPU busy" (timestamps per submit); NX_GPU_PASSES=1
  GPU ms per pass label (pass / after / resolve / expand); NX_PASS_SEQ=<present n> one frame's pass order.
  (present n ~10500 = Shibuya field in agent_scripts/sbperf.sh at 4K.) RTX 5070 Ti here.
- Before: 720p ~110 fps CPU-bound (GPU waits 0); 4K 94-103 fps with GPU busy 8.8-10.2 ms = GPU-bound. Passes at 4K:
  resolves 2.9 ms + expands 1.3 ms per frame (~12 each) vs the 8x passes themselves 0.4 ms.
- Cause: Shibuya's main scene pass (colour + depth D1) runs 1x (D1 is cleared in a depth-only 1x pass -> stale), and per
  object the game switches to one-draw passes on a second depth D2 that went 8x -> expand + resolve each switch.
- Fix (vk_replay.cpp begin_rendering): a colour target whose scene pass ran 1x this frame (g_ms_1x_frame) stays 1x for
  the rest of the frame (no expand). NX_MSAA_PINGPONG=1 = old rule.
- Measured (sbperf.sh 4K uncapped, 2 runs each A old / B new): 95.7-103.1 -> 115.3-124.7 fps; GPU busy 9.4-10.2 ->
  5.5-5.75 ms; worst gap 19-21 -> 13-18 ms. Shots vA/vB (user_video_1114/vAB.jpg, cAB.png): scene fine, edges alike.
- FINDING for the user: MSAA 8x is NOT applied to the main scene anywhere measured (Shibuya, Daitama b20, Observatory
  slot 2: all scene passes 1x, the depth-only clear makes the depth "stale"). s57 verified it worked; regressed since.
  Fixing it = real 8x at 4K (big GPU cost). User decision: fix MSAA, or leave it off (4K internal + FXAA/SMAA).
- Now at 4K the CPU is the limit (~8.3 ms frame, replay + submit ~3.3 ms) -> async replay (s71 plan) would now help at 4K
  too. NOT started. Other CPU items: CallCommands copies 5.7%, write-watch 5.4%, SRW locks 7.6% of the game thread.

### NOT done yet (next, in order)
1. Crash batch (uncap_batch.sh 99 420 NX_RES=720p) on be7a25a, saves md5 vs save_bak_1114, then release ZIP (package.ps1).
   ZIP NOT rebuilt this session yet (Desktop ZIP = s74 build, still has the car shake).
2. Fast travel: analysis only so far = none. Plan: find the Tokyo Map warp (X button "Tokyo Map" in the field) script /
   function + its area-unlock flags (flags.txt, Event_MapLayoutEventTable.bin), shop entrance warp points in Shibuya
   layouts; offer only places whose map flag is set, only in free roam (no event / script thread running), through the
   game's own warp call so story triggers run as normal. Report the analysis to the user before building.
3. Async replay (big, backup first) or smaller CPU items.
- Tools: agent_scripts carjit.py, carshown.py, cartick.py, sbperf.sh (now takes a shot before kill; NX_SHOT_TAG for names),
  obsperf.sh. Kill leftover rig instances: shibuya.sh leaves the game running (5 were found eating CPU mid-session).

## Milestone 5, session 76 (2026-11-14 ~02:10-, user away: "keep finishing / polishing / optimizing"; branch fix/shibuya-cars-fps)

### MSAA (83add03 follow-up): shadow maps excluded, VRAM cap, measured
- 83add03 let EVERY depth-only pass take MSAA (natt 0). Shadow maps are res-scaled too (vk.cpp: only NX_SHADOW_NATIVE
  keeps them at game size), so battle shadow maps 1024x2048 / 1024x1024 x3 at 4K would get 8x twins (~600 MB) for nothing.
- Fix (vk_replay.cpp begin_rendering): depth-only passes take MSAA only on depths a scene pass (colour + depth, same size)
  has used (g_scene_depth). One frame late on first use, then the scene stays 8x.
- Verified: tutorial battle 4K 8x (btlperf.sh bt8): 12 twins, all 3840x2160 (no shadow-sized twin), 2.87 GB total;
  1366-1397 frames per 10 s uncapped.
- Shibuya 4K uncapped (sbperf.sh, 30 s): MSAA off 110-114 fps (GPU waits 0); 4x 95-99 fps; 8x 69 fps (GPU busy 14.5 ms,
  GPU-bound). Shots m8a / m0a: scene correct (cars, crowd, characters), no artifacts.
- Twin log now prints the running VRAM total (first 24 twins).
- VRAM cap (PORTABILITY): ms_wanted halves the sample count while 12 screen-sized twins x 4 B x samples exceed a quarter
  of the largest device-local heap (4K 8x needs ~13 GB VRAM, 4K 4x ~7 GB, 1080p 8x ~3.5 GB). Logs "vk: MSAA 8x -> 4x
  (VRAM budget ...)". NX_MSAA_VRAM_MB=<n> (debug) pretends a smaller GPU.
- Settings help text for MSAA updated with the measured cost (old text said 4x at 4K = 0.7 GB).
- User advice: at 4K, 4x is the sweet spot (~15% fps); 8x costs ~40%.

### Fast travel (ANALYSIS ONLY, nothing built; user decision needed)
- Names (Common/MapName.msbt, UTF-8 MSBT; parser scratch msbt.py): Shibuya = f001 (f001_01..10); f003 = interiors:
  f003_01 Hee Ho Mart, f003_02 Fortuna Office, f003_03 Bloom Palace, f003_04 Jewelry Carabia, f003_05 Uzume Studio,
  f003_06 Seiren, f003_07 Office Storage, f003_08 Anzu. Harajuku = f007 (f007_b point = Anzu).
- The game's own Tokyo Map ("LargeMap") ALREADY has Shibuya sub-points: a Station (Hachiko), b Central City, c Hee Ho
  Mart (Dougenzaka-Shita), d Carabia (jewelry), e 106 (MapMessage LargeMapHelp_f001_01_A..E). Points are gated by
  lmapIsTownAccess (unlock / story flags) = "visited" is already respected.
- Vanilla opens the map only at area exits: Event/field/script_map/field/<area>/event/OpenLMap.lua =
  mapSetShibuyaStation(x) + ChangeLargeMap() (OpenLMap_106 also checks FLG_EVM_1023_06).
- Bindings (table at 0x7e4xxx, guest = file offset + 0x200000; ghidra/lmap.c): ChangeLargeMap 0x4490fc only sets
  (*0x9f0454)+4 = 1 (request flag on the large-map manager); mapSetShibuyaStation 0x44a374 sets +0x38;
  lmapIsTownAccess 0x446a30 -> 0x46ac0c(mgr, town, point); RequestChangeMap 0x448ff8 -> 0x46c1b4(kind, area, sub, entry).
- Proposed QoL: L3+R3 (or a port-menu item) in free roam = open the game's Tokyo Map (same as walking to the exit):
  set mgr+4 like ChangeLargeMap, only when the field has player control and no event / script thread runs. Shop doors
  are then one pick away (points c / d; Anzu via Harajuku b). Warping straight INTO shops (RequestChangeMap FIELD 3 n
  entry) is riskier (entry ids, story triggers): not proposed. Open: where +4 is consumed (safe states), field
  free-roam test for the gate.

### Checks + end state (s76, ~02:30)
- VRAM cap test (sbperf.sh 4K NX_MSAA=8): NX_MSAA_VRAM_MB=8192 -> "vk: MSAA 8x -> 4x (VRAM budget 2048 MB ...)", 4x twins
  (1.18 GB); without it 8x twins as before.
- Crash batch uncap_batch.sh 99 420 NX_RES=720p NX_MSAA=8: 4 x 420 s all "ok", 0 CRASH / fatal, logs end ~496 s,
  9-12 MSAA 8x twins each (battle cues 4 / 0 / 0 / 0).
- User save/ md5 = save_bak_1114/md5.txt (all equal); cache/pipelines.bin 46318885 B (not shrunk).
- Release ZIP Desktop\TMSRecomp-20261114.zip (116.2 MB) with s75 + s76 (car shake fix, MSAA ping-pong, real 8x, cap).
- Next: user decision on fast travel (L3+R3 opens the game's Tokyo Map); user test of MSAA 4x / 8x at 4K; async replay
  (backup first) or smaller CPU items (CallCommands copies 5.7%, write-watch 5.4%, SRW locks 7.6% of the game thread).

## Milestone 5, session 77 (2026-11-14 ~04:00-, with user; branch feat/tokyo-map-shortcut from fix/shibuya-cars-fps 4d6e65f; backup tag backup/pre-lmap-1114)

User: "yes build it" (s76 proposal: L3+R3 opens the game's Tokyo Map in free roam).

### Findings that change the s76 analysis
- L3+R3 is ALREADY the F1 port-menu combo (overlay.cpp), so the shortcut is an F1 / L3+R3 menu action instead:
  "Open Tokyo Map" (first row, shown only in town free roam). L3+R3, then A.
- s76 was WRONG that vanilla opens the map only at area exits: on town streets the game's own X button opens the same
  Tokyo Map (HUD "X Tokyo Map"). Free-roam state 0x47345c: next state 6 (large map, 0x47146c) when lmap mgr +4 == 1 OR
  (button at 0x9f53d8 +0xdc pressed AND current-map byte 0x9f52a8 +6 != 0). Gate byte: Shibuya f001_05 = 1, Fortuna
  Office f003_02 = 0 (no X prompt, X does nothing), Daitama d002_01 = 0. So the new action's real gain = opening the map
  INDOORS (shops, office) where the game hides X.
- Shop sub-points (Hee Ho Mart, Carabia, 106 ...) are not on the map at the u13b save's story point ("Select somewhere
  other than your current location" on Shibuya): they unlock by story flags, same as vanilla.
- Addresses: lmap mgr = *0x9f5290 (GOT 0x9f0454); +4 request (ChangeLargeMap), +0x10 == 2 destination picked, +0x14 map
  open, +0x38 Shibuya station (mapSetShibuyaStation); 0x46a240 = map reset (clears +4..+0x14, cursor = current map).
  Current map 0x9f52a8: kind +0x74 (0 = towns / interiors f0xx, 1 = Idolaspheres d0xx), area +0x76, sub +0x78.
  Event-end state 0x47203c ALSO goes to state 6 when +4 == 1 (how OpenLMap.lua works) -> a stale +4 would open the map
  after an event: never leave it set.

### Built
- hle_sys.cpp field_roam_update: logs "field: free roam in map kind K area A sub S (X map gate G)" on map change; tells
  the overlay town = kind 0. On a request: sets mgr +4 = 1, runs the game's free-roam update, and if the next state
  (obj +4) is not 6 clears +4 again ("request not taken"). Kind 1 (dungeons): request ignored.
- overlay.cpp: "Open Tokyo Map" action row (only within 300 ms of a town free-roam frame); action rows now close the menu.
  A request not taken within 2 s is dropped ("Tokyo Map request dropped"), e.g. camp menu open / event started.
- ui.cpp: NX_CONTROL "lmap" = the menu action. Rig: agent_scripts/lmap.sh <tag> (KEY=x tests the native button).

### Verified (720p, u13b Shibuya / b20 Daitama saves)
- Shibuya street: map opens ("You Are Here" on Shibuya), B returns to the same position (488.4 1.0 169.4), reopens.
- Fortuna Office (via the map): X does nothing, "lmap" opens the map with "You Are Here" on Fortuna Office.
- Daitama dungeon: "lmap" ignored, field unchanged. Camp menu open + lmap + B: request dropped, no map afterwards.
- Crash batch uncap_batch.sh 99 420 NX_RES=720p: 4 x 420 s all "ok", 0 CRASH / fatal (cues 33 / 0 / 0 / 0). User save/
  md5 = save_bak_1114 (all equal); cache/pipelines.bin 46318885 B.
- NOT seen by eye: the F1 overlay row itself (agent shots capture the game frame, not the overlay window); the
  "request not taken" branch (needs an event trigger on the same frame).

## Milestone 5, session 78 (2026-11-14 ~08:15-, user asleep; branch perf/msaa-resolve-1114 from feat/tokyo-map-shortcut 7143c8d)

User (s77 build, video D:\OBS VIDEO\OBS\2026-11-14 06-21-40.mp4, frames private/tms/user_video_1114b): vehicles OK ->
merge. 1) MSAA 8x at 4K stutters, 37-67 fps (off ~110): optimise. 2) Fast travel misunderstood: wants L1 (unused in free
roam) -> menu -> warp straight to Seiren cafe / item / weapon-armor shops; careful before Shibuya is reached (softlock).
Rule: pause at 5-hour 99% and write notes; scheduled task tmsrecomp-continue-1114 at 12:01 (+07) resumes.

### Merge
- fix/shibuya-cars-fps and master fast-forwarded to 7143c8d (linear history; tag backup/master-pre-merge-1114 = old master 3c71e12).

### MSAA 8x: resolves were half the GPU frame (FIXED, measured)
- Rig gotcha: private/tms/build/settings.ini has fx_fxaa = 4 (DLSS) and ms_wanted() returns 1 under FSR 3 / DLSS, so
  "NX_MSAA=8" alone measured NO MSAA. Pass NX_FX_FXAA=1 (FXAA) for MSAA runs. sbperf.sh: A retry until the field (4K
  title is later than the first A); SB_SEQ=1 logs one field frame's pass order (new NX_CONTROL "seq").
- Before (Shibuya 4K 8x FXAA, NX_GPU_PASSES): GPU 15.5-17.5 ms/frame; resolves 8.3 ms (29 "c1+d" per frame) vs draws 5 ms.
- Cause (seq): the Shibuya scene alternates two depth buffers D1 / D2 on one colour target (~25 switches a frame, many
  0-draw passes on D2). Old rule: any change of targets resolved every dirty twin (colour + depth at 8x 4K).
- Fix (vk_replay.cpp): a 1x pass resolves only its own dirty targets; an MSAA pass continues on the twins; other dirty
  twins wait until their image is read (sampled -> only that image, copy -> src/dst, clear -> none (clears both),
  dispatch / SMAA / end -> all). ms_flush groups by size, one depth per resolve pass (old one dropped a 2nd depth's
  dirty mark). Resolve labels carry the trigger. NX_MSAA_FLUSH_ALL=1 = old rule.
- Measured A/B same build (sbperf.sh 4K uncapped, NX_MSAA=8 NX_FX_FXAA=1): old 57.2 / 60.2 fps, GPU 17.4 / 16.5 ms;
  new 84.4 / 89.9 fps, GPU 10.2 / 10.1 ms (+48%). Shots mA / mB (user_video_1114b/mAB.jpg): same scene, edges smooth.
  Tutorial battle 4K 8x (btlperf.sh, now takes a shot): 152 fps (s76: ~137-140), shot bt8s.jpg correct, no errors.
- Commit 5d067d5.

### L1 fast travel (BUILT, verified on u13b with a forced flag)
- Doors (tools/lyts.py on Map/field/f001/f001_0x/model.apak, f007_01): ints (3, 0, 3, n, 1000) = RequestChangeMap(FIELD 0,
  area 3, sub n, entry 1000): Hee Ho Mart f003_01 (type 0x16 PlaySE_ConvenientStore), Carabia f003_04, Seiren f003_06
  (EnterCafe_A Lua: entry 1000, FlagOff FLG_MAP_CafeEnteredFromBack; B door = 1001), Uzume Lesson f003_05, Anzu f003_08
  (Harajuku). No weapon shop exists: weapons = Unity at Bloom Palace (via Fortuna Office), not offered.
- 0x46c1b4 only stores kind/area/sub/entry in 0x7e63a0..ac (GOT 0x9f0468/598/59c/5a0); field loop 0x46b7f0 turns a
  pending request into a map change (state 8) when the current state ends with next state != 4 (ghidra/reqmap*.c).
  So the warp = 0x46c1b4 + 0x46ed90(obj, 8) + return 0 from free roam, like Return to Title.
- Gate (hle_sys.cpp travel_mask): town free roam (kind 0, area 1 / 3 / 7), SHIBUYA_CORRUPT 0x54 off, isShibuyaHalfDead
  0x8805 off; Hee Ho Mart CVS1_TTL_DONE 0x65, Carabia JWL_TTL_DONE 0x67, Anzu GDS_TTL_DONE 0x6f (Facility/field/
  GoodsShop + JewelShop EntranceDemo set them); Seiren once any of those is on or MTLMAP_OPEN_AREA_SHIBUYA_A 0x1b5, not
  while quest 07 waits (0x8e61 on, 0x8e6f off, epilogue 0x3e07 off). The current shop is left out.
- u13b (chapter 1 Shibuya free roam) has ALL of these flags off -> menu shows "No shops yet" + Tokyo Map.
- overlay.cpp: L alone in town free roam -> FAST TRAVEL menu (shops + "Tokyo Map", moved out of F1 settings);
  B / L close. NX_CONTROL "travel n", "l". Rig agent_scripts/travel.sh <tag> <n> (FLAGS="0x65" forces flags).
- Verified (720p): flag 0x65 forced -> menu mask 0x3 (Seiren + Hee Ho Mart); travel 1 -> Hee Ho Mart free roam
  (shots tv2); travel 0 -> Cafe Seiren "Welcome!" + Drink / Food / Don't Buy (shots tv3). Not checked: leaving the shops
  back to the street, Anzu / Carabia warps, the menu by eye (overlay window is not in agent shots), money < 400 at the
  cafe (the door refuses; the warp does not check money).
- Commit eb64068.

### Checks + end state (s78)
- Crash batch uncap_batch.sh 99 420 NX_RES=720p NX_MSAA=8 NX_FX_FXAA=1 (batch78.out): 4 x 420 s all "ok", 0 CRASH / fatal /
  VK_ERROR, 9-12 MSAA 8x twins each (new resolve path ran). User save/ md5 = save_bak_1114 (all equal);
  cache/pipelines.bin 46759561 B (grew, not shrunk).
- Shibuya 4K uncapped after the fix (FXAA, sbperf.sh): MSAA off 96.7 / 99.6, 4x 102.3 / 99.5, 8x 84.4 / 89.9 fps. At 4K
  the CPU is now the limit (off = 4x); 8x costs ~12% (was ~40%). Settings help text updated.
- Next: user test of L1 menu (by eye) + shop exits; Carabia / Anzu warps on a later save; async replay / CPU items
  (now the 4K limit too); merge perf/msaa-resolve-1114 into master after the user's test.
- Later (s78): shop -> shop warp works (Hee Ho Mart -> Seiren, tv4). Shop exit NOT verified: Hee Ho Mart exit door =
  f003_01 record [36] type 0x16 at (0, 13, 3) ints (4, 0, 1, 5, 1200) -> Shibuya f001_05 entry 1200, fixed in the shop's
  layout (same as after walking in; entry 1000 spawn (0, -2) matches the walk-in spawn). setpos into the box does not
  fire it; goto.py (now GOTO_CTL / GOTO_LOG env) stalls at z ~ -0.5 (glass door / camera-relative stick). User test.


## Milestone 5, session 79 (2026-11-14 ~12:05-, scheduled run tmsrecomp-continue-1114, user asleep; branch perf/msaa-prewarm-1114 from perf/msaa-resolve-1114 7e685ee)

Task items a (merge vehicles), b (MSAA 8x 4K) and c (L1 shop fast travel) were already done in s78; this session checked
the MSAA stutter part of b and polished.

### MSAA stutter: pipeline recipes had no sample count (FIXED; effect not measurable on this PC)
- pipelines.recipes stored no sample count and prewarm built every recipe at 1x (vk_replay.cpp prewarm,
  ms.rasterizationSamples = 1). With MSAA on, every MSAA pipeline was therefore compiled live on a fresh driver cache
  (new user, driver update, first run at 8x) = pop-in / stutter in each new place.
- Fix: recipe_record appends the sample count (4 bytes) for MSAA pipelines; prewarm accepts both record sizes and builds an
  MSAA record at today's ms_wanted() (8x seen + 4x set = the 4x pipeline; MSAA off = 1x). Older builds skip the longer
  records (their size check), so the recipes file stays compatible both ways. Only rasterizationSamples differs between
  the live 1x and MSAA pipelines (checked pipeline()).
- Measured (sbperf.sh 4K 8x FXAA, empty pipelines.bin both times): run 1 recorded 218 new MSAA recipes (3296 -> 3514);
  run 2 prewarm 3344 pipelines in 0.8 s. In-game "pipelines created" 781 / 46 ms vs 808 / 46 ms = no visible change:
  NVIDIA's own driver disk cache still hits (same as s36), so the true cold case cannot be measured here.
- Caches: backup cache_bak_1114p (pipelines.bin 46759561 B before this session); pipelines.bin is rebuilt by the runs.
- Commit 3a327b8.

### MSAA while walking (new rig agent_scripts/sbwalk.sh: sbperf + walk a square + camera turn, 40 s)
- 4K FXAA, frame lines per 10 s after the field: MSAA off 118.5 / 170.9 / 206.0 / 196.6 fps, worst gap 16-39 ms, 0 gaps
  > 40 ms; MSAA 8x 118.8 / 146.3 / 162.3 / 164.3 fps, worst gap 10-42 ms, 1 gap > 40 ms (41.6 ms). 8x costs ~20% while
  walking. No MSAA twin is created while walking (all 20 twins at the area load, 17.5 s); hitches only at load.
  The 30-40 ms worst gaps happen with MSAA off too: not an MSAA cost (CPU / streaming, see CPU items).
- Rig note: these runs log "FSR 3 upscaling on (mode 4, scene 1280x720 of 3840x2160)" (settings.ini fsr3_quality = 4)
  and still make 8x 4K twins; same as the s78 mA / mB runs, so numbers compare. Standing at the sbperf spot now gives
  116-119 fps at 8x (s78 mB 84-90, same spot by script): not explained; maybe GPU clock / the view after the A retries.

### L1 fast travel: shop exit
- Not verified again (rig cannot walk through the shop door, s78). Safety net: the L1 menu also works inside a shop
  (area 3 = f003 shops; offers the other shops + Tokyo Map), so a door that fails is not a softlock. User test.

### Checks + end state (s79)
- Crash batch uncap_batch.sh 99 420 NX_RES=720p NX_MSAA=8 NX_FX_FXAA=1 (batch79.out): 4 x 420 s all "ok", 0 crash /
  fatal / VK_ERROR, 9-12 MSAA 8x twins each, prewarm 3377 pipelines in 0.7-1.7 s. User save/ md5 = save_bak_1114.
- cache/pipelines.bin restored from cache_bak_1114p (46759561 B; the cold-cache runs had rebuilt it at 22.7 MB);
  pipelines.recipes kept (now has the MSAA records). shaders.bin untouched.
- Release ZIP rebuilt (see the reply of this session / Desktop TMSRecomp-<date>.zip). Package ships no recipe seed, so
  the prewarm fix helps a player from the 2nd visit of a place on a fresh driver cache.
- Next: user test (L1 menu by eye, shop exits, 8x 4K feel); merge perf/msaa-resolve-1114 + perf/msaa-prewarm-1114 into
  master after it; async replay / CPU items (the 30-40 ms worst gaps while walking, MSAA off too).

## Milestone 5, session 80 (2026-11-14 ~18:05-, user asked to continue after the s72 screenshot; branch perf/walk-hitch-1114 from perf/msaa-prewarm-1114 3750043)

User showed the end of the s72 transcript ("Signed in again", final steps pending) and asked whether the last session failed.
Checked: s72 finished (commit cf27d90 = notes, crash batch, RESUME line); s73-s79 ran after it; s79 ended clean (3750043,
Desktop TMSRecomp-20261114.zip 12:19, batch79 0 crashes). Nothing lost. The memory dir of this project is empty.

### Walking hitches (s79 item: 30-40 ms worst gaps while walking, MSAA off too)
- New: NX_HITCH_MS=<ms> sets the hitch log threshold (default 50); hitch lines end with the frame's draw and texture bind
  counts. NX_PROFILE=1 NX_PROFILE_SPIKE=25 for the spike samples.
- sbwalk.sh 720p MSAA off: the worst gaps are 3 frames ~0.5-2 s after the first stick move (31.0 / 31.4 / 31.6 s, field at
  21.3 s); later walking stays under 25 ms. Hitch line: pipeline creation 8-10 ms + replay 29-35 ms of a 35-43 ms frame.
- Spike profile: the game thread waits on g_pipe_lock (pipe_wait) + NVIDIA driver time. ~650 pipelines are created per 10 s
  while walking, ALL driver / pipeline-cache hits (~36 us each); the async hand-off to a worker and back cost more than
  the creation. (Profiler "runtime caller" names like t / `string' / g_submitted are data pointers on the stack, not callers.)
- Fix (vk_replay.cpp pipeline()): with pipelineCreationCacheControl (Vulkan 1.3 feature, checked at device creation, off ->
  old async path) the game thread first tries vkCreateGraphicsPipelines with FAIL_ON_PIPELINE_COMPILE_REQUIRED; a hit is
  used at once, VK_PIPELINE_COMPILE_REQUIRED goes to the workers as before (cold cache: no new stalls). NX_PIPE_INLINE=0
  = old path. Frame stats line: "(N ms, M inline cache hits)".
- A/B same build, sbwalk.sh 720p 40 s, 2 runs each: old spikes 34/32/34 and 38/37/41 ms (pipeline 7-10 ms each);
  inline 38/31/29 and 30/26/28 ms (pipeline 5-6 ms); 100% of live pipelines were inline hits. Shot hw4 correct.
- Left: spike frames have ~1350 draws, the same as normal 10-15 ms frames (all-frames log, NX_HITCH_MS=1), so the rest
  is first-use work (new combos / descriptor layouts / driver state) when new content appears, not draw count. Small
  (3 frames once per area); not pursued.
- Commit cb0e1df.
- Found after: workers + prewarm started only with the first ASYNC job, so with every pipeline an inline hit prewarm never
  ran (batch logs had no "prewarm" line). Now pipe_workers_start() runs on the first pipeline request either way (as
  before s80). hw5: prewarm 3863 in 0.4 s, walk spikes 26 / 28 ms, 4756 / 4756 inline.
- Cold check (pipelines.bin moved aside, NX_PREWARM=0): still 818 / 818 inline hits = NVIDIA's own disk cache. With
  __GL_SHADER_DISK_CACHE_PATH=<empty dir> (truly cold): 863 created, 338 inline, 525 -> workers, "draws waiting" as
  designed, no errors, worst gap 26-31 ms after load. Use that env for future cold-cache tests on NVIDIA.
  pipelines.bin restored after each (46759561 B).

### Checks + end state (s80)
- Crash batch on cb0e1df (batch80.out): 4 x 420 s ok, 0 crash / fatal / VK_ERROR, all pipelines inline (m1 8902).
- Crash batch on 2e673ac (batch80b.out): 4 x 420 s ok, 0 crash / fatal / VK_ERROR, prewarm ran in all 4, all pipelines
  inline (m1 12352). Release ZIP rebuilt: Desktop TMSRecomp-20261114.zip 18:44 (116.2 MB).
- User save/ md5 = save_bak_1114; cache/pipelines.bin 46759561 B.
- Next: user test (L1 menu by eye, shop exits, 8x 4K feel, walking); merge perf/msaa-resolve-1114, perf/msaa-prewarm-1114,
  perf/walk-hitch-1114 into master after it (linear: walk-hitch contains both).

## Milestone 5, session 81 (2026-11-15, with user; branch perf/cpu-lows-1115 from master; STOPPED by the usage limit)

User: L1 fast travel + Seiren / accessory shop entry OK by eye. Asked: big fps + 1% low work (most important), then the open bugs.
- master fast-forwarded to c8303c9 (the three perf branches; tag backup/master-pre-merge-1115 = old master).
- New frame stats line: "frames: 1% low / 0.1% low / median / p99" per 10 s; "pacing waits" on the replay line (measured 0.00 ms uncapped).
- Baseline 720p uncapped (sbperf.sh, Shibuya spawn spot): 113-118 fps, 1% low 75-97, median 8.4-8.7 ms, replay + submit 3.0-3.4 ms.
  sbwalk.sh: 118 -> 212 fps as the player leaves the spawn spot, 1% low 65 -> 152.
- Measured per frame (temporary counters, removed): 2 nvnSyncWait, 1 submit, 1 nvnQueueFenceSync, 1 present, in that order; the
  waited sync is the one fenced two frames earlier (two syncs alternate) and is never pending; no object create / destroy /
  pool registration in steady state. So the game's own design allows the renderer to run one frame behind.
- BUILT, NOT RUN (nvn_hle.cpp "render thread", vk_replay.cpp ui_sprite_smooth clock): at fps 0 / > 60 submit, queue fence and
  present go to one render thread; render_drain() before object changes; sync waits wait for their fence job; game at most
  one frame ahead; NX_ASYNC_REPLAY=0 = old path; fps 30 / 60 unchanged (jobs run inline). Expected: frame 8.7 -> ~5.5 ms.
- NEXT, in order: 1) sbperf.sh / sbwalk.sh A/B with NX_ASYNC_REPLAY=0 vs default, shots compared; 2) battle (btlperf.sh), camp
  menu movie (campcycle.sh), map change, L1 travel, live "fps 60" <-> "fps 0" switch; 3) crash batch with fps 0; 4) only then
  ZIP. If it misbehaves: default it off. Smaller CPU items seen: per-frame Cmd vector alloc / free > 1 MB (recycle the
  vectors), CallCommands copies 5%, write-watch 6%, guest job waits 6-8%.
- Open bugs not touched: enemy target highlight speed (s74 item 2), walker yaw at 30 Hz, fern black edges, OPEN LIST (s39).
- Release ZIP NOT rebuilt (Desktop ZIP = s80 build): the new build is untested.

## Milestone 5, session 82 (2026-11-16 ~03:30-04:30, with user; branch perf/cpu-lows-1115, on 7b38774)

User: play-tested the s81 dev build (private/tms/build via play.bat, nx.log 11-15 19:13, 4K fps 240): Shibuya 90-110 -> 130-152 fps
(nx.log 10 s windows: min 127.7, median 151.6). Asked for the A/B and whether DLSS upscaling works (no fps or picture change seen).

### Render thread A/B (same build, NX_ASYNC_REPLAY=0 vs default; PC slower than on 11-15, compare only inside this session)
- sbperf.sh 720p spawn spot, 3 pairs: old 80-87 / 101-102 / 96-97 fps, new 115-122 / 114-119 / 124-135 fps; median 9.6-12.3 -> 7.0-8.5 ms.
  1% low the SAME (old 42-68, new 52-72): the slow frames are not replay time. Open.
- sbwalk.sh 40 s: 177 -> 200 fps, 1% low 98-119 both, worst gap 29 / 28 ms.
- btlperf.sh 4K battle: 757-772 -> 793-839 presents per 10 s, worst gap 25-28 -> 14.6 ms. The 175-180 ms gap at the end = the 4K
  screenshot write, both paths.
- Shots old vs new (shots/shOld.png, shNew.png): same picture (crowd / cars at another moment).
- travel.sh (FLAGS=0x65, NX_FPS=0): Hee Ho Mart in and out ok. Camp menu 10 x close / open at NX_FPS=0 (to_camp.sh + loop;
  campcycle.sh does not pass env): 152 fps, 12 decoders, shot correct. Live fps 60 / 0 / 30 / 240 switches + 20 fast 60 <-> 0
  toggles while walking: alive, no hitch, shot ok. "longest frame 5000-7600 ms" after such switches is a stats artifact, old path too.
- Crash batch (uncap_batch.sh 8110 420 NX_FX_FXAA=1 NX_MSAA=0, batch81.out): 4 x 420 s ok, 0 CRASH / fatal / VK_ERROR, all 4
  uncapped on the render thread, battle cues 62 / 47 / 0 / 0. First try without the env was INVALID: build/settings.ini is now
  fx_fxaa 4 + fsr3_quality 0 (4K DLAA) and 4 instances starve the GPU (15.7 fps, no replay end, no "fps 0"). Always pass
  NX_FX_FXAA=1 NX_MSAA=0 to batches.
- User save/ md5 unchanged over the session (65a80379...). pipelines.bin 51311952 B.

### DLSS question (ANSWERED: works; the mode is read once at start)
- nx.log of the user's session: "dlss: feature 1280x720 -> 3840x2160, quality value 3" = Ultra Performance for the whole session;
  the user's later "settings: fsr3_quality = 0" only writes the ini (vk.cpp upscale_lo_scale() is a static, rt.h says restart).
  So switching modes in the menu changed nothing until the next start = "no difference".
- Measured 4K Shibuya spot, DLSS, sbperf.sh NX_RES=4k NX_FX_FXAA=4 NX_FSR3_QUALITY=q: Native / DLAA 70.6 fps (GPU waits 11.3 ms),
  Quality 97.4 (4.4 ms), Ultra Performance 106.2 (2.9 ms). 1:1 crops shots/dlss_modes_crop.png: Native sharp, Quality close,
  Ultra Performance soft ground texture. Above Quality the CPU is the limit, so Balanced..Ultra add little.
- Change: camp_settings.cpp PC page 3 row help now ends "APPLIES AFTER A RESTART." (was "Restart."). Build only, not seen on screen.
- Not done: live mode switch (twin images + NGX feature rebuild). Only if the user asks.

### End state / next
- Release ZIP rebuilt on 7a0efbd: Desktop TMSRecomp-20261116.zip (116.2 MB).
- Next: 1) 1% low at the Shibuya spot (p99 13-14 ms vs median 7-8 ms: find what the slow frames do; NX_PROFILE_SPIKE); 2) merge
  perf/cpu-lows-1115 to master after the user's OK; 3) smaller CPU items (Cmd vector recycle, CallCommands copies, write-watch);
  4) open bugs (target highlight speed, walker yaw 30 Hz, fern edges, OPEN LIST s39).

## Milestone 5, session 83 (2026-11-16, with user; branch perf/cpu-lows-1115; first part STOPPED by the usage limit)

User: reported "TMSRecomp: fatal error / Vulkan: r failed (-4)" seen while the agent ran A/B tests.

### The fatal error (EXPLAINED, no code bug)
- -4 = VK_ERROR_DEVICE_LOST from VKC(r) in vk::gpu_wait (vkWaitSemaphores). Only in gwN1.log / gwN2.log (07:29, 07:31).
- Those 2 runs were a deliberate experiment of the first part of s83: a build WITHOUT a GPU wait, to see whether the
  render thread blocks on the GPU. The GPU reads game memory directly, so freeing / reusing it early faulted (VK_EXT_device_fault
  addresses 0x18007fcf80..0x18007fd3c0, same both runs, ~2 s after the field loaded). Reverted at once; tms.exe rebuilt 07:44.
- Current build, user's real AA (DLSS / DLAA, NX_FX_FXAA=4): sbperf 3 + 1 runs, 0 device faults. Lesson: experiments that drop a
  GPU wait must never run with the user watching without saying so.

### 1% low work (Shibuya spot, sbperf.sh 720p uncapped, NX_FX_FXAA=1 NX_MSAA=0, 3 x 40 s pairs each)
- Slow frames (p99 12-14 ms vs median 7) are NOT waits (new hitch fields: render thread waits ~0, slot waits ~0-2 ms): the game
  thread's own code takes 12-14 ms, and on those frames the sampling profiler got 1 sample instead of ~12 = the WHOLE process
  stalls a few ms. Lead for next time: what stops all threads (page faults / working-set trim, DPCs, the 5 threads at 100%).
- Job-worker poll pause (YieldProcessor when SwitchToThread finds nothing, kernel.cpp svc sleep < 1 ms): 1% low mean
  50.9 (off) vs 51.6 fps (on), pairs swing +-15 both ways = no gain. DROPPED (code removed, not committed).
- Clock thread (ui.cpp vsync_thread): at fps 0 / > 60 it now Sleep(1)s until 3 ms before the tick instead of spinning a core at
  time-critical priority (at those fps it does not pace frames). First part measured 2 pairs 84 -> 107 fps 1% low (other test);
  this part at the sbperf spot: spin 53.5 vs sleep 51.4 mean = noise. KEPT for the freed core (4-core / laptop CPUs), 30 / 60 keep
  the exact spin, NX_VSYNC_SPIN=1 / 0 forces.
- Stats added: hitch line "render thread waits / slot waits", frames line "(x for a submit slot)" and "render thread waits".

### Checks on the final build
- fin1.log DLSS sbperf: 0 faults, 1% low 71.1 fps.
- Crash batch uncap_batch.sh 8310 420 NX_FX_FXAA=1 NX_MSAA=0 (m1-m4): 4 x 420 s, 0 FATAL, 0 device faults, all 4 went uncapped on
  the render thread after the replay.

### Next
1) user OK -> merge perf/cpu-lows-1115 to master; 2) 1% low: whole-process stall lead (ETW / xperf on a slow frame);
3) smaller CPU items (Cmd vector recycle, CallCommands copies, write-watch); 4) open bugs (target highlight speed, walker yaw
30 Hz, fern edges, OPEN LIST s39).

## Milestone 5, session 84 (2026-11-16 ~10:00-10:40, with user then scheduled; branch fix/live-upscale-1116 from perf/cpu-lows-1115 fe1af4a)

User (playtest 09:58, nx.log): Shibuya 80-90 fps vs 130-150 before; DLSS Quality..Performance no fps or picture change; MSAA off..8x
no fps change. Asked: fix it, no questions, ship soon, excellent 1% low on weak PCs, lowest VRAM, no VRAM leak.

### Cause (NOT a code regression)
- nx.log: "dlss: feature 3840x2160 -> 3840x2160, quality value 5" = DLAA at native 4K for the whole run (settings.ini had
  fsr3_quality 0 at start; s82's 130-152 fps run was Ultra Performance 1280x720 -> 4K). GPU-bound: "GPU waits 15.74 ms per frame".
- The menu mode changes (1..4) only wrote the ini: upscale_lo_scale() was a static read once (s82 knew: "applies after a restart").
- MSAA: ms_wanted() returns 1 while Anti-aliasing is FSR 3 / DLSS (by design: they already anti-alias), so MSAA toggles did nothing.
  The user also passed through AA 0..2 with msaa 4: MSAA copies were made and never freed (VRAM 3072 -> 5376 MB in blocks).

### Fixes (all measured)
- FSR 3 / DLSS upscaling mode applies LIVE (vk.cpp): screen-size targets are always tracked as twins (lo image only while
  upscaling is on), vk::upscale_apply_setting() at the frame end (upscale_frame_end) rebuilds the lo images at the new scale
  (old ones via g_dead after the GPU), DLSS feature / FSR context rebuild on the size change by themselves; FSR history resets when
  the scene size changes. lo_for_setting() is 0 when Anti-aliasing is not FSR 3 / DLSS (no lo images in VRAM then).
  overlay.cpp fsr3_quality() cached atomic, set by the menu. Menu help (camp + F1) no longer says restart.
- MSAA copies (vk_replay.cpp ms_prune, start of a replay): freed when their image is freed (vk.cpp free_dead_images ->
  ms_image_dead) and all at once when the wanted sample count changes ("vk: MSAA 4x -> 1x: N MSAA copies freed").
- VRAM blocks (vk.cpp free_mem): an empty device-local, non-host-visible 256 MB block goes back to the driver when its type has
  another empty block (one spare kept: no allocation hitch). Before: blocks never returned.
- Menu text: MSAA row says "Off while Anti-aliasing is FSR 3 / DLSS"; upscaling row "With FSR 3 / DLSS: renders 3D smaller ...".
- Control commands for tests: "upq N" (upscaling mode 0..4), "msaa I" (row index 0 off, 1 2x, 2 4x, 3 8x).

### Measured (agent_scripts/upqswitch.sh: Shibuya spawn spot, 4K uncapped, DLSS, live switches upq 0 4 2 0, then aa 1 + msaa 4x / off)
- uq2: DLAA 55-72 fps, Ultra Performance 113-137, Balanced 89-111; dlss feature lines 3840x2160 -> 1280x720 -> 2256x1269 -> 3840x2160
  follow each switch within one frame. 6 / 6 shots correct (contact sheet checked: no black / stretched / garbled frame).
- VRAM in blocks: 2816 MB, MSAA 4x on 3840 MB, off again -> 3072 -> 2816 MB (uq1 without the block release stayed at 3840).
- Crash batch uncap_batch.sh 8410 420 NX_FX_FXAA=1 NX_MSAA=4 (m1-m4, batch84.out): 4 x 420 s ok, 0 FATAL, 0 device faults, all 4
  switched to fps 0 after the replay, battle cues 0 / 0 / 25 / 78.

### Next
1) user OK -> merge perf/cpu-lows-1115 + fix/live-upscale-1116 to master; 2) 1% low: whole-process stalls (ETW on a slow frame);
3) weak-PC first-run defaults (settings.h, launcher); 4) smaller CPU items; 5) open bugs (target highlight speed, walker yaw 30 Hz,
fern edges, OPEN LIST s39). Scheduled task tms-recomp-s84-1241 (12:41) continues with this list.

## Milestone 5, session 85 (2026-11-16 ~12:40-18:30, scheduled then with user; branch fix/live-upscale-1116)

### Part 1 (scheduled run; commits c9f5433, a1c128e, 415d112)
- 1% low: NX_STALL_STATS=1 showed ~1050 page faults per median Shibuya frame: big command lists got fresh memory each frame.
  Now recycled: faults 1050 -> 0 per median frame, median 5.9 -> 5.5 ms, Shibuya 1% low 113-122 -> 124-134 fps.
- Handle leak: command memory Used was always reported as 0, so the game's state blocks were never freed (handles +150/s
  standing, 85k after 150 s walking, ~2 MB/s RAM). Now a real estimate; a recorded block is freed when later recordings
  overwrite its memory (as on the console). Handles stay ~7700 walking, RAM flat; walking 1% low 194-205 -> 213-217 fps.
  Battle picture correct, 0 "unknown handle", crash batch 4 x 420 s ok.
- res auto: 720p under 3 GB VRAM or integrated GPU, 1080p under 8 GB, 4K only with 8 GB+. Settings / launcher MSAA + upscaling texts
  match the s84 behaviour.
- Pipelines shared by content across moved programs: tutorial battle 1639 -> 390 pipelines created, picture same, RAM saving small.
- The run ended (10 in a row) with an uncompiled WIP: make_module(t, shared) header line missing.

### Part 2 (with user "do it: battle RAM growth, memory diagnostic, open bugs"; commits 8a0d429, ae3261c)
- Build fixed (vk_shader.cpp make_module: lookup in g_module_by_hash before vkCreateShaderModule; prewarm modules unshared).
- Battle RAM growth, measured (agent_scripts/btlmash.sh, base60 tutorial battle 4K, mash 120 s seed 7, NX_FX_FXAA=1 NX_MSAA=0
  NX_TEX_PACK=0 NX_MEM_REGIONS=1): bmr2 (before) 4746 -> 6662 MB private (+1916), bmr3 (shared modules) 4999 -> 6113 (+1114).
  Pre-battle values of both runs equal within 1 MB until 131 s. Both curves PLATEAU ~60 s into the mash (bmr3 3950 MB host
  private from 241 s on, +6 MB / 10 s at the end): driver-side pipeline / shader memory for each new battle shader set, not an
  unbounded leak. NX_MEM_REGIONS: growth in big non-heap bases ("?" = not a Win32 heap = driver). 0 unknown-handle / device errors.
- Memory diagnostic kept: NX_MEM_REGIONS=1 (memory.cpp mem_regions_report, every 10 s stats line: host private outside the guest
  reservation by allocation base, new bases by size class, top growers + owning heap), "RAM N MB private" on the frames line.
- Walker / car yaw at 30 Hz (s74 left it): actor_set_dir 0x3c8734 writes yaw +0x1c = atan2(x, z) and dirty +0x54; actor_move_update
  0x3c8d90 sets +0x54 every frame and never writes +0x1c (Ghidra headless, g.sh Decomp). town_actor_update now glides +0x1c like the
  position (shortest turn, ends at the next 30 Hz tick, snaps with a > 4 unit position jump). NX_TOWN_YAW=0 off; [movef] logs yaw.
  A/B (shibuya.sh 240 720p NX_MOVE_LOG=2, agent_scripts/yaw_steps.py): turning frames 8037 -> 45139 of ~115k, steps > 0.05 rad
  852 -> 47, p99 step 0.115 -> 0.035 rad. Shot yw1: walkers + truck face their path.
- Not touched: target highlight (needs the deterministic rig, s74 item 2), fern edges (user check in the Fortuna Office), OPEN LIST s39.
- Ghidra MCP plugin answers 404 (old extension); headless private/tms/ghidra/g.sh works.
- Checks (final build): crash batch uncap_batch.sh 8510 420 NX_FX_FXAA=1 NX_MSAA=4 (batch85.out): 4 x 420 s ok, 0 FATAL / device
  errors, but battle cues 0 / 0 / 0 / 0: m4 reached fps 0 at 191 s and ran 1000-1300 fps, the other 3 dropped to ~11 fps (one
  RTX 5070 Ti for four 4K MSAA instances) and never finished the replay; m4 itself desynced (no battle). Rig artifact (s84: 0 / 0 /
  25 / 78). Battle coverage instead: btlmash bmr4 120 s seed 3 NX_MSAA=4: 2 battles, level-up screen + field shots correct, 0 errors.
  RAM with MSAA 4x: 6571 -> 8748 MB over the mash (+2177; MSAA pipeline set on top), also plateaus. Lead: driver memory per pipeline
  (MSAA variants), pipeline count per battle.

### Next
1) user OK -> merge perf/cpu-lows-1115 + fix/live-upscale-1116 to master; 2) target highlight rig (s74 item 2: wait for Itsuki's
turn in the log, pick Attack by cursor, fixdt 120 vs 30); 3) MSAA battle RAM (+2.2 GB, plateau); 4) fern edges = user check;
5) crash batch rig: stagger fps 0 (one uncapped instance starves the rest).

## Milestone 5, session 86 (2026-11-17 ~09:20-, user asleep after a playtest; branch fix/s86-report-1117 from fix/live-upscale-1116)

User playtest 11-17 08:50-08:58 (nx_20261117_085844.log, settings 4K / fps 240 / DLSS (fx_fxaa 4) / fsr3_quality 1 / msaa 4 / fx_bloom 0 /
fx_glow 0; videos D:/OBS VIDEO/OBS/2026-11-17 08-50-11 / 08-56-16 / 08-57-25 / 08-58-10.mp4): fps, 1% low, DLSS + FSR all good. Report:
1) why the Upscaler row only has Bilinear / FSR 1; 2) launcher start always freezes ~1 s; 3) giant dress in the 2nd idolasphere glitches;
4) enemy target highlight still too fast; 5) battle start in the 2nd idolasphere goes BLACK before the 3-character card; 6) look at
Touma / Itsuki battle entries for something wrong. Saves backed up first: private/tms/save_bak_1117 (+ md5.txt); testsave/u17 = copy.

### Rigs (private/tms/agent_scripts, all on testsave copies)
- i2.sh <tag> <fps> [env] (DOWN=n = Load cursor down n): u17 copy, Load slot 7 (DOWN=0: Shibuya 106 stairs before the gate) or slot 8
  (DOWN=1: idolasphere 2 1F entry room). NX_SHOT_TAG=<tag> so parallel rigs do not overwrite each other's shots.
- i2fly.sh: slot 7 -> gate -> Go Inside; 48 shots 0.5 s apart over the floor intro camera fly (shows the giant dress).
- i2btl.sh: slot 8, wanders + sword swings until an encounter; a watcher shoots from the fld_mevt_btlmove cue (NSHOT / SHOTGAP).
- i2tgt.sh: i2btl + waits for BTL_TURN + A A -> target selection (often lands in the intro: send A A again at the wheel).
- snap.sh <tag> <n> <out> [cols] [w]: tile the newest n shots. Runs at NX_FPS=30 from the title failed to load (Load menu timing):
  start at 240 and switch with "fps 30".

### 3. Giant dress flails (FIXED, measured)
- Reproduced with i2fly: at fps 30 the dress holds one pose for 4.5 s, at 240 the arm / sleeve jumps between two poses every frame.
- NX_ANIM_SHORT=1 (new probe on anim_policy_loop): the only short skeletal loop is start 0 end 1 (model_skel_update+0x40). The
  Switch steps 2 frames per update, so a loop of length <= 2 always lands on its start; above 30 fps the frame sweeps 0..1 and blends
  to the end key = another pose.
- Fix (hle_sys.cpp anim_policy_loop now an HLE_FN): loops with end - start <= 2 return their start. NX_ANIM_LOOP_PIN=0 off.
  Verified g240 shots: same pose as 30 fps through the fly. Commit 91a4624.

### 5. Black battle start (FIXED, measured)
- Normal and first-strike encounters both freeze the field (zoom-blurred capture) behind the green lines. At 720p and at 4K without
  DLSS it is correct; only 4K + DLSS / FSR 3 upscaling (Quality 2560x1440 of 3840x2160) shows black. 720p + DLSS has no lo twins
  (lo_for_setting: lo >= hi -> 0), so it hid the bug.
- Cause: the capture target is a 1280x720 screen-size target = an upscaling twin. It is written while the frame runs on the lo twins;
  the transition's later frames have no 3D scene, start on the full-size twins and sample the never-written hi image (bind path
  uploads pool data = black).
- Fix (vk.h Image::wgen / twin, vk::mark_written at every write: render target bind, buffer->tex, tex->tex copy, clear, FSR output;
  vk_replay.cpp twin_sync): a twin sampled or used as a copy source whose other size has a newer write is blitted over first (colour,
  linear). Stats line "N upscaling twin syncs": 0 in Shibuya free roam (4K DLSS sbperf ts1 95.5 vs NX_TWIN_SYNC=0 ts0 92.5 fps = noise),
  a few at the title / loads. Verified bd: field visible behind the lines at 4K + DLSS. Commit 0d744b6.

### 2. ~1 s freeze after every start (FIXED, measured)
- Every log (user + rigs): "hitch 1137-1282 ms ... (rest: game code, loading)" ~5 s after start on the title screen, between
  "skills: Attack Session on" and "help texts extended": skill_help_update's find_bytes scanned the whole 4 GB guest space byte by byte,
  twice, on the game thread. Not launcher specific (play.bat had it too).
- Fix: one memchr scan for both patterns on a std::async worker; the game thread re-checks each hit and patches when it is ready.
  t1.log: no title hitch, the same 6 msbt copies extended (scan done 0.8 s after start of search, off-thread). Commit 1b809bf.

### 4. Target flash too fast (FIXED, measured)
- i2tgt + consecutive-frame brightness of the target (/tmp/pulse.py idea: mean of the target box per shot): before, period 30 frames at
  BOTH fps 30 (1 s) and 60 (0.5 s) = per-frame counter.
- Found: dumps of the unit block (units from the new NX_DEBUG_BATTLE "weak marker unit" log, bcc6b640..) -> u16 counters at
  unit+0x710 (+0x1c stride x4) -> watch: writers 0x2ce490 / 0x2ce418 (generic tween: counter +1 per call, t = counter / length),
  stepped by 0x2ce764 (RGB tween x3) from 0x30df68 = per-unit colour effects update (5 tweens incl. the flash).
- Fix: names.txt 0x30df68 btl_unit_color_update (RE-LIFT done: lift.py, 20642 hooks); hook steps it only on battle 30 Hz ticks
  (tick_due, Switch pace). NX_UNIT_COLOR30=0 off. After: 240 fps ~1.7 cycles in 240 frames (was 8). Commit b4ef7f0.

### 1. Upscaler row (ANSWERED + text)
- FSR 3 / DLSS are temporal upscalers that replace the game's anti-aliasing, so they sit under Anti-aliasing, with their render size in
  the "FSR 3 / DLSS upscaling" row. The old "Upscaler" row (Bilinear / FSR 1) only stretches the finished frame when Resolution is below
  the screen. Renamed to "Screen scaler" (F1 menu, camp PC page, launcher) with help saying where FSR 3 / DLSS are. Setting key unchanged
  (upscaler). Build only, not seen on screen.

### 6. Touma / Itsuki entries (ANALYSED, nothing fixed)
- They (and Tsubasa) fight in swim trunks / bikini after "Carnage Form": all three match = an equipped costume set, not missing models.
- Long pure-white frames in the transformation: the game's flash (bloom / glow are OFF in the user's settings, so not our post); particles
  are dt-scaled (anim_update hook). No fps-dependent cause found; a 30 vs 240 comparison of the same intro was not achieved (intro
  character is random, 30 fps rigs failed at the title). If the user means something else, ask for a timestamp.

### Checks + end state
- Crash batch uncap_batch.sh 8610 420 NX_FX_FXAA=1 NX_MSAA=0 (batch86.out, final build b4ef7f0): 4 x 420 s ok, 0 FATAL / device
  errors, battle cues 52 / 121 / 0 / 0. User save/ md5 = save_bak_1117/md5.txt.
- Release ZIP Desktop/TMSRecomp-20261117.zip (116.2 MB) built 10:29 with all s86 fixes.

### Next
1) user playtest of items 2-5 (4K DLSS 240); 2) (done) crash batch; 3) merge perf/cpu-lows-1115 +
fix/live-upscale-1116 + fix/s86-report-1117 after the user's OK; 4) OPEN LIST s39, MSAA battle RAM (+2.2 GB plateau), fern edges;
5) optimization: Shibuya 1% low (whole-process stalls), weak-PC defaults.


## Milestone 5, session 87 (2026-11-17 ~14:10-, scheduled run tms-recomp-s86-1411, user asleep; branch fix/s86-report-1117)

Continues s86 (report items 2-5 fixed there). Commits fbfb75c (probe + rigs), 1476f59 (button atlas hitch). Not merged, not pushed.

### Item 6 (Touma / Itsuki entries): verified, nothing wrong left
- User video 08-58-10 (frames private/tms/user_video_1117/z_shards.jpg): the 3-character card shatters into BLACK shards. Same
  cause as item 5 (card = screen-size capture = upscaling twin): with the s86 twin sync the shards carry the card picture
  (i2btl sh6 at 4K + DLSS Quality: pink / blue / face pieces over the arena). Fixed by 0d744b6.
- Long pure white at "Carnage Form!": measured with the new NX_SHOT_LUM=1 probe ("shots N" logs each frame's mean brightness,
  no files) + rig i2lum.sh (slot 8, real time, log timestamps): m30 vs m240 white curves have the same shape and length
  (>230 brightness 0.80 s at 30 fps, 0.93 s at 240; 0.2 s buckets ...166 209 238 253 254 250 223... at both). = the game's own
  flash at Switch pace, not an fps bug.
- Rig notes: "fixdt" is useless for voice-gated sequences (the card waits for the voice line in real time). Per-frame readback
  (NX_SHOT_LUM / many shots) slows the battle load itself (btlmove -> MAP_DEFAULT init 0.3-1.1 s normally, 6-16 s while
  shooting every frame): rig artefact. "fps 30" is refused live; NX_FPS=30 runs need WAIT=20 (i2.sh title wait).

### Item 1: rows already together
- Resolution -> Screen scaler -> Anti-aliasing (FSR 3 / DLSS) -> FSR 3 / DLSS upscaling -> MSAA are adjacent on the page with
  s86's help texts; no regroup.

### Button atlas hitch (FIXED, measured; user log nx_20261117_085844)
- Every load of a controller-icon atlas painted the WHOLE atlas with a Direct2D software target: title HUD atlas
  ea576a96 (2048^2) = 147 ms hitch at the title, battle atlas 37357058 (4096^2, 64 MB) = 86-87 ms hitch each time it loads
  in battle (twice in the user's session), plus two 64 MB copies.
- Fix (pad_icons.cpp pad_icon_atlas): paint only the cells' bounding box (battle atlas: 34 x 126 px), cache the painted box per
  atlas hash + style, paint level0 in place (vk_texture.cpp). Log line now has the paint time. Title atlas 15.5 ms incl. the
  first D2D / DWrite start, no hitch line after it (was 144 ms). NX_PAD_ICONS_TEST selftest old vs new exe: 14 atlases, 8 differ
  in 8-49 edge pixels (max 47/255, rasterizer tile origin), not visible.

### RAM growth in the user's session (ANALYSED, driver-side, no fix)
- User log: process private 6.6 -> 15.7 GB over the session, never flat; follows new content (shader modules / programs made),
  not pipelines (pipelines flat at ~2000 while RAM +4.5 GB). Battle mash (btlmash 300 s, 4K DLSS): +2.8 / +1.4 GB with the UHD
  pack (same seed, run-to-run noise +-1.4 GB), +1.0 GB pack off; all plateau when content repeats.
- Ruled out by measurement: command handles (13 MB capacity in all); pipeline cache save cycle (10 x create-from-file / merge /
  destroy, same thread and new thread each: flat); destroying all 633 game pipelines (debug "pipeflush"): 0 MB returned;
  pack files read but never uploaded (a 30 s drop rule never fired).
- What grows (NX_MEM_REGIONS + a one-off dump of the top unattributed base): NVIDIA's shader compiler heap (GL extension
  strings of compiler contexts, SPIR-V copies, hashed option text), one reservation committing 100s of MB. Not returned by
  destroying pipelines. All experiments reverted. Leads if needed: pipeline layouts / set layouts per new combo (never
  destroyed), shader modules per moved program, AMD/Intel behaviour (only NVIDIA measured).

### Checks + end state
- Crash batch uncap_batch.sh 8710 420 NX_FX_FXAA=1 NX_MSAA=0 (batch87.out, build 1476f59): 4 x 420 s ok, 0 FATAL / device
  errors, RAM 5.0 -> 5.3 GB each; battle cues 0 / 0 / 0 / 0 (known rig artefact, s85). Battle coverage instead: 7 btlmash runs
  (4K DLSS, 150-300 s) + 8 i2btl / i2lum idolasphere battles this session, 0 crashes. User save/ md5 = save_bak_1117/md5.txt;
  cache/pipelines.bin 54.4 MB (grew, not shrunk).
- Release ZIP Desktop/TMSRecomp-20261117.zip (116.2 MB) rebuilt at the end with both s87 commits.

### Next
1) user playtest of s86 + s87 (4K DLSS 240, PlayStation pad: title / battle no button-atlas hitch); 2) merge perf/cpu-lows-1115 +
fix/live-upscale-1116 + fix/s86-report-1117 after the user's OK; 3) RAM growth: test on AMD / Intel, layouts per combo;
4) fern edges (user check), weak-PC defaults.

## Milestone 5, session 88 (2026-11-18, with user; branch fix/s86-report-1117)
User: "Poison Skewer help says causes Poison but no %"; "custom battle song SMT 3 Fiend is distorted so bad".

### Custom music: 40_SMT3_Fiend Battle.adx played as noise (FIXED, measured offline)
- Header byte 0x13 = 0 (the other 199 files in BGM_42.AWB: 9), but its frames ARE keyed with the P5R key (first scale words
  match 45_SMT3_Boss Battle's key stream). ext_bgm.cpp trusted the flag -> raw keyed scales -> 60% of samples clipped.
- Fix (Adx::open): flag 0 -> sum of the first 64 scale words plain vs keyed; keyed 4x smaller -> enc. adx_check (tools/tests)
  over 20 s: clipped samples 581589 -> 7, RMS 24021 -> 7281, no >20000 jumps. All 200 files decoded: Fiend no longer in the
  clipping top list (remaining top: 358_Catherine_Victory 4.7% clipped = hot master in the file itself, not fixed).
  Not heard in a real battle.

### Skill help: ailment chance (FIXED, boot checked, NOT seen on screen)
- StSkillTable: +0x30 ailment chance %, +0x32 ailment (2 Poison, 3 Sleep, 4 Confuse (label PANIC), 5 Charm, 6 Seal (CLOSE),
  7 Stun (HIT_STOP); 8-11 enemy-only, 999 = always). Poison Skewer (CS_POISON_SPEAR) 50, Poisma 60, Poisma all-foes 40.
- skill_details: "[Power 28, hit 95%, Poison 50%, one foe]"; pure ailment skills (power 0, had no suffix) "[Poison 60%, one foe]".
  Chance shown only for ids 2-7 and 1-100%. Longest line ~91 chars (Panic Bow). Boot: 952 texts x 6 languages, no crash.

### Open (answer to "what is not done")
- Merge perf/cpu-lows-1115 + fix/live-upscale-1116 + fix/s86-report-1117 to master (user OK); RAM growth (NVIDIA compiler
  heap; AMD/Intel untested); fern edges; weak-PC defaults; OPEN LIST s39: clean-PC test, 5 shader misses, chapter card speed,
  camp blur at 4K, O = Apply dialog, Quick Session icon, Attack Session (done s50?), FSR 1.


### s88 later: user closed items + merge
- Merged to master (fast-forward, user OK 2026-11-18): perf/cpu-lows-1115, fix/live-upscale-1116, fix/s86-report-1117 (df3d119).
- User closed from OPEN LIST s39: chapter title card speed (OK), camp blur at 4K (improved, OK), O = Apply dialog (done),
  Quick Session icon (done), FSR 1 (done).
- Still open: RAM growth on AMD/Intel (needs a tester with such a GPU), fern edges (user look at the Fortuna Office fern with
  the UHD pack on), weak-PC defaults (agent work, no user input), clean-PC test, 5 shader misses, UHD ZIP rebuild (-Uhd).

### s88: --set flag + self-contained shader translator (branch feat/cli-set-portable-shaderc)
- tms.exe --set key=value (repeatable): same as a settings.ini line, this run only, not saved (main.cpp, before
  load_settings; env beats the ini). Verified: a run configured only by --set (log, save_dir, replay, window, res,
  mods_disabled=uncensored) -> "fs: mod uncensored off", log at the --set path, settings.ini unchanged.
- Release shaderc\ = self-contained publish (private/tms/shaderc_sc, 198 files, 81 MB unzipped; README.md step 4b) with the
  dev app DLLs copied over it (cp -p) so the cache stamp (NxShader.dll size + time) is unchanged: players keep shaders.bin.
  tms.exe / shaderscan.py / setup.py run shaderc\NxShader.exe when shaderc\hostfxr.dll exists, else dotnet NxShader.dll
  (dev). Verified with dotnet removed from PATH: shaderscan pack_020_effect into an empty cache = 4399 translated, 0 failed;
  the 1015 shaders also in the player cache are byte-identical. README.txt: no .NET requirement.
- Rebuilding the self-contained folder: redo step 4b, then the cp -p, or players lose their shader cache.

## REFERENCE: release basics for a recomp / decomp (r/decomps open letter, 2026-11, RecompLauncher dev)
The six asks, and where TMSRecomp stands (2026-11-18):
1. One executable, no "builder exe that builds the game exe": OK. setup builds game.dll (not an exe); tms.exe runs on its
   own; launcher opens Setup only when the game is missing (launcher.cpp game_ready).
2. Portable by default (everything in the folder; delete folder = gone): OK since s88 (.NET install removed). Remaining
   outside writes: GPU driver shader caches (driver-owned), DLSS registry READ only.
3. Tarball next to the AppImage: n/a (no Linux build).
4. CLI flag for everything: OK since s88 via --set key=value + --data; launcher --page / --setup.
5. Native Linux: NOT done. Core is SDL3 + Vulkan; Windows-only parts: Win32 launcher, Direct2D/DWrite pad icons,
   SHBrowseForFolder, DLSS registry lookup, Win32 crash handler / process spawn (17 files include windows.h).
   Cheap first step: test under Proton / Wine.
6. Ask before building big things: process advice.
Reference project: LostOdysseyRecomp (github.com/freefrank/LostOdysseyRecomp, Xbox 360, GPL-3.0, v1.1.0): one exe with a
built-in importer (folder / default.xex / ISO / GOD), Windows ZIP 147 MB portable, Linux AppImage 85 MB + .tar.gz (for
RecompLauncher) + Flatpak, macOS DMG, Android APK 45 MB; flags --game --install --add-to-steam --setup
--prepare-shaders-only; shaders downloaded or compiled once; recomplauncher.json in the repo. The 45 MB APK (no compiler
on Android) means the recompiled game code ships INSIDE its binaries (README: "No game assets included" = assets only).
TMSRecomp ships no game code (game.dll built on the player's PC from their dump): that is why it needs the setup step;
matching "one exe with code inside" would mean shipping Nintendo's code = a legal choice, not a code fix.
Ideas from it for later: --add-to-steam, a recomplauncher.json manifest, Linux tarball/AppImage, shader download option.

## Milestone 5, session 89 (2026-11-20, with user; branch fix/turn-end-cross-1120)
User video 2026-11-20 03-34-08 (event m1029_01, 2nd idolasphere boss room, ~22 s): on "She was always working so hard!"
Tsubasa turns to Itsuki instead of facing Ayaha. Save slot 9 reproduces it by itself (load -> party walks in -> event).

### Turn end crossed in one update (FIXED, measured)
- Script: message 030 runs Seq_c17_03 = chrRotTo(Tsubasa, 280 deg, false, 0.6) (table {-53.4, 0, -4, 280}); the turn clip
  (action 131, 60 frames) is read by _chrActorRot each 30 Hz resume.
- 240 fps: the clip went 59.95 -> past 60 in ONE update, so it chained to the next clip without ever sitting on the end frame;
  the s59 hold (needs cur >= end before the update) never fired (0 "held at end" in the run) -> wrong yaw.
- Fix (hle_sys.cpp chr_motion_update): remember each chr's turn frame rate (frames per game second, last update); if this
  update would reach the end, put the frame on the end and hold (same 0.1 s hold as s59).
- Verified (agent_scripts/tsu1029.sh <tag> <fps>: testsave/u20 = user saves with Load cursor slot 9; shots at +0.5/1.5/2.5/3.5 s
  after voice EVT_m1029_01_0030): before ts240 shot 1 = Tsubasa in profile toward Itsuki, ts30 = facing front; after (tf240)
  = facing front at every offset like ts30; log "held at end 59.99" for her, plus one more turn held in the same event.
- Rig notes: no A presses after Load (A skips event lines; slot.sh spams A); the event starts ~3 min after load.

## Milestone 5, session 90 (2026-11-20, with user; branch fix/unity-prime-movie-1120)
User: merge fix/turn-end-cross-1120 (done, fast-forward to master). Report (video 08-40-07 + saves 11, 12): 1. Carnage Unity
audio late near the end; 2. Radiant Unity movement stutters though fps is flat; 3. after Tsubasa's transform before the
Aversa boss: broken scene. User saves backed up first: private/tms/save_bak_1120 (+ md5.txt); testsave/u21 = copy.

### 3. Aversa: mod movie m06 showed old movie frames (FIXED, measured)
- Event m1033_01 runs m1033_03 then PlayMovie("m06") then evtChangeBattle. The uncensored mod's pack_050 replaces m06, m07,
  m12 with Sofdec.Prime / MPEG-1 streams (mpeg_codec 1, 1280x720; stock = VP9 9). CRI MPV (software, in game code) decodes
  them; the game copies each frame (Mana 0x6dbc5c, memcpy per row at pitch desc+0xc) into linear R8 Y/U/V textures.
- Pitch = game helper 0x4fd820: align(row, nvnDeviceGetInteger(0x38)) = LINEAR_TEXTURE_STRIDE_ALIGNMENT; the real driver
  (run on our HLE device) answers 0 (analysis/nvn_real.txt; 0x39 = 0x80) -> pitch 0: all rows on row 0, the rest of the
  plane kept an older movie's NV12 frames (title logo m00 in rigs; camp key art in the user's run, read as Y/U/V = green +
  dots, red/green bar). The movie still ran its full 60.0 s (1801 frames), then the battle started.
- Fix (nvn.cpp): nvnDeviceGetInteger wrapped: 0x38 -> 32 when the driver says 0 (Maxwell pitch unit). Verified: m06 anime
  plays in colour (rig agent_scripts/aversa.sh: slotn.sh slot 12, walk up, A through m1033_03, shots); mod off = stock VP9
  m06 fine before and after. Camp 4K swap still matches (campcycle.sh, "movie plane 1280x720 -> 4K"). Commit ab7dc0a.

### 1. Carnage Unity timeline behind the song (FIXED, measured)
- Unity performances = Lua FusionDemo (sound time table in 30 Hz frames, timeChecker). script_resume_all set acc = 0
  whenever a script started; the demo starts actions / effects / camera steps constantly -> frame-counted timeline lost
  time vs the real-time BGM. Rig agent_scripts/cunity.sh <tag> <fps> (slot 11 -> Chrom -> Epee): SE vs table frames.
- 240 before: a +1.2, b +1.1, c +9.5, d +10.4, e +11.3 frames (0.38 s). Fix: the early resume borrows the next tick
  (acc -= 1/30, at most one tick of debt). After: +1.2 / +1.2 / +1.1 / +2.0 / +2.2..3.0; 30 fps reference -0.1 throughout.
  Resumes now exactly 30 per game second (temporary counter). Remaining ~1 frame = the new timeline's first tick. cfb75ae.

### 2. Radiant Unity cast stutter (FIXED, measured)
- NX_MOVE_LOG=1 in the performance: Itsuki + Chrom actors 81 script steps each "kept" (shown as 30 Hz jumps): flying
  4.2-7.9 units per 1/30 s > the s52 4-unit cap (teleports >= 39). Others moved by the script every 2nd resume: spread over
  one tick -> 5 frames moving, 5 still. (The 60 Hz UI gate is not it: uigate 0 no better.)
- Fix (actor_move_update): a step < 16 units is spread when the actor's previous step came within ~3.5 ticks (moving),
  over that measured interval (1-3 ticks); < 4 as before otherwise (a cutscene's first placement of ~14 units still cuts).
- Measured (agent_scripts/runity.sh + movesmooth.py, NX_MOVE_LOG=2): main pair frames showing motion 975 -> 1215, kept
  81 -> 9 (+ teleports); 15 Hz actor now moves every frame (0.067 / 0.153 per frame). Regression tent.sh (save 3 walk,
  240): std/mean 0.001 for 3 of 4 actors, jolts 2 (baseline) -> 1. Commit b26daf2.
- fixdt bursts: shots in a burst at normal dt are ~500 ms apart (BMP write) -> use "fixdt <fps>" + "shots N" (runity.sh).

### Rig notes
- agent_scripts/slotn.sh <tag> <fps> <slot> [env] (new: testsave/u21, Load cursor byte 4 = slot, no A after Load). By mistake
  it first overwrote slot.sh; slot.sh <tag> <savedir> [env] was rebuilt from its callers (A until the field, <tag>.pid).
- Not checked: m07 / m12 (later chapters; same codec, same path), crash batch on this build.

## Milestone 5, session 91 (2026-11-20, user playtested s90: all three fixes OK, merge OK)
- Merged fix/unity-prime-movie-1120 to master (fast-forward, b9720b0). New branch fix/help-text-exp-1120.

### Skill help cut off in the battle HELP bar (USER 11-20 screenshot, Itsuki's weapon Special Performance)
- Cause: OUR suffix (skill_details, setting skill_details): the text "(Phys/Sword) Heavy attack that lowers weapon resistance
  for one round. (Special Performance)" is 94 characters (the bar joins the msbt lines), + " [Power 120, hit 120%, one foe]"
  = 125. The user's shot: ~122 characters reach the screen edge (14.5 px each at 2000 wide). The game's own longest skill
  text is 120 (vanilla and the mod's USen SkillInfo.msbt are the same; the mod's JP copy is English too).
- Fix (hle_sys.cpp): help_width(text) (newlines 0, non-ASCII 2) and a 112 budget: the suffix drops the target, then all but
  the power, then itself. Verified on screen (agent_scripts/btlhelp.sh: slot 12 -> Aversa battle -> right, A, down x5):
  "... (Special Performance) [Power 120]" ends at x 1127 / 1280; short skills keep "[Power 30, hit 110%, one foe]".

### Sub Cast EXP (USER 11-20: "EXP shared between party members, is it right? option to disable")
- The game's rule (decompiled btl_add_reward 0x2cb2d4): per defeated enemy, EVERY joined member (0x35304c(id), ids 1..7) gets
  the full EXP x level-gap factor (100% same level; lower level up to 200%; higher level -2.5 x d x (d+1) %), x (+0x156 + 10) %
  when unit flag +0x83c & 0x40000000. Not divided: s91 log "EXP 610 x5 ... 1:+3355 2:+3355 3:+3355" (level gap 110%).
  Sub Cast members get the same as the front line.
- Battle actors: 0..2 = the front line (data +0 = character id), enemies follow (3+ with three members; enemy ids seen 8, 33,
  56, 57, 66, 108, 109, 151, 152). Unit data +2 is NOT a slot (Tsubasa and Touma both 1).
- Setting sub_exp (default 1 = the game's rule; F1 / L3+R3 "Sub Cast EXP", native PC 3/3 row 10, settings.ini comment):
  0 = btl_add_reward hook puts back the EXP of members whose unit is not actor 0..2 when the enemy falls. Log per enemy:
  "battle: reward ... members 1:+N 4(sub):+N undone".
- Verified: front line keeps its EXP with sub_exp 0 (slot 12 Aversa battle, agent_scripts/subexp.sh). NOT verified: a real
  Sub Cast member (the user's saves u21 slots 12 / 20 have only Itsuki, Tsubasa, Touma in battle); a mid-battle swap.
- Debug NX_ENEMY_HP1 loop now skips party ids 1..7 instead of starting at actor 4 (enemies start at 3 with three members:
  Aversa was never set to 1 HP and the party lost).
- Rig note: analysis/base60.rec no longer reaches the tutorial battle (replay finished in the field; likely the s90 Lua resume
  timing change shifts the replay). btlui.sh / btlmash.sh / tutexp.sh depend on it: re-record when needed.

### EXP level-gap penalty setting (USER 11-20: RESULTS "Exp 630", Touma "Next Lv 179", no level up)
- Answer: the RESULTS "Exp" panel is the raw sum (battle +0x528); each member gets per enemy 100 - 2.5 d (d + 1) % when d =
  member level - enemy level > 0 (d 1 95%, 2 85%, 3 70%, 4 50%, 5 25%, 6+ 0); below the enemy +10% per level (20% when byte
  +0xd of **(lit) + 0x520f8 < 2, probably difficulty), max 200%. So Touma's share of the 630 was < 179.
- Setting exp_gap (default 1 = the game's rule; F1 "EXP level-gap penalty"; settings.ini comment): 0 = btl_add_reward hook lifts
  a member above the enemy's level to the full EXP (x the game's flag 0x40000000 bonus). Member level = unit data byte +8.
- Native settings: new page PC 4/4 (camp_settings.cpp k_pages[4], L / R cycle of 5): rows 0-2 empty sliders, row 3 Sub Cast
  EXP (moved from PC 3 row 10), row 4 EXP level-gap penalty. Checked on screen (slot 20 copy, Y > System > Settings > L): both rows show On,
  left -> Off, log "settings: exp_gap = 0". On is the last choice: right does nothing there (no wrap), same as every page.
- Verified (agent_scripts/gapexp.sh: slot 20 d003_02 5F, setpos -96 151 -77 onto a Man o' War group, party Lv 15, x1 EXP):
  exp_gap 1: per enemy L10 35 -> +8, L12 50 -> +35, L14 68 -> +64 (= the formula); RESULTS Itsuki Next Lv 437. exp_gap 0
  (s20b, same save, same first battle + a second): +35/+50/+68 "full"; after both battles RESULTS 229 = 552 - 188 - 135, so
  the RESULTS bars use the patched battle +0x52c values (with the game rule it would have been ~359).
- Rig flake: the symbol is not always at -96 151 -77 (gapexp.sh re-teleports every 3 s; still missed twice); title load
  sometimes lands on slot 1 (WAIT=18 helps).

### Battle retry after a loss (USER 11-20 request; scoped first, then the user chose A: true restart; BUILT below)
- Wish: on a party wipe (random or boss battle) a game-styled prompt to restart that battle from turn 1 with the HP / EP /
  items it started with.
- Found: Battle/Event/btl_game_over.lua (pack_999_lua) is visual only (GameOver(): audience off, spotlight, map colour /
  light 0.3, sprite anim). After it the game goes to the title (s91 sx0 run: Aversa loss -> title, LOAD highlighted). No
  game retry path. btl_main 0x2c6ca8 states: 0..5 setup (units +0x36.. 16 slots), 6 battle loop (-> 7 / 9 / 0xb), 0xb..0xd
  end (0xd builds the result record -> result flow 0x318a30), 0xe -> 0xf = done (+0x14 = 1). Battle Lua env init 0x2e2b5c
  loads btl_game_over. Persistent party data (**0x9ef37c + 0x10, save layout) is the pre-battle state until RESULTS writes
  back (s42), so a snapshot at btl_open_chance holds HP / EP / items as the battle began (items: whether battle use writes the
  inventory at once is NOT checked).
- Options given to the user: A) true restart (snapshot at battle start, on the wipe restore it and request the same battle
  again: needs the battle request path for symbols and for Lua boss events + the defeat branch; multi-session, risk for boss
  events that wait on evtGetBattleResult 0x43f174); B) checkpoint retry (snapshot at battle start; on the wipe restore it and
  return to the field before the encounter / boss event instead of the title).

### Battle retry: built (USER chose A, true restart; hle_sys.cpp, setting battle_retry default 1)
- Battle request R = *0x9ef778 (0x290610()): +0 / +4 result (2 = lost), +8 encounter (Aversa 55), +0xa.. return map; filled by
  Lua ChangeBattle 0x448cfc (boss events: evtChangeBattle) or the field, then the jump flag (*0x9f0464 -> 1, 0x46c1f8) makes the
  field ask scene_change 0x49c420(3) (= battle scene). Battle task update 0x290808 -> btl_main; end 0x2909c8 (btl_task_end):
  state 0 waits for the battle (0x2ca754); battle (**0x9ef428) +8 == 2 -> screen_fade 0x20bc0c(0, 30, black, 3) -> state 1 ->
  0x28004c(..), scene_change(0x25) = GAME OVER -> title (0x24); otherwise state 3 -> result flow -> scene_change(0xe).
- Loss sequence (battle main states 6 -> 0xb -> 0xc (~6.6 s) -> 0xf): death voice line, then btl_game_over.lua GameOver()
  (btlSetMapColorScale / LightScale 0.3, btlPlaySpriteAnim = GAME OVER sprite) and a Lua FadeOut(BLACK, 20)
  (screen_fade from 0x2d02d4) - these cover any window.
- Built: btl_setup_units keeps the game data (**0x9ef37c + 0x10, 0x535c0 bytes = save layout: HP / EP, items, flags) and R
  (0x20 bytes); the battle scene id = the last scene_change before it. btl_task_end hook: battle +8 == 2 and main state >= 0xc,
  1.5 s after -> the game's own Yes / No box (Lua ShowDialogBoxCancelType path: dlg = 0x246a20(1), 0x2400d0(dlg, 2, UTF-8
  "Retry the battle?"), cursor put on Yes via dlg +0x34 = 0, SND_ID_SE_SM_SELECT); task held (returns 0) until A (pad 0x20:
  choice dlg +0x34) or B (= No); close = window vt+0x1c; SE 797 / 798 via 0x25e840(0, 0, 1, id, [sp] 0). While it is up:
  btl_main held in 0xc, lua_btlSetMapColorScale / LightScale / PlaySpriteAnim and screen_fade return at once (else black
  over the box). Yes: the game's fade, then scene_change(0x25) is swapped for the battle scene after the game data + R are
  put back. No: the game's fade -> title (without the dim / GAME OVER sprite, skipped while the box was up).
- Traps found: 0x25fed4 is NOT a sound effect (it formats a voice FILE path): calling it with "sy_decied" left the next
  battle stuck in btl_main state 0 forever. The SE name lookup 0x42e694 reads a Lua table: crashed from a hook (ids from
  ScriptCommon/Sound/SoundIdTable.lua, a TEXT Lua file in the pack). Pausing script_resume_all did not stop the dimming.
- Hooks added to names.txt (re-lifted): scene_change, btl_task_end, screen_fade, lua_btlSetMapColorScale,
  lua_btlSetMapLightScale, lua_btlPlaySpriteAnim.
- Verified (Aversa boss, slot 12 copy; rigs agent_scripts/bossretry.sh, retrywin.sh; debug NX_PARTY_HP1 / NX_RETRY_TEST =
  party at 1 HP before the first retry, enemies after; NX_RETRY_LOG): box over the live battlefield for 12 s (no dim); Yes
  -> ROUND 01, HP / EP 316/158 141/167 276/101 = before the battle; second wipe -> box again -> B -> title; retried battle won
  -> RESULTS -> scene 0xe (field) as normal.
- NOT verified: a random (symbol) encounter (same request + scene path; slot 20 symbols would not spawn for the rig), an
  item used before the wipe coming back (follows from restoring the save-layout block), the boss story event AFTER RESULTS,
  scripted story losses (the box needs the game's own game-over test +8 == 2, so they should not show it).
- Settings: F1 "Retry lost battles", native PC 4/4 row 5, settings.ini battle_retry.

## Milestone 5, session 92 (2026-11-21, USER playtest of s91 build: 3 OBS videos, D:/OBS VIDEO/OBS 01-01-11, 01-02-28, 01-03-36)
- User: random symbol battle retry works (video 01-03-36: Yes -> "SAVAGE ENEMY ENCOUNTER", same fight). Slot 12 symbols did not
  spawn for the s91 rig because Rooftop Stairs has no enemies (user); symbols are inside the building (slot 20, 7F).

### Dungeon music over the retry box and into the retried battle (FIXED)
- Log (user nx.log + rig bg1, NX_BGM_LOG=1 = new debug lines "bgm: by name ... lr" / "bgm: restore ... lr"): Cue:b01_d_daitama
  started exactly at "retry: prompt" and again at "retry: answer" = our play_se calls. Lua PlaySe = 0x456734 -> 0x25e840(r0 1
  (4 / 7 by mode), r1 sound index, r2 0, s0 = s1 = 0.0) (armdis 0x4567e0..0x456810). s91 called it (0, 0, 1, id): index 0 =
  b01_d_daitama (a BGM on an SE player: looped through the box and the retried battle). Fixed: (1, id, 0), s0/s1 = 0.
  Rig bg2: prompt -> Cue:sm_select, answer -> sy_decied, no b01; the retried boss battle starts b50_b_boss as before.
- The game stops its battle track at the loss (ExPlayer_Stop before btl_main 6 -> 0xb); custom battle music (P5R AWB) kept
  playing under the box (user log "rms custom 941"): btl_task_end now calls custom_bgm_stop("battle lost") on the loss test.
  Still heard under the box: the game's own bpro_gameover sting (btl_game_over.lua path, ~2.7 s, vanilla). Not muted.

### Field KO mark (red diamond over Itsuki when a member is down) blinking / cut with DLSS (FIXED)
- Rig agent_scripts/ko.sh <tag> [env] (user's 11-21 autosave copy testsave/u21k slot 20, 7F, Touma 0 HP; walks a square, 48
  shots 0.25 s). Red-pixel count per shot in the centre crop: native 4K 48/48 shots ~30 px; DLSS Quality 4K (user's settings
  fx_fxaa 4, fsr3_quality 1) ~5 px = fragments (= the video).
- Cause: the mark is drawn AFTER the FXAA draw (draw log: shader 9cdae030, ds 0x43 depth test + write, 64x64 texture), where
  upscaling switches every twin to its full-size image. The full-size DEPTH twin was never drawn this frame (scene on the lo
  depth), so the mark depth-tested against stale depth. twin_sync now also does depth / stencil (nearest blit; skipped with a
  log line if the format has no BLIT_SRC/DST) and begin_rendering syncs the depth attachment when its twin is newer (not when
  the pass clears depth first); depth twins get mark_written at pass begin (twins only: MSAA's written logic untouched).
- Verified ko6 (DLSS Quality 4K): 48/48 shots, ~30 px (= native). ~0.4 depth syncs per frame (23/s at 60 fps). FSR 3 path is
  the same code, not run. AMD / Intel depth blit support: checked at run time, not tested.

### Revive at 1 HP after battles (USER request; setting ko_revive, default 1)
- ko_revive(): joined party records (+8 level 1..99) with HP 0 -> HP 1 and record byte +0x52 -> 0. +0x52 = 1 only on the KO'd
  member in the user's autosave (Touma), 0 for the others: ASSUMED to be the KO flag (not proven). Runs every frame from the
  battle opening once battle main state >= 0xd (RESULTS) and at the first field step (escapes); never after a loss
  (g_battle_lost from the btl_task_end loss test, cleared at btl_open_chance).
- F1 "Revive at 1 HP after battles", native PC 4/4 row 6 (not seen on screen), settings.ini ko_revive.
- Rig agent_scripts/kowin.sh <tag> [env] (slot 12 Aversa, enemies 1 HP; debug NX_KO_TEST=<char id> = that member's battle unit
  at 0 HP): kw4 NX_KO_TEST=3: "ko revive: party record 2 (id 3) HP 0 -> 1" at 382.8 s, field scene at 383.7 s. Touma levelled
  up in that run, so the level-up refill filled him too: the HUD result does not isolate the revive.
- NOT verified: a member KO'd by an enemy (real KO flag) coming back after a won battle; escape; the field HUD / KO mark
  after it. A revive made in the field (debug, removed) did not change the HUD or the mark: the field reads the party at load.

## Milestone 5, session 93 (2026-11-21, USER: s92 fixes OK -> merged fix/help-text-exp-1120 to master (fast-forward 2edb322))
- New branch feat/settings-items-1121. Rig agent_scripts/setpages.sh <tag> "<control lines>" [env] (u21k slot 20 -> keys 1.2 s
  apart). Camp: y, down x6 = System, a, down x2 = Settings, a; R = next page. Items: y, down, a.

### Native settings pages (USER screenshots: PC 3/4 one empty row, PC 4/4 three empty sliders)
- PC 3/4 row 10 = Sub Cast EXP (moved from PC 4/4). PC 4/4: rows 0-2 empty, 3 EXP level-gap, 4 Retry, 5 Revive, 6 Carry 99.
- Rows 0-2 are always sliders in the game's draw 0x33cb14 (row < 3). New hooks (names.txt, RE-LIFT 20651 hooks):
  ui_draw_sprite 0x23d774 (row background; lr 0x33cccc: table kind 0x4e6a slider / 0x4e6b choice, selected 0x4e6c / 0x4e6d),
  ui_draw_gauge 0x23ce80 (bar, lr 0x33cd80), ui_draw_part 0x23c8e4 (knob, lr 0x33cda0); row index in r9 at those calls. On our
  pages an unnamed row 0-2 gets the choice background and no bar / knob. Verified on screen (sp3): blank pills like rows 7-10,
  cursor on them too. Rows 0-2 cannot hold On/Off items (no option text object on slider rows).

### Carry 99 of each item (USER request; setting item_max99, default 1)
- Table/ItemUseTable.dat (consumables): 256 records of 0x2c, +0x18 buy price, +0x22 stock cap byte (Life Stone 0x28 = 40, Patra
  Stone 0x5a = 90, Magic Mirror 5). Loader 0x27cec4 (path string 0x726784), object made in 0x27f974 (size 0xe014), pointer in
  *(0x9ef458); the table is COPIED into the object at +0x38 (scan of the object for the Life Stone record; +4 = load request,
  0 after loading). item_cap_poll (frame_begin, every 30 frames): caps saved, non-zero caps -> 99 or back; applies live.
  Performa (ItemMaterialTable, stride 24) already holds 99.
- Verified: log "items: consumable stock cap 99" at boot; Camp > Items shows x/99 for every consumable (it4). NOT verified: a
  shop buying past the old cap; stock above the old cap when the setting is turned off again (game behaviour unknown).
- F1 "Carry 99 of each item", PC 4/4 row 6, settings.ini item_max99.

### Story movies in 4K (USER question): NOT started, user decision
- pack_050_movie.cpk: 25 USM, 1.96 GB, VP9 1280x720 30 fps (m01: 2870 frames); ~36,000 frames in all; credits pack 0.16 GB more.
- The runtime swap (hle_movie.cpp movie_hd/*_<hash>.ivf) is generic: tools/camphd/camphd.py only needs the pack / folder
  generalised. Estimate from the camp batch (0.33 s/frame realesr-animevideov3 x3 + VP9 crf 24, 63 KB/frame): ~3.5-4 h of GPU,
  ~2.3 GB of 4K streams -> a separate ZIP like CampHD / UHD (derived game data: not in the program ZIP).
- Uncensored mod movies m06 / m07 / m12 (Sofdec.Prime MPEG-1) replace the stock ones: their first packet differs, so a stock HD
  stream would not match; they need their own batch (MPEG-1 decode, not usm2ivf).

## Milestone 5, session 94 (2026-11-21, with user; branch feat/settings-items-1121, uncommitted)

### Story movies 4K (user OK 11-21): batch RUNNING
- tools/camphd/camphd.py takes [work] [pack] [subdir]: `cd private/tms; python -u ../../tools/camphd/camphd.py . ../tools/esrgan
  ./story_hd pack_050_movie.cpk story` (log story_hd/run.log; rerun resumes). Output movie_hd/story/<name>_<hash>.ivf (runtime
  swap unchanged). m00 checked: VP9 3840x2160 30 fps 210 frames. NOT done: uncensored m06/m07/m12, MovieHD ZIP.

### Shibuya car off the road / through a wall (USER 11-21, chapter 2, not reproducible after reload): FIXED, measured
- Cause: vehicle_update 0x3df4fc copies the actor position +0xc into the car's own +4 first. Our hook put the stored true
  position back before it (town_true_pos) even when game code had moved the car since: the route controller (0x3e00ec etc.)
  parks a car at (100000, -200, 0) and warps it to a route start through 0x3de938 (speed 0, pos, dir, actor delta cleared).
  When no actor job ran between the warp and the next tick, the warp was undone: the car drove its new route from the old
  spot (off-road, through walls; cars have no collision) or went back to the parking spot.
- Fix (hle_sys.cpp town_true_pos): restore only while the actor's x/z still equal what we showed; otherwise the game's
  position wins (entry reset, snaps like a spawn). NX_TOWN_LOG logs "moved by the game: kept .. -> now ..".
- Measured (shibuya.sh 240 720p, save 6): 9 warps in 210 s the old code would have undone (8 from parking, one 35-unit
  mid-route move). carshown.py back-steps: fix 52 / 48792 moving frames vs old 31 / 25271 (same rate; old has half the
  moving cars = warped cars sent back to parking).
- Rig note: shibuya.sh's 2nd title A came too early this session (stopped on the Load list); press a until [pos] player.

### Shibuya cars still off the road (USER 11-21 video D:\OBS VIDEO\OBS6-11-21 08-39-31.mp4, warp fix build): REAL cause FIXED
- Video (frames private/tms/user_video_1121): bus U-turns on the scramble, cars cut across each other / the crossing.
- Cause: vehicle_update 0x3df4fc starts with 0x3c8758 = direction from the actor yaw +0x1c into the car's +0x28. Since s85
  town_actor_update writes the GLIDED yaw there between ticks, so every tick the car steered from a heading behind its true
  one: turns came out short, overshoot, circles. The lag is the glide share left at the tick frame: ~1/8 turn at 240 fps,
  1/2 at 60, worse with low frames (user ~100 fps 4K, OBS + upscale batch: 1% low 22). s77's "vehicles OK" predates s85;
  s94's first test ran at 240.
- Fix (hle_sys.cpp town_restore_true, before vehicle_update): position AND yaw (yaw_to, only while +0x1c == yaw_shown) back.
- Measured (save 6, 720p, 90 s, agent_scripts/carturn.py on NX_MOVE_LOG=2 + NX_TOWN_LOG): old 60 fps 0.693 rad turning per
  100 units, 26 full circles; fix 60 fps 0.258, 0 circles; fix 240 fps 0.248, 0. carshown back-steps 60 fps old 89 / 48322,
  fix 149 / 45465 (max 9 per car, spread over 29 cars = traffic noise, not the s75 every-frame shake). Shots shots/yaw_ab.png
  (old: van on the pavement; fix: cars on the road).

### PC 4/4 items moved to the top rows (USER 11-21: "why blank on first 3? move it to the top")
- The draw 0x33cb14 draws a row's option text (+4) whenever it is set, for any row; only the bar / knob / slider
  background are row < 3. The update 0x33c0a0 steps every row the same way (+8 within +0x10..+0x14 when +0xc).
- Text object: +0x50 x, +0x54 y (720p units; option x 850, label x 234, rows 50 apart, label and option same y).
- camp_settings.cpp lend_options: an On/Off item on rows 0-2 takes the option object of an empty row (9, 8, 7), moved to
  the row's label y; return_options puts it back (blank) on page change, leave, A dialog. Slider hooks treat a named
  On/Off row 0-2 like an empty one (choice background, no bar / knob). PC 4/4 = rows 0-3 EXP gap, Retry, Revive, Carry 99.
- Verified on screen (shots sd2 / sd3 / sd5): PC 4/4 rows 0-3 filled, Left / Right step them (On = top value, Right at
  On does nothing, same as rows 3-10), game page after L: its 3 sliders + rows 7-9 texts intact, A dialog clean, Yes closes.
- Seen, not changed: B on the A dialog went to the game page (log "PC page 4" then "game page" same frame); same code as
  before this change, not compared with the old build.
- USER 11-21: enemy target highlight (s74 item 2) now works: closed.

## Milestone 5, session 95 (2026-11-21 ~12:00-, SCHEDULED run tmsrecomp-polish-1121, user asleep; branch feat/moviehd-1121 from feat/settings-items-1121 93ad09d)
- Commits: 8c78669 mod MPEG-1 4K, cb856b8 weak-PC defaults, 49c4f25 B on Apply dialog, adbb61b shaderscan int variants +
  package -MovieHd, 5f532fd two-packet movie keys, 3c76658 NX_MOVIE_HD_CHECK, f0e0ea2 slow-CPU 4K fallback., bd5c13b row-MT decode.
  NOT merged (branch from feat/settings-items-1121, which is not merged either).
- Saves: user save/ md5 identical before / after every test (tests used testsave copies).
- Build note: build.cmd must be started as `cmd /d /c C:\...\build.cmd` from the repo root (PowerShell Set-Location
  first); `cmd /c build.cmd` says "not recognized" here (AutoRun). Git Bash `sed -i` turns CRLF files into LF: use Python /
  Edit on CRLF files. Commits need `git -c user.name=... -c user.email=...` (no global git identity in this session).

### Story movies in 4K (batch from s94)
- 25 movies done by the s94 batch (tools/camphd/camphd.py, log private/tms/story_hd/run.log). ffprobe: VP9 3840x2160 30 fps,
  packets = source frames (m01 2870, m22 2767, s1002_a_20 452).
- BUG found + FIXED (5f532fd): 9 story movies share the first packet (black keyframe): m0000_11 / m13 / m14 / m3083_01,
  m07 / m4103_01, m12 / s1003_s_15, m02 / s1005_s_10 (packet 1 always differs, measured). The index kept one file per key,
  so e.g. m13 would have shown m14's 4K frames. New key = FNV of packet 1 seeded with packet 0's hash, looked up at packet 1
  (4K frame 0 skipped; it is the black frame). Camp files keep their single-packet keys (still looked up at packet 0).
  tools/camphd/rekey.py renamed the finished files (no re-encode).
- Sync measured with NX_MOVIE_HD_CHECK=1 (mean |720p - downscaled 4K| luma per 60 frames, vs the previous 4K frame):
  m00 title 0.39 / 0.98 / 1.17 (previous frame 3.31 / 1.39 / 1.26); m06 stock (mods off, Aversa rig) 1.36-1.83 (previous
  3.84-18.97) = on the right frame. m06 opens 1 s after its first frame (the game prerolls packet 0, then pauses) and stays in sync.
- Slow CPUs (f0e0ea2): 4K decode timed per stream; a 30-frame average over 30 ms (33 ms = one movie frame) -> "too slow on
  this CPU, 720p for this movie". Here, with the batch using every core, m00 averaged 26.4 ms (tripped the first 25 ms limit).
  NX_MOVIE_HD_SLOW_MS=1 forces the fallback (verified: log line, no more swaps).

### Uncensored mod movies m06 / m07 / m12 in 4K (8c78669)
- Mod USMs = MPEG-1 (Sofdec.Prime) 1280x720: m06 1801, m07 3211, m12 3251 frames (one @SFV chunk per frame; ffmpeg decodes
  the concatenated chunks as .m1v). CRI MPV decodes them in game code, so the VP9 packet key does not apply.
- Hook names.txt 0x6dbc5c mana_frame_copy (re-lift 20652 hooks): r1 = 3 plane descs {ptr, w, h, pitch} (Y, U, V at +0, +16,
  +32). After the copy: 16x9 Y block means of the frame are matched against <name>_prime.thm (144 bytes per frame from
  ffmpeg extractplanes=y,scale=16:9:flags=area), near the last match, else every prime movie; mean diff <= 6 accepts.
  The 4K frame (I420) planes are registered under the fingerprints vk_texture.cpp computes for the R8 plane textures.
  Unknown / unmatched frames just stay 720p.
- Verified with a test 4K m06 (bicubic + red box marker): marker on screen, colours right (U/V order), 16 s of the movie
  "frame N (diff 0)", 0 unmatched. The real batch (ESRGAN): private/tms/prime_hd/chain.sh -> movie_hd/story_mod.
- camphd.py: Prime USMs detected by the MPEG sequence header; output <name>_prime.ivf + .thm; pack may be a path.

### Weak-PC first-run defaults (cb856b8)
- Already there: res auto (iGPU / < 3 GB 720p, < 8 GB at most 1440p), FXAA (game's own) default, MSAA 0 default + VRAM
  cap, VRAM-full spill to system RAM, Vulkan feature checks.
- New: tex_pack = auto (default; launcher drop-down Auto / Off / On): UHD pack off on integrated GPUs and under 4 GB VRAM
  ("textures: UHD pack auto -> off (weak GPU)"); pack cache budget = VRAM / 8 (128 MB..1 GB, was 1 GB fixed); screen scaler
  default FSR 1 (unset / auto; only runs when res is below the window). vk::vram_bytes / weak_gpu; NX_VRAM_MB=<n> pretends a
  smaller GPU (test).
- Measured (NX_VRAM_MB=2048, res / pack / scaler auto, Shibuya): "res auto -> 720p ... 2048 MB VRAM", pack auto off,
  VRAM 1280 MB in blocks. fps numbers of this session are NOT meaningful (the 4K batch used the GPU and every core).
- NOT testable here: a real iGPU / AMD / Intel / 2-4 GB card (only an RTX 5070 Ti), FSR 1 on screen in a rig (rigs run
  minimized: swapchain 0x0).

### 5 shader misses (OPEN LIST s39 c): FIXED, measured
- Dev cache 1836 entries vs a scan of everything (base packs all file types, mod packs, image.bin): 1766 keyed by
  shaderscan; 0 only in mods / skipped file types; the rest = vertex integer-attribute variants (brute force over the
  attribute types: 12 of 19 prefixes = attribute 7 uint, character / shading_effect / stainless .vspk + 2 in image.bin;
  7 prefixes unexplained, likely other type combos, not hit in the runs below).
- shaderscan.py: vertex shaders of image.bin + pack_030_etc also get the attribute-7-uint variant (+757 keys; a fresh
  scan now makes 7207 translations, 0 failed). Setup re-runs the scan after an update (shaderscan.py mtime is a dep).
- Measured on a scan-only cache (fresh shaderscan, 8 min, 7207 translations): boot + title + Shibuya load + walk, and the
  Rooftop event m1033 (Aversa rig): 0 "shader cache miss", 0 run-time translations. Dev cache restored after.

### Settings: B on the "Apply these settings?" dialog (49c4f25): FIXED, ours
- No / B pass state 7 (closing) before 2. We re-entered the PC page at 7; the "not browsing" branch then left it again in
  the same update (s94 log: "PC page 4" then "game page"). Now waits for state 2. Verified (setpages.sh bd1): R, A, B ->
  "PC page 1" again, screenshot shows PC 1/4.

### Not done / needs the user
- Traffic / crowds in Harajuku etc.: no save there (user saves end around chapter 2); the s94 car fix is in the shared
  vehicle_update path. User: play a bit in Harajuku with the new build.
- AMD / Intel / iGPU tester, clean-PC test, fern edges look (user).
- 1% low work not measured this session (GPU / CPU busy with the 4K batches all session).

### End state (s95)
- Mod batch (prime_hd/chain.sh, ESRGAN): movie_hd/story_mod m06 / m07 / m12 _prime.ivf + .thm, 1.2 GB; ffprobe VP9 3840x2160
  30 fps, 1801 / 3211 / 3251 packets = source frames = thumbnail frames. Story: movie_hd/story 25 files 5.4 GB.
- Mod m06 in game (Aversa rig, mod on, idle PC): 4K stream from frame 0, 0 unmatched frames over 14 s, no slow fallback.
  With the batch running it had fallen back after ~4 s (32.4 ms per 4K frame).
- 4K decode cost (m00, NX_MOVIE_HD_SLOW_MS=0.1 prints the 30-frame average): 19.9 ms before, 11.1 / 11.5 ms with libvpx row
  multithreading (bd5c13b; our streams have 4 tile columns = 4 decode threads otherwise). A later re-encode with more tile
  columns (-tile-columns 3) would help weak CPUs more; not done (8 h of GPU).
- ZIPs (Desktop): TMSRecomp-UHD-20261121.zip 11.61 GB (same byte size as the 11-02 one), TMSRecomp-MovieHD-20261121.zip and
  the release ZIP: MovieHD 6.54 GB (34 entries: README, story 25, story_mod 3 x ivf + thm), TMSRecomp-20261121.zip 149.6 MB.
- Old Desktop ZIPs left in place (TMSRecomp-UHD-20261102.zip, CampHD-20261102); the CampHD files keep their keys.
- Work folders kept: private/tms/story_hd/usm (2 GB), prime_hd (usm + .m1v, ~1.1 GB): delete when no re-encode is planned.

## Milestone 5, session 96 (2026-11-21 ~19:30-, with user; branch perf/lows-1121 from feat/moviehd-1121 6a32b8d)

User: "check frame rate and 1% low. Improve it."
- First baseline INVALID: Adobe Media Encoder used ~88% CPU (Shibuya 1% low 34 fps). User paused it. The GPU still runs the
  user's desktop (Lively video wallpaper, 25-49% GPU at idle): compare only inside this session. Always check
  `Get-Counter '\Processor(_Total)\% Processor Time'` + nvidia-smi before perf runs.
- Clean baseline (feat/moviehd-1121 exe, sbperf.sh 720p uncapped NX_FX_FXAA=1 NX_MSAA=0): spot 173 fps, 1% low 102-103,
  0.1% low 36-44, worst gap 23-28 ms; sbwalk 310 fps, 1% low 144-151, 0.1% low 40-45, worst gap 23-30 ms.

### Periodic hitch FIXED (nvn_hle.cpp nvnCommandBufferAddCommandMemory)
- NX_STALL_STATS: worst frame 27 ms wall, game thread ran 24 ms, 0 page faults = real work, every ~6 s. Every 27 ms hitch
  came 7 ms after the log line "nvn: N live command handles; process private .. MB (guest .. MB)" (every 3000
  AddCommandMemory calls). NX_PROFILE spike frames: rt::guest_committed_mb / NtQueryVirtualMemory in nearly all of them.
  guest_committed_mb walks the 4 GB guest reservation region by region (VirtualQuery), ~20 ms, inside g_lock (blocks the
  render thread too). It is the s83 "whole-process stall" lead.
- Fix: guest MB only with NX_MEM_REGIONS (log shows -1 otherwise; guest was flat 2111 MB in every log). Handles +
  process private still logged (GetProcessMemoryInfo, cheap).
- A/B interleaved (old exe in private/tms/build_old: the exe must keep the name tms.exe, a renamed copy crashes at
  nnosInitialize):
  spot old 1% low 88-103 / 0.1% low 30-34 / worst gap 29-33 ms; new 107-123 / 76-112 / 9-13 ms. Median same (5.6-5.9 ms).
  walk new 306-318 fps, 1% low 195-199, 0.1% low 121-134, worst gap 11 ms (baseline 144-151 / 40-45 / 23-30).
  btlperf 4K battle: old one window 0.1% low 45.7 / gap 21.9 ms; new worst gap 9.9 ms (both 152 presents/s flat).
  NX_FPS=60 spot: old 1 late vsync per 10 s (33-35 ms frame, 1% low ~50); new 0 late vsyncs, 1% low 59.8-59.9.
- Remaining slow 1% at the spot (8-8.5 ms vs median 5.6): game thread waits 2-3 ms in nvn::job_queue for the render
  thread, which waits on the GPU (hitch lines GPU waits 3-8 ms) while the desktop also uses the GPU. No other periodic spike.
- Not run: crash batch (change is a log argument only); 4K DLSS at the user's settings; weak / AMD / Intel PC.

### Part 2 (2026-11-22 ~03:00, user playtest report)
- User: "fatal error / Vulkan: vkQueueSubmit(queue, 1, &si, VK_NULL_HANDLE) failed (-4)" after switching DLSS modes in the
  menu (0 1 0 1 0 1 2 3, 4K fps 240 DLSS MSAA 4). Log: logs/nx_20261122_024634.log: "device fault: address 0 (+-1000) write
  invalid" right after "dlss: feature 1920x1080 -> 3840x2160".
- Rig agent_scripts/upqstress.sh <tag> <cycles> (upq 0 1 0 1 0 1 2 3 4 3 2 1, 1.5 s apart, user settings): crashed 3 / 3
  runs after 6-9 switches. A/B: NX_ASYNC_REPLAY=0 49 switches 0 faults; NX_FX_FXAA=3 (FSR 3) 49 / 0; NX_MSAA=0 still crashed.
  = DLSS + render thread (s81) only.
- Cause: vk_dlss.cpp released the old NGX feature after vkDeviceWaitIdle on the render thread. vkDeviceWaitIdle needs every
  queue externally synchronized; with the render thread other threads submit meanwhile. Since s84 (live mode switch) this
  runs at every switch (before: only at start).
- Fix (vk_dlss.cpp): no vkDeviceWaitIdle; the old feature waits in N.old with gpu_last_submitted() and is released once
  gpu_wait(serial, 0) passes. Measured: 2 x 49 switches 0 faults, 49 / 49 features made, 0 evaluation failures, last
  shot correct; switch frames now at most 23-30 ms (the wait-idle frame was up to 370 ms on a busy GPU).
- Tried first and dropped: running upscale_apply_setting on the game thread after render_drain (still crashed alone;
  not needed with the DLSS fix: 2 x 49 / 0 without it).
- vk_fsr3.cpp context(): same vkDeviceWaitIdle, but the FSR context is keyed by the OUTPUT size (fixed per resolution),
  so mode switches never reach it. Left as is.

### Menu "flicker" (user videos D:\OBS VIDEO\OBS\2026-11-22 02-49-26.mp4 / 02-49-36.mp4): NOT reproduced, question sent
- Frame-by-frame (60 fps capture of a 123-152 fps game): the camp-open wipe (green / black rings, then a white field with
  rings ~0.25-0.4 s, then the camp screen) steps forward monotonically; A-B-A pixel check finds only ring edges; no
  stutter in nx.log at the opens (worst gaps 12-18 ms).
- Rig agent_scripts/campflick.sh (NX_SHOT_LUM, shots of 150 frames after Y): same luma curve with NX_MOVIE_HD=1 / 0
  (white phase 16-17 shots both): the white phase is the game's own wipe, not the 4K camp movie. Shots stall each 4K frame
  ~100 ms, so timing-only effects can not show in this rig.
- A desktop capture (ffmpeg ddagrab) recorded the user's browser instead of the game window: deleted at once, script
  removed. Do not capture the desktop again.

### Camp menu flower flicker: FIXED (user video 2026-11-22 03-21-18.mp4 "look at the flowers")
- Why it was missed: whole-frame / downscaled metrics and OBS h264 hide it; the 60 fps capture at 4x zoom showed it:
  movie frames alternate A A B B (B = softer, washed-out colour) = every other camp movie frame had 720p colour.
- Rig: agent_scripts/campshots16.sh <tag> [env] (camp menu, 16 consecutive shots) + HSV saturation of a flower crop:
  before 183.5 / 178.5 alternating, after flat 183.3-183.5. Temporary bind trace (removed): the camp movie's 4 planes,
  second buffer's UV texture 640x360 drawn 720p 1534 / 1534 times, the other 3 always 4K.
- Cause (vk_texture.cpp movie_replace): one 4K image per guest GPU address, never freed. The title movie's Y plane
  (3840x2160 image, new in the 11-21 MovieHD pack: m00 4K) used an address that the camp's UV texture got later; the
  size check (1920x1080 needed) returned false for good. Fix: a mismatching cached image is replaced (defer_destroy) and
  logged "textures: movie plane X: 4K image ... (address reused)".
- Title movie: Y / UV planes 4K; 3 other 1280x720 linear textures change every frame but never match a movie frame's
  fingerprint (not movie planes; alpha / copies?), left as is.

## Milestone 5, session 97 (2026-11-22, with user; branch perf/lows-1121): release check + legal + GitHub prep
User: "people have been begging for me to release": check everything works, list open bugs, avoid legal issues, prepare
GitHub (first time).

### Release flow test (fresh ZIP, bare PATH)
- TMSRecomp-20261122.zip extracted to private/tms/release_test; data = exefs copy + romfs JUNCTION; PATH = System32 only
  (no system Python / LLVM / .NET). setup\python setup.py --folder: exit 0 in 521 s (link, lift, game.dll 40 MB, shaders).
- base60 replay from the release folder (release tms.exe + game.dll + release data): 0 crashes, 0 shader misses, 0
  translations in play, picture right (Daitama Lower, HUD + minimap). Logs: analysis/rel_cold.log, rel.log, setup.log.
- 60 cap, 1% low / 0.1% low per 10 s, warm run vs dev build same replay (analysis/devbase... = devbase.log in private/tms):
  release 27.8/11 44.7/22.5 59.6 25.5 29.1 52.4 47.5 49.3 45.4 38.3 42.8 49.5 48.2 26.8 47.4 35.9;
  dev 11.7 29.0 59.3 31.8 59.6 51.7 57.3 59.5 59.7 34.9 38.2 38.6 43.1 29.1 25.5 41.5 37.3. Dungeon part the same in both
  (worst gaps 25-37 ms); release 40-80 s lower in this ONE run (not repeated). OPEN: base60 dungeon at 60 cap has 1% low
  35-49 in both builds (Shibuya at 60 = 59.8): look at it with NX_PROFILE_SPIKE.
- release_test removed (junction first; real romfs checked intact).

### Legal fix: the release exes embedded the game's icon
- private/tms/icon.ico (made from the NSP's icon_AmericanEnglish.dat, game art) was compiled into tms.exe and
  launcher.exe of every release ZIP. CMakeLists NX_ICON is now a cache option; package.ps1 builds tms + launcher in
  private/tms/build_rel with -DNX_ICON= (refuses if build_rel\icon.rc exists) and takes the program files from there.
  The dev build keeps the icon. Release tms.exe 2,277,376 -> 2,083,328 bytes.
- Audit, rest: repo history has no game file ever (deleted files: StencilIds only); ZIP has no game code (package checks);
  DLSS downloaded from NVIDIA by the player; third-party notices in THIRD_PARTY.txt. Risks left (user decisions): commit
  emails (2 gmail addresses in 323 commits), NSP + prod.keys mode (key-based decryption via nstool = DMCA 1201 exposure;
  folder mode avoids it), subtitles_en.tsv = fan translation of battle voice lines (low), ext_bgm P5R ADX key (public in
  vgmstream, low). UHD / MovieHD ZIPs = upscaled game assets: never publish.
- README.md / README.txt: non-affiliation notice (Nintendo, ATLUS, SEGA, Intelligent Systems), own-copy rule, status
  updated (through chapter 2), "Playing" section. .github/ISSUE_TEMPLATE/bug_report.md (asks nx.log, GPU, settings).
- NOTES line 1217 had a NUL + TAB from an unescaped path: fixed (GitHub showed it as a binary file).
- GitHub guide for the user: private/RELEASE_GITHUB.md; release notes draft: private/release_notes.md. Needed from the
  user: account name (launcher.cpp k_update_repo "owner/TMSRecomp"), fresh history vs full history, keys mode decision.

### Open bugs (2026-11-22)
1. Untested: AMD / Intel / iGPU, weak CPUs, chapters after 2 (no user saves), Harajuku traffic.
2. base60 dungeon 1% low 35-49 at the 60 cap (above).
3. Fern black edges (user look, Fortuna Office, UHD on); walker yaw steps at 30 Hz (small).
4. Not verified in play: retry after a random (symbol) encounter, KO revive after a real KO, sub_exp real battle.
5. No Linux build; launcher update check off until k_update_repo is set.

## Milestone 5, session 98 (2026-11-22, with user; branch perf/lows-1121): launcher Guide, P5R key dropped
User: retry after a random encounter WORKS, 1 HP after a real KO WORKS (closed). UHD + MovieHD ZIPs go to the user's own
Google Drive (user decision, told the risk). Drop the P5R music key. Fresh history for GitHub, but only after the user's
own playtest of the release build. Asked for a first-time tutorial in the launcher.

- ext_bgm.cpp: no built-in ADX keycode any more. Setting custom_bgm_key (decimal keycode); encrypted (type 9) files
  without it are skipped with "custom music: <file> is encrypted: set custom_bgm_key ...". The flag-0 keyed-frame
  detection runs only with a key. The user's own settings.ini (private/tms/build, backup settings.ini.bak_s98) got the
  key line: 199 of their 200 BGM_42 files are type 9. NOTES no longer holds the number.
- Launcher page 7 "Guide" (6 topics: Get started, English / uncensor, UHD textures, 4K movies, Battle music, Controls &
  help) with buttons that do the step. Installs run setup.py through the Setup page's job/progress machinery
  (g_su_extra: a Guide job only rescans mods, never touches built.txt / data=):
  - setup.py --mod <folder> --data <data>: .xdelta patches matched to romfs\Pack\<cpk> by longest name prefix ->
    <data>\mods\<folder name>\romfs\Pack (vcdiff.py, progress callback); a folder with romfs\ is copied.
    Measured: pack_999_lua 1.3 s, pack_080_interface (485 MB patch) 173 s, both md5-identical to the user's mod.
  - --zip <ZIP>: only textures/pack/ + movie_hd/ entries (else refused), disk check, resumable, into <data>.
  - --music <folder>: every .adx below it -> <data>\music.
  - launcher --topic N (with --page 7) opens a Guide topic (used for the screenshots private/guide1.png, guide4.png).
  Setup page section 2/3 replaced by "Extras -> Open Guide". package.ps1 ships tools\vcdiff.py in setup\tools;
  -MovieHd now also packs movie_hd\camp (the camp backgrounds were the separate CampHD ZIP of 11-02).
- Fern (user asked for a picture): no picture of the fern exists. s41 saw it in passing at 4K with the pack "in the hall
  near the red chair"; s43 fixed the cause (uhd_pack bleed, 76 textures redone); the Fortuna Office shots
  (shots/fern_0000*.bmp, red chair = Maiko's desk) do not show it. Still a user look.

## Milestone 5, session 98 part 2 (2026-11-22): version 0.1.0 beta, research of other Switch recomps
- k_version 0.9.0 -> 0.1.0 (user: beta, 0.1.0). Release: tag v0.1.0-beta, title "TMSRecomp v0.1.0 Beta", NOT GitHub's
  --prerelease flag (the launcher reads releases/latest, which skips pre-releases). private/RELEASE_GITHUB.md + release_notes.md.
- Research (GitHub READMEs / releases; reddit not readable by fetch or the built-in browser):
  - Astral Chain Recomp (captainj-sparrow, fork of TotK Recomp, MIT, 715 stars): Setup.exe takes base 1.0.0 + update 1.0.1
    (XCI/NSP), builds the exe in ~1 min; HDR10, DLSS/XeSS/FSR3/FSR4, AF 16x, ultrawide, Reflex/Anti-Lag, F1 menu,
    F10 overlay, F12 no-HUD, remap/gyro/rumble, 4 languages, Linux AppImage, RecompLauncher manifest. Testing: README
    "Externally tested (Reddit, YouTube, ...): playable from intro to credits" = the COMMUNITY played it through;
    10 releases in 8 days (11-14..11-21), hotfix within a day; issue form asks port version + "Copy system info" + log;
    ~101 issues (34 open: 60 fps cutscene animations, Steam Deck/ROG Ally, Intel UHD startup crash, final-boss crash).
  - TotK Recomp (7.9k stars, base of Astral Chain and XCX), LAS Recomp (2.5k, beta 6, Win/mac/Linux/Android),
    MHGU Recomp (fully playable, updater keeps saves), XCX Recomp, OpenSmash. All: own dump built locally, boxed legal
    note, "for your own use, do not share", exact version pins + disk space, honest status words, release notes with
    issue numbers + per-setting workarounds, Linux AppImage, frequent dated releases, AI-written code disclosed.
  - Gaps of ours (ranked): no "Copy system info" / version in bug reports; base game only (no 1.0.x update / XCI);
    no Linux AppImage; no RecompLauncher manifest; no HDR / ultrawide / AF / perf overlay / remap; no "for your own use"
    line in README; no known-issues list; no SmartScreen note.
- s98 part 3 (user: "quick wins 1-3"): runtime/src/sysinfo.h sysinfo_line() (version, Windows build via RtlGetVersion,
  CPU brand via cpuid, threads, RAM); nx.log line 2 "system: ..." (checked: "TMSRecomp 0.1.0, Windows 10.0 build 26300,
  AMD Ryzen 7 9800X3D 8-Core Processor, 16 threads, 63.6 GB RAM"; GPU stays on the "vk:" line). Launcher "Copy system
  info" (Guide > Controls & help, Advanced): system line + GPU/driver from nx.log (else EnumDisplayDevices) + render
  settings, no paths; clipboard + message box (button drawn, NOT clicked: synthetic clicks do not reach the launcher).
  Issue form points at it. README: "for your own use, do not share", no instructions for files/keys, requirements,
  SmartScreen / antivirus note, Known issues (v0.1.0 beta). Game updates: only a stale source (perfectly-nintendo lists
  the base version only); setup already names a non-base exefs ("from another build of the game").

## Milestone 5, session 99 (2026-11-23, user asleep: "do not ask, continue, do not break anything"; branch perf/lows-1121)
User (after playing the new launcher build, "super impressed with the performance"): 1 TMS icon for launcher + game after
setup, and the launcher picture as in the dev build; 2 DLSS 4.5 + model preset; 3 ray tracing only if feasible; 4 VRR;
5 confirm the game works without UHD pack and uncensor patch; 6 Idolasphere reveal-map QoL in the L3+R3 menu + setting.
Scheduled task tmsrecomp-resume-1123 (15:00) continues if the usage limit stops this session.
s98 part 4 (before this, same day): Guide "Installed." showed on every topic (g_su_topic), folder pickers =
IFileOpenDialog (Explorer style), README "Use your emulator save" (untested with a real emulator save).

- 2 DLSS: setup already downloads DLSS 310.9.16 (NVIDIA/DLSS tags: v310.9.16 2026-10-16 is the newest; DLSS 4.5 =
  SDK 310.5+). With NVIDIA's default per mode the DLL already uses the DLSS 4.5 models M (Performance) and L (Ultra
  Performance), K elsewhere (SDK nvsdk_ngx_defs.h: preset J 10, K 11, L 12, M 13; G/H/I/N/O "do not use").
  New setting dlss_preset (0 auto default, 11 K, 13 M, 12 L): vk_dlss.cpp sets DLSS.Hint.Render.Preset.<every mode>
  before feature creation (only when 10+; 0 = nothing set = unchanged behaviour). Launcher Graphics row "DLSS model".
  Verified: NX_FX_FXAA=4 NX_DLSS_PRESET=13 -> "dlss: feature ..., preset M", no fallback, frames fine.
- 4 VRR: present_mode = vrr: vk.cpp FIFO (present_thread takes the waits, the game thread does not block); ui.cpp
  vrr_cap(): when fps is uncapped or above refresh-3 the cap becomes refresh-3 (30 / 60 keep their own pacing).
  Verified (slot 20, uncapped, 160 Hz): "ui: VRR: frame cap 157", swapchain fifo, 1% low 147.8 / median 6.58 ms after
  warm-up. NOT verified on a real G-SYNC / FreeSync screen (driver-side VRR cannot be observed from here).
- 1 Icon + picture (nothing of the game ships): setup.py get_icon(): after exefs/romfs, the smaller NCAs are extracted
  (nstool -x /) until icon_*.dat is found -> <data>\icon.jpg (tested on private/tms/nsp control NCA 6d2a8ad3: 256x256
  JPEG). tms.exe: game log "Cue:b56_title" -> rt::hero_capture_soon(): if no <data>\launcher_hero.(png|jpg|bmp), 6 s
  later the frame is written to <data>\launcher_hero.bmp (via .part + rename; NX_NO_HERO=1 off). Verified: title
  screen captured at 17.6 s. Launcher: apply_icon() makes <data>\icon.ico (WIC: icon.jpg whole, else a square around
  the title logo, 256 px PNG-in-ICO; redone when icon.jpg is newer) and sets WM_SETICON; on WM_ACTIVATE (back from
  the game) it reloads the picture + icon once launcher_hero.* exists. tms.exe sets the same icon.ico on its window.
  Both icon sources checked by eye (scratchpad). The exe FILE icons (Explorer) stay default: rewriting tms.exe /
  launcher.exe resources after setup is not done (launcher.exe is running; antivirus risk). Caption colour green.
  The user's own install was set up before this: it gets the title-screen icon after the next game start; "Set up
  again" (NSP) would give the NSP icon.
- 3 Ray tracing: not done. The game is a forward-rendered NVN title with baked lighting; RT needs scene geometry in
  acceleration structures (BLAS / TLAS) + new lighting shaders replacing the game's own; not feasible without a renderer
  rewrite. Told the user.
- 6 Reveal map: Lua ampSetFootAt (0x422284, string 0x739a2f, registration 0x7e22d4) -> 0x3bbdcc (y picks the floor
  section) -> painter 0x3bba18(mgr, section, &centre, s0/s1 half size, 1): 12-px cells, bitmap from 0x3c0c84(img id %
  1000), fog textures mgr +0x7c / +0x80 via 0x3bf4d4, rooms (sub pictures) it overlaps. Automap manager *0x9f44fc
  (+0x3c map data: +0x28 layers 0x48 each (+8 sections, +0x10 count), +0x30 layer count, +0x40 > 1 = sections tagged
  +4 == manager +0x48). Section 0x40: +0 id, +8 skip, +0x34/+0x38 offset; picture 0x23e174(0x23c4f8(id + 25000, 0)):
  +8/+0xc origin, +0x10/+0x14 size. hle_sys.cpp reveal_map() in field_roam_update (kind 1 = Idolasphere), once per
  (map, map data, drawn part) while setting map_reveal = 1 (default 0; F1 / L3+R3 "Reveal dungeon maps", launcher Game
  page). Uses the game's own explored bits (saved with the game). Verified: slot 20 d003_02 5F: sections 38/39/40
  175->336, 144->459, 0->476 of their cells, minimap shows the unexplored corridors (scratchpad mm.png); slot 12:
  8 sections filled. NOT verified: a floor change by stairs in play, the full map screen.
- 5 No UHD / no uncensor: slot 12 with NX_MODS_DISABLED=uncensored NX_TEX_PACK=0 NX_MOVIE_HD=0: "fs: mod uncensored
  off", field (Rooftop Stairs) renders right, no errors (also the s97 release test ran on stock data). Told the user: yes.
- Regression (this build, defaults): to_field.sh reg99 (base60 replay -> tutorial battle -> field control at
  (-630, -240, -760)): 0 crashes, 0 shader misses, 1% low 59.9 at the 60 cap; user saves md5 unchanged (48362e47...).
  Launcher pages Graphics / Display / Game checked by screenshot (new rows fit).
- NOT done: exe file icons; real VRR screen; ray tracing (not feasible).

## Milestone 5, session 100 (2026-11-23 ~10:00-, user asleep; overnight list: fresh-ZIP setup, reveal map, crash batch, optimisation, release notes)
- (1) Fresh-ZIP NSP setup DONE: Desktop\TMSRecomp-20261123.zip -> private/tms/release_test, bare PATH (System32 only),
  setup\python setup.py --nsp <user NSP> --keys %APPDATA%\eden\keys\prod.keys --data release_test\data: exit 0 in 389 s,
  "icon: from 6d2a8ad3...nca icon_AmericanEnglish.dat" -> data\icon.jpg, game.dll 40 MB, 7207 shader translations.
  base60 replay with the release tms.exe + fresh data (NX_MAP_REVEAL=1, 4K, walk 2): title screen saved as
  data\launcher_hero.bmp at 15.4 s, battle, field control at (-630, -240, -760), 0 crashes, 0 shader translations in
  play. Logs kept: analysis/setup.log, analysis/rel.log. release_test removed (no junctions in it).
- (2) Reveal map: TOPIC -> MAP tab (plus, then r r) shows the whole floor with map_reveal 1, fog with 0 (slot 20 5F,
  scratchpad tmmap.png). Map change d002_02 -> d002_01 in the replay: d002_01 2 sections filled at once. d002_02 gave 0:
  NX_REVEAL_DEBUG=1 dump: the drawn part (tag 2) has section +8 = 1 (the game's skip flag; its own painter returns
  there too) = nothing to reveal. Fix 578261f: n == 0 is retried next frame (quietly) instead of being marked done.
  Stairs inside one map: not driven (no known stair position); covered by the (map, map data, drawn part) key.
- (3) Crash batch DONE: batch.ps1 990 600 with NX_MAP_REVEAL=1 NX_PRESENT_MODE=vrr NX_FX_FXAA=4 NX_DLSS_PRESET=13
  NX_FSR3_QUALITY=1 (60 fps): 4 x 676 s, 0 crashes, battle cues 8 / 10 / 21 / 39, "preset M" in all, 0 DLSS fallbacks,
  reveal ran; user saves md5 unchanged (48362e47...). VRR cap not active at 60 (by design).
- (5) private/release_notes.md: SET UP + Guide, DLSS 4.5 models, VSync modes incl. VRR, revealed maps, emulator saves.
- (4) Optimisation: base60 at the 60 cap (reg99, s99): 1% low 59.0-59.9 in play; the only dips are map loads under
  black fades (game loading: 72-125 ms hitches with 0 ms in our parts = game code). BLOCKED for A/B: Adobe Media
  Encoder (user's encode) uses ~12.7 of 16 cores (s96 rule: no perf runs then). Not stopped (user's process).
- (4) Optimisation, measured once the encode finished (CPU 12 %, GPU 2 % idle): sbperf.sh Shibuya spot uncapped 720p
  with the user's ini (fx_fxaa 4, msaa 4, sharpen 100): 1% low 101-117, 0.1% low 46-80, median 5.9-6.3 ms (= s96 after
  the hitch fix: 107-123). NX_STALL_STATS slowest 1%: 8.1-8.7 ms wall, game thread ran 4.6-5.5 ms (median 4.5-4.9): the
  rest is waiting. NX_GPU_TIME: GPU busy 4.49-4.52 ms per frame = GPU-bound here; game-thread waits are nvnSyncWait on
  the GPU (HITCH_GPU_WAIT 1.3 ms / frame), render thread waits 0. base60 at the 60 cap: 59.0-59.9 in play, dips only
  at map loads under fades (game code). NO code change: no CPU-side gain left at this spot, and GPU pass work is not
  for the night before the release. Next (after release): per-pass GPU timestamps (which pass costs at 4K: MSAA resolve,
  SMAA / DLSS, sharpen) and a cheaper default for weak GPUs.
- Seen: private/tms/build/settings.ini starts with two stray lines "settings: tex_pack = 1" / "= 0" (log text written
  into the user's dev ini at some point; the parser ignores them: no "key = value" key). Left as is (user's file).

## Milestone 5, session 101 (2026-11-23 evening: user playtest, RAM leak)
- User: everything works, but tms.exe reached 43-51 GB private (Task Manager 99% RAM). Their nx.log (E:\GAMES\Tokyo Mirage
  Session PC Port\game): private 6.9 -> 51.6 GB over 238 stat lines, ~1 GB per battle; grows 28 MB/s in battle (scene 0x3),
  11 MB/s otherwise. Settings: 4K, DLSS (fx_fxaa 4, fsr3_quality 1), msaa 8, UHD pack, VRR, 240 fps.
- Ruled out: command handles (flat while RAM grew), command-list recycling, SMAA work images, pack reads, movie planes,
  map reveal. Correlation: 9978 new programs / 207k shared-by-content pipelines vs 581 / 10k in a test battle (17x, RAM 15x).
- Measured with a temporary NX_MEM_ATTR counter (private MB around program_of / combo_of / pipeline / descriptor pools):
  combo_of = 1822 of ~2500 MB battle growth. Each new combo made its own VkDescriptorSetLayout + VkPipelineLayout and the
  NVIDIA driver kept ~3 MB per pair. Battles load the same shaders at new addresses, so combos never stop coming.
- Fix (e858815): make_layout shares one layout pair per binding list (never destroyed); prewarm keeps its layouts.
  After: combo 12 MB, battle growth +0.9 GB (first-battle content), Aversa lose/retry x4 flat at 8.0 GB; batch 4x300 s
  0 crashes, 0 pipeline failures / shader misses. Test scripts: agent_scripts/leakab.sh, retryloop.sh, btlloop.sh
  (btlloop: post-battle menus stall it; i2.sh loads fail with 3 instances at once).
- ZIP rebuilt: Desktop\TMSRecomp-20261123.zip. Not checked: a 40-battle session like the user's.

### v0.1.1 queue (user 11-24: "later, with more fixes")
- c2900cb: a newer xdelta patch removes the older patch mod (only mods made solely of romfs/Pack cpks it covers);
  a new UHD / MovieHD ZIP removes files the old pack had; ZIP skip check = size + ZIP time (size alone kept changed
  same-size files). Tested with temp folders; Guide sentence not visually checked.
- Release steps: bump k_version above 0.1.0.1 (user's install reports 0.1.0.1 after the update test), commit the
  changed files on top of branch `public` (noreply identity), push public:main, package, gh release create --latest.
- agent_scripts/launcherpage.ps1 -> wincap.ps1 captures by process NAME: it grabbed the user's open launcher once.
  Capture the started pid only (or check no other launcher.exe runs) before using it again.
- Setup signature includes setup/tools: any setup.py change makes players' launcher rebuild game.dll after updating.
- 11-24 (s102): Overworld costume (field_costume, default 0) is in the v0.1.1 queue: names.txt changed (re-lift), so
  players' launchers rebuild game.dll after the update anyway.

## Milestone 5, session 102 (2026-11-24, with user): Overworld costume + Hard difficulty formula

### Overworld costume (USER 11-24: "costume wardrobe in battle, but overworld never shows it")
- How the game picks clothes (Ghidra): model loader 0x3cc560 (via 0x3cc6b4, desc {char, costume, use_equipped, use_default})
  builds "Character/player/%s/skin/%02d" (name = CharacterTable row 0x350634 +0x48, skin = PlayerCostume2SkinTable row
  0x350688(char, costume) +6). Costume source: use_default -> PlayerDefaultCostumeTable row 0x3506fc (12 bytes: id, s16
  costume +4, s16 flag that must be on +8, must be off +10, -1 none; story clothes); use_equipped -> 0x3613c0 (party slot
  -> 0x352f2c +0x54 dress item -> ItemDressTable +10; 1 when none; 0x3ec / 0x3ed / 0x3f2 fixed 0x31); else explicit.
  Then 0x35083c remaps Tsubasa (1002) 2/3/4/0x26 -> the glasses variants when save +0x52106 (SetGlasses) is set.
- Costume ids (ScriptCommon/CostumeID_Define.lua): 0 PRIM, 1 CLASSFORM (Carnage battle outfit = no dress), 2 TRAINING,
  3..6 USUAL1..4, 15 MARTH, 38 STUDENT, 39..41 DLC_01..03, 49 SWITCH, 50..53 glasses variants. Defaults: Itsuki 3 (4 after
  flag 0x3ee3), Tsubasa 0x26 school uniform (3 after flag 0x42a, 4 after 0x508), ...
- Fix: names.txt costume_default_row 0x3506fc (re-lift 20653 hooks); hle_sys.cpp hook puts the equipped dress into the
  row's +4 (restored from a host copy first on every call; the table is shared). Same row feeds the reload check 0x407ea4,
  so loader and check agree. Skipped: dress 1, the three fixed ids, not joined (0x3535f4), no skin row (0x350688 null).
- Setting field_costume (default 0): F1 "Overworld costume", native PC 4/4 row 4, settings.ini comment. Applies on the next
  model load (area change / load), not instantly: 0x3506fc is not called per frame (live "env" toggle test: no reload).
- New control command `env NX_KEY=v` (ui.cpp): _putenv a setting live, for rigs.
- Verified (slotn.sh slot 20 = user's 11-20 save, Itsuki has TRAINING (2) equipped, Tsubasa / Touma casual): on: log
  "costume: character 1001 outside battle wears 2 (story clothes 3)", Itsuki in the training outfit on 5F; battle (walk
  rig, fc4) normal; back in the field still the training outfit; off (fc5): blue jacket story clothes, no log line.
  NOT verified: story scenes with other members, town, the native PC 4/4 row on screen, a dress change in the Equip menu
  (expected: reload on the next area load via 0x407ea4).

### Difficulty (USER 11-24 question; save byte G + 0x52105 = config +0x520f8 +0xd; Lua Get/SetDifficulty 0x4355e0 / 0x435510)
- Values: 0 Friendly, 1 Easy, 2 Normal, 3 Hard, 4 Lunatic (DFCLSEL_MENU_ITEM_*; IsSysDiffLunaticUnlock).
- Battle setup 0x2c4108 writes battle floats +0x98 / +0x9c / +0xa0 / +0xa4 (+0xa8 = 20 always):
  Friendly 1.5 / 0.5 / 1.25 / 50; Easy 1.25 / 0.8 / 1.25 / 50; Normal 1 / 1 / 1 / 30; Hard 0.8 / 1.25 / 1 / 1;
  Lunatic 0.5 / 1.5 / 1 / 1.
- +0x98 = damage dealt by the party (end of damage formula 0x29d104: attacker side vt+0x160 == 1), +0x9c = damage the
  party takes (target side 1), +0xa0 = money (btl_add_reward), +0xa4 = base escape chance % (0x2a5c50 ~0x2a6c80:
  a4 + level ratio x a8 + ... + 7 per earlier try vs random).
- Ailment chance 0x29cbec: Normal and below: x0.7 when target unit data +0x198 == 1, else x1.0; Hard / Lunatic: x1.0
  when +0x198 == 1, else x0.85 (+0x198 assumed = party member; not checked at runtime).
- Friendly / Easy only (< 2): EXP for members below the enemy's level +20% per level (not +10%), max 200%; +1 on a
  per-member battle counter at battle +0x556 + 2 i (victory, 3 or 1 base; meaning not identified); +600 on a victory
  value (0x2c6ca8 state 0xd; meaning not identified); a one-time notice (0x465dc0).

### Unlock all difficulties (USER 11-24: "unlock it automatically and put it in launcher setting")
- Unlock bytes: system data **0x9ef37c + 0xa6b95 = Lunatic (set 1 at game clear, 0x269708), + 0xa6b96 = Friendly (set by
  the Game Over notice on Easy / Friendly, 0x465dc0). Readers: title 0x4a0060 / 0x4a0a30 (mirror into flags 0x55 Friendly /
  0x56 Lunatic for the New Game menu), Lua IsSysDiffFriendlyUnlock 0x43009c / IsSysDiffLunaticUnlock 0x4300d4, Settings
  fill 0x33b9e8 (row 10 difficulty: value +0x114, arrows +0x118, min +0x11c = 1 unless Friendly, max +0x120 = 3; 4..4
  when already Lunatic, so the game never lets you leave or reach Lunatic mid-game).
- Fix (names.txt 5 new: camp_settings_fill, title_menu_update, title_menu_return, lua_IsSysDiff*; re-lift 20658 hooks):
  probes set both bytes (log "difficulty: Friendly and Lunatic unlocked"); camp_settings_fill sets row 10 range 0..4 with
  arrows. Setting all_difficulties (default 1). Bytes persist in system.bin like the game's own unlocks (Off does not relock).
- Launcher Game page: new rows Overworld costume (FIELD) and Unlock all difficulties (new DIFFICULTY section).
- Verified (setpages.sh df1-df3, user's slot 20 on Hard): row shows Normal / Easy / Friendly / Lunatic; Apply Yes with
  Lunatic, leave, reopen: Lunatic with both arrows. NOT verified: the New Game difficulty screen (rig ng1 loaded a save;
  unlock log fired at the title 19.8 s), launcher page on screen.

### Setup: NSPs with a title-key ticket (Reddit report 11-24: "failed to find title.keys", prod.keys + title.keys in one folder)
- Cause: setup ran nstool on the program NCA alone; an NCA with a RightsId (eShop-style NSP, .tik + .cert inside) then has
  "NCA Partition 0 not readable. (AES-CTR Key was not determined)". The title.keys warning is nstool's (always printed).
  The user's own TMS NSP has no .tik (standard crypto), so it always worked here.
- Fix (setup.py extract_nsp / get_icon): pass --tik <the NSP's .tik> to every NCA extraction; the error text mentions the
  title key when there is no ticket. Verified with a ticketed NSP (Catherine update 0100BF00112C0800) and prod.keys alone:
  without --tik no exefs, with it exefs extracted (its romfs fails: update NCA = patch romfs, needs the base; expected).
  setup.py changed: players' launchers rebuild game.dll after the update.
