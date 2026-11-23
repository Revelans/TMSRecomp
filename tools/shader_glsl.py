"""Translate a shader dumped by `drawlog` (analysis/code_<src>_<stage>_<consts off>_<consts size>.bin) to GLSL with the
shaderc sidecar, for reading. Usage (from private/tms):
    python ../../tools/shader_glsl.py analysis/code_XXXXXXXX_1_0_0.bin out_dir [attr types, e.g. 7=2,1=0]
Attribute types (vertex only): location=Ryujinx AttributeType (0 float, 1 sint, 2 uint)."""
import os
import struct
import subprocess
import sys

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
here = os.path.dirname(os.path.abspath(__file__))
dll = os.path.join(here, "..", "private", "tms", "shaderc", "NxShader.dll")
r = subprocess.run(["dotnet", dll], input=req, capture_output=True, env={**os.environ, "NXSHADER_DUMP_GLSL": out})
print("status", struct.unpack_from("<I", r.stdout)[0] if r.stdout else None, r.stderr.decode().strip())
