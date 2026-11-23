"""VFP / NEON / ARMv8-AArch32 FP instructions -> C.

Operands come from Capstone, except NEON element loads/stores (VLDn/VSTn), decoded from the encoding here.
Register file in C: c->v (union): .f[n]/.w[n] = Sn, .d[n]/.x[n] = Dn, Qn = D(2n), D(2n+1).
Unknown forms return None (the lifter emits guest_unimpl, reported at run time and in the stats).
"""
import collections

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone import arm as A

import a32

_md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
_md.detail = True
UNHANDLED = collections.Counter()

CT = {"i8": "uint8_t", "u8": "uint8_t", "s8": "int8_t", "8": "uint8_t", "p8": "uint8_t",
      "i16": "uint16_t", "u16": "uint16_t", "s16": "int16_t", "16": "uint16_t",
      "i32": "uint32_t", "u32": "uint32_t", "s32": "int32_t", "32": "uint32_t", "f32": "float",
      "i64": "uint64_t", "u64": "uint64_t", "s64": "int64_t", "64": "uint64_t", "f64": "double"}
SIZE = {"uint8_t": 1, "int8_t": 1, "uint16_t": 2, "int16_t": 2, "uint32_t": 4, "int32_t": 4, "float": 4,
        "uint64_t": 8, "int64_t": 8, "double": 8}
WIDER = {"uint8_t": "uint16_t", "int8_t": "int16_t", "uint16_t": "uint32_t", "int16_t": "int32_t",
         "uint32_t": "uint64_t", "int32_t": "int64_t"}
NARROW = {v: k for k, v in WIDER.items()}
UNS = {"int8_t": "uint8_t", "int16_t": "uint16_t", "int32_t": "uint32_t", "int64_t": "uint64_t"}
SGN = {v: k for k, v in UNS.items()}
GPR = {"sb": 9, "sl": 10, "fp": 11, "ip": 12, "sp": 13, "lr": 14, "pc": 15}


class R:
    """A register operand: kind in s/d/q/r, index n (d index for q), lane or None."""

    def __init__(self, name, lane=None):
        self.k = name[0] if name[0] in "sdq" and name[1:].isdigit() else "r"
        if self.k == "r":
            self.n = GPR.get(name, int(name[1:]) if name[1:].isdigit() else -1)
        else:
            self.n = int(name[1:]) * (2 if name[0] == "q" else 1)
        self.lane = lane
        self.name = name

    @property
    def nbytes(self):
        return {"s": 4, "d": 8, "q": 16, "r": 4}[self.k]

    def f(self):  # scalar float view
        return f"c->vr.f[{self.n}]" if self.k == "s" else f"c->vr.d[{self.n}]"

    def bits(self):
        return f"c->vr.w[{self.n}]" if self.k == "s" else f"c->vr.x[{self.n}]"

    def g(self, pc_addr):
        return f"0x{pc_addr:08x}u" if self.n == 15 else f"c->r[{self.n}]"

    def lanes(self, t):
        return f"(({t}*)&c->vr.x[{self.n}])"


def ops_of(i):
    out = []
    for o in i.operands:
        if o.type == A.ARM_OP_REG:
            vi = o.vector_index if o.vector_index != -1 else None
            out.append(R(i.reg_name(o.reg), vi))
        elif o.type == A.ARM_OP_IMM:
            out.append(("imm", o.imm & 0xFFFFFFFF))
        elif o.type == A.ARM_OP_FP:
            out.append(("fp", o.fp))
        elif o.type == A.ARM_OP_MEM:
            out.append(("mem", i.reg_name(o.mem.base), o.mem.disp, o.subtracted))
        else:
            out.append(("other", o.type))
    return out


def decode(addr, w):
    if (w >> 24) == 0xF4:  # NEON element/structure load-store
        return neon_ldst(addr, w)
    i = next(_md.disasm(w.to_bytes(4, "little"), addr), None)
    if i is None:
        UNHANDLED["<capstone fail>"] += 1
        return None
    mn = i.mnemonic
    base = i.insn_name()
    dt = mn.split(".", 1)[1] if "." in mn else ""
    try:
        lines = emit(i, base, dt, ops_of(i), addr, w)
    except (KeyError, IndexError, ValueError, AttributeError, TypeError) as e:
        lines = None
    if lines is None:
        UNHANDLED[f"{base}.{dt}" if dt else base] += 1
        return None
    ins = a32.Insn(addr, w, text=f"{mn} {i.op_str}")
    ins.lines = lines
    return ins


