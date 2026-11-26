"""Self-check of lift.py reg_locals (register + flag locals): python tools/recomp/test_reg_locals.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from lift import reg_locals  # noqa: E402

f = [
    "void F_00001000(Cpu* c) {",
    "  HOOK(3);",
    "  const uint32_t ret0 = c->r[14];",
    "  c->r[0] = add_flags(c, c->r[0], ~(c->r[1]), 1);",
    "  if (c->z) {",
    "    goto L_1;",
    "  }",
    "  c->r[14] = 0x00001010u; F_00002000(c);",
    "  st32(c->r[1], c->r[0]); c->r[1] += 4u;",
    "L_1:;",
    "  { uint32_t t = c->r[1]; switch (t) { case 0x1u: goto L_1; default: JUMP(t); } }",
    "  F_00003000(c); return;",
    "}",
]
o = reg_locals(f, 3)
t = "\n".join(o)
assert o[1] == "  HOOK(3);" and o[2].startswith("  const uint32_t ret0 = c->r[14]"), t  # header kept, reads the Cpu
assert o[3] == "  uint32_t r0 = c->r[0], r1 = c->r[1];", o[3]  # r14: named once, stays in the Cpu
assert o[4] == "  Flags F = {c->n, c->z, c->cf, c->v};", o[4]
assert "r0 = add_flags_f(&F, r0, ~(r1), 1);" in t and "if (F.z)" in t, t
spill = "c->r[0] = r0; c->r[1] = r1; c->n = F.n; c->z = F.z; c->cf = F.cf; c->v = F.v; "
assert f"c->r[14] = 0x00001010u; {{ {spill}F_00002000(c); r0 = c->r[0];" in t, t       # spill before, reload after a call
assert f"default: {{ {spill}JUMP(t); }}" in t, t
assert f"{{ {spill}F_00003000(c); return; }}" in t, t                             # tail call: spill, no reload
assert "st32(r1, r0); r1 += 4u;" in t, t
# setjmp functions and helpers that read flags through c stay as they are
sj = f[:3] + ["  { GuestJmp* j_ = guest_setjmp_slot(c, c->r[0]); }", "}"]
assert reg_locals(sj, 3) == sj
sh = [f[0], "  c->r[0] = sh_lsl_c(c, c->r[0], c->r[1]); if (c->cf) { c->r[0] = c->r[1]; }", "  return;", "}"]
assert "Flags F" not in "\n".join(reg_locals(sh, 3)) and "c->cf" in "\n".join(reg_locals(sh, 3))
print("reg_locals ok")
# vector registers: S1 = half of D0, &c->vr.x[2] = D2 + D3 (written), D5 only read
v = [f[0], "  c->vr.f[1] = c->vr.f[1] * c->vr.d[5];", "  memcpy(&c->vr.x[2], &c->vr.x[0], 16);", "  F_00002000(c);",
     "  return;", "}"]
tv = "\n".join(reg_locals(v, 3, vec=True))
assert "VRegs V; V.x[0] = c->vr.x[0]; V.x[1] = c->vr.x[1]; V.x[2] = c->vr.x[2]; V.x[3] = c->vr.x[3]; V.x[5] = c->vr.x[5];" in tv, tv
assert "V.f[1] = V.f[1] * V.d[5];" in tv and "memcpy(&V.x[2], &V.x[0], 16);" in tv, tv
assert "c->vr.x[0] = V.x[0]; c->vr.x[1] = V.x[1]; c->vr.x[2] = V.x[2]; c->vr.x[3] = V.x[3]; F_00002000(c);" in tv, tv
assert "c->vr.x[5] = V.x[5]" not in tv, tv
nv = [f[0], "  neon_tbl(c, 0, 2, 1, 4, 0); c->vr.f[0] = 1.0f;", "  return;", "}"]
assert "VRegs" not in "\n".join(reg_locals(nv, 3, vec=True))
print("vector locals ok")
