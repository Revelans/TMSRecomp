"""AArch32 static recompiler driver: function discovery, then one C function per guest function.

    python tools/recomp/lift.py <link dir> <out dir> [--stats] [--names FILE]

<link dir> comes from link.py (image.bin + layout.json). Output: f_NNN.c files, funcs.h (prototypes),
table.c (address -> function and hookable-symbol tables). The names file (default: names.txt next to this script) lists
internal functions as `0xADDR name`: they become hookable like exports and also get a probe slot (runtime PROBE_FN /
NX_PROBE observe calls without replacing the function).
"""
import argparse
import collections
import io
import json
import os
import re
import struct
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
import a32  # noqa: E402
import vfp  # noqa: E402

NORETURN = {
    "abort", "exit", "_Exit", "__assert_fail", "__cxa_pure_virtual", "longjmp", "_longjmp", "__stack_chk_fail",
    "_ZN2nn4diag6detail9AbortImplEPKcS3_S3_i", "_ZN2nn4diag6detail9AbortImplEPKcS3_S3_iPKNS_6ResultES3_z",
    "_ZN2nn4diag6detail18OnAssertionFailureENS0_13AssertionTypeEPKcS4_S4_i",
    "_ZN2nn6detail21UnexpectedDefaultImplEPKcS2_i", "__cxa_throw", "__cxa_rethrow", "_Unwind_Resume",
}


class Image:
    def __init__(self, d):
        with open(os.path.join(d, "layout.json")) as f:
            self.L = json.load(f)
        with open(os.path.join(d, "image.bin"), "rb") as f:
            self.img = f.read()
        self.base = self.L["image_base"]
        self.texts = [tuple(m["text"]) for m in self.L["modules"]]

    def word(self, a):
        return struct.unpack_from("<I", self.img, a - self.base)[0]

    def in_text(self, a):
        return any(s <= a < e for s, e in self.texts)

    def text_of(self, a):
        for s, e in self.texts:
            if s <= a < e:
                return s, e
        return None


def exidx_starts(img, mod):
    """prel31 function starts from .ARM.exidx (bounded by MOD0's eh_frame_hdr fields on AArch32)."""
    base = mod["base"]
    # MOD0 is at text+word(text+4)
    mod0 = base + img.word(base + 4)
    eh_s = mod0 + struct.unpack("<i", struct.pack("<I", img.word(mod0 + 16)))[0]
    eh_e = mod0 + struct.unpack("<i", struct.pack("<I", img.word(mod0 + 20)))[0]
    out = []
    for p in range(eh_s, eh_e, 8):
        w0 = img.word(p)
        off = ((w0 & 0x7FFFFFFF) ^ 0x40000000) - 0x40000000
        out.append((p + off) & 0xFFFFFFFF)
    return out


# movw/movt pairs that build the game's 1/30 s frame time: the movt loads the function's own 1/30 literal word instead,
# which the runtime rewrites for 60 fps (runtime/src/hle_sys.cpp DT_LITERALS). TMS #FE Encore 1.0.0 main.
MOVT_LOADS = {0x363318: 0x363358, 0x3f8d38: 0x3f8e64}


class Lifter:
    def __init__(self, img):
        self.img = img
        self.cache = {}
        self.ctx = a32.Ctx(self.read_const, MOVT_LOADS)
        self.unknown = collections.Counter()
        self.vfp_mn = collections.Counter()

    def read_const(self, a):
        # text has no relocations (checked in NOTES), so its words are the same at run time
        return self.img.word(a) if self.img.in_text(a) and self.img.in_text(a + 3) else None

    def decode(self, a):
        ins = self.cache.get(a)
        if ins is None:
            w = self.img.word(a)
            try:
                ins = a32.decode(a, w, self.ctx, self.vfp_decode)
            except Exception as e:  # decoder bug: keep going, report
                ins = None
                self.unknown[f"exc {type(e).__name__}: {e}"] += 1
            if ins is None:
                ins = a32.Insn(a, w, a32.TRAP)
                ins.lines = [f"guest_unimpl(c, 0x{a:08x}u, 0x{w:08x}u);"]
                ins.text = "unknown"
            self.cache[a] = ins
        return ins

    def vfp_decode(self, a, w):
        ins = vfp.decode(a, w)
        if ins is not None:
            self.vfp_mn[ins.text.split()[0] if ins.text else "?"] += 1
        return ins