# ----------------------------------------------------------------------------------------------------- scalar

def fbin(op):
    return lambda d, a, b: f"{d.f()} = {a.f()} {op} {b.f()};"


def is_dbl(dt):
    return dt.endswith("f64") or dt == "f64"


def emit(i, base, dt, o, addr, w):
    vec = any(isinstance(x, R) and x.k == "q" for x in o) or (
        any(isinstance(x, R) and x.k == "d" for x in o) and not dt.startswith("f64") and base not in SCALAR_D_OK)
    if base in ("vldr", "vstr"):
        r, (_, rb, disp, sub) = o[0], o[1]
        rbn = GPR.get(rb, int(rb[1:]) if rb[1:].isdigit() else 0)
        pc = (addr + 8) & ~3
        a = f"0x{(pc + (-disp if sub else disp)) & 0xFFFFFFFF:08x}u" if rbn == 15 else \
            (f"(c->r[{rbn}] {'-' if sub else '+'} {disp}u)" if disp else f"c->r[{rbn}]")
        sz = "32" if r.k == "s" else "64"
        if base == "vldr":
            return [f"{r.bits()} = ld{sz}({a});"]
        return [f"st{sz}({a}, {r.bits()});"]
    if base in ("vpush", "vpop", "vldmia", "vldmdb", "vstmia", "vstmdb"):
        return vldm(i, base, o, w)
    if base in ("fconsts", "fconstd"):  # vmov.f32/.f64 #imm: VFPExpandImm(imm8)
        import struct
        imm8 = ((w >> 16) & 0xF) << 4 | (w & 0xF)
        a, b, rest = imm8 >> 7, (imm8 >> 6) & 1, imm8 & 0x3F
        if base == "fconsts":
            bits32 = (a << 31) | ((b ^ 1) << 30) | ((0x1F if b else 0) << 25) | (rest << 19)
            v = struct.unpack("<f", struct.pack("<I", bits32))[0]
            return [f"{o[0].f()} = {v!r}f;"]
        bits64 = (a << 63) | ((b ^ 1) << 62) | ((0xFF if b else 0) << 54) | (rest << 48)
        v = struct.unpack("<d", struct.pack("<Q", bits64))[0]
        return [f"{o[0].f()} = {v!r};"]
    if base == "fmstat":
        return ["c->n = c->fn; c->z = c->fz; c->cf = c->fc; c->v = c->fv;"]
    # vmov.32 dN[x], rT / rT, dN[x]: the word comes from the encoding (bit 21); Capstone's fmdhr/fmdlr (and
    # fmrdh/fmrdl) names are unreliable (measured: vmov.32 d0[0], r0 = ee000b10 came back as fmdhr)
    if base in ("fmdhr", "fmdlr"):
        d, r = o[0], o[1]
        return [f"((uint32_t*)&c->vr.x[{d.n}])[{scalar_lane(w)}] = c->r[{r.n}];"]
    if base in ("fmrdh", "fmrdl"):
        r, d = o[0], o[1]
        return [f"c->r[{r.n}] = ((uint32_t*)&c->vr.x[{d.n}])[{scalar_lane(w)}];"]
    if base == "vmvn" and any(isinstance(x, tuple) and x[0] == "imm" for x in o):
        imm = next(x[1] for x in o if isinstance(x, tuple) and x[0] == "imm")
        return vec_imm(o[0], dt, ~imm)
    if base == "vmrs":
        if o[0].name == "apsr_nzcv":
            return ["c->n = c->fn; c->z = c->fz; c->cf = c->fc; c->v = c->fv;"]
        return [f"c->r[{o[0].n}] = get_fpscr(c);"]
    if base == "vmsr":
        return [f"set_fpscr(c, c->r[{o[1].n}]);"]
    if base in ("vcmp", "vcmpe"):
        a = o[0]
        b = "0.0" if len(o) < 2 or not isinstance(o[1], R) else o[1].f()
        fn = "vfp_cmp_d" if is_dbl(dt) else "vfp_cmp_f"
        return [f"{fn}(c, {a.f()}, {b});"]
    if base == "vsel" or base.startswith("vsel"):
        cc = {"vseleq": "c->z", "vselge": "(c->n == c->v)", "vselgt": "(!c->z && c->n == c->v)", "vselvs": "c->v"}[
            base if base != "vsel" else i.mnemonic.split(".")[0]]
        d, n, m = o
        return [f"{d.f()} = {cc} ? {n.f()} : {m.f()};"]
    if base in ("vmaxnm", "vminnm") and not vec:
        d, n, m = o
        fn = ("fmax" if base == "vmaxnm" else "fmin") + ("" if is_dbl(dt) else "f")
        return [f"{d.f()} = {fn}({n.f()}, {m.f()});"]
    if base.startswith("vrint") and not vec:
        d, m = o
        mode = base[5:] or "r"
        suf = "" if is_dbl(dt) else "f"
        fn = {"m": "floor", "p": "ceil", "a": "round", "z": "trunc", "n": "nearbyint_even", "r": "rint", "x": "rint"}[mode]
        if fn == "nearbyint_even":
            return [f"{d.f()} = round_even{suf}({m.f()});"]
        return [f"{d.f()} = {fn}{suf}({m.f()});"]
    if base == "vmov":
        return vmov(i, dt, o, vec)
    if base == "vcvt" or base in ("vcvta", "vcvtn", "vcvtp", "vcvtm", "vcvtr"):
        dregs = any(isinstance(x, R) and x.k in "dq" for x in o)
        return vcvt(base, dt, o, dregs and "f64" not in dt)
    if not vec:
        return scalar_arith(base, dt, o)
    return neon(i, base, dt, o, w)


