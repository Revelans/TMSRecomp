#pragma once
#include <atomic>
#include <map>

#include "vk.h"

namespace vk {

struct Resource { uint8_t kind, set; uint16_t binding; int32_t slot, handle, type, count; };
struct Translated {
    std::vector<uint32_t> spirv;
    std::vector<Resource> res;
    uint32_t code_size = 0, frag_outputs = 0;
};
// consts: the shader's embedded constant data (glslc literal tables), which the driver binds as Maxwell cbuf 1
// src/src_consts: guest code (after the NVN header) and its constants' offset from there, for re-translating a vertex
// stage with integer attribute inputs (variants, keyed by the 32 attribute types)
struct StageVk {
    VkShaderStageFlagBits vk_stage; VkShaderModule module; uint32_t stage; Translated t; uint64_t consts = 0; uint32_t consts_size = 0;
    uint32_t src = 0, src_consts = 0;
    mutable std::map<std::string, VkShaderModule> variants;
};
struct ProgramVk { std::vector<StageVk> stages; };  // translated stages of one NVN program
// the programs bound to each NVN stage at draw time, combined: one descriptor set and pipeline layout
struct Combo {
    std::vector<const StageVk*> stages;
    VkDescriptorSetLayout set_layout = VK_NULL_HANDLE;
    VkPipelineLayout layout = VK_NULL_HANDLE;
    std::map<std::string, VkPipeline> pipelines;  // keyed by the packed fixed-function state
};

// consts: offset of the shader's constant data (Maxwell cbuf 1) from `code`, for jump tables the translator reads
// attr_types (vertex only, 32 bytes, Ryujinx AttributeType per input location; null = all float)
bool translate(uint32_t stage, const uint8_t* code, uint32_t len, const uint32_t local[3], uint32_t consts_off, uint32_t consts_size, Translated& out, const uint8_t* attr_types = nullptr);
// the vertex stage's module for these attribute types (all float: the stage's own module)
VkShaderModule alpha_module(const StageVk& st, uint32_t func, float ref);  // fragment stage + the hardware alpha test
VkShaderModule vertex_module(const StageVk& st, const uint8_t types[32]);
ProgramVk* program_of(nvn::Program* p);
Combo* combo_of(nvn::Program* const per_stage[6]);  // NVN stage order: vertex, fragment, geometry, tess c, tess e, compute
uint32_t nvn_stage(uint32_t ryu_stage);
// pipeline recipes / prewarm (vk_replay.cpp): shaders named by a hash of their SPIR-V
std::string seed_dir();  // <exe dir>/cache_seed: shaders.bin + pipelines.recipes shipped with a release (read only)
VkShaderModule make_module(const Translated& t, bool shared = true);  // shared: one module per SPIR-V, never destroy it
uint64_t spirv_hash(const Translated& t);
uint64_t module_hash(VkShaderModule m);               // 0: not made by make_module
const Translated* translation_by_hash(uint64_t h);    // from <data>/cache/shaders.bin, null if absent
void make_layout(const std::vector<std::pair<VkShaderStageFlagBits, const Translated*>>& stages, VkDescriptorSetLayout* set_layout, VkPipelineLayout* layout);
// frame stats (vk.cpp): sidecar translations (time, count) and translations served from the disk cache
extern std::atomic<uint32_t> g_translate_us, g_translate_n, g_translate_hits;
// pipelines: one VkPipelineCache kept in <data>/cache/pipelines.bin (saved by pipeline_cache_save when new ones exist)
VkPipelineCache pipeline_cache();
void pipeline_cache_save();
extern std::atomic<uint32_t> g_pipeline_us, g_pipeline_n, g_pipeline_inline,g_pipelines_total, g_programs_new, g_programs_shared, g_programs_moved;  // programs: since the last frame stats line

}  // namespace vk
