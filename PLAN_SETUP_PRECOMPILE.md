# Plan: first-run setup, all-shader precompile, no shipped game code

Written 2026-10-30 from a design talk with the user (no code changed, written while another
session was running). Read with NOTES.md "session 36" (pipeline recipes, prewarm, cache_seed).

## Goals (user)

1. No shader stutter from the very first minute, also in areas nobody has visited.
2. No need for anyone (user or dev) to do a full playthrough to build a cache seed.
3. Remove the legal risk: the release must not contain translated game code or data
   derived from the game.
4. Keep the Ryujinx MIT shader translator (user decision 10-30: do NOT write our own).

## Model: SavageWind (BotW/TotK recomp)

Their first-run screen: user picks the folder with their own extracted game (exact versions
listed), toggles "Precompile all shaders" (default On: "a few more minutes, ~1.5 GB", can be
done later from the config app), then "Set up game files". The download holds only tools; the
game code is built and every shader translated on the user's PC.

## Why the release is risky today

- `tms.exe` contains lifted game code (from `tools/recomp`). This is the risk.
- `cache_seed` (s36, `package.ps1 -Seed`) holds translated game shaders: also derived data.
- The Ryujinx translator itself is NOT a risk (MIT, credited in README). Its cost is the .NET
  runtime + Ryujinx files, which we accept.

## Target release layout

Ships: launcher.exe, runtime (as a static lib or object files), lifter `tools/recomp`, the
shader sidecar `tools/shaderc` (+ .NET runtime, or self-contained publish), a bundled
compiler toolchain (clang + lld + Windows SDK libs we may redistribute; check licences),
hook/address tables, data/ (subtitles etc., our own text only), LICENSE, README.
Never ships: tms.exe, generated .cpp, cache_seed, any game file.

## Phases (do in this order; each one is useful alone)

### Phase 1: offline all-shader translation (do first, smallest)

- Find where the game keeps shader binaries (NVN program blobs inside the game's archives /
  romfs). Same idea as `tools/texextract` (offline texture scan, same hashes as runtime).
- New tool (e.g. `tools/shaderscan`): walk the user's game data, extract every shader, key it
  exactly like the runtime does, translate via the existing sidecar, write into the normal
  `<data>/cache/shaders.bin`. Runtime then does 0 translations.
- Pipelines (vertex layout, blend, render-target formats) are only known at runtime. Keep the
  s36 recipes + prewarm for that part. Option to look at: record a generic recipe set made of
  OUR state descriptions only (no game bytes) and ship it, so prewarm can build most pipelines
  on first start. Check whether a recipe contains game-derived bytes before shipping it.
- Done when: fresh `<data>/cache`, run the scan, play new areas, hitch log shows no shader
  translations and pipeline creation near the s36 seeded number (36 ms).

Unknowns: does the game keep all shaders in files, or build/patch any at runtime? Do the
uncensor patches / UHD pack change shader blobs? (Most likely not, but check: the cache key
must still match.)

### Phase 2: build the game on the user's PC

- Launcher setup page: pick game folder (NSP, or extracted folder) -> verify -> lift -> compile
  -> link -> tms.exe in the install folder -> (optional) Phase 1 shader scan.
- Version check is required: all hooks use fixed addresses for the ASIA base (title
  0100A9400C9C2000). Hash main/sdk NSOs and refuse unknown versions with a clear message
  (list the supported version like SavageWind does). Other regions/updates = their own
  address tables later, not now.
- Keys: needs the user's own prod.keys to decrypt the NSP. Ask for the file in setup (same as
  emulators). Never ship keys. Supporting an already-extracted folder avoids keys entirely.
- Must reuse the dev build path (same lifter flags, same CMake/ninja steps) so dev and setup
  never differ. One script, two callers.

### Phase 3: package

- `tools/package/package.ps1`: new mode that builds the tools-only ZIP and asserts it has no
  tms.exe, no generated code, no cache_seed (fail the build if found).
- UHD pack ZIP: textures are upscaled game textures = derived data. Same problem as the
  seed. Options: ship the upscale pipeline (needs Real-ESRGAN, ~10 h, big) or keep the pack as
  a separate, clearly marked download. Needs a user decision.

## What a NEW user sees (consequences)

- Bigger first step: pick game folder (+ keys if NSP), wait. Estimate: lift + compile maybe
  5-20 min (measure our own build time and say the real number on screen), shader scan a few
  more minutes, disk ~1-2 GB extra. Must show progress, time left, and a working Cancel.
- Toolchain download or bundle size: clang + libs is hundreds of MB. Bundled = big ZIP,
  downloaded = needs internet at setup.
- Antivirus: an app that runs a compiler and writes a fresh exe can trigger heuristics. Keep
  everything inside the install folder; no admin rights; document it.
- Wrong game version or bad dump: must fail early with a plain message, never a crash later.
- After setup: no stutter in new areas from the first minute (the goal).
- Updates: when we update the runtime/hooks, setup must re-run the build (fast if the lift
  output is cached; slow if not). The launcher's GitHub updater has to trigger that.

## What it means for the DEV (consequences)

- Every bug report now depends on the user's local build: log the toolchain version, lifter
  version, game hash, and build log path in issues.log.
- Build must be deterministic and work on clean machines (no paths into private/, no
  dependence on our Ghidra project or private/third_party at runtime). Test on a clean user
  account / VM.
- `tools/shaderc` dll stamp keys the shader cache (NOTES s26). The setup scan and the runtime
  must use the SAME sidecar build, or every cache is thrown away. Never rebuild shaderc
  casually; ship it pinned. The Ryujinx `spirv-no-elseif.patch` must be in the shipped build.
- The s30 rule still applies: nothing may shrink a user's cache; the scan only adds.
- Keep the current dev path (play.bat, tms.exe built here) unchanged. Setup is an extra page
  and an extra script, not a replacement. That way nothing that works now breaks.

## User decisions (2026-10-30)

1. Toolchain: "whatever is easiest" -> BUNDLE clang/lld/libs inside the ZIP (no download
   code, no internet needed at setup; cost = bigger ZIP). Check each redistribution licence.
2. Game input: user dumps their OWN game + OWN prod.keys. Setup accepts NSP + prod.keys
   (decrypt like nstool does now); an extracted folder may also be accepted. Never ship keys.
3. UHD pack: user does NOT want users upscaling (~10 h). Keep sharing the user's own
   upscaled pack as a SEPARATE optional download (as now: TMSRecomp-UHD-*.zip). Note: it is
   still derived from game textures, so it carries some risk, but HD texture packs are
   commonly shared this way and keeping it apart keeps the program download clean.
   Do not mix it into the program ZIP.
4. Phase 1 already started in a running session (10-30). Check NOTES.md for its state
   before doing anything here.

## Status (2026-10-31, session 38)

Phase 1 done + in-game checked (5 translations left in a replay, see NOTES s38). Phase 2 built: game.dll split,
tools/setup/setup.py + build_game.py, launcher Setup page; NSP mode untested. Phase 3: package.ps1 ships setup\ and
refuses game code; needs the Python embeddable package + licence texts (downloads, ask user).

## Rules still in force

No GitHub upload until the user's full game test. Ask before delete/push/publish/install.
Measure before change. Logs as proof.
