TMSRecomp - Tokyo Mirage Sessions #FE Encore, recompiled for Linux (x86-64, experimental)
=========================================================================================

This tarball holds the program and its setup tools only: no game code, no game files. On the first start the
launcher's Setup page builds the game from YOUR OWN copy (Switch, title 0100A9400C9C2000, base game 1.0.0 without
update): pick your NSP and the prod.keys from your own console (or a folder you already extracted with exefs/ and
romfs/). Setup copies the game files (about 13 GB), translates the game code, compiles it into game.so next to tms
and translates all shaders. It takes about 5 to 15 minutes and needs no internet.

Requirements
- x86-64 Linux with glibc 2.39 or newer (Ubuntu 24.04, Debian 13, Fedora 40, SteamOS 3.7 or newer), a GPU with Vulkan 1.3
- cairo and pango (installed on every desktop)
- About 15 GB free disk space for the game files
- Nothing to install: Python, clang + lld (they compile the game code), nstool, the .NET runtime of the shader
  translator, SDL3 and libvpx are in this tarball (works on the Steam Deck's read-only SteamOS)

Start
1. Extract this folder anywhere (keep the setup/ folder): tar xzf TMSRecomp-*-linux-x64.tar.gz
2. Run ./launcher. The Setup page opens: pick your game, press "Set up game files", wait for "Done".
3. PLAY. Steam Deck: in Desktop Mode add tms (or launcher) to Steam as a non-Steam game for Game Mode.
   The game's saves, caches, logs and screenshots live in the game files folder.

Files
- tms          the game (F1 or L3+R3: settings overlay; F12: screenshot; Alt+Enter / F11: window)
  command line: --data <folder> (game files), --set key=value (any settings.ini key, this run only, repeatable)
- launcher     settings + PLAY
- settings.ini written on the first start next to tms (or ~/.config/TMSRecomp/ when this folder is read-only)
- shaderc/     shader translator (Ryujinx shader compiler, MIT; carries its own .NET runtime)
- setup/       first-run setup: Python, clang + lld (LLVM), nstool, our build tools
- game.so      made by setup from your game (not in the tarball)

Differences from Windows: no AMD FSR 3 and no NVIDIA DLSS (they fall back to SMAA); the launcher's Update button opens
the release page. Battles, AMD / Intel GPUs and the Steam Deck are not tested much yet: please report with your nx.log
(in the game files folder) at https://github.com/godofknife/TMSRecomp/issues

Licences: TMSRecomp is GPL-2.0-or-later (LICENSE). Third-party notices: THIRD_PARTY.txt.

TMSRecomp is an unofficial fan project. It is not affiliated with, endorsed or sponsored by Nintendo, ATLUS, SEGA or
Intelligent Systems. Tokyo Mirage Sessions #FE Encore and all related names, characters and assets are trademarks and
copyrights of their owners. You need your own legally obtained copy of the game; this project does not help you obtain
the game or its keys, and none of its files may be shared with these programs.
