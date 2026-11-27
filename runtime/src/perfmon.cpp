// Performance diagnosis for weak / laptop PCs (s124, issue #11): a background thread samples every 10 s what the
// game's own numbers cannot show and logs it as "perf:" lines:
// - NVIDIA GPUs: graphics / memory clock against their maximum, temperature, load and the driver's throttle reasons
//   (power cap, thermal, ...) through NVML (nvml.dll ships with the driver). PORTABILITY: other vendors, no NVML or a
//   call the GPU does not support: that part is left out.
// - Windows: power source (battery / mains), battery saver, the active power plan (Power saver caps laptop GPUs).
// Lines are logged when a value changes (clocks / temperature / load every 10 s while in game), so a log shows at once
// whether a laptop was held back by heat, battery or a power plan rather than by the game.
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <string>
#include <thread>
#ifdef _WIN32
#include <windows.h>
#else
#include <dlfcn.h>
#endif
#include "rt.h"

namespace {
using rt::log;
// NVML (nvml.h subset; stable C ABI since 2015)
typedef struct nvmlDevice_st* nvmlDevice_t;
struct nvmlUtilization_t { unsigned int gpu, memory; };
typedef int (*FnInit)();
typedef int (*FnCount)(unsigned int*);
typedef int (*FnHandle)(unsigned int, nvmlDevice_t*);
typedef int (*FnName)(nvmlDevice_t, char*, unsigned int);
typedef int (*FnClock)(nvmlDevice_t, int, unsigned int*);
typedef int (*FnTemp)(nvmlDevice_t, int, unsigned int*);
typedef int (*FnThrottle)(nvmlDevice_t, unsigned long long*);
typedef int (*FnUtil)(nvmlDevice_t, nvmlUtilization_t*);
typedef int (*FnPState)(nvmlDevice_t, int*);
struct Nvml {
    FnClock clock = nullptr, max_clock = nullptr;
    FnTemp temp = nullptr;
    FnThrottle throttle = nullptr;
    FnUtil util = nullptr;
    FnPState pstate = nullptr;
    nvmlDevice_t dev = nullptr;
};
static void* sym(void* lib, const char* name) {
#ifdef _WIN32
    return (void*)GetProcAddress((HMODULE)lib, name);
#else
    return dlsym(lib, name);
#endif
}
static bool nvml_open(Nvml& n, const char* gpu_name) {
#ifdef _WIN32
    void* lib = LoadLibraryW(L"nvml.dll");  // System32 (driver 4xx+)
    if (!lib) {
        wchar_t p[MAX_PATH];
        if (ExpandEnvironmentStringsW(L"%ProgramW6432%\\NVIDIA Corporation\\NVSMI\\nvml.dll", p, MAX_PATH)) lib = LoadLibraryW(p);
    }
#else
    void* lib = dlopen("libnvidia-ml.so.1", RTLD_NOW);
#endif
    if (!lib) { log("perf: NVML not found: no GPU clock / temperature lines"); return false; }
    auto init = (FnInit)sym(lib, "nvmlInit_v2");
    auto count = (FnCount)sym(lib, "nvmlDeviceGetCount_v2");
    auto handle = (FnHandle)sym(lib, "nvmlDeviceGetHandleByIndex_v2");
    auto name = (FnName)sym(lib, "nvmlDeviceGetName");
    n.clock = (FnClock)sym(lib, "nvmlDeviceGetClockInfo");
    n.max_clock = (FnClock)sym(lib, "nvmlDeviceGetMaxClockInfo");
    n.temp = (FnTemp)sym(lib, "nvmlDeviceGetTemperature");
    n.throttle = (FnThrottle)sym(lib, "nvmlDeviceGetCurrentClocksThrottleReasons");
    n.util = (FnUtil)sym(lib, "nvmlDeviceGetUtilizationRates");
    n.pstate = (FnPState)sym(lib, "nvmlDeviceGetPerformanceState");
    unsigned int c = 0;
    if (!init || !count || !handle || init() != 0 || count(&c) != 0 || !c) { log("perf: NVML did not start: no GPU clock / temperature lines"); return false; }
    for (unsigned int i = 0; i < c && !n.dev; i++) {  // the GPU the game renders on (laptops may list more)
        nvmlDevice_t d;
        char nm[96] = {};
        if (handle(i, &d) != 0) continue;
        if (c == 1 || (name && name(d, nm, sizeof nm) == 0 && (strstr(gpu_name, nm) || strstr(nm, gpu_name)))) n.dev = d;
    }
    if (!n.dev) { log("perf: NVML lists no GPU named %s", gpu_name); return false; }
    return true;
}
static std::string throttle_text(unsigned long long r) {
    static const struct { unsigned long long bit; const char* what; } k[] = {
        {0x4, "power limit"}, {0x8, "hardware slowdown (heat or power brake)"}, {0x20, "driver thermal limit"},
        {0x40, "hardware thermal limit"}, {0x80, "power brake"}, {0x2, "application clock setting"}, {0x100, "display clock setting"}};
    std::string s;
    for (auto& e : k) if (r & e.bit) s += (s.empty() ? "" : ", ") + std::string(e.what);
    return s.empty() ? "none" : s;
}
#ifdef _WIN32
static std::string power_text() {
    SYSTEM_POWER_STATUS ps{};
    std::string s = GetSystemPowerStatus(&ps) ? (ps.ACLineStatus == 0 ? "on battery" : ps.ACLineStatus == 1 ? "on mains power" : "power source unknown")
                                             : "power source unknown";
    if (ps.SystemStatusFlag & 1) s += ", battery saver ON";
    static auto get_scheme = [] {
        HMODULE m = LoadLibraryW(L"powrprof.dll");
        return m ? (DWORD(WINAPI*)(HKEY, GUID**))GetProcAddress(m, "PowerGetActiveScheme") : nullptr;
    }();
    GUID* g = nullptr;
    if (get_scheme && get_scheme(nullptr, &g) == 0 && g) {
        static const GUID saver = {0xa1841308, 0x3541, 0x4fab, {0xbc, 0x81, 0xf7, 0x15, 0x56, 0xf2, 0x0b, 0x4a}};
        static const GUID high = {0x8c5e7fda, 0xe8bf, 0x4a96, {0x9a, 0x85, 0xa6, 0xe2, 0x3a, 0x8c, 0x63, 0x5c}};
        static const GUID balanced = {0x381b4222, 0xf694, 0x41f0, {0x96, 0x85, 0xff, 0x5b, 0xb2, 0x60, 0xdf, 0x2e}};
        s += !memcmp(g, &saver, sizeof(GUID)) ? ", power plan Power saver (slows the GPU)" : !memcmp(g, &high, sizeof(GUID)) ? ", power plan High performance"
             : !memcmp(g, &balanced, sizeof(GUID)) ? ", power plan Balanced" : ", power plan custom";
        LocalFree(g);
    }
    return s;
}
#else
static std::string power_text() { return ""; }
#endif
}  // namespace

