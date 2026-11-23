"""A32 (ARM state) integer instruction decoder and C emitter.

Encodings from the ARM Architecture Reference Manual (ARMv7-A/R, ARMv8-A AArch32). VFP/NEON words are handed to
vfp.py. Each decode returns an Insn: control-flow kind for the analyser, and C source lines for the emitter.

Generated code conventions (runtime/include/guest.h):
  c->r[n] core registers, c->n/z/cf/v flags (0/1), ld32/st32... guest memory accessors, helpers for flags/shifts.
"""

COND_C = ["c->z", "!c->z", "c->cf", "!c->cf", "c->n", "!c->n", "c->v", "!c->v",
          "(c->cf && !c->z)", "(!c->cf || c->z)", "(c->n == c->v)", "(c->n != c->v)",
          "(!c->z && c->n == c->v)", "(c->z || c->n != c->v)", None, None]

PC, LR, SP = 15, 14, 13

# kinds
SEQ, B, BL, RET, IJMP, ICALL, JTAB, TRAP = "seq", "b", "bl", "ret", "ijmp", "icall", "jtab", "trap"


class Insn:
    __slots__ = ("addr", "word", "kind", "cond", "target", "lines", "text", "jt", "uses_ret0")

    def __init__(self, addr, word, kind=SEQ, cond=14, target=None, lines=None, text=""):
        self.addr, self.word, self.kind, self.cond, self.target = addr, word, kind, cond, target
        self.lines = lines or []
        self.text = text
        self.jt = None  # jump table: ('ldr'|'add', index expr, base addr)
        self.uses_ret0 = False

    @property
    def falls_through(self):
        if self.cond != 14:
            return True
        return self.kind not in (B, RET, IJMP, JTAB, TRAP)


def bits(w, hi, lo):
    return (w >> lo) & ((1 << (hi - lo + 1)) - 1)


def bit(w, n):
    return (w >> n) & 1


def ror(v, s):
    s &= 31
    return ((v >> s) | (v << (32 - s))) & 0xFFFFFFFF if s else v


def sx(v, n):
    return v - (1 << n) if v & (1 << (n - 1)) else v


class Ctx:
    """What the decoder needs from the analyser: constant reads of read-only words (literal pools)."""

    def __init__(self, read_const=None, movt_loads=None):
        self.read_const = read_const  # addr -> int or None
        self.movt_loads = movt_loads or {}  # movt addr -> literal word to load instead (runtime-patched constants)


def reg(n, addr, pc_off=8):
    return f"0x{(addr + pc_off) & 0xFFFFFFFF:08x}u" if n == PC else f"c->r[{n}]"


# ---------------------------------------------------------------------------------------------- shifter operands

def imm_shift(rm, typ, amt, addr, need_carry):
    """Register shifted by an immediate. Returns (value expr, carry expr or None)."""
    v = reg(rm, addr)
    if typ == 0:  # LSL
        if amt == 0:
            return v, "c->cf"
        return f"({v} << {amt})", (f"(({v} >> {32 - amt}) & 1)" if need_carry else None)
    if typ == 1:  # LSR, 0 means 32
        if amt == 0:
            return "0u", (f"({v} >> 31)" if need_carry else None)
        return f"({v} >> {amt})", (f"(({v} >> {amt - 1}) & 1)" if need_carry else None)
    if typ == 2:  # ASR, 0 means 32
        a = 31 if amt == 0 else amt
        val = f"(uint32_t)((int32_t){v} >> {a})"
        return val, (f"(({v} >> {(amt - 1) if amt else 31}) & 1)" if need_carry else None)
    if amt == 0:  # RRX
        return f"((c->cf << 31) | ({v} >> 1))", (f"({v} & 1)" if need_carry else None)
    return f"ror32({v}, {amt})", (f"(({v} >> {amt - 1}) & 1)" if need_carry else None)


def reg_shift(rm, typ, rs, addr, need_carry):
    """Register shifted by a register (bottom byte). Returns (value, carry or None)."""
    v, s = reg(rm, addr, 12), reg(rs, addr, 12)
    name = ("lsl", "lsr", "asr", "ror")[typ]
    if need_carry:
        return f"sh_{name}_c(c, {v}, {s})", "c->sh_carry"
    return f"sh_{name}({v}, {s})", None


def dp_operand2(w, addr, need_carry):
    if bit(w, 25):
        rot = bits(w, 11, 8) * 2
        val = ror(bits(w, 7, 0), rot)
        carry = ("c->cf" if rot == 0 else str(val >> 31)) if need_carry else None
        return f"0x{val:08x}u", carry, val
    rm = bits(w, 3, 0)
    typ = bits(w, 6, 5)
    if bit(w, 4):
        v, cy = reg_shift(rm, typ, bits(w, 11, 8), addr, need_carry)
    else:
        v, cy = imm_shift(rm, typ, bits(w, 11, 7), addr, need_carry)
    return v, cy, None


DP_NAMES = ["and", "eor", "sub", "rsb", "add", "adc", "sbc", "rsc", "tst", "teq", "cmp", "cmn", "orr", "mov", "bic", "mvn"]


