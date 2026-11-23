"""List the libvpx C sources of a VP9-decoder-only build, from libvpx's own makefiles and a configured build dir.

There is no `make` on our Windows setup, so this evaluates the few makefile forms libvpx's source lists use
(VAR-yes / VAR-$(FLAG) += file, ifeq/ifneq on one flag or $(filter yes,...), else, endif).
Usage: python tools/vpx_sources.py <libvpx src> <configured build dir>  -> writes <build dir>/sources.txt
"""
import glob
import os
import re
import sys

src, gen = sys.argv[1], sys.argv[2]
cfg = {}
for line in open(glob.glob(os.path.join(gen, "libs-*.mk"))[0]):  # configure's flags (CONFIG_*, HAVE_*)
    m = re.match(r"(\w+)=(\w*)\s*$", line)
    if m:
        cfg[m.group(1)] = m.group(2)


def val(expr):  # "$(FLAG)" or "yes"
    m = re.fullmatch(r"\$\((\w+)\)", expr.strip())
    return cfg.get(m.group(1), "") if m else expr.strip()


def cond(line):
    m = re.match(r"(ifeq|ifneq)\s*\((.*),(.*)\)\s*$", line)
    if not m:
        sys.exit("unknown conditional: " + line)
    a, b = m.group(2).strip(), m.group(3).strip()
    f = re.fullmatch(r"\$\(filter yes,(.*)\)", a)
    a = "yes" if f and any(val(x) == "yes" for x in f.group(1).split()) else ("" if f else val(a))
    return (a == val(b)) == (m.group(1) == "ifeq")


def sources(mk, vars_):
    out, stack = [], []
    for line in open(os.path.join(src, mk)):
        line = line.split("#")[0].rstrip()
        s = line.strip()
        if s.startswith(("ifeq", "ifneq")):
            stack.append(cond(s))
        elif s == "else":
            stack[-1] = not stack[-1]
        elif s == "endif":
            stack.pop()
        elif all(stack):
            m = re.match(r"(\w+)-(yes|\$\((\w+)\))\s*\+=\s*(\S+)", s)
            if m and m.group(1) in vars_ and (m.group(2) == "yes" or cfg.get(m.group(3)) == "yes"):
                out.append(m.group(4))
    return out


lists = [
    ("vpx/vpx_codec.mk", "vpx/", {"API_SRCS"}),
    ("vpx_mem/vpx_mem.mk", "vpx_mem/", {"MEM_SRCS"}),
    ("vpx_scale/vpx_scale.mk", "vpx_scale/", {"SCALE_SRCS"}),
    ("vpx_ports/vpx_ports.mk", "vpx_ports/", {"PORTS_SRCS"}),
    ("vpx_dsp/vpx_dsp.mk", "vpx_dsp/", {"DSP_SRCS"}),
    ("vpx_util/vpx_util.mk", "vpx_util/", {"UTIL_SRCS"}),
    ("vp9/vp9_common.mk", "vp9/", {"VP9_COMMON_SRCS"}),
    ("vp9/vp9dx.mk", "vp9/", {"VP9_DX_SRCS"}),
]
files = [os.path.join(src, pre + f).replace("\\", "/") for mk, pre, v in lists for f in sources(mk, v) if f.endswith(".c")]
files.append(os.path.join(gen, "vpx_config.c").replace("\\", "/"))
open(os.path.join(gen, "sources.txt"), "w").write("\n".join(files) + "\n")
print(len(files), "sources")
