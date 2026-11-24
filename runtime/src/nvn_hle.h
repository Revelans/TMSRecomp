// NVN, high level: host-side objects keyed by the guest object address, commands recorded per command buffer.
// Object and builder layouts come from the SDK's own NVN driver (see NOTES.md, "NVN"); builders and state objects
// are left to the real driver code, everything that would touch the GPU is implemented here.
#pragma once
#include "rt.h"
#include <chrono>
#include <memory>
#include <unordered_set>
#include <vector>

namespace nvn {

// GPU virtual addresses are guest CPU addresses (memory pool storage is guest memory), widened to 64 bits.
struct Pool { uint32_t addr = 0, size = 0, flags = 0; void* host = nullptr; };
struct Buffer { uint32_t pool = 0, offset = 0, size = 0; uint64_t gpu() const; };
struct Texture {
    uint32_t pool = 0, offset = 0, flags = 0, target = 0, width = 0, height = 0, depth = 0, levels = 0, format = 0,
             samples = 0, stride = 0, swizzle[4] = {}, ds_mode = 0;
    uint32_t layout = 0;  // builder +0x48 (SetPackagedTextureLayout): bits 0-3 set, bits 4-7 log2 GOBs per block in Y
    uint64_t gpu = 0;
    void* host = nullptr;  // backend image
    uint32_t guest = 0;
};
// the parts of an NVNtextureView we apply: flags bit 3 swizzle, bit 5 target (others: levels, layers, format, ds mode)
struct TexView { uint8_t flags = 0; uint32_t swizzle[4] = {}; uint32_t target = 0; uint32_t ds_mode = 0; bool has = false; };
struct Sampler { uint32_t words[18] = {}; void* host = nullptr; };  // the builder's state, copied
struct Program { struct Stage { uint64_t code; uint32_t control; } stages[6]; uint32_t mask = 0; void* host = nullptr; };

// one recorded command: opcode + arguments captured at record time (states are copied, never referenced)
enum Op : uint16_t {
    OP_NONE, OP_RENDER_TARGETS, OP_VIEWPORT, OP_SCISSOR, OP_CLEAR_COLOR, OP_CLEAR_DS, OP_PROGRAM, OP_BLEND, OP_COLOR,
    OP_CHANNEL_MASK, OP_DEPTH_STENCIL, OP_MULTISAMPLE, OP_POLYGON, OP_VTX_ATTRIB, OP_VTX_STREAM, OP_VTX_BUFFER,
    OP_UNIFORM, OP_STORAGE, OP_TEXTURE, OP_IMAGE, OP_DRAW, OP_DRAW_INDEXED, OP_DRAW_INSTANCED, OP_DRAW_INDEXED_INSTANCED,
    OP_DISPATCH, OP_COPY_BUF_TEX, OP_COPY_TEX_BUF, OP_COPY_TEX_TEX, OP_COPY_BUF_BUF, OP_BARRIER, OP_TEX_POOL,
    OP_SMP_POOL, OP_BLEND_COLOR, OP_DEPTH_RANGE, OP_LINE_WIDTH, OP_POINT_SIZE, OP_STENCIL_REF, OP_ALPHA_REF, OP_PRIM_RESTART,
    OP_DEPTH_BOUNDS, OP_INLINE_UNIFORM, OP_CALL, OP_COPY_CMDS, OP_SYNC, OP_WAIT_SYNC, OP_DISCARD, OP_RESOLVE,
    OP_TILED_CACHE, OP_CLEAR_TEX, OP_UNKNOWN,
};
// Copied state / inline data of a command. CallCommands copies whole recorded lists into the calling buffer every frame
// (profile s69: heap alloc / free + its locks ~20% of the game thread in big areas), so copies share the bytes; a write
// (only done while a command is recorded) copies first if the bytes are shared.
struct Blob {
    std::shared_ptr<std::vector<uint8_t>> p;
    size_t size() const { return p ? p->size() : 0; }
    bool empty() const { return size() == 0; }
    const uint8_t* data() const { return p ? p->data() : nullptr; }
    const uint8_t& operator[](size_t i) const { return (*p)[i]; }
    uint8_t& operator[](size_t i) { return (*own())[i]; }
    void resize(size_t n) { own()->resize(n); }
    template <class It> void assign(It a, It b) { own()->assign(a, b); }
    std::vector<uint8_t>* own() {
        if (!p) p = std::make_shared<std::vector<uint8_t>>();
        else if (p.use_count() > 1) p = std::make_shared<std::vector<uint8_t>>(*p);
        return p.get();
    }
};
struct Cmd {
    Op op = OP_NONE;
    uint32_t a[12] = {};
    Blob blob;
};
// chunk: current command memory (pool << 32 | offset), mem_size its size; mem_cmds: commands recorded into it (the used bytes
// the game reads back, nvn_hle.cpp cmdmem_used); rec_from: mem_cmds when the current recording began
struct CmdBuf { std::vector<Cmd> cmds; bool recording = false; uint64_t chunk = 0; uint32_t mem_size = 0, mem_cmds = 0, rec_from = 0; };

struct Queue { std::vector<uint32_t> pending; };
struct Window { uint32_t ntex = 0, textures[4] = {}, next = 0, interval = 1; };
extern std::unordered_set<uint32_t> g_window_tex;
extern bool g_ui_phase;  // vk_replay.cpp: ultrawide UI phase of the frame being recorded  // guest NVNtexture addresses the game presents (ultrawide: UI targets)

extern std::mutex g_lock;
template <class T> T* get(uint32_t guest);
template <class T> T& make(uint32_t guest);
void destroy(uint32_t guest);

Pool* pool_of(uint64_t gpu, uint32_t* off);

// backend (vk.cpp)
extern uint32_t g_depth_mode;  // NVNdepthMode: 0 near is -w (OpenGL clip space, the default), 1 near is zero
void backend_init();
void backend_submit(const std::vector<const std::vector<Cmd>*>& lists);
void sync_mark(uint32_t sync, uint64_t serial);  // nvn_hle.cpp: a FenceSync replayed in the submit with this serial
void backend_present(Texture* t);
void backend_texture_created(Texture* t);
void backend_texture_finalized(Texture* t);  // frees the backend image once the GPU is done with it
void write_texels(Texture* t, const int32_t region[6], const uint8_t* data);  // vk_texture.cpp

}  // namespace nvn

namespace vk {  // vk.cpp: GPU submit timeline
uint64_t gpu_last_submitted();
uint64_t gpu_recording_serial();
bool gpu_wait(uint64_t serial, uint64_t timeout_ns);
struct RenderWait { std::chrono::steady_clock::time_point t0 = std::chrono::steady_clock::now(); ~RenderWait(); };  // times the game thread blocked on the render thread (frame stats)
}  // namespace vk
