# make_shortcut.ps1 [folder] [-game]: a "Tokyo Mirage Sessions #FE Encore" shortcut to private\tms\build	mslauncher.exe
# (settings + PLAY), or straight to tms.exe with -game (default folder: your Desktop). Settings: build\settings.ini.
param([string]$folder = [Environment]::GetFolderPath("Desktop"), [switch]$game)
$exe = [System.IO.Path]::GetFullPath("$PSScriptRoot\..\private\tms\build\" + $(if ($game) { "tms.exe" } else { "tmslauncher.exe" }))
if (-not (Test-Path $exe)) { throw "$exe not found: run build.cmd first" }
$lnk = (New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $folder "Tokyo Mirage Sessions #FE Encore.lnk"))
$lnk.TargetPath = $exe
$lnk.WorkingDirectory = Split-Path $exe
$lnk.IconLocation = "$exe,0"
$lnk.Save()
"wrote $($lnk.FullName)"