def pcrel_code_ptrs(img):
    """Function pointers built at run time without a relocation: `ldr rY, [pc, #k]` ... `add rX, pc, rY`."""
    out = set()
    for s, e in img.texts:
        for a in range(s, e, 4):
            w = img.word(a)
            if (w >> 28) == 15 or (w & 0x0FFF0FF0) != 0x008F0000:
                continue
            rm = w & 15
            for b in range(1, 10):
                p = img.word(a - 4 * b)
                if (p & 0x0F7F0000) == 0x051F0000 and ((p >> 12) & 15) == rm and (p >> 28) != 15:
                    off = p & 0xFFF
                    la = a - 4 * b + 8 + (off if p & (1 << 23) else -off)
                    if img.in_text(la):
                        v = (img.word(la) + a + 8) & 0xFFFFFFFF
                        if img.in_text(v) and v % 4 == 0:
                            out.add(v)
                    break
    return out


def discover(lf, roots, names):
    img = lf.img
    noret = {a for a, n in names.items() if n in NORETURN}
    roots = set(r for r in roots if img.in_text(r) and r % 4 == 0)
    funcs = {}
    for it in range(50):
        starts = sorted(roots)
        nxt = {}
        for i, s in enumerate(starts):
            te = img.text_of(s)[1]
            nxt[s] = min(starts[i + 1] if i + 1 < len(starts) else te, te)
        new = set()
        funcs = {}
        for s in starts:
            if s in funcs:
                continue
            end = nxt[s]
            body, labels, data = {}, set(), set()
            work = [s]
            while work:
                a = work.pop()
                while a not in body:
                    if a >= end or a < s:
                        break
                    if a in data:
                        break
                    ins = lf.decode(a)
                    body[a] = ins
                    # literal pool words this instruction reads are data, not code
                    w = ins.word
                    if (w & 0x0F7F0000) == 0x051F0000 and (w >> 28) != 15:  # ldr rt, [pc, #imm]
                        off = w & 0xFFF
                        data.add((a + 8 + (off if w & (1 << 23) else -off)) & ~3)
                    k = ins.kind
                    if k == a32.B:
                        t = ins.target
                        if s <= t < end:
                            labels.add(t)
                            work.append(t)
                        elif img.in_text(t):
                            new.add(t)
                    elif k == a32.BL:
                        if img.in_text(ins.target):
                            new.add(ins.target)
                        if ins.target in noret and ins.cond == 14:
                            break
                    elif k == a32.JTAB:
                        if len(ins.jt) == 3:  # first visit; cached instructions keep their targets
                            kind, idx, base = ins.jt
                            n = jtab_count(lf, body, a)
                            ins.jt = (kind, idx, base, [base + 4 * i for i in range(n)])
                        tg = ins.jt[3]
                        for t in tg:
                            labels.add(t)
                            work.append(t)
                            data.discard(t)
                    elif k == a32.IJMP and (w & 0x0FFFFFF0) == 0x012FFF10:  # bx rX: computed jump inside this function?
                        tg = adr_jump(lf, s, end, a)
                        if tg:
                            ins.kind = a32.JTAB
                            ins.uses_ret0 = True
                            ins.jt = ("addr", f"c->r[{w & 15}]", None, tg)
                            for t in tg:
                                labels.add(t)
                                work.append(t)
                                data.discard(t)
                    elif k == a32.IJMP and (w & 0x0FE0FFF0) == 0x0080F000:  # add pc, rN, rM: relative jump table?
                        tg = rel_table(lf, s, end, a)
                        if tg:
                            ins.kind = a32.JTAB
                            ins.uses_ret0 = True
                            ins.jt = ("addr", f"c->r[{(w >> 16) & 15}] + c->r[{w & 15}]", None, tg)
                            for t in tg:
                                labels.add(t)
                                work.append(t)
                                data.discard(t)
                    if not ins.falls_through:
                        break
                    a += 4
            funcs[s] = (end, body, labels)
        new -= roots
        if not new:
            break
        roots |= new
        print(f"  pass {it}: {len(starts)} functions, +{len(new)} new roots", file=sys.stderr)
    return funcs, noret


