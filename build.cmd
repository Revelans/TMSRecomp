@echo off
rem Configure + build with clang and Ninja (both from LLVM / Visual Studio). Output: private\tms\build\tms.exe
set VSCM=C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake
set PATH=%VSCM%\CMake\bin;%VSCM%\Ninja;C:\Program Files\LLVM\bin;%PATH%
if not exist private\tms\build\build.ninja cmake -S . -B private\tms\build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ || exit /b 1
cmake --build private\tms\build %*
