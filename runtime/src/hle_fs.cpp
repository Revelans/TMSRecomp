// nn::fs on host files: "rom:" -> <data>/romfs, save mounts -> <data>/save. Positional Win32 reads (thread-safe).
// Mods (LayeredFS style): a file at <data>/mods/<name>/romfs/<path> replaces romfs/<path>. Every mod folder is on
// unless named in NX_MODS_DISABLED (ini mods_disabled, comma separated); earlier names (sorted) win.
#include <windows.h>

#include <algorithm>
#include <filesystem>

#include "rt.h"

using namespace rt;
namespace fs = std::filesystem;

constexpr uint32_t RES_PATH_NOT_FOUND = 0x202, RES_PATH_EXISTS = 0x402, RES_FAIL = 0x2802;

static std::mutex g_fs_lock;
static std::unordered_map<std::string, std::vector<fs::path>> g_mounts;  // roots, first existing file wins
static std::unordered_map<uint32_t, HANDLE> g_files;
struct Dir { std::vector<fs::directory_entry> ents; size_t pos = 0; };
static std::unordered_map<uint32_t, Dir> g_dirs;
static uint32_t g_next = 1;

static bool host_path(uint32_t gpath, fs::path& out) {
    std::string p = gstr(gpath);
    size_t colon = p.find(':');
    if (colon == std::string::npos) return false;
    std::lock_guard<std::mutex> l(g_fs_lock);
    auto it = g_mounts.find(p.substr(0, colon));
    if (it == g_mounts.end()) { log("fs: no mount for %s", p.c_str()); return false; }
    std::string rest = p.substr(colon + 1);
    while (!rest.empty() && rest[0] == '/') rest.erase(0, 1);
    fs::path rel = fs::u8path(rest);
    std::error_code ec;
    for (size_t i = 0; i + 1 < it->second.size(); i++)
        if (fs::is_regular_file(it->second[i] / rel, ec)) { out = it->second[i] / rel; return true; }
    out = it->second.back() / rel;
    return true;
}

static std::vector<fs::path> rom_roots() {
    std::vector<fs::path> roots;
    std::string off = getenv("NX_MODS_DISABLED") ? std::string(",") + getenv("NX_MODS_DISABLED") + "," : ",";
    std::error_code ec;
    for (auto& e : fs::directory_iterator(fs::path(g_data_dir) / "mods", ec)) {
        auto u8 = e.path().filename().u8string();
        std::string name((const char*)u8.data(), u8.size());
        if (!fs::is_directory(e.path() / "romfs", ec)) continue;
        if (off.find("," + name + ",") != std::string::npos) { log("fs: mod %s off", name.c_str()); continue; }
        roots.push_back(e.path() / "romfs");
    }
    std::sort(roots.begin(), roots.end());
    for (auto& r : roots) log("fs: mod %s on", r.parent_path().filename().string().c_str());
    roots.push_back(fs::path(g_data_dir) / "romfs");
    return roots;
}

HLE_FN(fs_QueryRomCache, "_ZN2nn2fs22QueryMountRomCacheSizeEPj") { st32(c->r[0], 0x1000); c->r[0] = 0; }
HLE_FN(fs_MountRom, "_ZN2nn2fs8MountRomEPKcPvj") {
    std::string name = gstr(c->r[0]);
    {
        std::lock_guard<std::mutex> l(g_fs_lock);
        g_mounts[name] = rom_roots();
    }
    log("fs: mount %s: -> romfs", name.c_str());
    c->r[0] = 0;
}
HLE_FN(fs_MountSave, "_ZN2nn2fs13MountSaveDataEPKcRKNS_7account3UidE") {
    std::string name = gstr(c->r[0]);
    // NX_SAVE_DIR: test runs use their own copy (replays pick the slot the cursor starts on: system.bin's last slot)
    fs::path p = getenv("NX_SAVE_DIR") ? fs::path(getenv("NX_SAVE_DIR")) : fs::path(g_data_dir) / "save";
    fs::create_directories(p);
    {
        std::lock_guard<std::mutex> l(g_fs_lock);
        g_mounts[name] = {p};
    }
    log("fs: mount %s: -> save", name.c_str());
    c->r[0] = 0;
}
HLE_FN(fs_EnsureSave, "_ZN2nn2fs14EnsureSaveDataERKNS_7account3UidE") { c->r[0] = 0; }
HLE_FN(fs_Commit, "_ZN2nn2fs6CommitEPKc") { c->r[0] = 0; }
HLE_FN(fs_Unmount, "_ZN2nn2fs7UnmountEPKc") {
    std::lock_guard<std::mutex> l(g_fs_lock);
    g_mounts.erase(gstr(c->r[0]));
}
HLE_FN(fs_EnableCache, "_ZN2nn2fs25EnableGlobalFileDataCacheEPvj") { c->r[0] = 0; }
HLE_FN(fs_DisableCache, "_ZN2nn2fs26DisableGlobalFileDataCacheEv") {}

