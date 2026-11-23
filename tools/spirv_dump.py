"""Translate a shader dumped by `drawlog` with the shaderc sidecar and print the SPIR-V the runtime would get, one
instruction per line (opcode names from the Ryujinx source's Spv.Generator enum; operands as raw %ids / numbers).
Usage (from private/tms):
    python ../../tools/spirv_dump.py analysis/code_XXXXXXXX_1_ed0_20.bin out.txt [attr types, e.g. 7=2,1=0]"""
import os
import re
import struct
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
src, out = sys.argv[1], sys.argv[2]
_, _, stage, coff, csize = os.path.basename(src)[:-4].split("_")
stage, coff, csize = int(stage), int(coff, 16), int(csize, 16)
code = open(src, "rb").read()
req = struct.pack("<III", 0x4853584E, stage, len(code))
if stage == 0:
    req += struct.pack("<III", 1, 1, 1)
req += struct.pack("<II", coff, csize)
if stage == 1:
    types = bytearray(32)
    for kv in (sys.argv[3].split(",") if len(sys.argv) > 3 else []):
        k, v = kv.split("=")
        types[int(k)] = int(v)
    req += bytes(types)
req += code
dll = os.path.join(here, "..", "private", "tms", "shaderc", "NxShader.dll")
r = subprocess.run(["dotnet", dll], input=req, capture_output=True)
status, size, n = struct.unpack_from("<III", r.stdout)
assert status == 0, r.stderr.decode()
spv = struct.unpack_from(f"<{n // 4}I", r.stdout, 12)
open(out[:-4] + ".spv", "wb").write(r.stdout[12:12 + n])

enum = open(os.path.join(here, "..", "private", "third_party", "ryubing", "src", "Spv.Generator", "spirv.cs")).read()
body = enum[enum.index("public enum Op"):]
body = body[:body.index("}")]
names = {int(v): k for k, v in re.findall(r"(Op\w+) = (\d+),", body)}
# opcodes with a result type + result id (the common case); the rest print raw operands
no_result = {"OpStore", "OpBranch", "OpBranchConditional", "OpReturn", "OpReturnValue", "OpKill", "OpSelectionMerge",
             "OpLoopMerge", "OpDecorate", "OpMemberDecorate", "OpName", "OpMemberName", "OpEntryPoint", "OpExecutionMode",
             "OpCapability", "OpExtension", "OpMemoryModel", "OpSwitch", "OpFunctionEnd", "OpSource", "OpUnreachable"}
result_only = {"OpLabel", "OpTypeVoid", "OpTypeBool", "OpTypeInt", "OpTypeFloat", "OpTypeVector", "OpTypeMatrix",
               "OpTypeArray", "OpTypeRuntimeArray", "OpTypeStruct", "OpTypePointer", "OpTypeFunction", "OpExtInstImport",
               "OpTypeImage", "OpTypeSampler", "OpTypeSampledImage"}
lines = []
w = 5
while w < len(spv):
    wc, op = spv[w] >> 16, spv[w] & 0xFFFF
    args = list(spv[w + 1:w + wc])
    name = names.get(op, f"Op{op}")
    if name in ("OpName", "OpExtInstImport", "OpSourceExtension", "OpExtension"):
        raw = struct.pack(f"<{len(args)}I", *args)
        s = raw[(4 if name == "OpName" else 0):].split(b"\0")[0].decode(errors="replace")
        lines.append(f"{name} {'%' + str(args[0]) if name == 'OpName' else ''} \"{s}\"")
    elif name in result_only and args:
        lines.append(f"%{args[0]} = {name} " + " ".join(str(a) for a in args[1:]))
    elif name not in no_result and len(args) >= 2:
        lines.append(f"%{args[1]} = {name} %{args[0]} " + " ".join(f"%{a}" for a in args[2:]))
    else:
        lines.append(f"{name} " + " ".join(f"%{a}" for a in args))
    w += wc
open(out, "w").write("\n".join(lines) + "\n")
print(len(lines), "instructions ->", out)
