// NVN entry: nvnBootstrapLoader / nvnDeviceGetProcAddress hand out host callbacks. Implemented functions live in
// g_nvn; every other name gets a logging stub returning 0, so the log shows what the game calls, in order.
#include <map>

#include "rt.h"

using namespace rt;

namespace rt {
uintptr_t host_callback_tag();
uint32_t host_callback(HleFn fn, uintptr_t tag);
std::unordered_map<std::string, HleFn>& nvn_table();
}  // namespace rt

std::unordered_map<std::string, HleFn>& rt::nvn_table() {
    static std::unordered_map<std::string, HleFn> t;
    return t;
}

static std::mutex g_nvn_lock;
static std::unordered_map<std::string, uint32_t> g_procs;
static std::vector<std::string> g_names;

static void nvn_stub(Cpu* c) {
    const std::string& n = g_names[host_callback_tag()];
    static std::map<std::string, int> calls;
    int k;
    {
        std::lock_guard<std::mutex> l(g_nvn_lock);
        k = ++calls[n];
    }
    if (k <= 3) log("nvn stub %s(%08x %08x %08x %08x) lr %s", n.c_str(), c->r[0], c->r[1], c->r[2], c->r[3], symbol_at(c->r[14]));
    c->r[0] = 0;
}

namespace rt { bool nvn_use_real(const std::string& n); }
static uint32_t g_real_gpa = 0;  // the real driver's nvnDeviceGetProcAddress

// The real driver answers from device state that our HLE nvnDeviceInitialize never fills: LINEAR_TEXTURE_STRIDE_ALIGNMENT
// (0x38) came back 0 (analysis/nvn_real.txt; 0x39, the render-target one, is 0x80). The game's pitch helper 0x4fd820
// aligns with it, so a linear texture got pitch 0: CRI Mana's MPEG / Sofdec.Prime frames (uncensored mod m06 / m07 /
// m12) were copied row after row onto row 0 and the movie showed an older movie's frames (USER 11-20 Aversa cutscene).
// Maxwell linear textures take their pitch in 32-byte units.
static uint32_t g_real_getint = 0;
static void device_get_integer(Cpu* c) {  // nvnDeviceGetInteger(const NVNdevice*, NVNdeviceInfo, int*)
    const uint32_t info = c->r[1], out = c->r[2];
    gcall(c, g_real_getint, {c->r[0], info, out});
    if (info == 0x38 && out && ld32(out) == 0) st32(out, 32);
}

static uint32_t proc(Cpu* c, const std::string& name) {
    {
        std::lock_guard<std::mutex> l(g_nvn_lock);
        auto it = g_procs.find(name);
        if (it != g_procs.end()) return it->second;
    }
    if (nvn_use_real(name)) {
        if (!g_real_gpa) {
            uint32_t s = hle_alloc(32);
            memcpy(GPTR(s), "nvnDeviceGetProcAddress", 24);
            g_real_gpa = call_unhooked(c, "nvnBootstrapLoader", {s});
        }
        uint32_t s = hle_alloc((uint32_t)name.size() + 1);
        memcpy(GPTR(s), name.c_str(), name.size() + 1);
        uint32_t keep[4] = {c->r[0], c->r[1], c->r[2], c->r[3]};
        uint32_t a = gcall(c, g_real_gpa, {0, s});
        memcpy(c->r, keep, sizeof keep);
        std::lock_guard<std::mutex> l(g_nvn_lock);
        if (name == "nvnDeviceGetInteger" && a) g_real_getint = a, a = host_callback(device_get_integer, 0);
        g_procs[name] = a;
        return a;
    }
    std::lock_guard<std::mutex> l(g_nvn_lock);
    auto& tbl = nvn_table();
    auto f = tbl.find(name);
    uint32_t a;
    if (f != tbl.end()) a = host_callback(f->second, 0);
    else {
        g_names.push_back(name);
        a = host_callback(nvn_stub, g_names.size() - 1);
    }
    g_procs[name] = a;
    return a;
}

static void get_proc(Cpu* c) {  // nvnDeviceGetProcAddress(const NVNdevice*, const char*)
    c->r[0] = proc(c, gstr(c->r[1]));
}

