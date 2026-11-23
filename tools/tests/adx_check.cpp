// Check of the custom music ADX decoder (runtime/src/ext_bgm.cpp): decodes the first N frames of an .adx file to raw
// s16 stereo, to compare with an independent decoder.
//   clang++ -std=c++20 -O1 -w -DNOMINMAX -DWIN32_LEAN_AND_MEAN -I../../runtime/src -I<SDL3 include> adx_check.cpp -o adx_check.exe
//   adx_check <file.adx> <frames> <out.raw>
#include "../../runtime/src/ext_bgm.cpp"
#include <cstdarg>
namespace rt {
std::string g_data_dir;
void log(const char* fmt, ...) { va_list a; va_start(a, fmt); vprintf(fmt, a); va_end(a); puts(""); }
}
int main(int argc, char** argv) {
    if (argc < 4) return 2;
    Adx a;
    if (!a.open(argv[1])) { puts("open failed"); return 1; }
    printf("rate %u ch %u total %u loop %d %u..%u\n", a.rate, a.ch, a.total, a.loop, a.loop_start, a.loop_end);
    FILE* o = fopen(argv[3], "wb");
    const uint64_t n = (uint64_t)atoi(argv[2]) * 32;
    for (uint64_t i = 0, k = 0; i < n; i++, k++) {  // k: the decoder's position (jumps back at the loop end)
        int l, r;
        if (!a.sample(k, l, r)) break;
        int16_t s[2] = {(int16_t)l, (int16_t)r};
        fwrite(s, 2, 2, o);
    }
    fclose(o);
    return 0;
}