def data_processing(w, addr, ctx):
    op = bits(w, 24, 21)
    s = bit(w, 20)
    rn, rd = bits(w, 19, 16), bits(w, 15, 12)
    logical = op in (0, 1, 8, 9, 12, 13, 14, 15)
    need_carry = bool(s) and logical
    op2, carry, imm = dp_operand2(w, addr, need_carry)
    pc_off = 12 if (not bit(w, 25) and bit(w, 4)) else 8
    a = reg(rn, addr, pc_off)
    lines = []
    ins = Insn(addr, w)
    if op in (8, 9, 10, 11):  # compare ops: always set flags
        if op == 8:
            lines += [f"{{ uint32_t t = {a} & {op2}; c->cf = {carry}; nz(c, t); }}"]
        elif op == 9:
            lines += [f"{{ uint32_t t = {a} ^ {op2}; c->cf = {carry}; nz(c, t); }}"]
        elif op == 10:
            lines += [f"add_flags(c, {a}, ~({op2}), 1);"]
        else:
            lines += [f"add_flags(c, {a}, {op2}, 0);"]
        ins.lines = lines
        return ins
    expr = {
        0: f"{a} & {op2}", 1: f"{a} ^ {op2}", 12: f"{a} | {op2}", 13: f"{op2}",
        14: f"{a} & ~({op2})", 15: f"~({op2})",
        2: f"{a} - {op2}", 3: f"{op2} - {a}", 4: f"{a} + {op2}",
        5: f"{a} + {op2} + c->cf", 6: f"{a} - {op2} - !c->cf", 7: f"{op2} - {a} - !c->cf",
    }[op]
    if s and rd != PC:
        if logical:
            if carry == "c->cf":
                lines += [f"{{ uint32_t t = {expr}; nz(c, t); c->r[{rd}] = t; }}"]
            else:
                lines += [f"{{ uint32_t t = {expr}; c->cf = {carry}; nz(c, t); c->r[{rd}] = t; }}"]
        else:
            fl = {2: f"add_flags(c, {a}, ~({op2}), 1)", 3: f"add_flags(c, {op2}, ~({a}), 1)",
                  4: f"add_flags(c, {a}, {op2}, 0)", 5: f"add_flags(c, {a}, {op2}, c->cf)",
                  6: f"add_flags(c, {a}, ~({op2}), c->cf)", 7: f"add_flags(c, {op2}, ~({a}), c->cf)"}[op]
            lines += [f"c->r[{rd}] = {fl};"]
        ins.lines = lines
        return ins
    if rd == PC:
        if s:
            ins.kind = TRAP
            ins.lines = [f"guest_trap(c, 0x{addr:08x}u, \"exception return\");"]
            return ins
        # mov pc, lr -> return; add pc, pc, rX, lsl #2 -> jump table of branches; else indirect jump
        if op == 13 and not bit(w, 25) and bits(w, 11, 4) == 0 and bits(w, 3, 0) == LR:
            ins.kind = RET
            ins.lines = ["return;"]
            return ins
        if op == 4 and rn == PC and not bit(w, 25) and not bit(w, 4) and bits(w, 6, 5) == 0 and bits(w, 11, 7) == 2:
            ins.kind = JTAB
            ins.jt = ("add", f"c->r[{bits(w, 3, 0)}]", addr + 8)
            return ins
        ins.kind = IJMP
        ins.lines = [f"{{ uint32_t t = {expr}; JUMP(t); }}"]
        ins.uses_ret0 = True
        return ins
    lines += [f"c->r[{rd}] = {expr};"]
    ins.lines = lines
    return ins


# ---------------------------------------------------------------------------------------------- loads / stores

def addr_mode(w, addr, rn, off_expr, ctx_const_ok=True):
    """P/U/W addressing. Returns (address expr, writeback line or None)."""
    p, u, wb = bit(w, 24), bit(w, 23), bit(w, 21)
    base = reg(rn, addr)
    sign = "+" if u else "-"
    ea = f"({base} {sign} {off_expr})" if off_expr != "0" else base
    if p:
        return ea, (f"c->r[{rn}] = {ea};" if wb else None)
    return base, f"c->r[{rn}] = {ea};"


LOADS = {"w": "ld32", "b": "ld8", "h": "ld16", "sb": "lds8", "sh": "lds16"}
STORES = {"w": "st32", "b": "st8", "h": "st16"}