def adr_jump(lf, s, end, a):
    """`add rX, pc, #k` ... `bx rX` (compiler-rt's unrolled division jumps backwards into its own body):
    every instruction between the add and its target is a possible landing point."""
    W = lf.img.word
    rx = W(a) & 15
    for back in range(1, 9):
        q = a - 4 * back
        if q < s:
            return None
        qw = W(q)
        if (qw & 0x0FFFF000) == (0x028F0000 | rx << 12) and (qw >> 28) != 15:
            base = (q + 8 + a32.ror(qw & 0xFF, ((qw >> 8) & 15) * 2)) & 0xFFFFFFFF
            if not (s <= base < end):
                return None
            return [t for t in range(a + 4, base + 4, 4)] or None
    return None


def rel_table(lf, s, end, a):
    """clang's relative tables: `add rA, pc, #k` ... `ldr rB, [rA, rX, lsl #2]` ... `add pc, rA, rB`
    (rA may be hoisted out of a loop). Targets are rA + table[i]. Returns the target list or None."""
    W = lf.img.word
    w = W(a)
    rn, rm = (w >> 16) & 15, w & 15
    for back in range(1, 13):  # 0x34720c: the ldr sits 7 before the add pc (6 was too few; artist menu crash)
        p = a - 4 * back
        if p < s:
            return None
        lw = W(p)
        if (lw & 0x0FF00FF0) == 0x07900100 and ((lw >> 12) & 15) in (rn, rm):  # ldr rB, [rA, rX, lsl #2]
            rb, ra, rx = (lw >> 12) & 15, (lw >> 16) & 15, lw & 15
            if {ra, rb} != {rn, rm}:
                return None
            break
    else:
        return None
    base = None
    for q in range(p - 4, max(s, p - 4 * 64) - 4, -4):
        qw = W(q)
        if (qw & 0x0FFFF000) == (0x028F0000 | ra << 12):  # add rA, pc, #imm
            base = (q + 8 + a32.ror(qw & 0xFF, ((qw >> 8) & 15) * 2)) & 0xFFFFFFFF
            break
        if ((qw >> 12) & 15) == ra and (qw >> 28) != 15:
            cls = (qw >> 26) & 3
            is_cmp = cls == 0 and 8 <= ((qw >> 21) & 15) <= 11 and (qw >> 20) & 1
            if (cls == 0 and not is_cmp) or (cls == 1 and (qw >> 20) & 1):
                return None  # rA redefined by something else (data processing or load)
    if base is None:
        return None
    n = table_bound(W, s, end, p, rx)
    out = []
    for i in range(n if n is not None else 512):
        if not lf.img.in_text(base + 4 * i):
            return None
        t = (base + a32.sx(W(base + 4 * i), 32)) & 0xFFFFFFFF
        if not (s <= t < end) or t % 4:
            if n is not None:
                return None
            break
        out.append(t)
    return out or None


def ends_block(w):
    """Unconditional instruction that never falls through (b, bx, pop/ldm or ldr into pc, data processing into pc)."""
    if (w >> 28) != 14:
        return False
    return ((w & 0x0F000000) == 0x0A000000 or (w & 0x0FFFFFF0) == 0x012FFF10 or (w & 0x0E108000) == 0x08108000
            or ((w >> 12) & 15) == 15 and ((w >> 26) & 3 == 0 and not 8 <= (w >> 21) & 15 <= 11
                                           or (w >> 26) & 3 == 1 and (w >> 20) & 1))


def cmp_imm(w, rx):
    """N of `cmp rX, #N`, else None."""
    if (w & 0x0FF0F000) == 0x03500000 and ((w >> 16) & 15) == rx and (w >> 28) != 15:
        return a32.ror(w & 0xFF, ((w >> 8) & 15) * 2)
    return None