SCALAR_D_OK = {"vldr", "vstr", "vmov", "vcmp", "vcmpe", "vcvt", "vpush", "vpop", "vldmia", "vldmdb", "vstmia",
               "vstmdb", "vmrs", "vmsr", "vsel", "vseleq", "vselge", "vselgt", "vselvs"}


def scalar_arith(base, dt, o):
    if base in ("vadd", "vsub", "vmul", "vdiv"):
        d, a, b = o
        return [fbin({"vadd": "+", "vsub": "-", "vmul": "*", "vdiv": "/"}[base])(d, a, b)]
    if base in ("vmla", "vmls", "vnmla", "vnmls", "vnmul"):
        d, a, b = o
        p = f"({a.f()} * {b.f()})"
        e = {"vmla": f"{d.f()} + {p}", "vmls": f"{d.f()} - {p}", "vnmla": f"-{d.f()} - {p}",
             "vnmls": f"-{d.f()} + {p}", "vnmul": f"-{p}"}[base]
        return [f"{d.f()} = {e};"]
    if base in ("vfma", "vfms", "vfnma", "vfnms"):
        d, a, b = o
        f = "fma" if is_dbl(dt) else "fmaf"
        e = {"vfma": f"{f}({a.f()}, {b.f()}, {d.f()})", "vfms": f"{f}(-{a.f()}, {b.f()}, {d.f()})",
             "vfnma": f"{f}(-{a.f()}, {b.f()}, -{d.f()})", "vfnms": f"{f}({a.f()}, {b.f()}, -{d.f()})"}[base]
        return [f"{d.f()} = {e};"]
    if base in ("vneg", "vabs", "vsqrt"):
        d, a = o
        suf = "" if is_dbl(dt) else "f"
        e = {"vneg": f"-{a.f()}", "vabs": f"fabs{suf}({a.f()})", "vsqrt": f"sqrt{suf}({a.f()})"}[base]
        return [f"{d.f()} = {e};"]
    return None


def vldm(i, base, o, w):
    regs = [x for x in o if isinstance(x, R) and x.k in "sd"]
    if base in ("vpush", "vpop"):
        rn, wb = 13, True
        db = base == "vpush"
        load = base == "vpop"
    else:
        rn = o[0].n
        wb = i.writeback
        db = base.endswith("db")
        load = base.startswith("vld")
    sz = regs[0].nbytes
    total = sz * len(regs)
    lines = [f"{{ uint32_t a = c->r[{rn}]{f' - {total}u' if db else ''};"]
    for k, r in enumerate(regs):
        b = "32" if sz == 4 else "64"
        if load:
            lines.append(f"{r.bits()} = ld{b}(a + {k * sz});")
        else:
            lines.append(f"st{b}(a + {k * sz}, {r.bits()});")
    if wb:
        lines.append(f"c->r[{rn}] {'-' if db else '+'}= {total}u;")
    lines.append("}")
    return lines


def scalar_lane(w):
    """Lane of VMOV core <-> scalar from the encoding (opc1 = bits 22:21, opc2 = bits 6:5). Measured: Capstone's
    vector_index is wrong for these (vmov.32 d0[0], r0 came back as lane 1)."""
    opc1, opc2 = (w >> 21) & 3, (w >> 5) & 3
    if opc1 & 2:
        return (opc1 & 1) << 2 | opc2  # 8-bit
    if opc2 & 1:
        return (opc1 & 1) << 1 | opc2 >> 1  # 16-bit
    return opc1 & 1  # 32-bit


