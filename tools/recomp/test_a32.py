"""Differential test: random A32/VFP/NEON instructions, our C translation vs Unicorn.

    python tools/recomp/test_a32.py [--n 400] [--seed 1] [--only class]
    python tools/recomp/test_a32.py --only game --link private/tms/link [--n 100000]

Class "game": every distinct VFP/NEON encoding in the linked image's code (main + sdk), not random ones.

Builds one test exe with every case (clang), runs it, compares registers/flags/memory with Unicorn.
"""
import argparse
import os
import random
import struct
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
import a32  # noqa: E402
import vfp  # noqa: E402
from unicorn import UC_ARCH_ARM, UC_MODE_ARM, Uc, UcError  # noqa: E402
from unicorn import arm_const as U  # noqa: E402

CLANG = r"C:\Program Files\LLVM\bin\clang.exe"
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
CODE = 0x1000
MEM = 0x10000       # data window the base registers point into
MEMSZ = 0x10000
REGS = [getattr(U, f"UC_ARM_REG_R{i}") for i in range(13)] + [U.UC_ARM_REG_SP, U.UC_ARM_REG_LR]


def rnd_cond(r):
    return 14 if r.random() < 0.6 else r.randrange(14)


def gen(cls, r):
    """Random encodings for one class; PC/SP are kept out of operands where they would branch or trash the stack."""
    c = rnd_cond(r) << 28
    reg = lambda: r.randrange(13)
    if cls == "dp_imm":
        return c | 0x02000000 | r.randrange(16) << 21 | r.randrange(2) << 20 | reg() << 16 | reg() << 12 | r.randrange(4096)
    if cls == "dp_reg":
        return c | r.randrange(16) << 21 | r.randrange(2) << 20 | reg() << 16 | reg() << 12 | r.randrange(32) << 7 | r.randrange(4) << 5 | reg()
    if cls == "dp_rsr":
        return c | r.randrange(16) << 21 | r.randrange(2) << 20 | reg() << 16 | reg() << 12 | reg() << 8 | r.randrange(4) << 5 | 0x10 | reg()
    if cls == "mul":
        op = r.choice([0, 1, 2, 3, 6, 8, 9, 10, 11, 12, 13, 14, 15, 4])
        rd, ra = r.sample(range(13), 2)
        return c | op << 20 | rd << 16 | ra << 12 | reg() << 8 | 0x90 | reg()
    if cls == "ldst":
        # base r0..r3 (pointed into MEM), rt r4..r12 different from base; offsets small
        rn, rt = r.randrange(4), r.randrange(4, 13)
        p, u, b, w, l = r.randrange(2), r.randrange(2), r.randrange(2), r.randrange(2), r.randrange(2)
        if not p:
            w = 0
        if r.random() < 0.5:
            return c | 0x04000000 | p << 24 | u << 23 | b << 22 | w << 21 | l << 20 | rn << 16 | rt << 12 | r.randrange(256)
        return c | 0x06000000 | p << 24 | u << 23 | b << 22 | w << 21 | l << 20 | rn << 16 | rt << 12 | r.randrange(4) << 7 | r.randrange(2) << 5 | r.randrange(4, 6)
    if cls == "acqrel":  # LDA/LDAB/LDAH, STL/STLB/STLH; base r0..r3 (into MEM, word aligned)
        rn, rt = r.randrange(4), r.randrange(4, 13)
        sz = r.choice([(0x01900C9F, 0x0180FC90), (0x01D00C9F, 0x01C0FC90), (0x01F00C9F, 0x01E0FC90)])
        return c | sz[0] | rn << 16 | rt << 12 if r.randrange(2) else c | sz[1] | rn << 16 | rt
    if cls == "ldst_extra":
        rn, rt = r.randrange(4), r.choice([4, 6, 8, 10])
        p, u, w = r.randrange(2), r.randrange(2), r.randrange(2)
        if not p:
            w = 0
        op2 = r.choice([1, 2, 3])
        l = r.randrange(2)
        imm = r.randrange(256)
        return c | p << 24 | u << 23 | 1 << 22 | w << 21 | l << 20 | rn << 16 | rt << 12 | (imm >> 4) << 8 | 0x90 | op2 << 5 | (imm & 0xF)
    if cls == "ldm":
        rn = r.randrange(4)
        lst = r.randrange(1, 1 << 13) & ~(1 << rn) | 0x10
        return c | 0x08000000 | r.randrange(2) << 24 | r.randrange(2) << 23 | r.randrange(2) << 21 | r.randrange(2) << 20 | rn << 16 | lst
    if cls == "media":
        f = r.choice(["ubfx", "sbfx", "bfi", "bfc", "ext", "rev", "sel", "ssat", "usat", "pkh", "div", "par", "smmul", "smlad"])
        rd, rn, rm = reg(), reg(), reg()
        if f in ("ubfx", "sbfx"):
            lsb = r.randrange(32)
            wm1 = r.randrange(32 - lsb)
            return c | (0x07E00050 if f == "ubfx" else 0x07A00050) | wm1 << 16 | rd << 12 | lsb << 7 | rm
        if f in ("bfi", "bfc"):
            lsb = r.randrange(32)
            msb = r.randrange(lsb, 32)
            return c | 0x07C00010 | msb << 16 | rd << 12 | lsb << 7 | (15 if f == "bfc" else rm)
        if f == "ext":
            o1 = r.choice([0b000, 0b010, 0b011, 0b100, 0b110, 0b111])
            return c | 0x06800070 | o1 << 20 | r.choice([rn, 15]) << 16 | rd << 12 | r.randrange(4) << 10 | rm
        if f == "rev":
            return c | r.choice([0x06BF0F30, 0x06BF0FB0, 0x06FF0F30, 0x06FF0FB0]) | rd << 12 | rm
        if f == "sel":
            return c | 0x06800FB0 | rn << 16 | rd << 12 | rm
        if f in ("ssat", "usat"):
            return c | (0x06A00010 if f == "ssat" else 0x06E00010) | r.randrange(32) << 16 | rd << 12 | r.randrange(32) << 7 | r.randrange(2) << 6 | rm
        if f == "pkh":
            return c | 0x06800010 | rn << 16 | rd << 12 | r.randrange(32) << 7 | r.randrange(2) << 6 | rm
        if f == "div":
            return c | r.choice([0x0710F010, 0x0730F010]) | rd << 16 | rm << 8 | rn
        if f == "par":
            return c | 0x06000F10 | r.choice([1, 2, 3, 5, 6, 7]) << 20 | rn << 16 | rd << 12 | r.choice([0, 1, 2, 3, 4, 7]) << 5 | rm
        if f == "smmul":
            return c | 0x07500010 | rd << 16 | r.choice([15, reg()]) << 12 | rm << 8 | r.randrange(2) << 5 | rn
        return c | 0x07000010 | rd << 16 | r.choice([15, reg()]) << 12 | rm << 8 | r.randrange(4) << 5 | rn
    if cls == "misc":
        f = r.choice(["clz", "mrs", "msr", "movw", "movt", "hmul", "qadd", "crc"])
        rd, rm = reg(), reg()
        if f == "clz":
            return c | 0x016F0F10 | rd << 12 | rm
        if f == "mrs":
            return c | 0x010F0000 | rd << 12
        if f == "msr":
            return c | 0x0128F000 | rm  # APSR_nzcvq
        if f in ("movw", "movt"):
            return c | (0x03000000 if f == "movw" else 0x03400000) | r.randrange(16) << 16 | rd << 12 | r.randrange(4096)
        if f == "hmul":
            return c | 0x01000080 | r.randrange(4) << 21 | rd << 16 | reg() << 12 | reg() << 8 | r.randrange(4) << 5 | rm
        if f == "qadd":
            return c | 0x01000050 | r.randrange(4) << 21 | reg() << 16 | rd << 12 | rm
        return c | 0x01000040 | r.randrange(3) << 21 | reg() << 16 | rd << 12 | r.randrange(2) << 9 | rm
    if cls == "vfp":
        f = r.choice(["arith", "arith_d", "cmp", "cvt", "mov", "unary"])
        d, n, m = r.randrange(32), r.randrange(32), r.randrange(32)
        sd = lambda x: ((x & 1) << 22 | (x >> 1) << 12)
        sn = lambda x: ((x >> 1) << 16 | (x & 1) << 7)
        sm = lambda x: ((x >> 1) | (x & 1) << 5)
        dd = lambda x: ((x >> 4) << 22 | (x & 15) << 12)
        dn = lambda x: ((x & 15) << 16 | (x >> 4) << 7)
        dm = lambda x: ((x & 15) | (x >> 4) << 5)
        if f == "arith":
            op = r.choice([0x0E000A00, 0x0E000A40, 0x0E100A00, 0x0E100A40, 0x0E200A00, 0x0E200A40, 0x0E300A00,
                           0x0E300A40, 0x0E800A00, 0x0EA00A00, 0x0EA00A40])
            return c | op | sd(d) | sn(n) | sm(m)
        if f == "arith_d":
            op = r.choice([0x0E000B00, 0x0E300B00, 0x0E300B40, 0x0E200B00, 0x0E800B00, 0x0E000B40])
            return c | op | dd(d) | dn(n) | dm(m)
        if f == "cmp":
            return c | r.choice([0x0EB40A40, 0x0EB40AC0]) | sd(d) | sm(m)
        if f == "cvt":
            op = r.choice([0x0EB80AC0, 0x0EB80A40, 0x0EBD0AC0, 0x0EBC0AC0])  # s32->f32, u32->f32, f32->s32, f32->u32
            return c | op | sd(d) | sm(m)
        if f == "mov":
            return c | 0x0EB00A40 | sd(d) | sm(m)
        return c | r.choice([0x0EB10A40, 0x0EB00AC0, 0x0EB10AC0]) | sd(d) | sm(m)  # vneg, vabs, vsqrt
    if cls == "neon":
        q = r.randrange(2)
        d, n, m = (r.randrange(16) & ~q) , (r.randrange(16) & ~q), (r.randrange(16) & ~q)
        op = r.choice([0xF2000800, 0xF3000800, 0xF2000110, 0xF2200110, 0xF3000110, 0xF2000D00, 0xF3000D10,
                       0xF2000D10, 0xF3000E00, 0xF2000F00, 0xF3200E00, 0xF2000900 | 0x10])
        sz = r.randrange(3) << 20 if op in (0xF2000800, 0xF3000800, 0xF2000900 | 0x10) else 0
        return op | sz | q << 6 | (d & 15) << 12 | (n & 15) << 16 | (m & 15)
    raise ValueError(cls)