def emit_load_store(ins, w, addr, rn, rt, kind, load, off_expr, ctx, const_off=None):
    ea, wbl = addr_mode(w, addr, rn, off_expr)
    lines = []
    p, u, wbit = bit(w, 24), bit(w, 23), bit(w, 21)
    if load:
        fn = LOADS[kind]
        # literal pool: pc-relative pre-indexed constant address in read-only text -> fold the value
        if rn == PC and const_off is not None and p and not wbit and kind == "w" and ctx.read_const:
            a = (addr + 8 + (const_off if u else -const_off)) & 0xFFFFFFFF
            v = ctx.read_const(a)
            if v is not None and rt != PC:
                ins.lines = [f"c->r[{rt}] = 0x{v:08x}u;"]
                return ins
        if rt == PC:
            if rn == SP and not p and u and const_off == 4:  # pop {pc}
                ins.kind = RET
                ins.lines = [f"c->r[13] += 4;", "return;"]
                return ins
            if not bit(w, 25) or True:
                ins.kind = IJMP
                ins.uses_ret0 = True
                lines.append(f"{{ uint32_t t = {fn}({ea});")
                if wbl:
                    lines.append(wbl)
                lines.append("JUMP(t); }")
                ins.lines = lines
                return ins
        if wbl and rt == rn:
            # loaded value wins over writeback (unpredictable for W, defined for post-index form only if rt != rn)
            lines += [f"{{ uint32_t t = {fn}({ea}); {wbl} c->r[{rt}] = t; }}"]
        elif wbl:
            lines += [f"{{ uint32_t t = {fn}({ea}); {wbl} c->r[{rt}] = t; }}"]
        else:
            lines += [f"c->r[{rt}] = {fn}({ea});"]
    else:
        fn = STORES[kind]
        val = reg(rt, addr)
        if wbl:
            lines += [f"{{ uint32_t v = {val}; uint32_t a = {ea}; {wbl} {fn}(a, v); }}"]
        else:
            lines += [f"{fn}({ea}, {val});"]
    ins.lines = lines
    return ins


def load_store_word_byte(w, addr, ctx):
    ins = Insn(addr, w)
    load = bit(w, 20)
    byte = bit(w, 22)
    rn, rt = bits(w, 19, 16), bits(w, 15, 12)
    const_off = None
    if bit(w, 25):
        off, _ = imm_shift(bits(w, 3, 0), bits(w, 6, 5), bits(w, 11, 7), addr, False)
    else:
        const_off = bits(w, 11, 0)
        off = f"{const_off}u" if const_off else "0"
    if not bit(w, 24) and bit(w, 21):  # LDRT/STRT: user-mode access, same thing for us
        pass
    return emit_load_store(ins, w, addr, rn, rt, "b" if byte else "w", load, off, ctx, const_off)


def extra_load_store(w, addr, ctx):
    """LDRH/STRH/LDRSB/LDRSH/LDRD/STRD."""
    ins = Insn(addr, w)
    op2 = bits(w, 6, 5)
    load = bit(w, 20)
    rn, rt = bits(w, 19, 16), bits(w, 15, 12)
    if bit(w, 22):
        k = (bits(w, 11, 8) << 4) | bits(w, 3, 0)
        off = f"{k}u" if k else "0"
    else:
        off = reg(bits(w, 3, 0), addr)
    if op2 == 1:
        return emit_load_store(ins, w, addr, rn, rt, "h", load, off, ctx)
    if op2 == 2 and load:
        return emit_load_store(ins, w, addr, rn, rt, "sb", True, off, ctx)
    if op2 == 3 and load:
        return emit_load_store(ins, w, addr, rn, rt, "sh", True, off, ctx)
    # doubleword: op2 2 + L0 = LDRD, op2 3 + L0 = STRD
    ea, wbl = addr_mode(w, addr, rn, off)
    if op2 == 2:
        ins.lines = [f"{{ uint32_t a = {ea}; uint32_t lo = ld32(a), hi = ld32(a + 4); "
                     + (wbl or "") + f" c->r[{rt}] = lo; c->r[{rt + 1}] = hi; }}"]
    else:
        ins.lines = [f"{{ uint32_t a = {ea}; uint32_t lo = {reg(rt, addr)}, hi = {reg(rt + 1, addr)}; "
                     + (wbl or "") + " st32(a, lo); st32(a + 4, hi); }"]
    return ins


def block_transfer(w, addr, ctx):
    ins = Insn(addr, w)
    p, u, s, wb, load = bit(w, 24), bit(w, 23), bit(w, 22), bit(w, 21), bit(w, 20)
    rn = bits(w, 19, 16)
    regs = [i for i in range(16) if bit(w, i)]
    n = len(regs)
    if n == 0:
        ins.kind = TRAP
        ins.lines = [f"guest_trap(c, 0x{addr:08x}u, \"empty ldm/stm\");"]
        return ins
    if u:
        start = "a0 + 4" if p else "a0"
        wbv = f"a0 + {4 * n}"
    else:
        start = f"a0 - {4 * n}" if p else f"a0 - {4 * n - 4}"
        wbv = f"a0 - {4 * n}"
    lines = [f"{{ uint32_t a0 = {reg(rn, addr)}; uint32_t a = {start};"]
    if load:
        for i, r in enumerate(regs):
            if r == PC:
                lines.append(f"uint32_t t = ld32(a + {4 * i});")
            elif r == rn:
                lines.append(f"uint32_t nb = ld32(a + {4 * i});")
            else:
                lines.append(f"c->r[{r}] = ld32(a + {4 * i});")
        if wb and rn not in regs:
            lines.append(f"c->r[{rn}] = {wbv};")
        if rn in regs:
            lines.append(f"c->r[{rn}] = nb;")
        if PC in regs:
            if rn == SP and u and not p:
                ins.kind = RET
                lines.append("(void)t; return; }")
            else:
                ins.kind = IJMP
                ins.uses_ret0 = True
                lines.append("JUMP(t); }")
            ins.lines = lines
            return ins
        lines.append("}")
    else:
        for i, r in enumerate(regs):
            lines.append(f"st32(a + {4 * i}, {reg(r, addr)});")
        if wb:
            lines.append(f"c->r[{rn}] = {wbv};")
        lines.append("}")
    ins.lines = lines
    return ins