def vmov(i, dt, o, vec):
    w = i.bytes
    enc = int.from_bytes(w, "little")
    if len(o) == 2:
        d, s = o
        if isinstance(s, tuple):  # immediate
            if s[0] == "fp":
                if d.k == "s":
                    return [f"{d.f()} = {float(s[1])!r}f;"]
                if d.k == "d" and dt in ("f64",):
                    return [f"{d.f()} = {float(s[1])!r};"]
                return vec_imm(d, dt, s[1])
            return vec_imm(d, dt, s[1])
        if d.k == "r" and s.k == "s":
            return [f"c->r[{d.n}] = {s.bits()};"]
        if d.k == "s" and s.k == "r":
            return [f"{d.bits()} = c->r[{s.n}];"]
        if d.k == "s" and s.k == "s":
            return [f"{d.bits()} = {s.bits()};"]
        if d.k == "d" and s.k == "d" and d.lane is None and s.lane is None:
            return [f"{d.bits()} = {s.bits()};"]
        if d.k == "q" and s.k == "q":
            return [f"c->vr.x[{d.n}] = c->vr.x[{s.n}]; c->vr.x[{d.n + 1}] = c->vr.x[{s.n + 1}];"]
        if d.k == "r" and s.k == "d" and s.lane is not None:  # vmov.32/u16/s8 rN, dM[x]
            t = CT[dt] if dt else "uint32_t"
            ln = scalar_lane(enc)
            return [f"c->r[{d.n}] = (uint32_t)(int32_t){s.lanes(t)}[{ln}];" if t.startswith("int") else
                    f"c->r[{d.n}] = (uint32_t){s.lanes(t)}[{ln}];"]
        if d.k == "d" and d.lane is not None and s.k == "r":  # vmov.32 dM[x], rN
            t = CT[dt] if dt else "uint32_t"
            return [f"{d.lanes(t)}[{scalar_lane(enc)}] = ({t})c->r[{s.n}];"]
        return None
    if len(o) == 3:
        a, b, cc = o
        if a.k == "r" and b.k == "r" and cc.k == "d":  # vmov rA, rB, dM
            return [f"c->r[{a.n}] = (uint32_t){cc.bits()}; c->r[{b.n}] = (uint32_t)({cc.bits()} >> 32);"]
        if a.k == "d" and b.k == "r" and cc.k == "r":
            return [f"{a.bits()} = ((uint64_t)c->r[{cc.n}] << 32) | c->r[{b.n}];"]
        return None
    if len(o) == 4:
        a, b, cc, d = o
        if a.k == "r" and b.k == "r":  # vmov rA, rB, sM, sM+1
            return [f"c->r[{a.n}] = {cc.bits()}; c->r[{b.n}] = {d.bits()};"]
        return [f"{a.bits()} = c->r[{cc.n}]; {b.bits()} = c->r[{d.n}];"]
    return None


def vec_imm(d, dt, imm):
    """vmov/vmvn immediate into a d/q register: Capstone gives the expanded element value."""
    t = CT.get(dt, "uint32_t")
    if dt == "f32":
        import struct
        imm = struct.unpack("<I", struct.pack("<f", float(imm)))[0] if isinstance(imm, float) else imm
        t = "uint32_t"
    n = d.nbytes // SIZE[t]
    v = f"({t})0x{int(imm) & ((1 << (8 * SIZE[t])) - 1):x}u"
    return [f"{{ {t}* p_ = {d.lanes(t)}; for (int k = 0; k < {n}; k++) p_[k] = {v}; }}"]


