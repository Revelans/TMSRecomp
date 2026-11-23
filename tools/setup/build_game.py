"""Compile the lifted game code (lift.py output) into game.dll, next to tms.exe.

    python tools/setup/build_game.py --gen <lift.py out dir> --obj <obj dir> --out <game.dll>
        --include <dir with guest.h> --lib <tms.lib> --lib <crt_math.lib> --lib <vcruntime.lib> --def <game.def>
        [--clang clang.exe] [--lld lld-link.exe] [-j N]

One script, two callers: the dev build (CMakeLists.txt) and the player's first-run setup (setup.py), so both build
game.dll the same way. Needs only clang + lld-link: no C library headers or Windows SDK (guest.h NX_GAME_DLL). Objects
are rebuilt only when their .c, a header or this script is newer. Progress on stdout: "compile i/n name", "link".
"""
import argparse
import concurrent.futures
import os
import subprocess
import sys

# same code generation as the old static build (CMake RelWithDebInfo + NX_GEN_OPT): -O1, guest float semantics
CFLAGS = ["--target=x86_64-pc-windows-msvc", "-std=gnu11", "-O1", "-g", "-gcodeview", "-DNDEBUG", "-DNX_GAME_DLL",
          "-nostdinc", "-ffp-contract=off", "-fwrapv", "-fno-strict-aliasing", "-w"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", required=True)
    ap.add_argument("--obj", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--include", required=True)
    ap.add_argument("--lib", action="append", default=[])
    ap.add_argument("--def", dest="deffile", required=True)
    ap.add_argument("--clang", default="clang")
    ap.add_argument("--lld", default="lld-link")
    ap.add_argument("-j", type=int, default=os.cpu_count() or 4)
    a = ap.parse_args()

    os.makedirs(a.obj, exist_ok=True)
    with open(os.path.join(a.gen, "files.txt")) as f:
        sources = [os.path.join(a.gen, l.strip()) for l in f if l.strip()]
    stub = os.path.join(a.obj, "fltused.c")  # the marker symbol the MSVC CRT normally defines for float code
    if not os.path.exists(stub):
        with open(stub, "w") as f:
            f.write("int _fltused = 0x9875;\n")
    sources.append(stub)
    deps = [os.path.join(a.include, "guest.h"), os.path.join(a.gen, "funcs.h"), os.path.abspath(__file__)]
    newest_dep = max(os.path.getmtime(d) for d in deps)

    def obj_of(src):
        return os.path.join(a.obj, os.path.basename(src) + ".obj")

    def stale(src):
        o = obj_of(src)
        return not os.path.exists(o) or os.path.getmtime(o) < max(os.path.getmtime(src), newest_dep)

    todo = [s for s in sources if stale(s)]
    # biggest files first: the long ones start early, the pool stays full at the end
    todo.sort(key=os.path.getsize, reverse=True)

    def compile_one(src):
        o = obj_of(src)
        r = subprocess.run([a.clang, *CFLAGS, "-I", a.include, "-I", a.gen, "-c", src, "-o", o + ".part"],
                           capture_output=True, text=True)
        if r.returncode:
            return src, r.stdout + r.stderr
        os.replace(o + ".part", o)  # a cancelled or failed compile never leaves a half object that looks current
        return src, None

    failed = []
    with concurrent.futures.ThreadPoolExecutor(max(1, a.j)) as ex:
        for i, (src, err) in enumerate(ex.map(compile_one, todo), 1):
            print(f"compile {i}/{len(todo)} {os.path.basename(src)}", flush=True)
            if err:
                failed.append(src)
                print(err, flush=True)
    if failed:
        sys.exit(f"build_game: {len(failed)} file(s) failed to compile")

    objs = [obj_of(s) for s in sources]
    inputs = objs + a.lib + [a.deffile]
    if os.path.exists(a.out) and os.path.getmtime(a.out) >= max(os.path.getmtime(p) for p in inputs):
        print("game.dll up to date", flush=True)
        return
    print("link", flush=True)
    out_dir = os.path.dirname(os.path.abspath(a.out))
    part = os.path.join(out_dir, "game.part.dll")
    rsp = os.path.join(a.obj, "link.rsp")  # 40+ long paths: a response file keeps the command line short
    with open(rsp, "w") as f:
        f.write("\n".join(f'"{p}"' for p in objs + a.lib) + "\n")
    r = subprocess.run([a.lld, "/nologo", "/DLL", "/NOENTRY", "/NODEFAULTLIB", "/MACHINE:X64", "/DEBUG",
                        f"/DEF:{a.deffile}", f"/OUT:{part}", f"/PDB:{os.path.splitext(a.out)[0]}.pdb",
                        f"/IMPLIB:{os.path.join(a.obj, 'game.lib')}", f"@{rsp}"])
    if r.returncode:
        sys.exit("build_game: link failed")
    os.replace(part, a.out)
    print(f"wrote {a.out}", flush=True)


if __name__ == "__main__":
    main()