# ---------------------------------------------------------------------------------------------- multiplies

def multiply(w, addr):
    ins = Insn(addr, w)
    op = bits(w, 23, 20)
    rd, ra, rm, rn = bits(w, 19, 16), bits(w, 15, 12), bits(w, 11, 8), bits(w, 3, 0)
    s = op & 1
    R = lambda x: f"c->r[{x}]"
    if op in (0, 1):  # MUL
        e = f"{R(rn)} * {R(rm)}"
    elif op in (2, 3):  # MLA
        e = f"{R(rn)} * {R(rm)} + {R(ra)}"
    elif op == 6:  # MLS
        e = f"{R(ra)} - {R(rn)} * {R(rm)}"
    elif op == 4:  # UMAAL
        ins.lines = [f"{{ uint64_t t = (uint64_t){R(rn)} * {R(rm)} + {R(ra)} + {R(rd)}; "
                     f"{R(ra)} = (uint32_t)t; {R(rd)} = (uint32_t)(t >> 32); }}"]
        return ins
    else:
        # long: 8/9 UMULL, 10/11 UMLAL, 12/13 SMULL, 14/15 SMLAL ; rdhi=rd(19:16) rdlo=ra(15:12)
        signed = op >= 12
        acc = op in (10, 11, 14, 15)
        if signed:
            m = f"(uint64_t)((int64_t)(int32_t){R(rn)} * (int32_t){R(rm)})"
        else:
            m = f"((uint64_t){R(rn)} * {R(rm)})"
        if acc:
            m = f"({m} + (((uint64_t){R(rd)} << 32) | {R(ra)}))"
        ln = f"{{ uint64_t t = {m}; {R(ra)} = (uint32_t)t; {R(rd)} = (uint32_t)(t >> 32);"
        if s:
            ln += " c->n = (uint32_t)(t >> 63); c->z = t == 0;"
        ins.lines = [ln + " }"]
        return ins
    if s:
        ins.lines = [f"{{ uint32_t t = {e}; nz(c, t); {R(rd)} = t; }}"]
    else:
        ins.lines = [f"{R(rd)} = {e};"]
    return ins


def halfword_multiply(w, addr):
    """SMLAxy/SMLAWy/SMULWy/SMLALxy/SMULxy (00010xx0 ... 1yx0)."""
    ins = Insn(addr, w)
    op = bits(w, 22, 21)
    rd, ra, rm, rn = bits(w, 19, 16), bits(w, 15, 12), bits(w, 11, 8), bits(w, 3, 0)
    x, y = bit(w, 5), bit(w, 6)
    R = lambda r: f"c->r[{r}]"
    hn = f"(int32_t)(int16_t)({R(rn)} >> {16 if x else 0})"
    hm = f"(int32_t)(int16_t)({R(rm)} >> {16 if y else 0})"
    if op == 0:  # SMLAxy (sets Q on overflow; ignored)
        ins.lines = [f"{R(rd)} = (uint32_t)({hn} * {hm} + (int32_t){R(ra)});"]
    elif op == 1:
        hmy = f"(int64_t)(int16_t)({R(rm)} >> {16 if y else 0})"
        prod = f"(uint32_t)(((int64_t)(int32_t){R(rn)} * {hmy}) >> 16)"
        if x:  # SMULWy
            ins.lines = [f"{R(rd)} = {prod};"]
        else:  # SMLAWy
            ins.lines = [f"{R(rd)} = {prod} + {R(ra)};"]
    elif op == 2:  # SMLALxy
        ins.lines = [f"{{ int64_t t = (int64_t)((((uint64_t){R(rd)}) << 32) | {R(ra)}) + (int64_t)({hn} * {hm}); "
                     f"{R(ra)} = (uint32_t)t; {R(rd)} = (uint32_t)((uint64_t)t >> 32); }}"]
    else:  # SMULxy
        ins.lines = [f"{R(rd)} = (uint32_t)({hn} * {hm});"]
    return ins


# ---------------------------------------------------------------------------------------------- misc / media