def vcvt(base, dt, o, vec):
    if vec:
        return neon_cvt(base, dt, o)
    to, frm = dt.split(".")
    d, s = o[0], o[1]
    fbits = o[2][1] if len(o) > 2 and isinstance(o[2], tuple) else None
    if fbits is not None:  # fixed point, same register
        if to in ("f32", "f64"):
            src = f"(int32_t){s.bits()}" if frm.startswith("s") else f"{s.bits()}"
            if frm.endswith("16"):
                src = f"(int16_t){s.bits()}" if frm.startswith("s") else f"(uint16_t){s.bits()}"
            return [f"{d.f()} = ({'double' if to == 'f64' else 'float'}){src} / {float(1 << fbits)!r};"]
        fn = f"cvt_{'d' if frm == 'f64' else 'f'}2{to[0]}32"
        return [f"{d.bits()} = (uint32_t){fn}({s.f()} * {float(1 << fbits)!r});"]
    if to in ("f32", "f64") and frm in ("s32", "u32"):
        src = f"(int32_t){s.bits()}" if frm == "s32" else s.bits()
        return [f"{d.f()} = ({'double' if to == 'f64' else 'float'}){src};"]
    if to == "f64" and frm == "f32":
        return [f"{d.f()} = (double){s.f()};"]
    if to == "f32" and frm == "f64":
        return [f"{d.f()} = (float){s.f()};"]
    if to in ("s32", "u32") and frm in ("f32", "f64"):
        k = "d" if frm == "f64" else "f"
        mode = {"vcvt": "", "vcvtr": "_r", "vcvta": "_a", "vcvtn": "_n", "vcvtp": "_p", "vcvtm": "_m"}[base]
        return [f"{d.bits()} = (uint32_t)vcvt_{k}2{to[0]}32{mode}(c, {s.f()});"]
    if to == "f32" and frm == "f16":
        return None
    return None


# ----------------------------------------------------------------------------------------------------- NEON

def vloop(d, t, n, expr_fn, srcs, out_t=None):
    """Generic lane loop: r_[k] = expr(k) for k < n, then copy to d. srcs: list of (name, R, type)."""
    out_t = out_t or t
    decl = " ".join(f"const {st}* {nm} = {r.lanes(st)};" for nm, r, st in srcs)
    return [f"{{ {out_t} r_[{n}]; {decl} for (int k = 0; k < {n}; k++) r_[k] = {expr_fn('k')}; "
            f"memcpy(&c->vr.x[{d.n}], r_, sizeof r_); }}"]


def lane_or_k(r, nm, k):
    return f"{nm}[{r.lane}]" if r.lane is not None else f"{nm}[{k}]"


