// nn::fs on host files: "rom:" -> <data>/romfs, save mounts -> <data>/save. Positional Win32 reads (thread-safe).
// Mods (LayeredFS style): a file at <data>/mods/<name>/romfs/<path> replaces romfs/<path>. Every mod folder is on
// unless named in NX_MODS_DISABLED (ini mods_disabled, comma separated); earlier names (sorted) win.
// Loose-file mods (s125, user request: P5R-style modding): a file at <data>/mods/<name>/cpk/<pack>/<path> replaces the
// file <path> inside romfs/Pack/<pack>.cpk, so a mod holds only the files it changes (e.g. cpk/pack_030_etc/Skill/
// SkillData.dat) instead of a whole multi-GB CPK. The game opens a virtual CPK: the original bytes, with the TOC (and
// the header's ContentSize) served from a patched copy whose rows for the replaced files point past the original end,
// where the loose files are served from disk (stored uncompressed: FileSize = ExtractSize). The packs have no TOC / file
// CRCs (EnableTocCrc 0, EnableFileCrc 0, checked per pack: else the pack is left alone). Only files already in the pack
// can be replaced (new names would need a re-sorted TOC); others are logged and ignored. The launcher's "Dump game
// files" writes <data>/dump/<pack>/<path> with the same paths.
#include "plat.h"
#ifndef _WIN32
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#endif

#include <algorithm>
#include <filesystem>
#include <fstream>
#include <map>
#include <memory>

#include "rt.h"

using namespace rt;
namespace fs = std::filesystem;

constexpr uint32_t RES_PATH_NOT_FOUND = 0x202, RES_PATH_EXISTS = 0x402, RES_FAIL = 0x2802;

static std::mutex g_fs_lock;
static std::unordered_map<std::string, std::vector<fs::path>> g_mounts;  // roots, first existing file wins
#ifdef _WIN32
using FileH = HANDLE;
static const FileH k_bad_file = INVALID_HANDLE_VALUE;
#else
// Linux: file descriptors, positional reads and writes (pread / pwrite: thread-safe like the OVERLAPPED reads)
using FileH = int;
static const FileH k_bad_file = -1;
using DWORD = uint32_t;
static constexpr DWORD GENERIC_READ = 1, GENERIC_WRITE = 2;
static FileH f_open(const fs::path& p, DWORD access) {
    return open(p.c_str(), (access & GENERIC_WRITE ? (access & GENERIC_READ ? O_RDWR : O_WRONLY) : O_RDONLY) | O_CLOEXEC);
}
// Windows paths ignore case, the game's own paths may not match the dumped names letter for letter: a component that
// does not exist is looked up case-insensitively in its folder (only on a miss, so normal opens cost nothing extra).
static fs::path ci_path(const fs::path& root, const fs::path& rel) {
    fs::path cur = root;
    std::error_code ec;
    for (auto it = rel.begin(); it != rel.end(); ++it) {
        fs::path next = cur / *it;
        if (!fs::exists(next, ec)) {
            const std::string want = it->string();
            for (auto& e : fs::directory_iterator(cur, ec))
                if (!strcasecmp(e.path().filename().c_str(), want.c_str())) { next = e.path(); break; }
        }
        cur = next;
    }
    return cur;
}
#endif
struct VCpk;  // below
struct FsFile { FileH h; std::shared_ptr<VCpk> v; };
static std::unordered_map<uint32_t, FsFile> g_files;
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
    // Language option (s116): the Uncensored mod's pack_031_message.cpk holds its English text in all five language
    // folders (JP_Japanese, EUfr, CNzh, TWzh = USen copies), so with another language the base pack wins.
    static const bool non_en = strcmp(rt::language(), "en-US") != 0;
    const size_t mods = non_en && rest == "Pack/pack_031_message.cpk" ? 0 : it->second.size() - 1;
#ifdef _WIN32
    for (size_t i = 0; i < mods; i++)
        if (fs::is_regular_file(it->second[i] / rel, ec)) { out = it->second[i] / rel; return true; }
    out = it->second.back() / rel;
#else
    for (size_t i = 0; i < mods; i++)
        if (fs::path q = ci_path(it->second[i], rel); fs::is_regular_file(q, ec)) { out = q; return true; }
    out = ci_path(it->second.back(), rel);