// NX_DUMP_NVN=<file>: ask NVIDIA's real driver (recompiled SDK) for every NVN entry point, for reverse engineering
static void dump_real_procs(Cpu* c) {
    const char* out = getenv("NX_DUMP_NVN");
    if (!out) return;
    FILE* names = fopen((g_data_dir + "/analysis/nvn_names.txt").c_str(), "r");
    FILE* f = fopen(out, "w");
    if (!names || !f) { log("NX_DUMP_NVN: cannot open files"); return; }
    uint32_t s = hle_alloc(256);
    memcpy(GPTR(s), "nvnDeviceGetProcAddress", 24);
    uint32_t gpa = call_unhooked(c, "nvnBootstrapLoader", {s});
    log("real nvnDeviceGetProcAddress = %s", symbol_at(gpa));
    char line[256];
    int n = 0;
    while (fgets(line, sizeof line, names)) {
        line[strcspn(line, "\r\n")] = 0;
        memset(GPTR(s), 0, 256);
        memcpy(GPTR(s), line, strlen(line));
        uint32_t a = gcall(c, gpa, {0, s});
        fprintf(f, "%s %08x\n", line, a);
        n++;
    }
    fclose(names);
    fflush(f);
    // device integers straight from the real driver (a zeroed device object; constants do not depend on it)
    uint32_t real_gi = 0;
    {
        FILE* r = fopen(out, "r");
        char nm[128];
        unsigned ad;
        while (r && fscanf(r, "%127s %x", nm, &ad) == 2)
            if (!strcmp(nm, "nvnDeviceGetInteger")) real_gi = ad;
        if (r) fclose(r);
    }
    uint32_t dev = hle_alloc(0x4000, 64), outp = hle_alloc(8);
    for (uint32_t e = 0; e < 0x60 && real_gi; e++) {
        st32(outp, 0xDEADBEEF);
        gcall(c, real_gi, {dev, e, outp});
        fprintf(f, "devint %#x %#x\n", e, ld32(outp));
    }
    // texture storage sizes from the real driver for each format id: 64x64 2D, 1 level (bytes per texel = size/4096)
    auto real = [&](const char* nm) {
        FILE* r = fopen(out, "r");
        char x[128];
        unsigned ad, found = 0;
        while (r && fscanf(r, "%127s %x", x, &ad) == 2)
            if (!strcmp(x, nm)) found = ad;
        if (r) fclose(r);
        return found;
    };
    uint32_t tb = hle_alloc(0x100, 64);
    uint32_t sdef = real("nvnTextureBuilderSetDefaults"), sdev = real("nvnTextureBuilderSetDevice"),
             ssz = real("nvnTextureBuilderSetSize2D"), sfmt = real("nvnTextureBuilderSetFormat"),
             gsz = real("nvnTextureBuilderGetStorageSize"), gal = real("nvnTextureBuilderGetStorageAlignment");
    for (uint32_t fmt = 0; fmt < 0x100 && gsz; fmt++) {
        gcall(c, sdef, {tb});
        gcall(c, sdev, {tb, dev});
        gcall(c, ssz, {tb, 64, 64});
        gcall(c, sfmt, {tb, fmt});
        uint32_t sz = gcall(c, gsz, {tb});
        uint32_t al = gcall(c, gal, {tb});
        fprintf(f, "texfmt %#x size %#x align %#x target %u\n", fmt, sz, al, ld32(tb + 0x14));
    }
    fclose(f);
    log("NX_DUMP_NVN: %d names written to %s", n, out);
}

HLE_FN(nvn_Bootstrap, "nvnBootstrapLoader") {
    static bool dumped = false;
    if (!dumped) {
        dumped = true;
        uint32_t keep[4] = {c->r[0], c->r[1], c->r[2], c->r[3]};
        dump_real_procs(c);
        memcpy(c->r, keep, sizeof keep);
    }
    std::string n = gstr(c->r[0]);
    log("nvnBootstrapLoader(\"%s\")", n.c_str());
    if (n == "nvnDeviceGetProcAddress") {
        static uint32_t a = host_callback(get_proc, 0);
        c->r[0] = a;
        return;
    }
    c->r[0] = proc(c, n);
}