def neon(i, base, dt, o, w):
    regs = [x for x in o if isinstance(x, R)]
    d = regs[0]
    t = CT.get(dt.split(".")[0], "uint32_t") if dt else "uint64_t"
    n = d.nbytes // SIZE[t]
    imm = next((x[1] for x in o if isinstance(x, tuple) and x[0] == "imm"), None)
    if base in ("vadd", "vsub", "vmul", "vand", "vorr", "veor", "vbic", "vorn", "vmax", "vmin", "vqadd", "vqsub",
                "vmla", "vmls", "vtst", "vceq", "vcge", "vcgt", "vcle", "vclt", "vrecps", "vrsqrts", "vabd", "vshl",
                "vrshl", "vhadd", "vrhadd") and len(regs) == 3:
        a, b = regs[1], regs[2]
        bt = t
        if base in ("vand", "vorr", "veor", "vbic", "vorn"):
            t = bt = "uint64_t"
            n = d.nbytes // 8
        A_, B_, D_ = lane_or_k(a, "a_", "k"), lane_or_k(b, "b_", "k"), "d_[k]"
        mt = "uint32_t" if t == "float" else UNS.get(t, t)
        e = {"vadd": f"({t})({A_} + {B_})", "vsub": f"({t})({A_} - {B_})", "vmul": f"({t})({A_} * {B_})",
             "vand": f"{A_} & {B_}", "vorr": f"{A_} | {B_}", "veor": f"{A_} ^ {B_}", "vbic": f"{A_} & ~{B_}",
             "vorn": f"{A_} | ~{B_}",
             "vmax": (f"fmaxf_arm({A_}, {B_})" if t == "float" else f"({A_} > {B_} ? {A_} : {B_})"),
             "vmin": (f"fminf_arm({A_}, {B_})" if t == "float" else f"({A_} < {B_} ? {A_} : {B_})"),
             "vqadd": f"sat_add_{t}({A_}, {B_})", "vqsub": f"sat_sub_{t}({A_}, {B_})",
             "vmla": f"({t})({D_} + {A_} * {B_})", "vmls": f"({t})({D_} - {A_} * {B_})",
             "vabd": (f"fabsf({A_} - {B_})" if t == "float" else f"({t})({A_} > {B_} ? {A_} - {B_} : {B_} - {A_})"),
             "vhadd": f"({t})(((int64_t){A_} + {B_}) >> 1)", "vrhadd": f"({t})(((int64_t){A_} + {B_} + 1) >> 1)",
             "vtst": f"({mt})(({mt}){A_} & ({mt}){B_} ? -1 : 0)",
             "vceq": f"({mt})({A_} == {B_} ? -1 : 0)", "vcge": f"({mt})({A_} >= {B_} ? -1 : 0)",
             "vcgt": f"({mt})({A_} > {B_} ? -1 : 0)", "vcle": f"({mt})({A_} <= {B_} ? -1 : 0)",
             "vclt": f"({mt})({A_} < {B_} ? -1 : 0)",
             "vrecps": f"(2.0f - {A_} * {B_})", "vrsqrts": f"((3.0f - {A_} * {B_}) * 0.5f)",
             "vshl": f"neon_shl_{t}({A_}, (int8_t){B_})", "vrshl": f"neon_rshl_{t}({A_}, (int8_t){B_})"}[base]
        if base in ("vceq", "vcge", "vcgt", "vcle", "vclt", "vtst"):
            out = mt
        else:
            out = t
        srcs = [("a_", a, t), ("b_", b, t)]
        if base in ("vmla", "vmls"):
            srcs.append(("d_", d, t))
        return vloop(d, t, n, lambda k: e, srcs, out)
    if base in ("vbsl", "vbit", "vbif"):
        a, b = regs[1], regs[2]
        n = d.nbytes // 8
        e = {"vbsl": "(d_[k] & a_[k]) | (~d_[k] & b_[k])", "vbit": "(a_[k] & b_[k]) | (d_[k] & ~b_[k])",
             "vbif": "(d_[k] & b_[k]) | (a_[k] & ~b_[k])"}[base]
        return vloop(d, "uint64_t", n, lambda k: e, [("a_", a, "uint64_t"), ("b_", b, "uint64_t"), ("d_", d, "uint64_t")])
    if base in ("vceq", "vcge", "vcgt", "vcle", "vclt") and len(regs) == 2:  # compare with #0
        a = regs[1]
        mt = UNS.get(t, t) if t != "float" else "uint32_t"
        op = {"vceq": "==", "vcge": ">=", "vcgt": ">", "vcle": "<=", "vclt": "<"}[base]
        return vloop(d, t, n, lambda k: f"({mt})(a_[k] {op} 0 ? -1 : 0)", [("a_", a, t)], mt)
    if base in ("vneg", "vabs", "vmvn", "vcnt", "vrecpe", "vrsqrte", "vqabs", "vqneg") and len(regs) == 2:
        a = regs[1]
        if base == "vmvn":
            t, n = "uint64_t", d.nbytes // 8
        e = {"vneg": f"({t})-a_[k]", "vabs": (f"fabsf(a_[k])" if t == "float" else f"({t})(a_[k] < 0 ? -a_[k] : a_[k])"),
             "vmvn": "~a_[k]", "vcnt": "(uint8_t)__builtin_popcount(a_[k])",
             "vrecpe": "recip_est(a_[k])", "vrsqrte": "rsqrt_est(a_[k])",
             "vqabs": f"sat_abs_{t}(a_[k])", "vqneg": f"sat_neg_{t}(a_[k])"}[base]
        return vloop(d, t, n, lambda k: e, [("a_", a, t)])
    if base == "vdup":
        s = regs[1]
        if s.k == "r":
            return vloop(d, t, n, lambda k: f"({t})c->r[{s.n}]", [])
        return [f"{{ {t} v_ = {s.lanes(t)}[{s.lane}]; {t}* p_ = {d.lanes(t)}; for (int k = 0; k < {n}; k++) p_[k] = v_; }}"]
    if base in ("vshl", "vshr", "vsra", "vrshr", "vrsra", "vsli", "vsri") and imm is not None:
        a = regs[1]
        bitsz = 8 * SIZE[t]
        if base == "vshl":
            e = f"({t})(a_[k] << {imm})" if imm < bitsz else "0"
        elif base in ("vshr", "vsra"):
            e = f"({t})(a_[k] >> {min(imm, bitsz - 1) if t.startswith('int') else imm})" if imm < bitsz or t.startswith('int') else "0"
            if base == "vsra":
                e = f"({t})(d_[k] + {e})"
        elif base in ("vrshr", "vrsra"):
            e = f"({t})(((int64_t)a_[k] + ((int64_t)1 << {imm - 1})) >> {imm})" if t.startswith("int") else \
                f"({t})(((uint64_t)a_[k] + ((uint64_t)1 << {imm - 1})) >> {imm})"
            if base == "vrsra":
                e = f"({t})(d_[k] + {e})"
        elif base == "vsli":
            m = ((1 << bitsz) - 1) << imm & ((1 << bitsz) - 1)
            e = f"({t})((a_[k] << {imm}) | (d_[k] & ~({t})0x{m:x}u))"
        else:
            m = ((1 << bitsz) - 1) >> imm
            e = f"({t})((a_[k] >> {imm}) | (d_[k] & ~({t})0x{m:x}u))"
        srcs = [("a_", a, t)] + ([("d_", d, t)] if base in ("vsra", "vrsra", "vsli", "vsri") else [])
        return vloop(d, t, n, lambda k: e, srcs)
    if base in ("vmovl", "vshll"):
        a = regs[1]
        wt = WIDER[t] if t in WIDER else None
        nn = 16 // SIZE[wt]
        sh = imm or 0
        return vloop(d, wt, nn, lambda k: f"({wt})((({wt})a_[k]) << {sh})", [("a_", a, t)])
    if base in ("vmovn", "vqmovn", "vqmovun", "vshrn", "vrshrn", "vqshrn", "vqrshrn", "vqshrun", "vqrshrun"):
        a = regs[1]
        # dt is the source element type (i16 -> result i8) for vmovn/vshrn; for vq* forms it is the source too
        st = t
        if st in ("uint8_t", "int8_t"):
            return None
        nt = NARROW[st]
        nn = 8 // SIZE[nt]
        sh = imm or 0
        if base.startswith("vr") or base.startswith("vqr"):
            src = f"(((int64_t)a_[k] + ((int64_t)1 << {sh - 1})) >> {sh})" if sh else "a_[k]"
        else:
            src = f"((int64_t)a_[k] >> {sh})" if sh else "a_[k]"
        if base.startswith("vq"):
            out = UNS[nt] if base.endswith("un") and nt in UNS else nt
            e = f"sat_narrow_{out}((int64_t){src})"
        else:
            out = UNS.get(nt, nt)
            e = f"({out}){src}"
        return vloop(d, out, nn, lambda k: e, [("a_", a, st)])
    if base in ("vmull", "vmlal", "vmlsl", "vqdmull"):
        a, b = regs[1], regs[2]
        wt = WIDER[t]
        nn = 16 // SIZE[wt]
        p = f"(({wt}){lane_or_k(a, 'a_', 'k')} * ({wt}){lane_or_k(b, 'b_', 'k')})"
        e = {"vmull": p, "vmlal": f"({wt})(d_[k] + {p})", "vmlsl": f"({wt})(d_[k] - {p})",
             "vqdmull": f"({wt})(2 * {p})"}[base]
        srcs = [("a_", a, t), ("b_", b, t)] + ([("d_", d, wt)] if base in ("vmlal", "vmlsl") else [])
        return vloop(d, wt, nn, lambda k: e, srcs)
    if base == "vpadd":
        a, b = regs[1], regs[2]
        half = n // 2 if d.k == "d" else n
        if d.k != "d":
            return None
        e = f"(k < {n // 2} ? ({t})(a_[2*k] + a_[2*k+1]) : ({t})(b_[2*(k-{n // 2})] + b_[2*(k-{n // 2})+1]))"
        return vloop(d, t, n, lambda k: e, [("a_", a, t), ("b_", b, t)])
    if base in ("vpmax", "vpmin"):
        a, b = regs[1], regs[2]
        op = ">" if base == "vpmax" else "<"
        h = n // 2

        def pm(x, y):
            return f"({x} {op} {y} ? {x} : {y})"
        e = f"(k < {h} ? {pm('a_[2*k]', 'a_[2*k+1]')} : {pm(f'b_[2*(k-{h})]', f'b_[2*(k-{h})+1]')})"
        return vloop(d, t, n, lambda k: e, [("a_", a, t), ("b_", b, t)])
    if base == "vext":
        a, b = regs[1], regs[2]
        nb = d.nbytes
        sh = imm * SIZE[t]
        return [f"{{ uint8_t t_[{2 * nb}]; memcpy(t_, &c->vr.x[{a.n}], {nb}); memcpy(t_ + {nb}, &c->vr.x[{b.n}], {nb}); "
                f"memcpy(&c->vr.x[{d.n}], t_ + {sh}, {nb}); }}"]
    if base in ("vzip", "vuzp", "vtrn"):
        a, b = regs[0], regs[1]
        return [f"neon_{base[1:]}(c, {a.n}, {b.n}, {a.nbytes}, {SIZE[t]});"]
    if base in ("vrev16", "vrev32", "vrev64"):
        a = regs[1]
        grp = int(base[4:]) // 8 // SIZE[t]
        return vloop(d, t, n, lambda k: f"a_[(k / {grp}) * {grp} + ({grp - 1} - k % {grp})]", [("a_", a, t)])
    if base in ("vtbl", "vtbx"):
        dst, idx = regs[0], regs[-1]
        tbl = regs[1:-1]
        return [f"neon_tbl(c, {dst.n}, {tbl[0].n}, {len(tbl)}, {idx.n}, {1 if base == 'vtbx' else 0});"]
    if base == "vswp":
        a, b = regs[0], regs[1]
        nd = a.nbytes // 8
        return [f"{{ uint64_t t_[{nd}]; memcpy(t_, &c->vr.x[{a.n}], {a.nbytes}); memcpy(&c->vr.x[{a.n}], &c->vr.x[{b.n}], {a.nbytes}); "
                f"memcpy(&c->vr.x[{b.n}], t_, {a.nbytes}); }}"]
    return None


