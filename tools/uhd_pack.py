"""UHD texture pack: upscale the textures tms.exe dumped (NX_TEX_DUMP=1) into <data>/textures/pack.

    python tools/uhd_pack.py <data> [--scale 2] [--limit N] [--tools private/tools] [--dump DIR]

Per texture in <data>/textures/dump: texconv decodes it to PNG, Real-ESRGAN (realesrgan-x4plus-anime) upscales it 4x,
ImageMagick resizes to --scale (2 = 4x the pixels; 4 = 16x, a lot of VRAM), texconv compresses to BC7 with a full mip
chain. Textures already in the pack, smaller than 16 px, larger than --max, or normal maps (mostly (0.5, 0.5, 1) blue)
are skipped, and so is everything but BCn colour formats (uncompressed RGBA8 and BC4/BC5 hold masks and data, which
the upscaler would change). Run it again after more play with dumping on: only new textures are done. --dump <data>/textures/dump_all takes the
whole game from tools/texextract/texextract.py instead of what play dumped.
Tools (not in the repo): Real-ESRGAN-ncnn-vulkan (MIT) and Microsoft texconv (MIT), ImageMagick (magick on PATH).
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile


# NVN formats: BC1 / BC2 / BC3 (+ sRGB 0x45-0x48), BC7 (0x4d, sRGB 0x4e)
COLOUR_FORMATS = {0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x4d, 0x4e}
SRGB_FORMATS = {0x45, 0x46, 0x47, 0x48, 0x4e}
BC1_FORMATS = {0x41, 0x42, 0x45, 0x46}


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError("%s failed: %s" % (os.path.basename(args[0]), (r.stderr or r.stdout).strip()[-300:]))
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("--scale", type=int, default=2, choices=(2, 3, 4))
    ap.add_argument("--small-scale", type=int, default=4, choices=(2, 3, 4),
                    help="scale for textures no larger than --small (cheap in VRAM, the most visible gain)")
    ap.add_argument("--small", type=int, default=256)
    ap.add_argument("--limit", type=int, default=0, help="at most N new textures this run")
    ap.add_argument("--chunk", type=int, default=40, help="textures per upscaler run (the pack grows as it goes)")
    ap.add_argument("--max", type=int, default=2048, help="skip textures wider or taller than this")
    ap.add_argument("--tools", default=os.path.join(os.path.dirname(__file__), "..", "private", "tools"))
    ap.add_argument("--dump", help="dumped textures (default <data>/textures/dump)")
    ap.add_argument("--sources", help="'<hash> <pack> <file>' lines (texextract.py --list): map textures get the "
                    "general model, RGBA8 Interface textures (UI atlases) are done too")
    ap.add_argument("--remip", action="store_true", help="only rebuild the mips of pack textures with transparency")
    a = ap.parse_args()
    texconv = os.path.join(a.tools, "texconv", "texconv.exe")
    if a.remip:
        return remip(os.path.join(a.data, "textures", "pack"), texconv)
    esrgan_dir = os.path.join(a.tools, "esrgan")
    esrgan = os.path.join(esrgan_dir, "realesrgan-ncnn-vulkan.exe")
    dump = a.dump or os.path.join(a.data, "textures", "dump")
    pack = os.path.join(a.data, "textures", "pack")
    os.makedirs(pack, exist_ok=True)
    source = {}  # hash -> (pack, file) of its first copy
    if a.sources:
        for line in open(a.sources, encoding="utf-8"):
            f = line.split(" ", 2)
            if len(f) == 3:
                source.setdefault(f[0], (f[1], f[2].strip()))
    have = set(os.listdir(pack))
    todo = []
    for n in sorted(os.listdir(dump)):
        if not n.endswith(".dds") or n in have or n.startswith("padicons_"):
            continue
        w, h = (int(x) for x in n.split("_")[0].split("x"))
        fmt = int(n.split("_")[1], 16)
        src = source.get(n[-20:-4], ("", ""))
        ui = fmt == 0x25 and src[1].startswith("Interface/")  # RGBA8 elsewhere holds masks and data
        if min(w, h) < 16 or max(w, h) > a.max or (fmt not in COLOUR_FORMATS and not ui):
            continue
        todo.append(n)
    if a.limit:
        todo = todo[:a.limit]
    # environment textures (stone, wood, foliage) keep their detail with the general model; the anime model flattens
    # them. Characters, UI and effects are drawn art: the anime model keeps lines clean.
    def model(n):
        return "realesrgan-x4plus" if source.get(n[-20:-4], ("",))[0] == "pack_000_map.cpk" else "realesrgan-x4plus-anime"
    todo.sort(key=lambda n: (model(n), n))
    print("%d new textures" % len(todo), flush=True)
    done = skipped = 0
    for i in range(0, len(todo), a.chunk):
        part = todo[i:i + a.chunk]
        for m in sorted({model(n) for n in part}):
            k = do_chunk([n for n in part if model(n) == m], m, a, dump, pack, texconv, esrgan, esrgan_dir)
            done += k
            skipped += len([n for n in part if model(n) == m]) - k
        print("%d / %d done (%d normal maps skipped)" % (done, len(todo), skipped), flush=True)
    print("pack: %s" % pack)


def do_chunk(todo, model, a, dump, pack, texconv, esrgan, esrgan_dir):
    tmp = tempfile.mkdtemp(prefix="uhd_")
    try:
        return chunk_work(todo, model, a, dump, pack, texconv, esrgan, esrgan_dir, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def remip(pack, texconv):
    """Packs made before 2026-11-02 built their mips without -sepalpha: texconv filtered RGB weighted by alpha, so RGB
    under transparent texels went black in every mip but the first. The game reads that RGB with alpha as a mask
    (Itsuki's trousers in Daitama: black patches with blue edges at a distance). Level 0 is kept byte for byte; the
    mips are rebuilt from it with -sepalpha. Resumable: done names go to <pack>/../remip_done.txt."""
    done_path = os.path.join(os.path.dirname(pack), "remip_done.txt")
    done = set(open(done_path).read().split()) if os.path.exists(done_path) else set()
    log = open(done_path, "a")
    tmp = tempfile.mkdtemp(prefix="remip_")
    names = sorted(n for n in os.listdir(pack) if n.endswith(".dds") and n not in done)
    fixed = 0
    try:
        for i, n in enumerate(names):
            path = os.path.join(pack, n)
            old = open(path, "rb").read()
            # texconv's BC7 DDS: 128-byte header + DX10 extension (20), dxgi 98 BC7_UNORM / 99 BC7_UNORM_SRGB
            if old[84:88] != b"DX10" or int.from_bytes(old[128:132], "little") not in (98, 99):
                log.write(n + "\n")
                continue
            srgb = int.from_bytes(old[128:132], "little") == 99
            h, w = int.from_bytes(old[12:16], "little"), int.from_bytes(old[16:20], "little")
            level0 = ((w + 3) // 4) * ((h + 3) // 4) * 16
            run([texconv, "-nologo", "-ft", "png", "-m", "1", "-y"] + (["-srgb"] if srgb else []) + ["-o", tmp, path])
            png = os.path.join(tmp, n[:-4] + ".png")
            # BC7 leaves opaque textures at alpha ~0.98: only real transparency darkened the mips
            if float(run(["magick", png, "-format", "%[fx:minima.a]", "info:"])) < 0.9:
                run([texconv, "-nologo", "-f", "BC7_UNORM_SRGB" if srgb else "BC7_UNORM", "-m", "0", "-sepalpha", "-y"] +
                    (["-srgb"] if srgb else []) + ["-o", tmp, png])
                new = bytearray(open(os.path.join(tmp, n), "rb").read())
                if len(new) != len(old) or new[:148] != old[:148]:
                    raise RuntimeError("%s: rebuilt file differs in size or header" % n)
                new[148:148 + level0] = old[148:148 + level0]
                open(os.path.join(tmp, n + ".new"), "wb").write(new)
                os.replace(os.path.join(tmp, n + ".new"), path)  # whole files only: the game may be reading the pack
                fixed += 1
            os.remove(png)
            log.write(n + "\n")
            log.flush()
            if i % 100 == 0:
                print("%d / %d checked, %d rebuilt" % (i, len(names), fixed), flush=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("done: %d rebuilt" % fixed, flush=True)


def bleed(png):
    """RGB under (nearly) transparent texels -> the colour of the nearest visible ones (pull-push). BC1 cut-outs
    decode their transparent texels as black: upscaled as an opaque picture, the black ran into the leaf edges (black
    fringes around ferns, 10-31). Alpha itself is untouched."""
    import numpy as np
    w, h = (int(x) for x in run(["magick", png, "-format", "%w %h", "info:"]).split())
    raw = subprocess.run(["magick", png, "-depth", "8", "rgba:-"], capture_output=True, check=True).stdout
    px = np.frombuffer(raw, np.uint8).reshape(h, w, 4).astype(np.float64)
    known = (px[..., 3] >= 16).astype(np.float64)
    if known.all() or not known.any():
        return
    levels = [(px[..., :3] * known[..., None], known)]
    while max(levels[-1][1].shape) > 1:  # pull: 2x2 sums of colour x weight and weight
        c, k = levels[-1]
        ph, pw = c.shape[0] % 2, c.shape[1] % 2
        c = np.pad(c, ((0, ph), (0, pw), (0, 0)))
        k = np.pad(k, ((0, ph), (0, pw)))
        levels.append((c[0::2, 0::2] + c[1::2, 0::2] + c[0::2, 1::2] + c[1::2, 1::2],
                       k[0::2, 0::2] + k[1::2, 0::2] + k[0::2, 1::2] + k[1::2, 1::2]))
    fill = levels[-1][0] / np.maximum(levels[-1][1], 1e-9)[..., None]
    for c, k in reversed(levels[:-1]):  # push: empty texels take the coarser level's average
        up = np.repeat(np.repeat(fill, 2, 0), 2, 1)[:c.shape[0], :c.shape[1]]
        fill = np.where((k > 0)[..., None], c / np.maximum(k, 1e-9)[..., None], up)
    out = px.copy()
    unknown = px[..., 3] < 16
    out[unknown, :3] = fill[unknown]
    subprocess.run(["magick", "-size", "%dx%d" % (w, h), "-depth", "8", "rgba:-", png],
                   input=np.clip(out + 0.5, 0, 255).astype(np.uint8).tobytes(), check=True)


def chunk_work(todo, model, a, dump, pack, texconv, esrgan, esrgan_dir, tmp):
    src, up = os.path.join(tmp, "src"), os.path.join(tmp, "up")
    alpha, alpha_up = os.path.join(tmp, "alpha"), os.path.join(tmp, "alpha_up")
    for d in (src, up, alpha, alpha_up):
        os.makedirs(d)
    srgb = {n: int(n.split("_")[1], 16) in SRGB_FORMATS for n in todo}
    for n in todo:  # decode (-srgb: keep the stored sRGB values, no conversion to linear)
        try:
            run([texconv, "-nologo", "-ft", "png", "-y"] + (["-srgb"] if srgb[n] else []) + ["-o", src, os.path.join(dump, n)])
        except RuntimeError as e:
            print("  skipped %s: %s" % (n, e), flush=True)
            continue
        png = os.path.join(src, n[:-4] + ".png")
        mean = run(["magick", png, "-format", "%[fx:mean.r] %[fx:mean.g] %[fx:mean.b]", "info:"]).split()
        r, g, b = (float(x) for x in mean)
        if b > 0.75 and abs(r - 0.5) < 0.12 and abs(g - 0.5) < 0.12:  # normal map: AI upscaling would bend it
            os.remove(png)
            continue
        # alpha often is a mask, not coverage: the upscaler blackens RGB where alpha is low (Itsuki turned grey).
        # Upscale RGB opaque and alpha on its own (as grey, same model: crisp edges on UI and hair cards), join after.
        if float(run(["magick", png, "-format", "%[fx:minima.a]", "info:"])) < 1:
            run(["magick", png, "-alpha", "extract", "-colorspace", "sRGB", "-type", "TrueColor", os.path.join(alpha, n[:-4] + ".png")])
            # only BC1 cut-outs store black under transparent texels; BC2 / BC3 / BC7 keep real RGB there, which the
            # game's shaders read with alpha as a mask (Itsuki's shading map turned his trousers black, 11-02)
            if int(n.split("_")[1], 16) in BC1_FORMATS:
                bleed(png)
            run(["magick", png, "-alpha", "off", png])
    pngs = os.listdir(src)
    if not pngs:
        return 0
    em = ["-n", model, "-s", "4", "-f", "png", "-m", os.path.join(esrgan_dir, "models")]
    run([esrgan, "-i", src, "-o", up] + em)
    if os.listdir(alpha):
        run([esrgan, "-i", alpha, "-o", alpha_up] + em)
    for p in sorted(os.listdir(up)):
        n = p[:-4] + ".dds"
        w, h = (int(x) for x in n.split("_")[0].split("x"))
        s = a.small_scale if max(w, h) <= a.small else a.scale
        f = os.path.join(up, p)
        if s != 4:
            run(["magick", f, "-filter", "Lanczos", "-resize", "%dx%d!" % (w * s, h * s), f])
        am = os.path.join(alpha_up, p)
        if os.path.exists(am):
            run(["magick", f, "(", am, "-colorspace", "Gray", "-filter", "Lanczos", "-resize", "%dx%d!" % (w * s, h * s), ")",
                 "-alpha", "off", "-compose", "CopyOpacity", "-composite", f])
        fmt = "BC7_UNORM_SRGB" if srgb.get(n) else "BC7_UNORM"
        out = os.path.join(tmp, n[:-4] + ".dds")
        run([texconv, "-nologo", "-f", fmt, "-m", "0", "-sepalpha", "-y"] + (["-srgb"] if srgb.get(n) else []) + ["-o", tmp, f])
        os.replace(out, os.path.join(pack, n))  # whole files only: the game may be reading the pack
    return len(pngs)


if __name__ == "__main__":
    sys.exit(main())