def synch(w, addr):
    """LDREX/STREX family (bits 27:23 = 00011, 7:4 = 1001)."""
    ins = Insn(addr, w)
    op = bits(w, 22, 20)
    rn, rt = bits(w, 19, 16), bits(w, 15, 12)
    rm = bits(w, 3, 0)
    R = lambda r: f"c->r[{r}]"
    size = {0: 32, 1: 32, 2: 64, 3: 64, 4: 8, 5: 8, 6: 16, 7: 16}[op]
    if bits(w, 23, 23) == 0:  # SWP/SWPB
        sz = "8" if bit(w, 22) else "32"
        ins.lines = [f"{R(rt)} = atomic_swap{sz}({R(rn)}, {R(rm)});"]
        return ins
    load = op & 1
    if bits(w, 9, 8) == 0 and size != 64:
        # LDA/LDAB/LDAH, STL/STLB/STLH (ARMv8): plain load-acquire / store-release, no exclusive monitor (bits 9:8:
        # 00 plain, 10 exclusive acquire/release, 11 exclusive). Store: Rt in bits 3:0, bits 15:12 are 1111.
        if load:
            ins.lines = [f"{R(rt)} = acq_load{size}({R(rn)});"]
        else:
            ins.lines = [f"rel_store{size}({R(rn)}, {R(rm)});"]
        return ins
    if load:
        if size == 64:
            ins.lines = [f"{{ uint64_t t = excl_load64(c, {R(rn)}); {R(rt)} = (uint32_t)t; {R(rt + 1)} = (uint32_t)(t >> 32); }}"]
        else:
            ins.lines = [f"{R(rt)} = excl_load{size}(c, {R(rn)});"]
    else:
        # STREX Rd, Rt, [Rn]: Rd = bits 15:12, Rt = bits 3:0
        rd, rt2 = rt, rm
        if size == 64:
            ins.lines = [f"{R(rd)} = excl_store64(c, {R(rn)}, ((uint64_t){R(rt2 + 1)} << 32) | {R(rt2)});"]
        else:
            ins.lines = [f"{R(rd)} = excl_store{size}(c, {R(rn)}, {R(rt2)});"]
    return ins


def misc(w, addr):
    """Miscellaneous instructions (bits 27:23 = 00010, bit 20 = 0, bit 7 = 0)."""
    ins = Insn(addr, w)
    op2 = bits(w, 6, 4)
    op = bits(w, 22, 21)
    R = lambda r: f"c->r[{r}]"
    rd, rm = bits(w, 15, 12), bits(w, 3, 0)
    if op2 == 0:
        if op in (0, 2):  # MRS
            ins.lines = [f"{R(rd)} = get_cpsr(c);"]
        else:  # MSR (register)
            mask = bits(w, 19, 16)
            ins.lines = [f"set_cpsr(c, {reg(rm, addr)}, {mask});"]
        return ins
    if op2 == 1 and op == 1:  # BX
        if rm == LR:
            ins.kind = RET
            ins.lines = ["return;"]
        else:
            ins.kind = IJMP
            ins.uses_ret0 = True
            ins.lines = [f"{{ uint32_t t = {R(rm)}; JUMP(t); }}"]
        return ins
    if op2 == 1 and op == 3:  # CLZ
        ins.lines = [f"{R(rd)} = clz32({R(rm)});"]
        return ins
    if op2 == 3 and op == 1:  # BLX register
        ins.kind = ICALL
        ins.lines = [f"{{ uint32_t t = {R(rm)}; c->r[14] = 0x{addr + 4:08x}u; dispatch(c, t); }}"]
        return ins
    if op2 == 5:  # QADD/QSUB/QDADD/QDSUB
        rn = bits(w, 19, 16)
        fn = ("qadd", "qsub", "qdadd", "qdsub")[op]
        ins.lines = [f"{R(rd)} = {fn}(c, {R(rm)}, {R(bits(w, 19, 16))});"]
        return ins
    if op2 == 4:  # CRC32{B,H,W} / CRC32C{B,H,W} (ARMv8): sz = op, C = bit 9
        rn = bits(w, 19, 16)
        fn = ("crc32c" if bit(w, 9) else "crc32") + ("b", "h", "w", "x")[op]
        ins.lines = [f"{R(rd)} = {fn}({R(rn)}, {R(rm)});"]
        return ins
    if op2 == 7 and op == 1:  # BKPT
        ins.kind = TRAP
        ins.lines = [f"guest_trap(c, 0x{addr:08x}u, \"bkpt\");"]
        return ins
    return None