#endif
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

// ------------------------------------------------------------------------------------------------ loose-file CPK mods
struct VCpk {
    uint64_t base_size = 0, size = 0;
    std::vector<std::pair<uint64_t, std::vector<uint8_t>>> patches;  // (offset, bytes) served instead of the original
    struct Extra { uint64_t off, size; FileH h; };
    std::vector<Extra> extras;  // loose files past base_size
};
static FileH open_ro(const fs::path& p) {
#ifdef _WIN32
    return CreateFileW(p.c_str(), GENERIC_READ, FILE_SHARE_READ | FILE_SHARE_WRITE, nullptr, OPEN_EXISTING, 0, nullptr);
#else
    return f_open(p, GENERIC_READ);
#endif
}
static bool pread_all(FileH h, uint64_t off, void* dst, size_t n) {
#ifdef _WIN32
    OVERLAPPED o{};
    o.Offset = (DWORD)off;
    o.OffsetHigh = (DWORD)(off >> 32);
    DWORD got = 0;
    return ReadFile(h, dst, (DWORD)n, &got, &o) && got == n;
#else
    size_t got = 0;
    while (got < n) {
        ssize_t r = pread(h, (uint8_t*)dst + got, n - got, (off_t)(off + got));
        if (r < 0 && errno == EINTR) continue;
        if (r <= 0) return false;
        got += (size_t)r;
    }
    return true;
#endif
}
static uint64_t file_size_of(FileH h) {
#ifdef _WIN32
    LARGE_INTEGER sz{};
    GetFileSizeEx(h, &sz);
    return (uint64_t)sz.QuadPart;
#else
    struct stat st{};
    fstat(h, &st);
    return (uint64_t)st.st_size;
#endif
}
// @UTF table (big-endian): column name -> (storage, type, byte position in a row); rows / strings located
struct Utf {
    const uint8_t* b = nullptr;
    size_t n = 0;
    uint32_t rows_off = 0, str_off = 0, row_len = 0, nrows = 0;
    struct Col { std::string name; int st, type, pos; };
    std::vector<Col> cols;
    static uint32_t be32(const uint8_t* p) { return (uint32_t)p[0] << 24 | p[1] << 16 | p[2] << 8 | p[3]; }
    static int width(int t) { static const int w[12] = {1, 1, 2, 2, 4, 4, 8, 8, 4, 8, 4, 8}; return t < 12 ? w[t] : 0; }
    std::string str(uint32_t o) const {
        o += str_off;
        std::string r;
        while (o < n && b[o]) r += (char)b[o++];
        return r;
    }
    bool parse(const uint8_t* data, size_t len) {  // data = "@UTF"
        b = data, n = len;
        if (len < 32 || memcmp(b, "@UTF", 4)) return false;
        const uint8_t* h = b + 8;
        rows_off = (uint32_t)((h[2] << 8 | h[3]) + 8), str_off = be32(h + 4) + 8;
        const int ncols = h[16] << 8 | h[17];
        row_len = h[18] << 8 | h[19], nrows = be32(h + 20);
        size_t p = 8 + 0x18;
        int rp = 0;
        for (int i = 0; i < ncols; i++) {
            if (p + 5 > n) return false;
            const int fl = b[p], st = fl & 0xF0, t = fl & 0xF;
            Col c{str(be32(b + p + 1)), st, t, -1};
            p += 5;
            if (st == 0x30) p += width(t);
            if (st == 0x50) c.pos = rp, rp += width(t);
            cols.push_back(c);
        }
        return rows_off + (uint64_t)row_len * nrows <= n;
    }
    const Col* col(const char* name) const {
        for (auto& c : cols) if (c.name == name) return &c;
        return nullptr;
    }
    uint64_t get(uint32_t row, const Col* c) const {
        const uint8_t* p = b + rows_off + row * row_len + c->pos;
        uint64_t v = 0;
        for (int i = 0; i < width(c->type); i++) v = v << 8 | p[i];
        return v;
    }
    static void put(uint8_t* row_base, const Col* c, uint64_t v) {
        for (int i = width(c->type) - 1; i >= 0; i--) row_base[c->pos + i] = (uint8_t)v, v >>= 8;
    }
};
static std::string lower(std::string s) {
    for (char& ch : s) ch = (char)tolower((unsigned char)ch);
    return s;
}
// enabled mod folders with cpk/<pack> (sorted: earlier names win, as for romfs)
static std::vector<fs::path> loose_dirs(const std::string& pack) {
    std::vector<fs::path> v;
    const std::string off = getenv("NX_MODS_DISABLED") ? std::string(",") + getenv("NX_MODS_DISABLED") + "," : ",";
    std::error_code ec;
    for (auto& e : fs::directory_iterator(fs::path(g_data_dir) / "mods", ec)) {
        auto u8 = e.path().filename().u8string();
        if (off.find("," + std::string((const char*)u8.data(), u8.size()) + ",") != std::string::npos) continue;
        if (fs::is_directory(e.path() / "cpk" / pack, ec)) v.push_back(e.path() / "cpk" / pack);
    }
    std::sort(v.begin(), v.end());
    return v;
}
static std::shared_ptr<VCpk> build_vcpk(const fs::path& cpk_path, FileH base) {
    const std::string pack = cpk_path.stem().string();
    auto dirs = loose_dirs(pack);
    if (dirs.empty()) return nullptr;
    std::map<std::string, std::pair<fs::path, std::string>> loose;  // lower-case inner path -> (file, mod name)
    std::error_code ec;
    for (auto& d : dirs)
        for (auto& f : fs::recursive_directory_iterator(d, ec)) {
            if (!f.is_regular_file(ec)) continue;
            auto u8 = fs::relative(f.path(), d, ec).generic_u8string();
            loose.emplace(lower(std::string((const char*)u8.data(), u8.size())), std::make_pair(f.path(), d.parent_path().parent_path().filename().string()));
        }
    if (loose.empty()) return nullptr;
    auto fail = [&](const char* why) { log("fs: loose mods for %s.cpk not used: %s", pack.c_str(), why); return std::shared_ptr<VCpk>(); };
    std::vector<uint8_t> head(0x800);
    if (!pread_all(base, 0, head.data(), head.size()) || memcmp(head.data(), "CPK ", 4)) return fail("not a CPK");
    Utf hu;
    if (!hu.parse(head.data() + 0x10, head.size() - 0x10)) return fail("header unreadable");
    auto hc = [&](const char* n) -> uint64_t { const Utf::Col* c = hu.col(n); return c && c->st == 0x50 ? hu.get(0, c) : 0; };
    if (hc("EnableTocCrc") || hc("EnableFileCrc") || hc("TocCrc")) return fail("the pack checks CRCs");
    const uint64_t toc_off = hc("TocOffset"), toc_size = hc("TocSize"), align = std::max<uint64_t>(hc("Align"), 0x800);
    if (!toc_off || toc_size < 0x30 || toc_size > (64u << 20)) return fail("no TOC");
    std::vector<uint8_t> toc(toc_size);
    if (!pread_all(base, toc_off, toc.data(), toc.size())) return fail("TOC unreadable");
    Utf tu;
    if (!tu.parse(toc.data() + 0x10, toc.size() - 0x10)) return fail("TOC unreadable (encrypted?)");
    const Utf::Col *cdir = tu.col("DirName"), *cname = tu.col("FileName"), *cfs = tu.col("FileSize"), *ces = tu.col("ExtractSize"), *coff = tu.col("FileOffset");
    if (!cname || !cfs || !ces || !coff || cname->st != 0x50 || cfs->st != 0x50 || ces->st != 0x50 || coff->st != 0x50)
        return fail("TOC columns not per file");
    auto v = std::make_shared<VCpk>();
    v->base_size = file_size_of(base);
    uint64_t end = (v->base_size + align - 1) / align * align;
    uint8_t* rows = toc.data() + 0x10 + tu.rows_off;
    std::map<std::string, int> per_mod;
    for (uint32_t r = 0; r < tu.nrows; r++) {
        std::string dir = cdir && cdir->st == 0x50 ? tu.str((uint32_t)tu.get(r, cdir)) : std::string();
        if (dir == "<NULL>") dir.clear();
        const std::string name = tu.str((uint32_t)tu.get(r, cname)), inner = lower(dir.empty() ? name : dir + "/" + name);
        auto it = loose.find(inner);
        if (it == loose.end()) continue;
        FileH h = open_ro(it->second.first);
        if (h == k_bad_file) { log("fs: loose mod file %s cannot be opened", it->second.first.string().c_str()); loose.erase(it); continue; }
        const uint64_t sz = file_size_of(h);
        if (sz >> 32) { log("fs: loose mod file %s over 4 GB: ignored", it->second.first.string().c_str()); loose.erase(it); continue; }
        // FileOffset counts from 0x800 here (tools/cpk.py, measured): the file goes to `end`
        uint8_t* row = rows + (size_t)r * tu.row_len;
        Utf::put(row, coff, end - 0x800), Utf::put(row, cfs, sz), Utf::put(row, ces, sz);
        v->extras.push_back({end, sz, h});
        per_mod[it->second.second]++;
        end = (end + sz + align - 1) / align * align;
        loose.erase(it);
    }
    for (auto& [inner, f] : loose) log("fs: mod %s: %s is not in %s.cpk: ignored (only files the pack has can be replaced)", f.second.c_str(), inner.c_str(), pack.c_str());
    if (v->extras.empty()) return nullptr;
    v->size = end;
    v->patches.push_back({toc_off, std::move(toc)});
    if (const Utf::Col* cs = hu.col("ContentSize"); cs && cs->st == 0x50) {  // the content now reaches the new end
        const uint64_t content_off = hc("ContentOffset");
        Utf::put(head.data() + 0x10 + hu.rows_off, cs, end - content_off);
        v->patches.push_back({0, std::move(head)});
    }
    for (auto& [m, k] : per_mod) log("fs: mod %s: %d loose file%s in %s.cpk", m.c_str(), k, k == 1 ? "" : "s", pack.c_str());
    return v;
}
static std::shared_ptr<VCpk> vcpk_for(const fs::path& p, FileH base) {
    static std::mutex m;
    static std::map<fs::path, std::shared_ptr<VCpk>> cache;  // mods do not change while the game runs
    std::lock_guard<std::mutex> l(m);
    auto it = cache.find(p);
    if (it != cache.end()) return it->second;
    return cache[p] = build_vcpk(p, base);
}
static uint32_t vread(const VCpk& v, FileH h, uint64_t off, uint32_t buf, uint32_t size, uint32_t* got) {
    if (off >= v.size) { *got = 0; return 0; }
    const uint32_t n = (uint32_t)std::min<uint64_t>(size, v.size - off);
    std::vector<uint8_t> tmp(n, 0);  // bounce buffer (also keeps Linux write-watched guest pages safe)
    if (off < v.base_size) {
        const size_t k = (size_t)std::min<uint64_t>(n, v.base_size - off);
        if (!pread_all(h, off, tmp.data(), k)) return RES_FAIL;
    }
    for (auto& [po, pb] : v.patches) {
        const uint64_t a = std::max(off, po), b = std::min(off + n, po + pb.size());
        if (a < b) memcpy(tmp.data() + (a - off), pb.data() + (a - po), (size_t)(b - a));
    }
    for (auto& e : v.extras) {
        const uint64_t a = std::max(off, e.off), b = std::min(off + n, e.off + e.size);
        if (a < b && !pread_all(e.h, a - e.off, tmp.data() + (a - off), (size_t)(b - a))) return RES_FAIL;
    }
    memcpy(GPTR(buf), tmp.data(), n);
    *got = n;
    return 0;
}