CLASSES = ["dp_imm", "dp_reg", "dp_rsr", "mul", "ldst", "ldst_extra", "ldm", "acqrel", "media", "misc", "vfp", "neon", "game"]


def game_words(link):
    """Distinct VFP/NEON words in the image's text: coprocessor 10/11 (cond != 0xF), NEON data processing (0xF2/0xF3),
    NEON element load/store (0xF4)."""
    import json
    lay = json.load(open(os.path.join(link, "layout.json")))
    img = open(os.path.join(link, "image.bin"), "rb").read()
    base = lay["image_base"]
    seen = set()
    for m in lay["modules"]:
        s, e = m["text"]
        for w in struct.unpack_from(f"<{(e - s) // 4}I", img, s - base):
            top = w >> 24
            vfp_ = (w >> 28) != 0xF and ((w >> 25) & 7) in (6, 7) and ((w >> 9) & 7) == 5
            if vfp_ or top in (0xF2, 0xF3, 0xF4):
                seen.add(w)
    return sorted(seen)


def rnd_state(r, cls):
    regs = [r.getrandbits(32) for _ in range(15)]
    if cls == "game":  # loads/stores: every core register points into MEM (16-byte aligned); post-index adds stay inside
        for i in range(13):
            regs[i] = MEM + 0x4000 + r.randrange(0x4000) & ~15
    if cls in ("ldst", "ldst_extra", "ldm", "acqrel"):
        for i in range(4):
            regs[i] = MEM + 0x4000 + r.randrange(0x4000) & ~3
        if cls != "ldm":
            for i in range(4, 13):
                regs[i] = r.getrandbits(32)
            # register offsets used by the reg-offset forms are r4/r5: keep them small
            regs[4] = r.randrange(64)
            regs[5] = r.randrange(64)
    if r.random() < 0.3:
        for i in range(13):
            regs[i] = r.choice([0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, r.randrange(64), regs[i]])
    flags = r.randrange(16)
    vregs = []
    for _ in range(32):
        k = r.random()
        if k < 0.5:
            vregs.append(struct.unpack("<Q", struct.pack("<ff", r.uniform(-1000, 1000), r.uniform(-4, 4)))[0])
        elif k < 0.7:
            vregs.append(struct.unpack("<Q", struct.pack("<d", r.uniform(-1e6, 1e6)))[0])
        else:
            vregs.append(r.getrandbits(64))
    mem = bytes(r.getrandbits(8) for _ in range(MEMSZ))
    ge = r.randrange(16)
    return regs, flags, vregs, mem, ge