def media(w, addr):
    ins = Insn(addr, w)
    op1 = bits(w, 24, 20)
    op2 = bits(w, 7, 5)
    rd, rn, rm = bits(w, 15, 12), bits(w, 19, 16), bits(w, 3, 0)
    R = lambda r: f"c->r[{r}]"
    if op1 == 0b11111 and op2 == 0b111:  # UDF
        ins.kind = TRAP
        ins.lines = [f"guest_trap(c, 0x{addr:08x}u, \"udf\");"]
        return ins
    if (op1 & 0b11110) == 0b11110 and (op2 & 0b011) == 0b010:  # UBFX
        lsb, wm1 = bits(w, 11, 7), bits(w, 20, 16)
        rd2 = bits(w, 15, 12)
        mask = (1 << (wm1 + 1)) - 1
        ins.lines = [f"{R(rd2)} = ({R(rm)} >> {lsb}) & 0x{mask:x}u;"]
        return ins
    if (op1 & 0b11110) == 0b11010 and (op2 & 0b011) == 0b010:  # SBFX
        lsb, wm1 = bits(w, 11, 7), bits(w, 20, 16)
        width = wm1 + 1
        ins.lines = [f"{R(rd)} = (uint32_t)(((int32_t)({R(rm)} << {32 - lsb - width})) >> {32 - width});"]
        return ins
    if (op1 & 0b11110) == 0b11100 and (op2 & 0b011) == 0b000:  # BFC / BFI
        lsb, msb = bits(w, 11, 7), bits(w, 20, 16)
        if msb < lsb:
            return None
        mask = (((1 << (msb - lsb + 1)) - 1) << lsb) & 0xFFFFFFFF
        if rm == 15:
            ins.lines = [f"{R(rd)} &= 0x{~mask & 0xFFFFFFFF:08x}u;"]
        else:
            ins.lines = [f"{R(rd)} = ({R(rd)} & 0x{~mask & 0xFFFFFFFF:08x}u) | (({R(rm)} << {lsb}) & 0x{mask:08x}u);"]
        return ins
    if op1 == 0b11000 and op2 == 0 and rd == 15:  # USAD8
        ins.lines = [f"{R(rn)} = usad8({R(rm)}, {R(bits(w, 11, 8))});"]
        return ins
    if (op1 & 0b11000) == 0b10000:  # signed multiplies, SDIV/UDIV
        o = op1 & 0b111
        ra, rmm, rdd, rnn = bits(w, 15, 12), bits(w, 11, 8), bits(w, 19, 16), bits(w, 3, 0)
        if o == 0b001 and op2 == 0:
            ins.lines = [f"{R(rdd)} = sdiv32({R(rnn)}, {R(rmm)});"]
            return ins
        if o == 0b011 and op2 == 0:
            ins.lines = [f"{R(rdd)} = udiv32({R(rnn)}, {R(rmm)});"]
            return ins
        if o == 0b101 and (op2 & 0b110) == 0:  # SMMLA / SMMUL (ra==15), R bit = round
            rnd = " + 0x80000000ll" if bit(w, 5) else ""
            acc = "" if ra == 15 else f"((int64_t)(int32_t){R(ra)} << 32) + "
            ins.lines = [f"{R(rdd)} = (uint32_t)((uint64_t)({acc}(int64_t)(int32_t){R(rnn)} * (int32_t){R(rmm)}{rnd}) >> 32);"]
            return ins
        if o == 0b101 and (op2 & 0b110) == 0b110:  # SMMLS
            rnd = " + 0x80000000ll" if bit(w, 5) else ""
            ins.lines = [f"{R(rdd)} = (uint32_t)((uint64_t)(((int64_t)(int32_t){R(ra)} << 32) - (int64_t)(int32_t){R(rnn)} * (int32_t){R(rmm)}{rnd}) >> 32);"]
            return ins
        if o == 0b000:  # SMLAD/SMUAD/SMLSD/SMUSD
            sw = bit(w, 5)
            m = f"({R(rmm)} >> 16 | {R(rmm)} << 16)" if sw else R(rmm)
            lo = f"(int32_t)(int16_t){R(rnn)} * (int32_t)(int16_t)({m})"
            hi = f"(int32_t)(int16_t)({R(rnn)} >> 16) * (int32_t)(int16_t)(({m}) >> 16)"
            sub = bit(w, 6)
            e = f"({lo}) {'-' if sub else '+'} ({hi})"
            if ra != 15:
                e = f"({e}) + (int32_t){R(ra)}"
            ins.lines = [f"{R(rdd)} = (uint32_t)({e});"]
            return ins
        return None
    if (op1 & 0b11000) == 0b01000:  # pack, unpack, saturate, reverse
        o1 = op1 & 0b111
        if o1 == 0 and (op2 & 1) == 0:  # PKHBT / PKHTB
            imm = bits(w, 11, 7)
            if bit(w, 6):  # PKHTB: rd = (rn & 0xffff0000) | ((rm asr imm) & 0xffff)
                sh = f"(uint32_t)((int32_t){R(rm)} >> {imm if imm else 31})"
                ins.lines = [f"{R(rd)} = ({R(rn)} & 0xffff0000u) | ({sh} & 0xffffu);"]
            else:
                ins.lines = [f"{R(rd)} = ({R(rn)} & 0xffffu) | (({R(rm)} << {imm}) & 0xffff0000u);"]
            return ins
        if op2 == 0b011:  # extend (with optional add): SXTAB16 .. UXTAH
            rot = bits(w, 11, 10) * 8
            src = f"ror32({R(rm)}, {rot})" if rot else R(rm)
            kind = {0b000: "sxtb16", 0b010: "sxtb", 0b011: "sxth", 0b100: "uxtb16", 0b110: "uxtb", 0b111: "uxth"}.get(o1)
            if kind is None:
                return None
            ext = {"sxtb": f"(uint32_t)(int32_t)(int8_t){src}", "sxth": f"(uint32_t)(int32_t)(int16_t){src}",
                   "uxtb": f"({src} & 0xffu)", "uxth": f"({src} & 0xffffu)",
                   "uxtb16": f"({src} & 0x00ff00ffu)", "sxtb16": f"sxtb16({src})"}[kind]
            if rn == 15:
                ins.lines = [f"{R(rd)} = {ext};"]
            elif kind.endswith("16"):
                ins.lines = [f"{R(rd)} = add16({R(rn)}, {ext});"]
            else:
                ins.lines = [f"{R(rd)} = {R(rn)} + {ext};"]
            return ins
        if o1 == 0b000 and op2 == 0b101:  # SEL
            ins.lines = [f"{R(rd)} = sel_ge(c, {R(rn)}, {R(rm)});"]
            return ins
        if o1 == 0b011 and op2 == 0b001:  # REV
            ins.lines = [f"{R(rd)} = __builtin_bswap32({R(rm)});"]
            return ins
        if o1 == 0b011 and op2 == 0b101:  # REV16
            ins.lines = [f"{R(rd)} = ((({R(rm)} >> 8) & 0x00ff00ffu) | (({R(rm)} << 8) & 0xff00ff00u));"]
            return ins
        if o1 == 0b111 and op2 == 0b001:  # RBIT
            ins.lines = [f"{R(rd)} = rbit32({R(rm)});"]
            return ins
        if o1 == 0b111 and op2 == 0b101:  # REVSH
            ins.lines = [f"{R(rd)} = (uint32_t)(int32_t)(int16_t)__builtin_bswap16((uint16_t){R(rm)});"]
            return ins
        if (o1 & 0b110) in (0b010, 0b110) and (op2 & 1) == 0:  # SSAT / USAT
            sat = bits(w, 20, 16)
            sh = bit(w, 6)
            imm = bits(w, 11, 7)
            src = f"(int32_t){R(rm)} >> {imm if imm else 31}" if sh else f"(int32_t)({R(rm)} << {imm})"
            if o1 & 0b100:
                ins.lines = [f"{R(rd)} = usat(c, {src}, {sat});"]
            else:
                ins.lines = [f"{R(rd)} = ssat(c, {src}, {sat + 1});"]
            return ins
        if o1 in (0b010, 0b110) and op2 == 0b001:  # SSAT16 / USAT16
            return None
        return None
    if (op1 & 0b11000) == 0b00000:  # parallel add/sub
        op = (bits(w, 22, 20), op2)
        names = {1: "s", 2: "q", 3: "sh", 5: "u", 6: "uq", 7: "uh"}
        ops = {0: "add16", 1: "asx", 2: "sax", 3: "sub16", 4: "add8", 7: "sub8"}
        if op[0] in names and op[1] in ops:
            fn = f"par_{names[op[0]]}{ops[op[1]]}"
            ins.lines = [f"{R(rd)} = {fn}(c, {R(rn)}, {R(rm)});"]
            return ins
    return None


