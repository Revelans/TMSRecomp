#pragma once
// One line about the PC for bug reports: tms.exe writes it at the top of nx.log, the launcher's "Copy system info" copies
// it (plus the GPU) to the clipboard. Windows + MSVC/clang only.
#include <windows.h>
#include <intrin.h>

#include <cstdio>
#include <cstring>
#include <string>
#include <thread>

#include "settings.h"

inline std::string sysinfo_line() {
    char cpu[49] = {};
    int r[4];
    __cpuid(r, 0x80000000);
    if ((unsigned)r[0] >= 0x80000004)
        for (int i = 0; i < 3; i++) __cpuid(r, 0x80000002 + i), memcpy(cpu + 16 * i, r, 16);
    const char* c = cpu;
    while (*c == ' ') c++;
    for (size_t n = strlen(cpu); n && cpu[n - 1] == ' ';) cpu[--n] = 0;  // AMD pads the name with spaces
    OSVERSIONINFOW v{sizeof v};  // GetVersionEx lies on Windows 10+: RtlGetVersion tells the truth
    if (auto f = (LONG(WINAPI*)(OSVERSIONINFOW*))GetProcAddress(GetModuleHandleW(L"ntdll.dll"), "RtlGetVersion")) f(&v);
    MEMORYSTATUSEX m{sizeof m};
    GlobalMemoryStatusEx(&m);
    char b[256];
    snprintf(b, sizeof b, "TMSRecomp %s, Windows %lu.%lu build %lu, %s, %u threads, %.1f GB RAM", k_version, v.dwMajorVersion,
             v.dwMinorVersion, v.dwBuildNumber, *c ? c : "unknown CPU", std::thread::hardware_concurrency(),
             m.ullTotalPhys / 1073741824.0);
    return b;
}