def run_unicorn(w, regs, flags, vregs, mem, ge):
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(CODE, 0x1000)
    uc.mem_map(MEM, MEMSZ)
    uc.mem_write(CODE, struct.pack("<I", w))
    uc.mem_write(MEM, mem)
    uc.reg_write(U.UC_ARM_REG_C1_C0_2, uc.reg_read(U.UC_ARM_REG_C1_C0_2) | (0xF << 20))
    uc.reg_write(U.UC_ARM_REG_FPEXC, 0x40000000)
    cpsr = uc.reg_read(U.UC_ARM_REG_CPSR) & 0x0000FFFF & ~0x1F | 0x10
    uc.reg_write(U.UC_ARM_REG_CPSR, cpsr | flags << 28 | ge << 16)  # mode first: SP/LR are banked
    for i, rr in enumerate(REGS):
        uc.reg_write(rr, regs[i])
    for i in range(32):
        uc.reg_write(getattr(U, f"UC_ARM_REG_D{i}"), vregs[i])
    try:
        uc.emu_start(CODE, CODE + 4, count=1)
    except UcError as e:
        return None
    if uc.reg_read(U.UC_ARM_REG_PC) != CODE + 4:
        return None
    out = [uc.reg_read(rr) for rr in REGS]
    cp = uc.reg_read(U.UC_ARM_REG_CPSR)
    fp = uc.reg_read(U.UC_ARM_REG_FPSCR) >> 28
    vo = [uc.reg_read(getattr(U, f"UC_ARM_REG_D{i}")) for i in range(32)]
    return out, cp >> 28, (cp >> 16) & 0xF, fp, vo, bytes(uc.mem_read(MEM, MEMSZ))