# ---------------------------------------------------------------------------------------------- top-level decode

def decode(addr, w, ctx, vfp_decode):
    cond = w >> 28
    if cond == 15:
        return decode_uncond(addr, w, ctx, vfp_decode)
    ins = decode_cond(addr, w, ctx, vfp_decode)
    if ins is not None:
        ins.cond = cond
    return ins


def decode_cond(addr, w, ctx, vfp_decode):
    op1 = bits(w, 27, 25)
    if op1 in (0, 1):
        if op1 == 0 and bit(w, 4) and bit(w, 7):
            if bits(w, 6, 5) == 0:
                if bits(w, 24, 24) == 0:
                    return multiply(w, addr)
                return synch(w, addr)
            if bits(w, 24, 23) == 0b10 and bits(w, 6, 5) and False:
                return None
            return extra_load_store(w, addr, ctx)
        if bits(w, 24, 23) == 0b10 and not bit(w, 20):
            if op1 == 0:
                if bit(w, 7) and not bit(w, 4):
                    return halfword_multiply(w, addr)
                return misc(w, addr)
            # op1 == 1: MOVW/MOVT/MSR imm/hints
            o = bits(w, 22, 21)
            rd = bits(w, 15, 12)
            imm16 = (bits(w, 19, 16) << 12) | bits(w, 11, 0)
            if o == 0:
                ins = Insn(addr, w)
                ins.lines = [f"c->r[{rd}] = 0x{imm16:x}u;"]
                return ins
            if o == 2:
                ins = Insn(addr, w)
                ins.lines = [f"c->r[{rd}] = (c->r[{rd}] & 0xffffu) | 0x{imm16 << 16:08x}u;"]
                if ctx and addr in ctx.movt_loads:
                    ins.lines = [f"c->r[{rd}] = ld32(0x{ctx.movt_loads[addr]:08x}u);"]
                return ins
            if o == 1 and bits(w, 19, 16) == 0:  # hints: nop/yield/wfe/wfi/sev/dbg
                ins = Insn(addr, w)
                h = bits(w, 7, 0)
                ins.lines = ["guest_yield(c);"] if h in (1, 2, 3) else []
                return ins
            if o in (1, 3):  # MSR immediate
                ins = Insn(addr, w)
                val = ror(bits(w, 7, 0), bits(w, 11, 8) * 2)
                ins.lines = [f"set_cpsr(c, 0x{val:08x}u, {bits(w, 19, 16)});"]
                return ins
            return None
        return data_processing(w, addr, ctx)
    if op1 == 2 or (op1 == 3 and not bit(w, 4)):
        return load_store_word_byte(w, addr, ctx)
    if op1 == 3:
        return media(w, addr)
    if op1 == 4:
        return block_transfer(w, addr, ctx)
    if op1 == 5:
        off = sx(bits(w, 23, 0), 24) * 4
        tgt = (addr + 8 + off) & 0xFFFFFFFF
        return Insn(addr, w, BL if bit(w, 24) else B, target=tgt)
    # op1 6/7: coprocessor, VFP, SVC
    if op1 == 7 and bit(w, 24):
        ins = Insn(addr, w)
        ins.lines = [f"guest_svc(c, 0x{bits(w, 23, 0):x}u, 0x{addr:08x}u);"]
        return ins
    cp = bits(w, 11, 8)
    if op1 == 6 and bits(w, 24, 21) == 0b0010 and cp == 15:  # MRRC/MCRR p15: generic timer counters
        ins = Insn(addr, w)
        rt, rt2, opc1, crm = bits(w, 15, 12), bits(w, 19, 16), bits(w, 7, 4), bits(w, 3, 0)
        if bit(w, 20) and crm == 14 and opc1 in (0, 1):  # CNTPCT / CNTVCT
            ins.lines = [f"{{ uint64_t t = guest_counter(); c->r[{rt}] = (uint32_t)t; c->r[{rt2}] = (uint32_t)(t >> 32); }}"]
        else:
            ins.lines = [f"guest_unimpl(c, 0x{addr:08x}u, 0x{w:08x}u);"]
        return ins
    if cp in (10, 11):
        return vfp_decode(addr, w)
    if cp == 15 and op1 == 7 and bit(w, 4):
        return cp15(w, addr)
    return None