def table_bound(W, s, end, p, rx):
    """Entry count of a jump table indexed by rX, dispatched at p: a `cmp rX, #N` in p's own block (N+1); when the block
    is only reached by a branch (the dispatch is hoisted), the `cmp` before a `bls`/`blo` to the block start
    (N+1 / N). None if not found. The backward scan must stop at a block end: a `cmp` before an unconditional branch
    guards some other path (seen: `cmp r0, #4; bls; b` right above a 6-entry table)."""
    q = p - 4
    while q >= max(s, p - 4 * 12):
        qw = W(q)
        if ends_block(qw):
            break
        n = cmp_imm(qw, rx)
        if n is not None:
            return n + 1
        q -= 4
    else:
        return None
    start = q + 4
    for b in range(s, end, 4):
        bw = W(b)
        if (bw & 0x0F000000) != 0x0A000000 or (bw >> 28) not in (3, 9):  # blo / bls
            continue
        if (b + 8 + (a32.sx(bw & 0xFFFFFF, 24) << 2)) & 0xFFFFFFFF != start:
            continue
        for c in range(b - 4, max(s, b - 16) - 4, -4):
            n = cmp_imm(W(c), rx)
            if n is not None:
                return n + 1 if bw >> 28 == 9 else n
    return None


def jtab_count(lf, body, a):
    """Entries of an `add pc, pc, rX, lsl #2` table: from a preceding `cmp rX, #N` (N+1), else scan branches."""
    idx_reg = lf.img.word(a) & 0xF
    for back in range(1, 6):
        p = body.get(a - 4 * back)
        if p is None or ends_block(p.word):
            break
        n = cmp_imm(p.word, idx_reg)
        if n is not None:
            return n + 1
    n = 0
    while n < 1024 and (lf.img.word(a + 8 + 4 * n) & 0x0F000000) == 0x0A000000:
        n += 1
    return n


SETJMP = {"setjmp", "_setjmp", "__setjmp"}


def plt_targets(img, funcs, thunk_lo):
    """PLT stub start -> real target: `add ip, pc, #a; add ip, ip, #b; ldr pc, [ip, #c]!` reads a relocated GOT slot."""
    out = {}
    for s in funcs:
        w0, w1, w2 = img.word(s), img.word(s + 4), img.word(s + 8)
        if (w0 & 0xFFFFF000) != 0xE28FC000 or (w1 & 0xFFFFF000) != 0xE28CC000 or (w2 & 0xFFFFF000) != 0xE5BCF000:
            continue
        got = (s + 8 + a32.ror(w0 & 0xFF, ((w0 >> 8) & 0xF) * 2) + a32.ror(w1 & 0xFF, ((w1 >> 8) & 0xF) * 2)
               + (w2 & 0xFFF)) & 0xFFFFFFFF
        v = img.word(got)
        if v in funcs or v >= thunk_lo:
            out[s] = v
    return out


def cond_wrap(ins, lines):
    if ins.cond == 14 or not lines:
        return lines
    return [f"if ({a32.COND_C[ins.cond]}) {{"] + ["  " + x for x in lines] + ["}"]