namespace rt {
std::atomic<bool> g_perf_in_game{false};  // vk.cpp: a 3D scene was drawn in the last 10 s (clock lines only then)
void perfmon_start(const char* gpu_name, uint32_t vendor) {
    static bool started = false;
    if (started || (getenv("NX_PERFMON") && atoi(getenv("NX_PERFMON")) == 0)) return;
    started = true;
    std::string name = gpu_name;
    std::thread([name, vendor] {
#ifdef _WIN32
        SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_LOWEST);
#endif
        Nvml n;
        const bool nv = vendor == 0x10DE && nvml_open(n, name.c_str());
        std::string last_power, last_thr;
        unsigned int max_g = 0, max_m = 0;
        if (nv && n.max_clock) n.max_clock(n.dev, 0, &max_g), n.max_clock(n.dev, 2, &max_m);
        for (;;) {
            const std::string pw = power_text();
            if (!pw.empty() && pw != last_power) log("perf: %s", pw.c_str()), last_power = pw;
            if (nv) {
                unsigned int g = 0, m = 0, t = 0;
                unsigned long long thr = 0;
                nvmlUtilization_t u{};
                int ps = -1;
                const bool hg = n.clock && n.clock(n.dev, 0, &g) == 0, hm = n.clock && n.clock(n.dev, 2, &m) == 0;
                const bool ht = n.temp && n.temp(n.dev, 0, &t) == 0, hu = n.util && n.util(n.dev, &u) == 0;
                const bool hthr = n.throttle && n.throttle(n.dev, &thr) == 0;
                if (n.pstate) n.pstate(n.dev, &ps);
                const std::string tt = hthr ? throttle_text(thr) : "unknown";
                if (g_perf_in_game.exchange(false) || tt != last_thr) {
                    char b[320];
                    snprintf(b, sizeof b, "perf: GPU clock %s/%u MHz, memory %s/%u MHz, %s, load %s, P%d, slowed by: %s",
                             hg ? std::to_string(g).c_str() : "?", max_g, hm ? std::to_string(m).c_str() : "?", max_m,
                             ht ? (std::to_string(t) + " C").c_str() : "temperature ?", hu ? (std::to_string(u.gpu) + "%").c_str() : "?", ps, tt.c_str());
                    log("%s", b);
                    last_thr = tt;
                }
            }
            std::this_thread::sleep_for(std::chrono::seconds(10));
        }
    }).detach();
}
}  // namespace rt
