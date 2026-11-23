"""Run a translated vertex shader (GLSL from tools/shader_glsl.py) on the CPU: wraps it as C++ with the GLSL builtins it
uses and feeds it a `drawlog` skin dump (analysis/skin_<vbuf0>.bin: c4 0x200, c8 0x1c0, c9 0x3000, 8 vertices of stride 20).
Shortcut: c1 (BRX table) is hard-coded for vertex shader 7e942600, normals are (0,0,1); edit for other shaders.
    python tools/glsl_emu.py Vertex_X.glsl out.cpp  &&  clang++ -O0 -w -ffp-contract=off out.cpp -o emu.exe  &&  emu.exe skin.bin"""
import sys, re
src = open(sys.argv[1]).read()
body = src[src.index("void main()"):].replace("void main()", "void shade()").replace("precise ", "")
hdr = r'''
#include <cmath>
#include <cstdio>
#include <cstring>
#include <cstdint>
typedef unsigned uint;
struct vec4 { float x, y, z, w; float& operator[](int i) { return (&x)[i]; } };
struct uvec4 { uint x, y, z, w; };
struct UB { vec4 data[4096]; };
static UB vp_c1, vp_c4, vp_c6, vp_c8, vp_c9;
static vec4 in_attr0, in_attr1, in_attr2, in_attr3, in_attr4, in_attr5, in_attr6, out_attr0, out_attr1, out_attr2, out_attr3, out_attr4, gl_Position;
static uvec4 in_attr7;
static float gl_PointSize;
static const int undef = 0;
static int floatBitsToInt(float f) { int i; memcpy(&i, &f, 4); return i; }
static float intBitsToFloat(int i) { float f; memcpy(&f, &i, 4); return f; }
static double min(double a, double b) { return a < b ? a : b; }
static double max(double a, double b) { return a > b ? a : b; }
static uint min(uint a, uint b) { return a < b ? a : b; }
static float inversesqrt(float x) { return 1.0f / sqrtf(x); }

'''
main = r'''
int main(int argc, char** argv) {
    FILE* f = fopen(argv[1], "rb"); static unsigned char d[0x3c0 + 0x3000 + 160]; fread(d, 1, sizeof d, f); fclose(f);
    memcpy(vp_c4.data, d, 0x200); memcpy(vp_c8.data, d + 0x200, 0x1c0); memcpy(vp_c9.data, d + 0x3c0, 0x3000);
    uint c1[8] = {0x158, 0x170, 0x180, 0x198, 0x900, 0x918, 0x930, 0x940}; memcpy(vp_c1.data, c1, 32);
    for (int v = 0; v < 8; v++) {
        unsigned char* p = d + 0x33c0 + 20 * v;
        memcpy(&in_attr0, p, 12); in_attr0.w = 1;
        in_attr7 = {p[12], p[13], p[14], p[15]};
        in_attr1 = {p[16] / 255.f, p[17] / 255.f, p[18] / 255.f, p[19] / 255.f};
        in_attr2 = {0, 0, 1, 0}; in_attr3 = {1, 1, 1, 1}; in_attr4 = {0, 0, 0, 0};
        shade();
        printf("v%d pos %g %g %g idx %u %u %u w %.3f %.3f %.3f clip %g %g %g %g ndc %g %g\n", v, in_attr0.x, in_attr0.y, in_attr0.z,
               in_attr7.x, in_attr7.y, in_attr7.z, in_attr1.x, in_attr1.y, in_attr1.z, gl_Position.x, gl_Position.y, gl_Position.z, gl_Position.w,
               gl_Position.x / gl_Position.w, gl_Position.y / gl_Position.w);
    }
}
'''
open(sys.argv[2], "w").write(hdr + body + main)