HLE_FN(fs_OpenFile, "_ZN2nn2fs8OpenFileEPNS0_10FileHandleEPKci") {
    fs::path p;
    if (!host_path(c->r[1], p)) { c->r[0] = RES_PATH_NOT_FOUND; return; }
    uint32_t mode = c->r[2];
    DWORD access = (mode & 1 ? GENERIC_READ : 0) | (mode & 6 ? GENERIC_WRITE : 0);
    HANDLE h = CreateFileW(p.c_str(), access, FILE_SHARE_READ | FILE_SHARE_WRITE, nullptr, OPEN_EXISTING, 0, nullptr);
    if (h == INVALID_HANDLE_VALUE) {
        LOGV("fs: open %s: not found", p.string().c_str());
        c->r[0] = RES_PATH_NOT_FOUND;
        return;
    }
    std::lock_guard<std::mutex> l(g_fs_lock);
    uint32_t id = g_next++;
    g_files[id] = h;
    st32(c->r[0], id);
    LOGV("fs: open %s -> %u", p.string().c_str(), id);
    c->r[0] = 0;
}
static HANDLE file(uint32_t id) {
    std::lock_guard<std::mutex> l(g_fs_lock);
    auto it = g_files.find(id);
    return it == g_files.end() ? INVALID_HANDLE_VALUE : it->second;
}
static uint32_t do_read(uint32_t id, uint64_t off, uint32_t buf, uint32_t size, uint32_t* got) {
    HANDLE h = file(id);
    if (h == INVALID_HANDLE_VALUE) return RES_FAIL;
    OVERLAPPED o{};
    o.Offset = (DWORD)off;
    o.OffsetHigh = (DWORD)(off >> 32);
    DWORD n = 0;
    if (!ReadFile(h, GPTR(buf), size, &n, &o) && GetLastError() != ERROR_HANDLE_EOF) return RES_FAIL;
    *got = n;
    LOGV("fs: read %u off %llx size %x -> %lx", id, (unsigned long long)off, size, n);
    return 0;
}
HLE_FN(fs_ReadFile, "_ZN2nn2fs8ReadFileENS0_10FileHandleExPvj") {  // (h r0, off r2:r3, buf [sp], size [sp+4])
    uint32_t got;
    c->r[0] = do_read(c->r[0], (uint64_t)c->r[3] << 32 | c->r[2], arg(c, 4), arg(c, 5), &got);
}
HLE_FN(fs_ReadFile2, "_ZN2nn2fs8ReadFileEPjNS0_10FileHandleExPvj") {  // (out r0, h r1, off r2:r3, buf, size)
    uint32_t got = 0, out = c->r[0];
    c->r[0] = do_read(c->r[1], (uint64_t)c->r[3] << 32 | c->r[2], arg(c, 4), arg(c, 5), &got);
    if (out) st32(out, got);
}
HLE_FN(fs_WriteFile, "_ZN2nn2fs9WriteFileENS0_10FileHandleExPKvjRKNS0_11WriteOptionE") {
    HANDLE h = file(c->r[0]);
    uint64_t off = (uint64_t)c->r[3] << 32 | c->r[2];
    OVERLAPPED o{};
    o.Offset = (DWORD)off;
    o.OffsetHigh = (DWORD)(off >> 32);
    DWORD n;
    c->r[0] = WriteFile(h, GPTR(arg(c, 4)), arg(c, 5), &n, &o) ? 0 : RES_FAIL;
}
HLE_FN(fs_FlushFile, "_ZN2nn2fs9FlushFileENS0_10FileHandleE") { FlushFileBuffers(file(c->r[0])); c->r[0] = 0; }
HLE_FN(fs_GetSize, "_ZN2nn2fs11GetFileSizeEPxNS0_10FileHandleE") {
    LARGE_INTEGER sz{};
    GetFileSizeEx(file(c->r[1]), &sz);
    st64(c->r[0], (uint64_t)sz.QuadPart);
    c->r[0] = 0;
}
HLE_FN(fs_SetSize, "_ZN2nn2fs11SetFileSizeENS0_10FileHandleEx") {
    HANDLE h = file(c->r[0]);
    FILE_END_OF_FILE_INFO e;
    e.EndOfFile.QuadPart = (LONGLONG)((uint64_t)c->r[3] << 32 | c->r[2]);
    c->r[0] = SetFileInformationByHandle(h, FileEndOfFileInfo, &e, sizeof e) ? 0 : RES_FAIL;
}
HLE_FN(fs_CloseFile, "_ZN2nn2fs9CloseFileENS0_10FileHandleE") {
    std::lock_guard<std::mutex> l(g_fs_lock);
    auto it = g_files.find(c->r[0]);
    if (it != g_files.end()) { CloseHandle(it->second); g_files.erase(it); }
}
HLE_FN(fs_CreateFile, "_ZN2nn2fs10CreateFileEPKcx") {  // (path r0, size r2:r3)
    LOGV("fs: create %s size %x", gstr(c->r[0]).c_str(), c->r[2]);
    fs::path p;
    if (!host_path(c->r[0], p)) { c->r[0] = RES_PATH_NOT_FOUND; return; }
    if (fs::exists(p)) { c->r[0] = RES_PATH_EXISTS; return; }
    HANDLE h = CreateFileW(p.c_str(), GENERIC_WRITE, 0, nullptr, CREATE_NEW, 0, nullptr);
    if (h == INVALID_HANDLE_VALUE) { c->r[0] = RES_PATH_NOT_FOUND; return; }
    FILE_END_OF_FILE_INFO e;
    e.EndOfFile.QuadPart = (LONGLONG)((uint64_t)c->r[3] << 32 | c->r[2]);
    SetFileInformationByHandle(h, FileEndOfFileInfo, &e, sizeof e);
    CloseHandle(h);
    c->r[0] = 0;
}
HLE_FN(fs_DeleteFile, "_ZN2nn2fs10DeleteFileEPKc") {
    LOGV("fs: delete %s", gstr(c->r[0]).c_str());
    fs::path p;
    std::error_code ec;
    c->r[0] = host_path(c->r[0], p) && fs::remove(p, ec) ? 0 : RES_PATH_NOT_FOUND;
}
HLE_FN(fs_RenameFile, "_ZN2nn2fs10RenameFileEPKcS2_") {
    fs::path a, b;
    std::error_code ec;
    if (!host_path(c->r[0], a) || !host_path(c->r[1], b)) { c->r[0] = RES_PATH_NOT_FOUND; return; }
    fs::rename(a, b, ec);
    c->r[0] = ec ? RES_PATH_NOT_FOUND : 0;
}
HLE_FN(fs_EntryType, "_ZN2nn2fs12GetEntryTypeEPNS0_18DirectoryEntryTypeEPKc") {
    LOGV("fs: entry type %s", gstr(c->r[1]).c_str());
    fs::path p;
    std::error_code ec;
    if (!host_path(c->r[1], p) || !fs::exists(p, ec)) { c->r[0] = RES_PATH_NOT_FOUND; return; }
    st32(c->r[0], fs::is_directory(p) ? 0 : 1);
    c->r[0] = 0;
}
HLE_FN(fs_OpenDir, "_ZN2nn2fs13OpenDirectoryEPNS0_15DirectoryHandleEPKci") {
    LOGV("fs: open dir %s mode %u", gstr(c->r[1]).c_str(), c->r[2]);
    fs::path p;
    std::error_code ec;
    if (!host_path(c->r[1], p) || !fs::is_directory(p, ec)) { c->r[0] = RES_PATH_NOT_FOUND; return; }
    Dir d;
    uint32_t mode = c->r[2];
    for (auto& e : fs::directory_iterator(p))
        if ((e.is_directory() && (mode & 1)) || (!e.is_directory() && (mode & 2))) d.ents.push_back(e);
    std::lock_guard<std::mutex> l(g_fs_lock);
    uint32_t id = g_next++;
    g_dirs[id] = std::move(d);
    st32(c->r[0], id);
    c->r[0] = 0;
}
HLE_FN(fs_ReadDir, "_ZN2nn2fs13ReadDirectoryEPxPNS0_14DirectoryEntryENS0_15DirectoryHandleEx") {
    // (out count r0, entries r1, handle r2, max count [sp] as int64)
    uint32_t out = c->r[0], ents = c->r[1];
    int64_t max = (int64_t)ld64(c->r[13]);
    std::lock_guard<std::mutex> l(g_fs_lock);
    Dir& d = g_dirs[c->r[2]];
    int64_t n = 0;
    for (; n < max && d.pos < d.ents.size(); n++, d.pos++) {
        uint32_t e = ents + (uint32_t)n * 0x310;  // DirectoryEntry: name[769], type @0x304, size @0x308
        memset(GPTR(e), 0, 0x310);
        auto u8 = d.ents[d.pos].path().filename().u8string();
        std::string name((const char*)u8.data(), u8.size());
        memcpy(GPTR(e), name.data(), std::min<size_t>(name.size(), 768));
        bool dir = d.ents[d.pos].is_directory();
        st8(e + 0x304, dir ? 0 : 1);
        st64(e + 0x308, dir ? 0 : (uint64_t)d.ents[d.pos].file_size());
    }
    st64(out, (uint64_t)n);
    c->r[0] = 0;
}
HLE_FN(fs_DirCount, "_ZN2nn2fs22GetDirectoryEntryCountEPxNS0_15DirectoryHandleE") {
    std::lock_guard<std::mutex> l(g_fs_lock);
    st64(c->r[0], g_dirs[c->r[1]].ents.size());
    c->r[0] = 0;
}
HLE_FN(fs_CloseDir, "_ZN2nn2fs14CloseDirectoryENS0_15DirectoryHandleE") {
    std::lock_guard<std::mutex> l(g_fs_lock);
    g_dirs.erase(c->r[0]);
}