def cp15(w, addr):
    ins = Insn(addr, w)
    load = bit(w, 20)
    opc1, crn, rt, opc2, crm = bits(w, 23, 21), bits(w, 19, 16), bits(w, 15, 12), bits(w, 7, 5), bits(w, 3, 0)
    key = (opc1, crn, crm, opc2)
    if load:
        if key == (0, 13, 0, 3):
            ins.lines = [f"c->r[{rt}] = c->tpidruro;"]
            return ins
        if key == (0, 13, 0, 2):
            ins.lines = [f"c->r[{rt}] = c->tpidrurw;"]
            return ins
        ins.lines = [f"c->r[{rt}] = cp15_read(c, {opc1}, {crn}, {crm}, {opc2});"]
        return ins
    if key == (0, 13, 0, 2):
        ins.lines = [f"c->tpidrurw = c->r[{rt}];"]
        return ins
    if crn == 7 and crm in (5, 10) and opc1 == 0:  # legacy ISB/DSB/DMB
        ins.lines = ["__atomic_thread_fence(__ATOMIC_SEQ_CST);"]
        return ins
    ins.lines = [f"cp15_write(c, {opc1}, {crn}, {crm}, {opc2}, c->r[{rt}]);"]
    return ins


def decode_uncond(addr, w, ctx, vfp_decode):
    ins = Insn(addr, w)
    if bits(w, 27, 25) == 0b101:  # BLX immediate (switches to Thumb)
        off = (sx(bits(w, 23, 0), 24) << 2) | (bit(w, 24) << 1)
        ins.kind = TRAP
        ins.lines = [f"guest_trap(c, 0x{addr:08x}u, \"blx to thumb\");"]
        return ins
    if (w & 0xFFFFFFF0) in (0xF57FF040, 0xF57FF050):  # DSB / DMB
        ins.lines = ["__atomic_thread_fence(__ATOMIC_SEQ_CST);"]
        return ins
    if (w & 0xFFFFFFF0) == 0xF57FF060:  # ISB
        return ins
    if w == 0xF57FF01F:  # CLREX
        ins.lines = ["c->excl_valid = 0;"]
        return ins
    if (w & 0xFD70F000) == 0xF550F000 or (w & 0xFD70F000) == 0xF510F000 or (w & 0xFF70F000) == 0xF450F000 \
            or (w & 0xFF70F010) == 0xF650F000 or (w & 0xFF30F010) == 0xF710F000 or (w & 0xFF30F010) == 0xF610F000:
        return ins  # PLD / PLDW / PLI: no-ops
    if bits(w, 27, 25) == 0b001 or bits(w, 27, 24) == 0b0100 or bits(w, 27, 24) == 0b1110:
        return vfp_decode(addr, w)  # NEON data processing / element load-store / VFPv8 (vsel, vmaxnm, vrint)
    return None
