"""Compile the lifted game code (lift.py output) into game.dll, next to tms.exe.

    python tools/setup/build_game.py --gen <lift.py out dir> --obj <obj dir> --out <game.dll>
        --include <dir with guest.h> --lib <tms.lib> --lib <crt_math.lib> --lib <vcruntime.lib> --def <game.def>
        [--clang clang.exe] [--lld lld-link.exe] [-j N]

Linux: the same with --out <game.so> and no --lib / --def. It needs clang and lld (ld.lld) and links against the libc /
libm that tms already loads; the runtime functions come from tms itself (built with -rdynamic).

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
LINUX = sys.platform.startswith("linux")
CFLAGS = ["--target=x86_64-pc-windows-msvc", "-std=gnu11", "-O1", "-g", "-gcodeview", "-DNDEBUG", "-DNX_GAME_DLL",
          "-nostdinc", "-ffp-contract=off", "-fwrapv", "-fno-strict-aliasing", "-w"]
if LINUX:
    # a shared library: position independent, only table.c's tables exported (guest.h), unwind tables so the
    # runtime's C++ exceptions (thread exit) and longjmp pass through the generated frames
    CFLAGS = ["--target=x86_64-linux-gnu", "-std=gnu11", "-O1", "-DNDEBUG", "-DNX_GAME_DLL", "-nostdinc", "-fPIC",
              "-fvisibility=hidden", "-funwind-tables", "-ffp-contract=off", "-fwrapv", "-fno-strict-aliasing", "-w"]

# -O2 for the generated code (s117, after Astral Chain Recomp's build_game.py): Shibuya on 2 cores 133 -> 149 fps against
# -O1. Their notes: clang 21 at -O2 miscompiled their game's video decoder, clang 22+ did not; older clang stays at -O1.
MIN_O2_CLANG = 22


def clang_major(clang):
    try:
        out = subprocess.run([clang, "--version"], capture_output=True, text=True).stdout
        return int(out.split("version ")[1].split(".")[0])
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", required=True)
    ap.add_argument("--obj", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--include", required=True)
    ap.add_argument("--lib", action="append", default=[])
    ap.add_argument("--def", dest="deffile", required=not LINUX)
    ap.add_argument("--clang", default="clang")
    ap.add_argument("--lld", default="ld.lld" if LINUX else "lld-link")
    ap.add_argument("-j", type=int, default=os.cpu_count() or 4)
    ap.add_argument("--opt", default="auto", help="optimisation flags for the generated code; auto: -O2 with clang "
                    f"{MIN_O2_CLANG} or newer, else -O1 (objects are not rebuilt when only this changes: use another --obj)")
    ap.add_argument("--no-lto", dest="lto", action="store_false", default=not LINUX,
                    help="no ThinLTO (default on Windows: s117 Shibuya one core +3%%, 129.0 -> 132.9 fps)")
    ap.add_argument("--pgo-gen", action="store_true", help="instrumented build: game.dll writes a .profraw (dev only)")
    # tms.profdata (s117): Shibuya + tutorial battle + office / camp runs of an instrumented build (--pgo-gen, NX_PGO_OUT,
    # llvm-profdata merge). It matches the lifted code of this lift.py; after a lifter change, record it again (stale
    # functions are only left unoptimised). Shibuya one core with ThinLTO: 133.9 -> 137.5 fps. Windows only (the
    # bundled clang reads it; a Linux system clang may be older than the profile format).
    prof = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tms.profdata")
    ap.add_argument("--pgo-use", default=prof if os.path.exists(prof) and not LINUX else None,
                    help="profile (.profdata) for profile-guided optimisation (default: tms.profdata next to this script)")
    ap.add_argument("--no-pgo", dest="pgo_use", action="store_const", const=None, help="no profile")
    a = ap.parse_args()
    if a.lto:
        CFLAGS.append("-flto=thin")
    if a.pgo_gen:
        CFLAGS.append("-fprofile-instr-generate")
    if a.pgo_gen:
        a.pgo_use = None
    if a.pgo_use:
        print(f"profile-guided: {a.pgo_use}", flush=True)
        CFLAGS.extend([f"-fprofile-instr-use={a.pgo_use}", "-Wno-profile-instr-unprofiled", "-Wno-profile-instr-out-of-date"])
    opt = a.opt
    if opt == "auto":
        major = clang_major(a.clang)
        opt = "-O2" if major and major >= MIN_O2_CLANG else "-O1"
        print(f"generated code: {opt} (clang {major})", flush=True)
    CFLAGS[CFLAGS.index("-O1"):CFLAGS.index("-O1") + 1] = opt.split()

    os.makedirs(a.obj, exist_ok=True)
    with open(os.path.join(a.gen, "files.txt")) as f:
        sources = [os.path.join(a.gen, l.strip()) for l in f if l.strip()]
    if not LINUX:
        stub = os.path.join(a.obj, "fltused.c")  # the marker symbol the MSVC CRT normally defines for float code
        if not os.path.exists(stub):
            with open(stub, "w") as f:
                f.write("int _fltused = 0x9875;\n")
        if not a.pgo_gen:  # msvcrt.lib (instrumented build) has its own
            sources.append(stub)
        if a.pgo_gen:  # the profile runtime is built with /GS: its stack cookie, without the CRT's startup code
            gs = os.path.join(a.obj, "pgo_gs.c")
            with open(gs, "w") as f:
                f.write("unsigned long long __security_cookie = 0x2B992DDFA232ull;\n"
                        "void __security_check_cookie(unsigned long long c) { (void)c; }\n"
                        "int atexit(void (*f)(void)) { (void)f; return 0; }\n")
            sources.append(gs)
    deps = [os.path.join(a.include, "guest.h"), os.path.join(a.gen, "funcs.h"), os.path.abspath(__file__)] +         ([a.pgo_use] if a.pgo_use else [])
    newest_dep = max(os.path.getmtime(d) for d in deps)

    def obj_of(src):
        return os.path.join(a.obj, os.path.basename(src) + (".o" if LINUX else ".obj"))

    def stale(src):
        o = obj_of(src)
        return not os.path.exists(o) or os.path.getmtime(o) < max(os.path.getmtime(src), newest_dep)

    todo = [s for s in sources if stale(s)]
    # biggest files first: the long ones start early, the pool stays full at the end
    todo.sort(key=os.path.getsize, reverse=True)

    def compile_one(src):
        o = obj_of(src)
        # the _fltused marker stays a real object: as LTO bitcode nothing at IR level keeps it, and the link misses it
        flags = [f for f in CFLAGS if f != "-flto=thin"] if src.endswith("fltused.c") else CFLAGS
        r = subprocess.run([a.clang, *flags, "-I", a.include, "-I", a.gen, "-c", src, "-o", o + ".part"],
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
    inputs = objs + a.lib + ([a.deffile] if a.deffile else [])
    if os.path.exists(a.out) and os.path.getmtime(a.out) >= max(os.path.getmtime(p) for p in inputs):
        print("game.dll up to date", flush=True)
        return
    print("link", flush=True)
    out_dir = os.path.dirname(os.path.abspath(a.out))
    part = os.path.join(out_dir, "game.part.so" if LINUX else "game.part.dll")
    rsp = os.path.join(a.obj, "link.rsp")  # 40+ long paths: a response file keeps the command line short
    with open(rsp, "w") as f:
        f.write("\n".join(f'"{p}"' for p in objs + a.lib) + "\n")
    if LINUX:
        # no libraries at all: the few C library functions (math, _setjmp) and the runtime's entry points bind when tms
        # loads game.so, to what tms itself uses, so game.so asks for no particular glibc version
        lld = a.lld if os.path.dirname(a.lld) else None
        cmd = [a.clang, "--target=x86_64-linux-gnu", "-shared", "-nostdlib", "-Wl,-O1", "-Wl,--gc-sections",
               "-Wl,-z,noexecstack", "-o", part, f"@{rsp}"]
        cmd.insert(1, f"--ld-path={lld}" if lld else "-fuse-ld=lld")
        if subprocess.run(cmd).returncode:
            sys.exit("build_game: link failed")
        os.replace(part, a.out)
        print(f"wrote {a.out}", flush=True)
        return
    extra = []
    if a.lto:
        extra += [f"/opt:lldltojobs={a.j}", f"/lldltocache:{os.path.join(a.obj, 'lto-cache')}", "/opt:lldlto=2"]
    if a.pgo_gen:
        # dev only: the profile runtime needs the real C runtime (Visual Studio + Windows SDK libraries); the runtime
        # (dispatch.cpp game_load) calls the exported writer, since a /NOENTRY DLL runs no exit hooks
        import glob
        vc = sorted(glob.glob(r"C:\Program Files\Microsoft Visual Studio\2022\*\VC\Tools\MSVC\*\lib\x64"))[-1]
        sdk = sorted(glob.glob(r"C:\Program Files (x86)\Windows Kits\10\Lib\10.*"))[-1]
        extra += [os.path.join(os.path.dirname(a.clang), "..", "lib", "clang", str(clang_major(a.clang)), "lib", "windows",
                               "clang_rt.profile-x86_64.lib"),
                  f"/LIBPATH:{vc}", f"/LIBPATH:{sdk}\\ucrt\\x64", f"/LIBPATH:{sdk}\\um\\x64",
                  os.path.join(os.path.dirname(a.clang), "..", "lib", "clang", str(clang_major(a.clang)), "lib", "windows",
                               "clang_rt.builtins-x86_64.lib"), "ucrt.lib", "vcruntime.lib", "oldnames.lib", "kernel32.lib", "msvcrt.lib",
                  "/EXPORT:__llvm_profile_write_file", "/EXPORT:__llvm_profile_set_filename"]
    r = subprocess.run([a.lld, "/nologo", "/DLL", "/NOENTRY", "/NODEFAULTLIB", "/MACHINE:X64", "/DEBUG", *extra,
                        f"/DEF:{a.deffile}", f"/OUT:{part}", f"/PDB:{os.path.splitext(a.out)[0]}.pdb",
                        f"/IMPLIB:{os.path.join(a.obj, 'game.lib')}", f"@{rsp}"])
    if r.returncode:
        sys.exit("build_game: link failed")
    os.replace(part, a.out)
    print(f"wrote {a.out}", flush=True)


if __name__ == "__main__":
    main()
