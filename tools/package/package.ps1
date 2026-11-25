# package.ps1 [-Out <dir>] [-Uhd] [-StageOnly]: release ZIPs from the current build (private\tms\build) on the Desktop.
#   TMSRecomp-<date>.zip      program + setup tools: tms.exe (runtime only), launcher, SDL3.dll, subtitles, shader
#                             translator, setup\ (python, clang + lld-link, nstool, sdk, our tools), README, licences.
#                             NO game code or data: game.dll, the lifted C, translated shaders and caches are made on
#                             the player's PC by setup (tools\setup\setup.py). The script fails if any of them is staged.
#   TMSRecomp-UHD-<date>.zip  (-Uhd) the UHD texture pack: textures\pack\*.dds, to extract into the data folder.
#   -StageOnly                stop after staging (%TEMP%\tmsr_package\TMSRecomp), for setup tests.
# Third-party files expected in private\third_party: python-embed\ (python-3.12 embeddable package + capstone package in
# python-embed\Lib\site-packages, python312._pth with "Lib\site-packages"), nstool\nstool.exe + nstool\LICENSE,
# llvm-LICENSE.TXT (LLVM's licence); clang.exe/lld-link.exe come from C:\Program Files\LLVM\bin.
#   TMSRecomp-MovieHD-<date>.zip  (-MovieHd) 4K story movies: movie_hd\story (stock VP9) + movie_hd\story_mod (the
#                             uncensored mod's MPEG-1 m06 / m07 / m12), made by tools\camphd\camphd.py; into the data folder.
param([string]$Out = [Environment]::GetFolderPath("Desktop"), [switch]$Uhd, [switch]$MovieHd, [switch]$StageOnly)
$ErrorActionPreference = "Stop"
$tar = Join-Path $env:SystemRoot "System32\tar.exe"  # Windows bsdtar (writes ZIP); not a Git Bash tar on PATH
$root = Resolve-Path "$PSScriptRoot\..\.."
$build = "$root\private\tms\build"
$tp = "$root\private\third_party"
$llvm = "C:\Program Files\LLVM\bin"
$date = Get-Date -Format "yyyyMMdd"
$stage = Join-Path $env:TEMP "tmsr_package\TMSRecomp"
if (Test-Path (Split-Path $stage)) { Remove-Item (Split-Path $stage) -Recurse -Force }
New-Item -ItemType Directory -Force $stage | Out-Null
foreach ($f in "$tp\python-embed\python.exe", "$tp\nstool\nstool.exe", "$tp\nstool\LICENSE", "$tp\llvm-LICENSE.TXT") {
    if (-not (Test-Path $f)) { if ($StageOnly) { Write-Warning "missing $f (staged without it)" } else { throw "missing $f (see the header)" } }
}

# program files come from a release build WITHOUT the exe icon: the dev build embeds private\tms\icon.ico = the game's own
# art (CMakeLists NX_ICON), which must not ship. Same sources and settings as build.cmd, own build folder.
$rel = "$root\private\tms\build_rel"
$vscm = "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake"
$env:PATH = "$vscm\CMake\bin;$vscm\Ninja;$llvm;$env:PATH"
if (-not (Test-Path "$rel\build.ninja")) {
    cmake -S $root -B $rel -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ "-DNX_ICON="
    if ($LASTEXITCODE) { throw "release configure failed" }
}
cmake --build $rel --target tms launcher
if ($LASTEXITCODE) { throw "release build failed" }
if (Test-Path "$rel\icon.rc") { throw "$rel embeds an icon (the game's art): delete $rel and run again" }
foreach ($f in "tms.exe", "launcher.exe", "SDL3.dll", "subtitles_en.tsv") { Copy-Item "$rel\$f" $stage }
# AMD FSR 3 (Anti-aliasing = FSR 3): the SDK's MIT-licensed signed Vulkan DLLs, unmodified (NOTES s62). Nothing from NVIDIA.
foreach ($f in "amd_fidelityfx_loader_vk.dll", "amd_fidelityfx_upscaler_vk.dll") { Copy-Item "$rel\$f" $stage }
# Microsoft C++ runtime next to the exes (Distributable Code, app-local): without it a PC lacking the VC++ redistributable cannot even
# open launcher.exe to say why. Newest toolset installed, so never older than the one that built the exes.
$crt = Get-ChildItem "$env:ProgramFiles\Microsoft Visual Studio\*\*\VC\Redist\MSVC\*\x64\Microsoft.VC*.CRT" -Directory | Sort-Object { [version]$_.Parent.Parent.Name } | Select-Object -Last 1
if (-not $crt) { throw "no Visual C++ redistributable folder found (Visual Studio is needed to package)" }
foreach ($f in "vcruntime140.dll", "vcruntime140_1.dll", "msvcp140.dll", "msvcp140_atomic_wait.dll") { Copy-Item (Join-Path $crt.FullName $f) $stage }
Copy-Item "$rel\resist_icons" $stage -Recurse  # resistance badge icons (user's own art)
Copy-Item "$PSScriptRoot\README.txt" $stage
Copy-Item "$root\LICENSE" $stage
# shader translator: robocopy keeps file times (the shader cache is stamped with NxShader.dll's time)
#   self-contained build (players need no .NET install): README.md build step 4b; app DLLs copied from shaderc\ (same stamp)
robocopy "$root\private\tms\shaderc_sc" "$stage\shaderc" /E /XF *.pdb *.nupkg /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy shaderc failed ($LASTEXITCODE)" }