def neon_cvt(base, dt, o):
    regs = [x for x in o if isinstance(x, R)]
    d, a = regs[0], regs[1]
    to, frm = dt.split(".")
    n = d.nbytes // 4
    fb = next((x[1] for x in o if isinstance(x, tuple) and x[0] == "imm"), 0)
    sc = f" * {float(1 << fb)!r}f" if fb else ""
    dv = f" / {float(1 << fb)!r}f" if fb else ""
    if to == "f32" and frm == "s32":
        return vloop(d, "float", n, lambda k: f"(float)a_[k]{dv}", [("a_", a, "int32_t")])
    if to == "f32" and frm == "u32":
        return vloop(d, "float", n, lambda k: f"(float)a_[k]{dv}", [("a_", a, "uint32_t")])
    if to == "s32" and frm == "f32":
        return vloop(d, "int32_t", n, lambda k: f"cvt_f2s32(a_[k]{sc})", [("a_", a, "float")])
    if to == "u32" and frm == "f32":
        return vloop(d, "uint32_t", n, lambda k: f"cvt_f2u32(a_[k]{sc})", [("a_", a, "float")])
    return None


def neon_ldst(addr, w):
    """VLD1-4 / VST1-4: multiple structures, single lane, all lanes. Encoding from the ARM ARM."""
    load = (w >> 21) & 1
    rn = (w >> 16) & 0xF
    rm = w & 0xF
    dd = ((w >> 22) & 1) << 4 | (w >> 12) & 0xF
    ins = a32.Insn(addr, w, text="vldst")
    if (w >> 23) & 1 == 0:  # multiple structures
        typ = (w >> 8) & 0xF
        size = (w >> 6) & 3
        table = {0b0111: (1, 1, 1), 0b1010: (1, 1, 2), 0b0110: (1, 1, 3), 0b0010: (1, 1, 4),
                 0b1000: (2, 1, 1), 0b1001: (2, 2, 1), 0b0011: (2, 2, 2),
                 0b0100: (3, 1, 1), 0b0101: (3, 2, 1), 0b0000: (4, 1, 1), 0b0001: (4, 2, 1)}
        if typ not in table:
            UNHANDLED["vldst bad type"] += 1
            return None
        nst, inc, regs = table[typ]
        esz = 1 << size
        total = 8 * nst * regs
        call = f"neon_ldst_multi(c, a_, {dd}, {nst}, {inc}, {regs}, {esz}, {load});"
    else:
        size = (w >> 10) & 3
        nst = ((w >> 8) & 3) + 1
        if size == 3:  # all lanes
            esz = 1 << ((w >> 6) & 3)
            t = (w >> 5) & 1
            if nst == 1:
                call = f"neon_ld_all(c, a_, {dd}, 1, 1, {esz}, {t + 1});"
            else:
                call = f"neon_ld_all(c, a_, {dd}, {nst}, {t + 1}, {esz}, 1);"
            total = nst * esz
            if not load:
                UNHANDLED["vst all lanes"] += 1
                return None
        else:
            esz = 1 << size
            ia = (w >> 4) & 0xF
            if size == 0:
                idx, inc = ia >> 1, 1
            elif size == 1:
                idx, inc = ia >> 2, 2 if ia & 2 else 1
            else:
                idx, inc = ia >> 3, 2 if ia & 4 else 1
            call = f"neon_ldst_lane(c, a_, {dd}, {nst}, {inc}, {esz}, {idx}, {load});"
            total = nst * esz
    wb = "" if rm == 15 else (f" c->r[{rn}] += {total}u;" if rm == 13 else f" c->r[{rn}] += c->r[{rm}];")
    ins.lines = [f"{{ uint32_t a_ = c->r[{rn}]; {call}{wb} }}"]
    return ins