// ------------------------------------------------------------------------------------------------ dump (tms.exe --dump)
// CRILAYLA (CRI's LZ, read backwards; the first 0x100 bytes stored raw at the end). Same as tools/cpk.py crilayla.
static bool crilayla(const std::vector<uint8_t>& src, std::vector<uint8_t>& out) {
    if (src.size() < 0x10 || memcmp(src.data(), "CRILAYLA", 8)) return false;
    auto le32 = [&](size_t o) { return (uint32_t)src[o] | src[o + 1] << 8 | src[o + 2] << 16 | (uint32_t)src[o + 3] << 24; };
    const uint32_t usize = le32(8), csize = le32(12);
    if ((uint64_t)0x10 + csize + 0x100 > src.size()) return false;
    out.assign((size_t)usize + 0x100, 0);
    memcpy(out.data(), src.data() + 0x10 + csize, 0x100);
    int64_t inp = 0x10 + (int64_t)csize - 1, o = (int64_t)out.size() - 1;
    uint32_t pool = 0;
    int left = 0;
    bool bad = false;
    auto bits = [&](int k) {
        uint32_t v = 0;
        while (k) {
            if (!left) {
                if (inp < 0x10) { bad = true; return 0u; }
                pool = src[(size_t)inp--], left = 8;
            }
            const int take = std::min(left, k);
            v = v << take | ((pool >> (left - take)) & ((1u << take) - 1));
            left -= take, k -= take;
        }
        return v;
    };
    while (o >= 0x100 && !bad) {
        if (bits(1)) {
            const int64_t off = bits(13) + 3;
            int64_t len = 3;
            static const int w[3] = {2, 3, 5};
            bool more = true;
            for (int i = 0; i < 3 && more; i++) {
                const uint32_t x = bits(w[i]);
                len += x;
                more = x == (1u << w[i]) - 1;
            }
            if (more)
                for (;;) { const uint32_t x = bits(8); len += x; if (x != 0xFF || bad) break; }
            for (; len > 0 && o >= 0; len--, o--) {
                if (o + off >= (int64_t)out.size()) return false;
                out[(size_t)o] = out[(size_t)(o + off)];
            }
        } else out[(size_t)o--] = (uint8_t)bits(8);
    }
    return !bad;
}
bool rt::cpk_read_file(const char* pack, const char* inner_path, std::vector<uint8_t>& out) {
    if (!pack || !*pack || !inner_path || !*inner_path || g_data_dir.empty()) return false;
    fs::path p = fs::path(g_data_dir) / "romfs" / "Pack" / (std::string(pack) + ".cpk");
    FileH h = open_ro(p);
    if (h == k_bad_file) { log("fs: cpk_read_file: cannot open %s", p.string().c_str()); return false; }
    auto close_h = [&] {
#ifdef _WIN32
        CloseHandle(h);
#else
        close(h);
#endif
    };
    std::vector<uint8_t> head(0x800), toc;
    Utf hu, tu;
    auto hc = [&](const char* n) -> uint64_t { const Utf::Col* c = hu.col(n); return c && c->st == 0x50 ? hu.get(0, c) : 0; };
    bool ok = pread_all(h, 0, head.data(), head.size()) && !memcmp(head.data(), "CPK ", 4) && hu.parse(head.data() + 0x10, head.size() - 0x10);
    if (ok) {
        const uint64_t tsz = hc("TocSize"), toff = hc("TocOffset");
        ok = toff && tsz > 0x10 && tsz <= (128ull << 20);
        if (ok) toc.resize((size_t)tsz), ok = pread_all(h, toff, toc.data(), toc.size()) && tu.parse(toc.data() + 0x10, toc.size() - 0x10);
    }
    const Utf::Col *cdir = ok ? tu.col("DirName") : nullptr, *cname = ok ? tu.col("FileName") : nullptr, *cfs = ok ? tu.col("FileSize") : nullptr,
                   *ces = ok ? tu.col("ExtractSize") : nullptr, *coff = ok ? tu.col("FileOffset") : nullptr;
    if (!ok || !cname || !cfs || !ces || !coff) { close_h(); return false; }
    const std::string want = lower(inner_path);
    for (uint32_t r = 0; r < tu.nrows; r++) {
        std::string dir = cdir && cdir->st == 0x50 ? tu.str((uint32_t)tu.get(r, cdir)) : std::string();
        if (dir == "<NULL>") dir.clear();
        const std::string inner = lower(dir.empty() ? tu.str((uint32_t)tu.get(r, cname)) : dir + "/" + tu.str((uint32_t)tu.get(r, cname)));
        if (inner != want) continue;
        const uint64_t fsz = tu.get(r, cfs), esz = tu.get(r, ces), off = tu.get(r, coff) + 0x800;
        if (fsz > (256ull << 20) || esz > (256ull << 20)) { close_h(); return false; }
        std::vector<uint8_t> buf((size_t)fsz);
        bool good = pread_all(h, off, buf.data(), buf.size());
        close_h();
        if (!good) return false;
        if (esz != fsz) return crilayla(buf, out) && out.size() == esz;
        out = std::move(buf);
        return true;
    }
    close_h();
    return false;
}
// every pack in <data>/romfs/Pack (movies only with all) -> <data>/dump/<pack>/<path>; files already there at the right
// size are skipped (a stopped dump continues). Progress on stdout. Returns the process exit code.
int rt::cpk_dump(const std::string& data, bool all, const std::string& only) {
    std::error_code ec;
    std::vector<fs::path> packs;
    for (auto& e : fs::directory_iterator(fs::path(data) / "romfs" / "Pack", ec))
        if (e.path().extension() == ".cpk" && (only.empty() ? all || e.path().stem().string().find("movie") == std::string::npos : e.path().stem().string() == only))
            packs.push_back(e.path());
    std::sort(packs.begin(), packs.end());
    if (packs.empty()) { printf("No game packs in %s\\romfs\\Pack: set up the game first.\n", data.c_str()); return 1; }
    const fs::path out_root = fs::path(data) / "dump";
    uint64_t total = 0, failed = 0;
    for (size_t i = 0; i < packs.size(); i++) {
        const std::string stem = packs[i].stem().string();
        FileH h = open_ro(packs[i]);
        if (h == k_bad_file) { printf("%s: cannot open\n", stem.c_str()); continue; }
        std::vector<uint8_t> head(0x800), toc;
        Utf hu, tu;
        auto hc = [&](const char* n) -> uint64_t { const Utf::Col* c = hu.col(n); return c && c->st == 0x50 ? hu.get(0, c) : 0; };
        bool ok = pread_all(h, 0, head.data(), head.size()) && !memcmp(head.data(), "CPK ", 4) && hu.parse(head.data() + 0x10, head.size() - 0x10);
        if (ok) toc.resize(hc("TocSize")), ok = hc("TocOffset") && toc.size() > 0x10 && pread_all(h, hc("TocOffset"), toc.data(), toc.size()) && tu.parse(toc.data() + 0x10, toc.size() - 0x10);
        const Utf::Col *cdir = ok ? tu.col("DirName") : nullptr, *cname = ok ? tu.col("FileName") : nullptr, *cfs = ok ? tu.col("FileSize") : nullptr,
                       *ces = ok ? tu.col("ExtractSize") : nullptr, *coff = ok ? tu.col("FileOffset") : nullptr;
        if (!ok || !cname || !cfs || !ces || !coff) { printf("%s: no readable file table: skipped\n", stem.c_str()); continue; }
        printf("[%zu/%zu] %s: %u files\n", i + 1, packs.size(), stem.c_str(), tu.nrows);
        fflush(stdout);
        std::vector<uint8_t> buf, dec;
        for (uint32_t r = 0; r < tu.nrows; r++) {
            std::string dir = cdir && cdir->st == 0x50 ? tu.str((uint32_t)tu.get(r, cdir)) : std::string();
            if (dir == "<NULL>") dir.clear();
            const std::string inner = dir.empty() ? tu.str((uint32_t)tu.get(r, cname)) : dir + "/" + tu.str((uint32_t)tu.get(r, cname));
            const uint64_t fsz = tu.get(r, cfs), esz = tu.get(r, ces), off = tu.get(r, coff) + 0x800;
            const fs::path dst = out_root / stem / fs::u8path(inner);
            if (fs::is_regular_file(dst, ec) && fs::file_size(dst, ec) == esz) continue;
            buf.resize((size_t)fsz);
            bool good = pread_all(h, off, buf.data(), buf.size());
            const std::vector<uint8_t>* w = &buf;
            if (good && esz != fsz) good = crilayla(buf, dec) && dec.size() == esz, w = &dec;
            if (!good) { failed++; printf("  %s: could not be read\n", inner.c_str()); continue; }
            fs::create_directories(dst.parent_path(), ec);
            fs::path part = dst;
            part += ".part";
            {
                std::ofstream f(part, std::ios::binary);
                good = f && f.write((const char*)w->data(), (std::streamsize)w->size()).good();
            }
            if (good) fs::rename(part, dst, ec);
            if (!good || ec) failed++, printf("  %s: could not be written\n", inner.c_str());
            if (++total % 1000 == 0) printf("  %llu files written\n", (unsigned long long)total), fflush(stdout);
        }
#ifdef _WIN32
        CloseHandle(h);
#else
        close(h);
#endif
    }
    printf("\nDone: %s (%llu files written now, %llu failed)\n", out_root.string().c_str(), (unsigned long long)total, (unsigned long long)failed);
    printf("To mod a file: copy it to mods\\<your mod name>\\cpk\\<pack>\\<same path> and edit the copy.\n");
    return failed ? 1 : 0;
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
#ifdef _WIN32
    HANDLE h = CreateFileW(p.c_str(), access, FILE_SHARE_READ | FILE_SHARE_WRITE, nullptr, OPEN_EXISTING, 0, nullptr);
#else
    FileH h = f_open(p, access);
#endif
    if (h == k_bad_file) {
        LOGV("fs: open %s: not found", p.string().c_str());
        c->r[0] = RES_PATH_NOT_FOUND;
        return;
    }
    // loose-file mods: a read-only CPK from the rom mount may be served as a virtual CPK
    std::shared_ptr<VCpk> v;
    if (mode == 1 && p.extension() == ".cpk") v = vcpk_for(p, h);
    std::lock_guard<std::mutex> l(g_fs_lock);
    uint32_t id = g_next++;
    g_files[id] = {h, v};
    st32(c->r[0], id);
    LOGV("fs: open %s -> %u", p.string().c_str(), id);
    c->r[0] = 0;
}
static FileH file(uint32_t id, std::shared_ptr<VCpk>* v = nullptr) {
    std::lock_guard<std::mutex> l(g_fs_lock);
    auto it = g_files.find(id);
    if (it == g_files.end()) return k_bad_file;
    if (v) *v = it->second.v;
    return it->second.h;
}
static uint32_t do_read(uint32_t id, uint64_t off, uint32_t buf, uint32_t size, uint32_t* got) {
    std::shared_ptr<VCpk> v;
    FileH h = file(id, &v);
    if (h == k_bad_file) return RES_FAIL;
    if (v) return vread(*v, h, off, buf, size, got);
#ifndef _WIN32
    // straight into guest memory; a write-watched page (memory.cpp) makes the kernel return EFAULT instead of
    // faulting, so the rest then goes through a bounce buffer (written by the CPU: the watch sees it)
    uint32_t n = 0;
    while (n < size) {
        ssize_t r = pread(h, GPTR(buf + n), size - n, (off_t)(off + n));
        if (r > 0) { n += (uint32_t)r; continue; }
        if (r == 0) break;
        if (errno == EINTR) continue;
        if (errno != EFAULT) return RES_FAIL;
        std::vector<uint8_t> tmp(std::min<uint32_t>(size - n, 4u << 20));
        r = pread(h, tmp.data(), tmp.size(), (off_t)(off + n));
        if (r < 0) return RES_FAIL;
        if (r == 0) break;
        memcpy(GPTR(buf + n), tmp.data(), (size_t)r);
        n += (uint32_t)r;
    }
    *got = n;
    LOGV("fs: read %u off %llx size %x -> %x", id, (unsigned long long)off, size, n);
    return 0;
#else
    OVERLAPPED o{};
    o.Offset = (DWORD)off;
    o.OffsetHigh = (DWORD)(off >> 32);
    DWORD n = 0;
    if (!ReadFile(h, GPTR(buf), size, &n, &o) && GetLastError() != ERROR_HANDLE_EOF) return RES_FAIL;
    *got = n;
    LOGV("fs: read %u off %llx size %x -> %lx", id, (unsigned long long)off, size, n);
    return 0;
#endif
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
    FileH h = file(c->r[0]);
    uint64_t off = (uint64_t)c->r[3] << 32 | c->r[2];
#ifdef _WIN32
    OVERLAPPED o{};
    o.Offset = (DWORD)off;
    o.OffsetHigh = (DWORD)(off >> 32);
    DWORD n;
    c->r[0] = WriteFile(h, GPTR(arg(c, 4)), arg(c, 5), &n, &o) ? 0 : RES_FAIL;
#else
    const uint32_t buf = arg(c, 4), size = arg(c, 5);
    uint32_t n = 0;
    while (n < size) {
        ssize_t r = pwrite(h, GPTR(buf + n), size - n, (off_t)(off + n));
        if (r < 0 && errno == EINTR) continue;
        if (r <= 0) break;
        n += (uint32_t)r;
    }
    c->r[0] = n == size ? 0 : RES_FAIL;
#endif
}
#ifdef _WIN32
HLE_FN(fs_FlushFile, "_ZN2nn2fs9FlushFileENS0_10FileHandleE") { FlushFileBuffers(file(c->r[0])); c->r[0] = 0; }
HLE_FN(fs_GetSize, "_ZN2nn2fs11GetFileSizeEPxNS0_10FileHandleE") {
    LARGE_INTEGER sz{};
    std::shared_ptr<VCpk> v;
    GetFileSizeEx(file(c->r[1], &v), &sz);
    st64(c->r[0], v ? v->size : (uint64_t)sz.QuadPart);
    c->r[0] = 0;
}
HLE_FN(fs_SetSize, "_ZN2nn2fs11SetFileSizeENS0_10FileHandleEx") {
    HANDLE h = file(c->r[0]);
    FILE_END_OF_FILE_INFO e;
    e.EndOfFile.QuadPart = (LONGLONG)((uint64_t)c->r[3] << 32 | c->r[2]);
    c->r[0] = SetFileInformationByHandle(h, FileEndOfFileInfo, &e, sizeof e) ? 0 : RES_FAIL;
}
#else
HLE_FN(fs_FlushFile, "_ZN2nn2fs9FlushFileENS0_10FileHandleE") { fsync(file(c->r[0])); c->r[0] = 0; }
HLE_FN(fs_GetSize, "_ZN2nn2fs11GetFileSizeEPxNS0_10FileHandleE") {
    struct stat st{};
    std::shared_ptr<VCpk> v;
    fstat(file(c->r[1], &v), &st);
    st64(c->r[0], v ? v->size : (uint64_t)st.st_size);
    c->r[0] = 0;
}
HLE_FN(fs_SetSize, "_ZN2nn2fs11SetFileSizeENS0_10FileHandleEx") {
    c->r[0] = ftruncate(file(c->r[0]), (off_t)((uint64_t)c->r[3] << 32 | c->r[2])) == 0 ? 0 : RES_FAIL;
}
#endif
HLE_FN(fs_CloseFile, "_ZN2nn2fs9CloseFileENS0_10FileHandleE") {
    std::lock_guard<std::mutex> l(g_fs_lock);
    auto it = g_files.find(c->r[0]);
#ifdef _WIN32
    if (it != g_files.end()) { CloseHandle(it->second.h); g_files.erase(it); }
#else
    if (it != g_files.end()) { close(it->second.h); g_files.erase(it); }
#endif
}
HLE_FN(fs_CreateFile, "_ZN2nn2fs10CreateFileEPKcx") {  // (path r0, size r2:r3)
    LOGV("fs: create %s size %x", gstr(c->r[0]).c_str(), c->r[2]);
    fs::path p;
    if (!host_path(c->r[0], p)) { c->r[0] = RES_PATH_NOT_FOUND; return; }
    if (fs::exists(p)) { c->r[0] = RES_PATH_EXISTS; return; }
#ifdef _WIN32
    HANDLE h = CreateFileW(p.c_str(), GENERIC_WRITE, 0, nullptr, CREATE_NEW, 0, nullptr);
    if (h == INVALID_HANDLE_VALUE) { c->r[0] = RES_PATH_NOT_FOUND; return; }
    FILE_END_OF_FILE_INFO e;
    e.EndOfFile.QuadPart = (LONGLONG)((uint64_t)c->r[3] << 32 | c->r[2]);
    SetFileInformationByHandle(h, FileEndOfFileInfo, &e, sizeof e);
    CloseHandle(h);
#else
    int h = open(p.c_str(), O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0666);
    if (h < 0) { c->r[0] = RES_PATH_NOT_FOUND; return; }
    if (ftruncate(h, (off_t)((uint64_t)c->r[3] << 32 | c->r[2]))) log("fs: create %s: cannot set the size", p.string().c_str());
    close(h);
#endif
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
