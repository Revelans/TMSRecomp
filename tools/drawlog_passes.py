# drawlog_passes.py <log> [start line]: summarise an NX_LOG_DRAWS / NX_CONTROL drawlog frame as passes:
# consecutive draws into the same target, with the textures they sample (guest address, size, format) and shaders.
import re, sys

lines = open(sys.argv[1], encoding="utf-8", errors="replace").read().splitlines()
start = int(sys.argv[2]) if len(sys.argv) > 2 else next(i for i, l in enumerate(lines) if "drawlog: frame" in l or "NX_LOG_DRAWS: frame" in l)
tex, passes, cur = [], [], None
for l in lines[start + 1:]:
    if "frames:" in l and "/s" in l: continue
    if "NX_CONTROL drawlog" in l or "replay finished" in l: break
    m = re.search(r"tex cbuf .* -> tex (\w+) (\d+x\d+) nvn fmt (0x\w+)", l)
    if m: tex.append(f"{m[1]}:{m[2]}:{m[3]}"); continue
    m = re.search(r"viewport (\S+ \S+ \S+ \S+) scissor .* target0 (\w+)", l)
    if m: vp, tgt = m[1], m[2]; continue
    m = re.search(r"draw op \d+ mode (\d+) args (\S+ \S+).*vs (\w+) fs (\w+)", l)
    if m:
        key = (tgt, vp)
        if not cur or cur["key"] != key:
            cur = {"key": key, "n": 0, "tex": set(), "sh": set()}
            passes.append(cur)
        cur["n"] += 1
        cur["tex"].update(tex)
        cur["sh"].add(m[3])
        tex = []
for i, p in enumerate(passes):
    print(f"{i:3} target {p['key'][0]} vp {p['key'][1]} draws {p['n']:4} vs {','.join(sorted(p['sh']))[:40]}")
    for t in sorted(p["tex"]): print("        samples", t)