def c_case(k, ins):
    body = a32.cond_c_lines(ins) if hasattr(a32, "cond_c_lines") else None
    lines = list(ins.lines)
    if ins.cond != 14:
        lines = [f"if ({a32.COND_C[ins.cond]}) {{"] + lines + ["}"]
    return f"static void T{k}(Cpu* c) {{\n  " + "\n  ".join(lines) + "\n}\n"


HARNESS = r"""
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include "guest.h"
GuestFn g_hooks[1];
void dispatch(Cpu* c, uint32_t t) { (void)c; (void)t; }
void guest_trap(Cpu* c, uint32_t a, const char* w) { (void)c; (void)a; (void)w; }
void guest_unimpl(Cpu* c, uint32_t a, uint32_t w) { (void)c; (void)a; (void)w; }
void guest_bad_branch(Cpu* c, uint32_t f, uint32_t t) { (void)c; (void)f; (void)t; }
void guest_noreturn(Cpu* c, uint32_t a) { (void)c; (void)a; }
void guest_svc(Cpu* c, uint32_t i, uint32_t a) { (void)c; (void)i; (void)a; }
void guest_yield(Cpu* c) { (void)c; }
uint32_t cp15_read(Cpu* c, int a, int b, int d, int e) { return 0; }
void cp15_write(Cpu* c, int a, int b, int d, int e, uint32_t v) { }
%CASES%
typedef void (*T)(Cpu*);
static T tests[] = { %LIST% };
static const uint32_t words[] = { %WORDS% };
int main(int argc, char** argv) {
    if (!VirtualAlloc((void*)(GUEST_BASE + 0x10000), 0x10000, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)) return 2;
    if (!VirtualAlloc((void*)(GUEST_BASE + 0x1000), 0x1000, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)) return 2;  // code page (pc-relative loads)
    FILE* in = fopen(argv[1], "rb"); FILE* out = fopen(argv[2], "wb");
    for (int k = 0; k < (int)(sizeof tests / sizeof tests[0]); k++) {
        Cpu c; memset(&c, 0, sizeof c);
        uint32_t regs[15], flags, ge; uint64_t v[32];
        fread(regs, 4, 15, in); fread(&flags, 4, 1, in); fread(&ge, 4, 1, in); fread(v, 8, 32, in);
        fread(GPTR(0x10000), 1, 0x10000, in);
        memcpy(c.r, regs, sizeof regs);
        c.n = flags >> 3 & 1; c.z = flags >> 2 & 1; c.cf = flags >> 1 & 1; c.v = flags & 1; c.ge = ge;
        memcpy(c.vr.x, v, sizeof v);
        if (getenv("T_TRACE")) { fprintf(stderr, "case %d ", k); fflush(stderr); }
        memset(GPTR(0x1000), 0, 0x1000); memcpy(GPTR(0x1000), &words[k], 4);
        tests[k](&c);
        flags = c.n << 3 | c.z << 2 | c.cf << 1 | c.v;
        uint32_t fp = c.fn << 3 | c.fz << 2 | c.fc << 1 | c.fv;
        fwrite(c.r, 4, 15, out); fwrite(&flags, 4, 1, out); fwrite(&c.ge, 4, 1, out); fwrite(&fp, 4, 1, out);
        fwrite(c.vr.x, 8, 32, out); fwrite(GPTR(0x10000), 1, 0x10000, out);
    }
    fclose(out);
    return 0;
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--only")
    ap.add_argument("--link", help="linked image dir (image.bin + layout.json), for class game")
    a = ap.parse_args()
    r = random.Random(a.seed)
    ctx = a32.Ctx(None)
    cases = []
    if a.only == "game":
        words = game_words(a.link)
        print(f"{len(words)} distinct VFP/NEON words in the image")
        for w in words[:a.n]:
            ins = a32.decode(CODE, w, ctx, vfp.decode)
            if ins is None or ins.kind != a32.SEQ or not ins.lines:
                continue
            for _ in range(2):
                st = rnd_state(r, "game")
                ref = run_unicorn(w, *st)
                if ref is not None:
                    cases.append(("game", w, ins, st, ref))
                    break
    for cls in ([a.only] if a.only and a.only != "game" else CLASSES[:-1] if not a.only else []):  # game: --only only
        made = 0
        tries = 0
        while made < a.n and tries < a.n * 20:
            tries += 1
            w = gen(cls, r) & 0xFFFFFFFF
            ins = a32.decode(CODE, w, ctx, vfp.decode)
            if ins is None or ins.kind != a32.SEQ or not ins.lines:
                continue
            st = rnd_state(r, cls)
            ref = run_unicorn(w, *st)
            if ref is None:
                continue
            cases.append((cls, w, ins, st, ref))
            made += 1
    tmp = tempfile.mkdtemp(dir=os.path.join(ROOT, "private"))
    src = os.path.join(tmp, "t.c")
    with open(src, "w") as f:
        f.write(HARNESS.replace("%CASES%", "\n".join(c_case(k, x[2]) for k, x in enumerate(cases)))
                .replace("%LIST%", ", ".join(f"T{k}" for k in range(len(cases))))
                .replace("%WORDS%", ", ".join(f"0x{x[1]:08x}u" for x in cases)))
    exe = os.path.join(tmp, "t.exe")
    subprocess.run([CLANG, "-O1", "-w", "-ffp-contract=off", "-fwrapv", "-fno-strict-aliasing",
                    "-I", os.path.join(ROOT, "runtime", "include"), src, "-o", exe], check=True)
    with open(os.path.join(tmp, "in.bin"), "wb") as f:
        for _, _, _, (regs, flags, vregs, mem, ge), _ in cases:
            f.write(struct.pack("<15I", *regs) + struct.pack("<II", flags, ge) + struct.pack("<32Q", *vregs) + mem)
    rc = subprocess.run([exe, os.path.join(tmp, "in.bin"), os.path.join(tmp, "out.bin")]).returncode
    if rc:  # a case crashed: rerun with tracing to name it
        tr = subprocess.run([exe, os.path.join(tmp, "in.bin"), os.path.join(tmp, "out.bin")], capture_output=True, text=True,
                            env={**os.environ, "T_TRACE": "1"})
        k = int(tr.stderr.strip().split()[-1])
        print(f"case {k} crashed: {cases[k][1]:08x} {cases[k][2].text}")
        print(f"  C: {' '.join(cases[k][2].lines)[:400]}")
        regs = cases[k][3][0]
        print("  regs", " ".join(f"{x:#x}" for x in regs))
        sys.exit(1)
    data = open(os.path.join(tmp, "out.bin"), "rb").read()
    rec = 15 * 4 + 12 + 256 + MEMSZ
    bad = {}
    for k, (cls, w, ins, st, ref) in enumerate(cases):
        o = data[k * rec:(k + 1) * rec]
        regs = list(struct.unpack_from("<15I", o, 0))
        flags, ge, fp = struct.unpack_from("<III", o, 60)
        v = list(struct.unpack_from("<32Q", o, 72))
        mem = o[72 + 256:]
        rregs, rflags, rge, rfp, rv, rmem = ref
        diffs = []
        if regs != rregs:
            diffs.append("regs " + ", ".join(f"r{i}={regs[i]:#x} want {rregs[i]:#x}" for i in range(15) if regs[i] != rregs[i]))
        if flags != rflags:
            diffs.append(f"nzcv {flags:04b} want {rflags:04b}")
        if cls == "media" and ge != rge:
            diffs.append(f"ge {ge:04b} want {rge:04b}")
        if cls in ("vfp", "game") and "vcmp" in (ins.text or "") and fp != rfp:
            diffs.append(f"fpscr nzcv {fp:04b} want {rfp:04b}")
        if v != rv:
            for i in range(32):
                if v[i] != rv[i]:
                    # NaN payload / sign of NaN differences are not interesting
                    a_, b_ = struct.unpack("<ff", struct.pack("<Q", v[i])), struct.unpack("<ff", struct.pack("<Q", rv[i]))
                    if all((x != x and y != y) or x == y for x, y in zip(a_, b_)):
                        continue
                    da, db = struct.unpack("<d", struct.pack("<Q", v[i]))[0], struct.unpack("<d", struct.pack("<Q", rv[i]))[0]
                    if da != da and db != db:
                        continue
                    diffs.append(f"d{i}={v[i]:#018x} want {rv[i]:#018x}")
        if mem != rmem:
            diffs.append("memory")
        if diffs:
            bad.setdefault(cls, []).append((w, ins, diffs))
    total = len(cases)
    print(f"{total} cases, {sum(len(x) for x in bad.values())} mismatches")
    for cls in CLASSES:
        n = sum(1 for x in cases if x[0] == cls)
        b = bad.get(cls, [])
        print(f"  {cls:10s} {n:4d} cases, {len(b)} bad")
        if cls == "game":  # one example per mnemonic
            import collections
            byk = collections.OrderedDict()
            for x in b:
                byk.setdefault((x[1].text or "").split()[0], []).append(x)
            for k, xs in byk.items():
                print(f"     {k}: {len(xs)} bad")
            b = [xs[0] for xs in byk.values()]
        for w, ins, d in b[:6 if cls != "game" else 60]:
            print(f"     {w:08x} {ins.text or ''} :: {'; '.join(d)[:300]}")
            print(f"        C: {' '.join(ins.lines)[:300]}")


if __name__ == "__main__":
    main()
