TMSRecomp - Tokyo Mirage Sessions #FE Encore, recompiled for Windows
=====================================================================

This ZIP holds the program and its setup tools only: no game code, no game files. On the first start the launcher's
Setup page builds the game from YOUR OWN copy (Switch, title 0100A9400C9C2000, base game 1.0.0 without update):
pick your NSP and the prod.keys from your own console (or a folder you already extracted with exefs\ and romfs\).
Setup copies the game files (about 13 GB), translates the game code, compiles it into game.dll next to tms.exe and
translates all shaders. It takes about 5 to 15 minutes and needs no internet.

Requirements
- Windows 10/11, 64-bit, a GPU with Vulkan 1.3
- Nothing else to install (the shader translator in shaderc\ carries its own .NET runtime)
- About 15 GB free disk space for the game files

Start
1. Extract this folder anywhere (keep the setup\ folder).
2. Run launcher.exe. The Setup page opens: pick your game, press "Set up game files", wait for "Done".
3. PLAY. The game's saves, caches, logs and screenshots live in the game files folder.
   Some antivirus tools look closely at a program that runs a compiler; everything stays inside these folders.

Files
- tms.exe        the game (F1 or L3+R3: settings overlay; F12: screenshot; Alt+Enter / F11: window)
  command line: --data <folder> (game files), --set key=value (any settings.ini key, this run only, repeatable),
  for example: tms.exe --set window=window --set res=1080p --set fps=60
- launcher.exe   settings + PLAY
- settings.ini   written on the first start (fps, resolution, window, ...)
- subtitles_en.tsv   English subtitles for the battle voices
- shaderc\       shader translator (Ryujinx shader compiler, MIT)
- amd_fidelityfx_loader_vk.dll, amd_fidelityfx_upscaler_vk.dll   AMD FSR 3 (MIT), used only with Anti-aliasing = FSR 3
- setup\         first-run setup: Python, clang + lld-link (LLVM), nstool, our build tools
- game.dll       made by setup from your game (not in the ZIP)

Optional (the launcher's Guide page explains each one and installs it for you)
- Mods: <data>\mods\<name>\romfs\... replaces game files (LayeredFS style). The program works with or without an
  English/uncensor patch.
- Making mods (no tools of ours needed; restart the game after a change):
  - Game files: put them in <data>/mods/<ModName>/romfs/ at the same path as in <data>/romfs/ (setup extracts the
    game there, so you can copy a file out, change it and put it in your mod). Files you do not ship come from the game.
  - Textures: set tex_dump = 1 in settings.ini and play: every texture shown is saved once to
    <data>/textures/dump/<w>x<h>_<format>_<hash>.dds. Edit one, keep the _<hash> at the end of the name, and put it in
    <data>/mods/<ModName>/textures/ (subfolders are fine). Any size works (2x, 4x); DDS in BC1-BC7 or RGBA8, with a mip
    chain (texconv -m 0). Mod textures replace the UHD pack's, and follow the same on/off switch (tex_pack).
  - Several mods: for the same file or texture the mod whose folder name sorts first wins. Turn mods off without deleting
    them with mods_disabled = Name1,Name2 in settings.ini (or the launcher's Mods page).
  - The log (<data>/nx.log) lists each mod at start: "fs: mod <name> on", "textures: mod <name>: N".
- UHD textures: the separate TMSRecomp-UHD ZIP. Extract it into the data folder (it adds textures\pack\). Toggle in
  the F1 overlay ("UHD textures", after a restart) or settings.ini tex_pack = 0/1. Textures without a replacement
  (for example with a different mod installed) stay as they are.
- Your own battle music: put CRI .adx files (for example the loose files of a Persona 5 Royal battle music mod,
  "<id>_<series>_<title>.adx"; titles with "Victory" are victory themes) into <data>\music, or set custom_bgm_dir
  in settings.ini. Then Random battle music = Custom (or Mixed) in the launcher, the F1 menu or the PC settings
  page. Encrypted .adx files (header type 9) need their keycode in settings.ini custom_bgm_key
  (none is included); nx.log names such files. The victory theme of the same series plays when you win. Volume: Custom music volume.
- FSR 1: with Resolution below your screen size, Upscaler = FSR 1 scales the image up with sharp edges (more fps
  than rendering at full size).
- Anti-aliasing = FSR 3: AMD FSR 3 temporal anti-aliasing at full resolution (like DLAA). Smoothest edges and no
  shimmer on the city; moving characters are smoothed a little less. Without the two amd_fidelityfx DLLs it uses SMAA.
- Anti-aliasing = DLSS: NVIDIA DLSS / DLAA on RTX GPUs. Not in this ZIP: on the launcher's Setup page tick "Download NVIDIA
  DLSS" (the file comes from NVIDIA's own GitHub and is under NVIDIA's licence). Without it FSR 3 runs instead. Upscaling
  row: Native = DLAA, Quality .. Ultra Performance = DLSS modes. The file is DLSS 310.9 (DLSS 4.5 models); the DLSS model
  row (settings.ini dlss_preset) picks K, M or L, Auto = NVIDIA's pick per mode. NVIDIA and DLSS are trademarks of NVIDIA
  Corporation; TMSRecomp is not affiliated with or endorsed by NVIDIA.
- VSync = VRR: for G-SYNC / FreeSync screens (turn VRR on in the GPU driver). Classic vsync plus a frame cap 3 fps under
  the refresh rate when the frame rate is set higher (or uncapped), so the screen follows every frame without tearing.
- Window icon and the launcher's picture come from your own game: the NSP's icon (setup) and the title screen, saved
  once on the first start (launcher_hero.bmp in the game files folder; replace it with any picture you like).

Licences: TMSRecomp is GPL-2.0-or-later (LICENSE). Third-party notices: THIRD_PARTY.txt.

TMSRecomp is an unofficial fan project. It is not affiliated with, endorsed or sponsored by Nintendo, ATLUS, SEGA or
Intelligent Systems. Tokyo Mirage Sessions #FE Encore and all related names, characters and assets are trademarks and
copyrights of their owners. You need your own legally obtained copy of the game; this project does not help you obtain
the game or its keys, and none of its files may be shared with these programs.