def emit_function(lf, s, end, body, labels, funcs, noret, hooks, plt, names, thunk_lo, probes=()):
    out = [f"void F_{s:08x}(Cpu* c) {{"]
    if s in probes:
        out.append(f"  PROBE({hooks[s]});")
    if s in hooks:
        out.append(f"  HOOK({hooks[s]});")
    if any(i.uses_ret0 for i in body.values()):
        out.append("  const uint32_t ret0 = c->r[14];")
    addrs = sorted(body)
    for j, a in enumerate(addrs):
        ins = body[a]
        if a in labels:
            out.append(f"L_{a:08x}:;")
        k = ins.kind
        if k == a32.B:
            t = ins.target
            if t in labels and s <= t < end:
                lines = [f"goto L_{t:08x};"]
            else:
                t = plt.get(t, t)
                if t in funcs:
                    lines = [f"F_{t:08x}(c); return;"]
                elif t >= thunk_lo:
                    lines = [f"dispatch(c, 0x{t:08x}u); return;"]
                else:
                    lines = [f"guest_bad_branch(c, 0x{a:08x}u, 0x{t:08x}u); return;"]
        elif k == a32.BL:
            t = plt.get(ins.target, ins.target)
            if t in funcs and names.get(t) in SETJMP:
                # setjmp returns twice: the host-side jump buffer must live in this (the caller's) frame
                lines = [f"c->r[14] = 0x{a + 4:08x}u;",
                         "{ GuestJmp* j_ = guest_setjmp_slot(c, c->r[0]);",
                         "  if (setjmp(j_->host) == 0) guest_setjmp_save(c, j_); else guest_setjmp_resume(c, j_); }"]
            else:
                if t in funcs:
                    call = f"F_{t:08x}(c);"
                elif t >= thunk_lo:
                    call = f"dispatch(c, 0x{t:08x}u);"
                else:
                    call = f"guest_bad_branch(c, 0x{a:08x}u, 0x{t:08x}u);"
                lines = [f"c->r[14] = 0x{a + 4:08x}u; {call}"]
                if t in noret:
                    lines.append(f"guest_noreturn(c, 0x{a:08x}u); return;")
        elif k == a32.JTAB:
            kind, idx, base, tg = ins.jt
            if kind == "addr":
                cases = " ".join(f"case 0x{t:08x}u: goto L_{t:08x};" for t in sorted(set(tg)))
                lines = [f"{{ uint32_t t = {idx}; switch (t) {{ {cases} default: JUMP(t); }} }}"]
            else:
                cases = " ".join(f"case {i}: goto L_{t:08x};" for i, t in enumerate(tg))
                lines = [f"switch ({idx}) {{ {cases} default: guest_bad_branch(c, 0x{a:08x}u, {base}u + 4 * {idx}); return; }}"]
        else:
            lines = list(ins.lines)
        out += ["  " + x for x in cond_wrap(ins, lines)]
        # falling off the end of this function's code into the next one: tail call it
        if ins.falls_through and (a + 4 not in body):
            if not (k == a32.BL and ins.target in noret and ins.cond == 14):
                n = a + 4
                if n in funcs:
                    out.append(f"  F_{n:08x}(c); return;")
                else:
                    out.append(f"  guest_bad_branch(c, 0x{a:08x}u, 0x{n:08x}u); return;")
    out.append("}")
    return out


REG_REF = re.compile(r"c->r\[(\d+)\]")
# Where the lifted code hands the Cpu to someone else: a guest function, dispatch, a runtime entry (guest_*), JUMP
# (dispatch or return), a return. The static inline helpers of guest.h that take c (add_flags, nz, neon_*, vfp_*,
# excl_*, ...) never touch c->r, so they are not escapes.
ESCAPE = re.compile(r"((?:F_[0-9a-f]{8}\(c\)|dispatch\(c, [^;]*\)|guest_\w+\(c\b[^;]*\));)( return;)?"
                    r"|JUMP\((\w+)\);|\breturn;")


FLAG_REF = re.compile(r"c->(n|z|cf|v)\b")
# helpers that read or write the APSR flags through c besides add_flags / nz: such a function keeps its flags in the Cpu
FLAG_CPU = re.compile(r"\b(?:sh_\w+_c|get_cpsr|set_cpsr)\(c\b")


VREF = re.compile(r"(&?)c->vr\.([fwdx])\[(\d+)\]")
# vector helpers that name registers by number (they reach c->vr themselves): such a function keeps vectors in the Cpu
VEC_CPU = re.compile(r"\bneon_\w+\(c\b|c->vr\.\w+\[[^\]0-9]")
VLOCALS_MAX = 12  # D registers a function may keep locally; more: all stay in the Cpu (copies at every call cost more)