# setup\: everything the first-run setup needs to build game.dll from the player's own game (tools\setup\setup.py)
$su = "$stage\setup"
New-Item -ItemType Directory -Force "$su\llvm", "$su\sdk", "$su\tools\recomp", "$su\tools\texextract", "$su\tools\shaderscan", "$su\tools\setup" | Out-Null
Copy-Item "$llvm\clang.exe", "$llvm\lld-link.exe" "$su\llvm"
if (Test-Path "$tp\nstool\nstool.exe") { Copy-Item "$tp\nstool\nstool.exe" $su }
if (Test-Path "$tp\python-embed") { Copy-Item "$tp\python-embed" "$su\python" -Recurse }
Copy-Item "$root\runtime\include\guest.h", "$rel\tms.lib", "$build\nx_crt_math.lib", "$build\nx_vcruntime.lib", "$root\tools\setup\game.def" "$su\sdk"
Copy-Item "$root\tools\recomp\link.py", "$root\tools\recomp\lift.py", "$root\tools\recomp\a32.py", "$root\tools\recomp\vfp.py", "$root\tools\recomp\names.txt" "$su\tools\recomp"
Copy-Item "$root\tools\nso.py", "$root\tools\cpk.py", "$root\tools\vcdiff.py" "$su\tools"  # vcdiff: launcher Guide, xdelta mods
Copy-Item "$root\tools\texextract\texextract.py", "$root\tools\texextract\fasttex.dll" "$su\tools\texextract"
Copy-Item "$root\tools\shaderscan\shaderscan.py" "$su\tools\shaderscan"
Copy-Item "$root\tools\setup\setup.py", "$root\tools\setup\build_game.py" "$su\tools\setup"

# no game code or data in the program ZIP (plan: the release must not contain translated game code or game-derived data)
$bad = Get-ChildItem $stage -Recurse -File | Where-Object {
    $_.Name -match '^(nvngx.*\.dll|nvsdk_ngx.*|game\.dll|game\.pdb|tms\.pdb|image\.bin|layout\.json|shaders\.bin|pipelines\.(bin|recipes)|files\.txt|funcs\.h|table\.c|f_\d+\.c)$' -or
    $_.Extension -in ".nca", ".nsp", ".obj", ".cpk", ".keys" }
if ($bad) { throw "game code/data staged, refusing to package: $($bad.FullName -join ', ')" }
if ((Get-Item "$stage\tms.exe").Length -gt 8MB) { throw "tms.exe is $((Get-Item "$stage\tms.exe").Length) bytes: does it still contain game code?" }
if ($StageOnly) { Write-Output "staged $stage"; return }

