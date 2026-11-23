@echo off
rem Play TMSRecomp. The game writes its full log to private\tms\live.log; this window shows only problems
rem (private\tms\issues.log) as they happen, with the time. The previous run's logs move to private\tms\logs\.
rem Close this window after the game.
cd /d "%~dp0private\tms"
if not exist build\tms.exe (echo build\tms.exe not found: run build.cmd first & pause & exit /b 1)
set NX_LOG=live.log
rem window, internal resolution and frame rate: private\tms\build\settings.ini (written on the first run)
rem every run records the pad input the game reads (input.rec, replay with NX_REPLAY=...); old ones go to logs\
set NX_RECORD=input.rec
rem play.bat 60: game logic at 60 fps; play.bat 144 (any N > 60): capped at N; play.bat 0: uncapped (default: settings.ini)
if not "%1"=="" set NX_FPS=%1
start "" /b cmd /c "build\tms.exe --data . 2>nul >nul"
rem wait until the game has created the new issues.log, then follow it
:wait
timeout /t 1 /nobreak >nul
if not exist issues.log goto wait
title TMSRecomp - live issues (problems only; full log: private\tms\live.log)
powershell -NoProfile -Command "Get-Content -Path issues.log -Wait -Tail 50"