def vec_regs(text):
    """D registers (0-31) the function names, and the ones it may write, or None when vectors must stay in the Cpu.
    S2n/S2n+1 and W2n/W2n+1 are halves of Dn; &c->vr.x[n] (a Q register or a D register seen as lanes, at most 16
    bytes) covers Dn and Dn+1 and counts as a write."""
    if "c->vr" not in text or VEC_CPU.search(text):
        return None
    used, wr = set(), set()
    for m in VREF.finditer(text):
        i = int(m.group(3))
        d = i // 2 if m.group(2) in "fw" else i
        if m.group(1):
            used |= {d, (d + 1) & 31}
            wr |= {d, (d + 1) & 31}
        else:
            used.add(d)
            if re.match(r"\s*(?:[-+*/%&|^]|<<|>>)?=(?!=)", text[m.end():]):
                wr.add(d)
    return (used, wr) if len(used) <= VLOCALS_MAX else None


def reg_locals(lines, k, flags=True, vec=False):
    """Keep the k general registers a function names most in C locals (after Astral Chain Recomp's recomp/regs.py),
    and with flags its N Z C V in a local Flags F (after its recomp/flags.py).

    Every guest store goes through a pointer that may alias the Cpu, so clang reloads c->r[n] and the flags after each
    one. With locals it can keep them in host registers. The Cpu is made current where it escapes: before every call,
    dispatch, runtime entry and return the locals the function writes are stored (spill), and after a call that
    returns all of them are loaded again (reload: no trust in the callee-saved registers, since hooks replace guest
    functions; flags reloaded after a call are dead in AAPCS code, so clang drops those loads). Functions that lift
    setjmp (it returns twice, with registers from the jump buffer) keep every register in the Cpu.
    """
    hdr = 1
    while hdr < len(lines) and lines[hdr].lstrip().startswith(("PROBE(", "HOOK(", "const uint32_t ret0")):
        hdr += 1
    body = lines[hdr:-1]
    text = "\n".join(body)
    if "guest_setjmp" in text:
        return lines
    cnt = collections.Counter(int(m) for m in REG_REF.findall(text))
    regs = sorted(r for r, n in cnt.most_common(k) if n >= 3 and r <= 14)
    fl = flags and FLAG_REF.search(text) is not None and FLAG_CPU.search(text) is None
    vr = vec_regs(text) if vec else None
    if not regs and not fl and not vr:
        return lines
    keep = set(regs)
    text = REG_REF.sub(lambda m: f"r{m.group(1)}" if int(m.group(1)) in keep else m.group(0), text)
    wr = [r for r in regs if re.search(rf"\br{r}\s*(?:[-+*/%&|^]|<<|>>)?=(?!=)|\br{r}\s*(?:\+\+|--)|(?:\+\+|--)r{r}\b", text)]
    spill = "".join(f"c->r[{r}] = r{r}; " for r in wr)
    reload = "".join(f" r{r} = c->r[{r}];" for r in regs)
    decl = ["  uint32_t " + ", ".join(f"r{r} = c->r[{r}]" for r in regs) + ";"] if regs else []
    if fl:
        text = FLAG_REF.sub(r"F.\1", text).replace("add_flags(c, ", "add_flags_f(&F, ").replace("nz(c, ", "nz_f(&F, ")
        spill += "c->n = F.n; c->z = F.z; c->cf = F.cf; c->v = F.v; "
        reload += " F.n = c->n; F.z = c->z; F.cf = c->cf; F.v = c->v;"
        decl.append("  Flags F = {c->n, c->z, c->cf, c->v};")
    if vr:
        used, vw = vr
        text = text.replace("c->vr.", "V.")
        spill += "".join(f"c->vr.x[{d}] = V.x[{d}]; " for d in sorted(vw))
        reload += "".join(f" V.x[{d}] = c->vr.x[{d}];" for d in sorted(used))
        decl.append("  VRegs V; " + " ".join(f"V.x[{d}] = c->vr.x[{d}];" for d in sorted(used)))

    def esc(m):
        if m.group(1):
            return f"{{ {spill}{m.group(1)}{m.group(2)} }}" if m.group(2) else f"{{ {spill}{m.group(1)}{reload} }}"
        if m.group(3):
            return f"{{ {spill}JUMP({m.group(3)}); }}"
        return f"{{ {spill}return; }}"

    text = ESCAPE.sub(esc, text)
    return lines[:hdr] + decl + text.split("\n") + lines[-1:]