$notice = "Third-party software in this package`r`n`r`n"
foreach ($l in @(@("SDL3 (SDL3.dll), zlib licence", "$tp\SDL3-3.4.16\LICENSE.txt"),
                 @("libvpx (VP9 movie decoding, in tms.exe), BSD-3-Clause", "$tp\libvpx\LICENSE"),
                 @("Ryujinx shader translator (shaderc\) and BC7 tables (in tms.exe, runtime/src/bc7.h), MIT", "$tp\ryubing\LICENSE.txt"),
                 @("Spv.Generator (shaderc\, sharpening/overlay shaders in tms.exe), MIT", "$tp\ryubing\src\Spv.Generator\LICENSE"),
                 @("LLVM clang + lld-link (setup\llvm\), Apache-2.0 WITH LLVM-exception", "$tp\llvm-LICENSE.TXT"),
                 @("AMD FidelityFX / FSR SDK 2.4.0 (amd_fidelityfx_loader_vk.dll, amd_fidelityfx_upscaler_vk.dll), MIT", "$tp\FidelityFX-SDK-2.4.0\LICENSE-shipped-MIT.txt"),
                 @("nstool (setup\nstool.exe), MIT", "$tp\nstool\LICENSE"),
                 @("Python (setup\python\), PSF licence", "$tp\python-embed\LICENSE.txt"),
                 @("Capstone (setup\python\Lib\site-packages\capstone), BSD-3-Clause", "$tp\python-embed\Lib\site-packages\capstone-5.0.9.dist-info\LICENSE.TXT"))) {
    $notice += "==== " + $l[0] + "`r`n`r`n" + (Get-Content $l[1] -Raw) + "`r`n`r`n"
}
$notice += "==== Microsoft Visual C++ runtime (vcruntime140.dll, vcruntime140_1.dll, msvcp140.dll, msvcp140_atomic_wait.dll)`r`n`r`nCopyright (c) Microsoft Corporation. Unmodified Distributable Code of Microsoft Visual Studio, under its licence terms.`r`n`r`n"
Set-Content "$stage\THIRD_PARTY.txt" $notice -Encoding utf8

# write to a temporary name first: a failed run never removes the previous ZIP
$zip = Join-Path $Out "TMSRecomp-$date.zip"
& $tar --format zip -c -f "$zip.part" -C (Split-Path $stage) TMSRecomp
if ($LASTEXITCODE) { throw "tar failed" }
Move-Item -Force "$zip.part" $zip
Write-Output "wrote $zip ($([math]::Round((Get-Item $zip).Length / 1MB, 1)) MB)"

if ($Uhd) {
    $ustage = Join-Path $env:TEMP "tmsr_package\uhd"
    New-Item -ItemType Directory -Force $ustage | Out-Null
    Set-Content "$ustage\README_UHD.txt" ("TMSRecomp UHD textures. Install: launcher.exe, Guide page, UHD textures, Install ZIP. Or by hand: extract into your game data folder (the one with romfs), so that " +
        "textures\pack\*.dds sits next to romfs. Toggle: F1 overlay 'UHD textures' (after a restart) or settings.ini tex_pack.") -Encoding utf8
    $uzip = Join-Path $Out "TMSRecomp-UHD-$date.zip"
    # the pack is added in place (-C <data> textures/pack): no copy of tens of GB
    & $tar --format zip -c -f "$uzip.part" -C $ustage README_UHD.txt -C "$root\private\tms" textures/pack
    if ($LASTEXITCODE) { throw "tar (UHD) failed" }
    Move-Item -Force "$uzip.part" $uzip
    Write-Output "wrote $uzip ($([math]::Round((Get-Item $uzip).Length / 1GB, 2)) GB)"
}

if ($MovieHd) {
    $mstage = Join-Path $env:TEMP "tmsr_package\moviehd"
    New-Item -ItemType Directory -Force $mstage | Out-Null
    Set-Content "$mstage\README_MovieHD.txt" ("TMSRecomp 4K movies: story movies + camp menu backgrounds (AI-upscaled offline from the " +
        "game's 720p movies with Real-ESRGAN, VP9; camp backgrounds redone 11-25 with the anime model: sharper faces).`r`nInstall: launcher.exe, Guide page, 4K movies, Install ZIP. " +
        "Or by hand: extract into your game data folder (the one with romfs), so that movie_hd\ sits next to romfs. The game " +
        "plays them in place of the 720p movies; any movie without a 4K file plays as before.`r`nstory_mod = m06 / m07 / m12 of " +
        "the uncensored mod (used only while that mod is on).`r`nOff: settings.ini line movie_hd = 0, or delete the folder. " +
        "Decoding 4K VP9 costs some CPU during movies; a CPU too slow for it plays the 720p movie.") -Encoding utf8
    $mzip = Join-Path $Out "TMSRecomp-MovieHD-$date.zip"
    # camp menu backgrounds were the separate CampHD ZIP (11-02): one ZIP now
    $parts = @("movie_hd/story") + @(foreach ($d in "story_mod", "camp") { if (Test-Path "$root\private\tms\movie_hd\$d") { "movie_hd/$d" } })
    & $tar --format zip -c -f "$mzip.part" -C $mstage README_MovieHD.txt -C "$root\private\tms" @parts
    if ($LASTEXITCODE) { throw "tar (MovieHD) failed" }
    Move-Item -Force "$mzip.part" $mzip
    Write-Output "wrote $mzip ($([math]::Round((Get-Item $mzip).Length / 1GB, 2)) GB)"
}
