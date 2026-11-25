// bc7_check <in.dds BC7> <out.raw>: level 0 decoded by runtime/src/bc7.h to raw RGBA8 (compare with texconv's decode);
// also re-encodes every block with mode 6 and prints the mean abs error (encoder sanity). s113.
#include "../../runtime/src/bc7.h"
#include <cstdio>
#include <cstdlib>
#include <vector>
int main(int argc, char** argv) {
    if (argc < 3) return 1;
    FILE* f = fopen(argv[1], "rb");
    if (!f) return 1;
    std::vector<uint8_t> b;
    for (int c; (c = fgetc(f)) != EOF;) b.push_back((uint8_t)c);
    fclose(f);
    uint32_t h = *(uint32_t*)&b[12], w = *(uint32_t*)&b[16];
    const uint8_t* d = b.data() + 148;
    std::vector<uint8_t> out((size_t)w * h * 4);
    double err = 0;
    for (uint32_t by = 0; by < h / 4; by++)
        for (uint32_t bx = 0; bx < w / 4; bx++) {
            uint8_t px[64], re[16], px2[64];
            bc7::decode_block(d + ((size_t)by * (w / 4) + bx) * 16, px);
            for (int i = 0; i < 16; i++) memcpy(&out[(((size_t)by * 4 + i / 4) * w + bx * 4 + i % 4) * 4], px + i * 4, 4);
            if ((bx + by) % 7 == 0) {
                bc7::encode_block_mode6(px, re), bc7::decode_block(re, px2);
                for (int i = 0; i < 64; i++) err += abs(px[i] - px2[i]);
            }
        }
    FILE* o = fopen(argv[2], "wb");
    fwrite(out.data(), 1, out.size(), o);
    fclose(o);
    printf("%ux%u decoded; mode-6 re-encode mean abs error %.3f\n", w, h, err / ((double)w * h * 4 / 7));
    return 0;
}