class out:
    """Write a generated file only when its text changed, so the build recompiles only the C files a change touched."""

    def __init__(self, path):
        self.path, self.f = path, io.StringIO()

    def __enter__(self):
        return self.f

    def __exit__(self, *exc):
        text = self.f.getvalue()
        if exc[0] is None and (not os.path.exists(self.path) or open(self.path, newline="").read() != text):
            with open(self.path, "w", newline="\n") as f:
                f.write(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("link")
    ap.add_argument("out")
    ap.add_argument("--stats", action="store_true", help="discovery + coverage only, no output")
    ap.add_argument("--file-bytes", type=int, default=3_000_000)
    ap.add_argument("--reg-locals", type=int, default=6, metavar="K",
                    help="keep the K most used general registers of each function in C locals (default 6: Shibuya on one core 118 -> 126 fps with flag locals; 8 was 124; 0 = all in the Cpu)")
    ap.add_argument("--no-flag-locals", action="store_true", help="with --reg-locals: flags stay in the Cpu")
    ap.add_argument("--vec-locals", action="store_true", help="with --reg-locals: VFP / NEON registers in a local too "
                    "(off: no gain measured, s117: Shibuya one core 134.7 both, tutorial battle at the cap)")
    ap.add_argument("--names", default=os.path.join(os.path.dirname(__file__), "names.txt"))
    ap.add_argument("--probe-range", action="append", default=[], metavar="LO:HI",
                    help="give every function in [LO, HI) a probe slot (named fn_XXXXXXXX), for NX_COVER")
    a = ap.parse_args()
    t0 = time.time()
    img = Image(a.link)
    lf = Lifter(img)
    names = {}  # addr -> symbol (exports of all modules)
    aliases = []  # every (name, addr) export
    roots = set()
    for m in img.L["modules"]:
        roots |= set(exidx_starts(img, m))
        for nm, ad in sorted(m["exports"].items()):
            names.setdefault(ad, nm)
            aliases.append((nm, ad))
            roots.add(ad)
    probes = set()  # internal functions named in the names file
    if os.path.exists(a.names):
        for line in open(a.names):
            f = line.split("#")[0].split()
            if len(f) >= 2:
                ad = int(f[0], 16)
                names.setdefault(ad, f[1])
                aliases.append((f[1], ad))
                roots.add(ad)
                probes.add(ad)
        if m["init"]:
            roots.add(m["init"])
        ia = m["init_array"]
        if ia:
            for p in range(ia[0], ia[0] + ia[1], 4):
                roots.add(img.word(p))
    # code pointers stored in data (vtables, callbacks): every relocated word that lands in text
    roots |= set(img.L["code_ptrs"])
    roots |= pcrel_code_ptrs(img)
    print(f"roots {len(roots)}", file=sys.stderr)
    funcs, noret = discover(lf, roots, names)
    for r in a.probe_range:
        rlo, rhi = (int(x, 16) for x in r.split(":"))
        for ad in funcs:
            if rlo <= ad < rhi and ad not in names:
                names[ad] = f"fn_{ad:08x}"
                aliases.append((names[ad], ad))
                probes.add(ad)
    ninsn = sum(len(b) for _, b, _ in funcs.values())
    print(f"functions {len(funcs)}, instructions {ninsn}, {time.time() - t0:.0f}s", file=sys.stderr)
    traps = collections.Counter()
    for s, (e, body, _) in funcs.items():
        for ins in body.values():
            if ins.text == "unknown":
                traps[f"{ins.word:08x}"[:3]] += 1
    print("unknown words by top bits:", traps.most_common(30), file=sys.stderr)
    print("unhandled vfp/neon:", vfp.UNHANDLED.most_common(60), file=sys.stderr)
    print("decoder exceptions:", lf.unknown.most_common(10), file=sys.stderr)
    if a.stats:
        return
    thunk_lo = min(img.L["thunks"].values()) if img.L["thunks"] else 0xFFFFFFFF
    plt = plt_targets(img, funcs, thunk_lo)
    print(f"plt stubs resolved: {len(plt)}", file=sys.stderr)
    # hookable functions: every exported function (runtime may replace any of them), plus import thunks
    hooks = {}
    hook_names = []
    for ad, nm in sorted(names.items()):
        if ad in funcs:
            hooks[ad] = len(hook_names)
            hook_names.append((nm, ad))
    os.makedirs(a.out, exist_ok=True)
    starts = sorted(funcs)
    with out(os.path.join(a.out, "funcs.h")) as f:
        f.write("#pragma once\n#include \"guest.h\"\n")
        for s in starts:
            f.write(f"void F_{s:08x}(Cpu* c);\n")
    files = []
    buf, size, idx = [], 0, 0

    def flush():
        nonlocal buf, size, idx
        if not buf:
            return
        fn = f"f_{idx:03d}.c"
        with out(os.path.join(a.out, fn)) as f:
            f.write("#include \"funcs.h\"\n\n")
            f.write("\n".join(buf))
            f.write("\n")
        files.append(fn)
        buf, size, idx = [], 0, idx + 1

    for s in starts:
        e, body, labels = funcs[s]
        lines = emit_function(lf, s, e, body, labels, funcs, noret, hooks, plt, names, thunk_lo, probes)
        if a.reg_locals:
            lines = reg_locals(lines, a.reg_locals, not a.no_flag_locals, a.vec_locals)
        buf += lines + [""]
        size += sum(len(x) for x in lines)
        if size >= a.file_bytes:
            flush()
    flush()
    with out(os.path.join(a.out, "table.c")) as f:
        f.write("#include \"funcs.h\"\n\nconst GuestFunc g_guest_funcs[] = {\n")
        for s in starts:
            f.write(f"  {{0x{s:08x}u, F_{s:08x}}},\n")
        f.write("};\nconst uint32_t g_guest_func_count = sizeof(g_guest_funcs) / sizeof(g_guest_funcs[0]);\n\n")
        f.write("const GuestHookName g_hook_names[] = {\n")
        for nm, ad in hook_names:
            f.write(f"  {{\"{nm}\", 0x{ad:08x}u}},\n")
        f.write("};\nconst uint32_t g_hook_count = sizeof(g_hook_names) / sizeof(g_hook_names[0]);\n")
        f.write(f"GuestFn g_hooks[{max(1, len(hook_names))}];\n\n")
        f.write(f"GuestFn g_probes[{max(1, len(hook_names))}];\n\n")
        f.write("const GuestHookName g_hook_aliases[] = {\n")
        for nm, ad in aliases:
            if ad in hooks:
                f.write(f"  {{\"{nm}\", 0x{ad:08x}u}},\n")
        f.write("};\nconst uint32_t g_hook_alias_count = sizeof(g_hook_aliases) / sizeof(g_hook_aliases[0]);\n\n")
        f.write("const GuestHookName g_thunks[] = {\n")
        for nm, ad in sorted(img.L["thunks"].items(), key=lambda x: x[1]):
            f.write(f"  {{\"{nm}\", 0x{ad:08x}u}},\n")
        f.write("  {0, 0}\n};\n")
        f.write(f"const uint32_t g_thunk_count = {len(img.L['thunks'])};\n\n")
        f.write("const GuestModule g_modules[] = {\n")
        for m in img.L["modules"]:
            vals = [m["base"], m["size"], *m["text"], *m["ro"], *m["data"], m["init"] or 0]
            f.write(f"  {{\"{m['name']}\", " + ", ".join(f"0x{v:08x}u" for v in vals) + "},\n")
        f.write("};\n")
        f.write(f"const uint32_t g_module_count = {len(img.L['modules'])};\n")
        f.write(f"const uint32_t g_image_size = 0x{img.L['image_size']:08x}u;\n")
    with out(os.path.join(a.out, "files.txt")) as f:
        f.write("\n".join(files + ["table.c"]) + "\n")
    print(f"wrote {len(files)} files, {len(hook_names)} hooks, {time.time() - t0:.0f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
