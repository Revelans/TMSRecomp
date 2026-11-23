// HIPC/CMIF sessions for the services the SDK still talks to directly. Message layout from Switchbrew (IPC_Marshalling).
// Unknown commands answer success with zeroed output and are logged once, so the log lists what is worth implementing.
#include <set>

#include "rt.h"

namespace rt {

uint32_t kernel_add_object(std::shared_ptr<KObject> o);

struct KSession : KObject {
    std::string svc;
    bool domain = false;
    uint32_t next_obj = 1;
    std::unordered_map<uint32_t, std::string> objs;  // domain object id -> interface name
};

struct Request {
    uint32_t buf, type, cmd, token, data;  // data = guest address of the CMIF payload (after the SFCI header)
    uint32_t domain_obj = 0, domain_cmd = 0;
    std::vector<uint32_t> copy, move;
    std::vector<std::pair<uint32_t, uint32_t>> x, a, b;  // (addr, size)
    bool pid = false;
};

struct Reply {
    uint32_t result = 0;
    std::vector<uint8_t> out;
    std::vector<uint32_t> move, copy, objs;
    template <class T> void push(T v) { auto p = (uint8_t*)&v; out.insert(out.end(), p, p + sizeof v); }
};

static std::mutex g_ipc_lock;
static std::set<std::string> g_seen;

uint32_t ipc_new_session(const std::string& name) {
    auto s = std::make_shared<KSession>();
    s->svc = name;
    return kernel_add_object(s);
}
uint32_t ipc_connect(const char* port) {
    log("ConnectToNamedPort(\"%s\")", port);
    return ipc_new_session(port);
}

KObject* kernel_get_object(uint32_t h);

static bool parse(uint32_t buf, KSession* s, Request& q) {
    q.buf = buf;
    uint32_t w0 = ld32(buf), w1 = ld32(buf + 4);
    q.type = w0 & 0xFFFF;
    uint32_t nx = (w0 >> 16) & 0xF, na = (w0 >> 20) & 0xF, nb = (w0 >> 24) & 0xF, nw = (w0 >> 28) & 0xF;
    uint32_t p = buf + 8;
    if (w1 >> 31) {
        uint32_t sh = ld32(p);
        p += 4;
        q.pid = sh & 1;
        if (q.pid) p += 8;
        for (uint32_t i = 0; i < ((sh >> 1) & 0xF); i++, p += 4) q.copy.push_back(ld32(p));
        for (uint32_t i = 0; i < ((sh >> 5) & 0xF); i++, p += 4) q.move.push_back(ld32(p));
    }
    for (uint32_t i = 0; i < nx; i++, p += 8) q.x.emplace_back(ld32(p + 4), ld32(p) >> 16);
    for (uint32_t i = 0; i < na; i++, p += 12) q.a.emplace_back(ld32(p + 4), ld32(p));
    for (uint32_t i = 0; i < nb; i++, p += 12) q.b.emplace_back(ld32(p + 4), ld32(p));
    p += 12 * nw;
    p = buf + ((p - buf + 15) & ~15u);
    if (s->domain && q.type == 4) {  // domain header: u8 cmd, u8 nobj, u16 size, u32 object, u32 pad, u32 token
        q.domain_cmd = ld8(p);
        q.domain_obj = ld32(p + 4);
        p += 16;
    }
    if (ld32(p) != 0x49434653 && q.type != 2 && q.domain_cmd != 2) {  // "SFCI"
        log("ipc %s: no SFCI magic (type %u)", s->svc.c_str(), q.type);
        return false;
    }
    q.cmd = ld32(p + 8);
    q.token = ld32(p + 12);
    q.data = p + 16;
    return true;
}

static void write_reply(KSession* s, const Request& q, const Reply& r) {
    uint32_t buf = q.buf;
    bool special = !r.move.empty() || !r.copy.empty();
    uint32_t hdr_words = 2 + (special ? 1 + (uint32_t)(r.copy.size() + r.move.size()) : 0);
    uint32_t payload = (s->domain ? 16 : 0) + 16 + (uint32_t)((r.out.size() + 3) & ~3u) + 4 * (uint32_t)r.objs.size();
    uint32_t data_words = 4 + payload / 4;  // 16 bytes of alignment padding are always reserved
    st32(buf, 0);
    st32(buf + 4, data_words | (special ? 0x80000000u : 0));
    uint32_t p = buf + 8;
    if (special) {
        st32(p, (uint32_t)(r.copy.size() << 1 | r.move.size() << 5));
        p += 4;
        for (uint32_t h : r.copy) { st32(p, h); p += 4; }
        for (uint32_t h : r.move) { st32(p, h); p += 4; }
    }
    (void)hdr_words;
    p = buf + ((p - buf + 15) & ~15u);
    if (s->domain) {
        memset(GPTR(p), 0, 16);
        st32(p, (uint32_t)r.objs.size());
        p += 16;
    }
    st32(p, 0x4F434653);  // "SFCO"
    st32(p + 4, 0);
    st32(p + 8, r.result);
    st32(p + 12, 0);
    p += 16;
    memcpy(GPTR(p), r.out.data(), r.out.size());
    p += (uint32_t)((r.out.size() + 3) & ~3u);
    for (uint32_t o : r.objs) { st32(p, o); p += 4; }
}

// ------------------------------------------------------------------------------------------------ services
static void sm(KSession* s, Request& q, Reply& r) {
    if (q.cmd == 0) return;  // RegisterClient
    if (q.cmd == 1) {        // GetService(name u64)
        char name[9] = {};
        memcpy(name, GPTR(q.data), 8);
        log("sm GetService(\"%s\")", name);
        r.move.push_back(ipc_new_session(name));
        return;
    }
    log("sm cmd %u", q.cmd);
}

static void control(KSession* s, Request& q, Reply& r) {
    switch (q.cmd) {
        case 0: s->domain = true; r.push<uint32_t>(s->next_obj++); return;  // ConvertCurrentObjectToDomain
        case 2: case 4: r.move.push_back(ipc_new_session(s->svc)); return;  // CloneCurrentObject(Ex)
        case 3: r.push<uint16_t>(0x8000); return;                             // QueryPointerBufferSize
        default: log("ipc control cmd %u", q.cmd);
    }
}

uint32_t ipc_request(uint32_t handle, uint32_t buf, uint32_t size) {
    (void)size;
    KSession* s = dynamic_cast<KSession*>(kernel_get_object(handle));
    if (!s) { log("ipc to bad handle %08x", handle); return 0xE401; }
    std::lock_guard<std::mutex> l(g_ipc_lock);
    Request q;
    if (!parse(buf, s, q)) return 0xF601;
    if (q.type == 2) return 0;  // close
    Reply r;
    if (q.type == 5 || q.type == 7) control(s, q, r);
    else if (s->svc == "sm:") sm(s, q, r);
    else {
        std::string key = s->svc + "#" + std::to_string(q.cmd);
        if (g_seen.insert(key).second) log("ipc %s cmd %u: unimplemented, returning success", s->svc.c_str(), q.cmd);
        r.out.assign(0x40, 0);
    }
    write_reply(s, q, r);
    return 0;
}

}  // namespace rt
