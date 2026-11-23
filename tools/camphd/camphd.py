"""Camp menu background movies in 4K (user decision 11-02: AI re-encode offline).
Per Movie/camp/*.usm in <data>/romfs/Pack/pack_049_movie_camp.cpk: USM -> IVF (usm2ivf), ffmpeg decodes the 1280x720
frames, Real-ESRGAN realesr-animevideov3 x3 makes them 3840x2160, ffmpeg libvpx-vp9 encodes them to
<data>/movie_hd/camp/<name>.ivf, which the runtime plays instead (hle_movie.cpp). Skips movies already done; frames are
deleted after each movie. Story movies: camphd.py <data> <esrgan dir> <data>/story_hd pack_050_movie.cpk story
Sofdec.Prime (MPEG-1) movies (the uncensored mod's m06 / m07 / m12): <name>_prime.ivf + <name>_prime.thm (16x9 Y block
means per frame, 144 bytes; the runtime matches the game's decoded frames by it, hle_movie.cpp mana_frame_copy):
camphd.py <data> <esrgan dir> <data>/prime_hd mods/uncensored/romfs/Pack/pack_050_movie.cpk story_mod
Usage: camphd.py <data> <esrgan dir> [work dir] [pack] [subdir]  (pack: a name in romfs/Pack or a path from <data>)"""
import os
import shutil
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
sys.path.insert(0, os.path.join(here, ".."))
import usm2ivf  # noqa: E402


def first_packet_hash(ivf, packets=2):
    """FNV-1a 64 of the first 4096 bytes of frame 0, continued over frame 1's (hle_movie.cpp movie_packet_hash; story
    movies share black first packets, packet 1 differs; packets=1 = the old single-packet key of the camp files)"""
    b = open(ivf, "rb").read()
    h, o = 1469598103934665603, 32
    for _ in range(packets):
        n = int.from_bytes(b[o:o + 4], "little")
        for c in b[o + 12:o + 12 + min(n, 4096)]:
            h = ((h ^ c) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
        o += 12 + n
    return h


def main(data, esrgan_dir, work=None, pack="pack_049_movie_camp.cpk", sub="camp"):
    work = work or os.path.join(data, "camp_hd")
    out_dir = os.path.join(data, "movie_hd", sub)
    os.makedirs(out_dir, exist_ok=True)
    usm_dir = os.path.join(work, "usm")
    if not os.path.isdir(usm_dir):
        src = os.path.join(data, pack) if os.sep in pack or "/" in pack else os.path.join(data, "romfs", "Pack", pack)
        subprocess.run([sys.executable, os.path.join(here, "..", "cpk.py"), "extract", src, usm_dir], check=True)
    usms = sorted(os.path.join(r, f) for r, _, fs in os.walk(usm_dir) for f in fs if f.endswith(".usm"))
    for path in usms:
        name = os.path.basename(path)[:-4]
        ivf, lo, hi = (os.path.join(work, x) for x in (name + ".ivf", "lo", "hi"))
        chunks = list(usm2ivf.frames(open(path, "rb").read()))
        prime = chunks[0][:4] == b"\0\0\1\xb3"  # MPEG-1 sequence header (Sofdec.Prime), not IVF
        if prime:
            dst = os.path.join(out_dir, name + "_prime.ivf")  # runtime matches it by the thumbnails
            if os.path.exists(dst):
                continue
            ivf = os.path.join(work, name + ".m1v")
            open(ivf, "wb").write(b"".join(chunks))
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", ivf, "-fps_mode", "passthrough", "-vf",
                            "extractplanes=y,scale=16:9:flags=area", "-f", "rawvideo", "-pix_fmt", "gray",
                            dst[:-4] + ".thm.tmp"], check=True)
        else:
            usm2ivf.main(path, ivf)
            dst = os.path.join(out_dir, "%s_%016x.ivf" % (name, first_packet_hash(ivf)))  # runtime finds it by the hash
            if os.path.exists(dst):
                continue
        n = len(chunks)
        if len(os.listdir(hi) if os.path.isdir(hi) else []) != n:  # an interrupted run's frames are kept
            for d in (lo, hi):
                shutil.rmtree(d, ignore_errors=True)
                os.makedirs(d)
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", ivf, "-fps_mode", "passthrough",
                            os.path.join(lo, "%04d.png")], check=True)
            subprocess.run([os.path.join(esrgan_dir, "realesrgan-ncnn-vulkan.exe"), "-i", lo, "-o", hi,
                           "-n", "realesr-animevideov3", "-s", "3", "-f", "png"], check=True, capture_output=True)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", "30", "-i",
                        os.path.join(hi, "%04d.png"), "-c:v", "libvpx-vp9", "-pix_fmt", "yuv420p", "-crf", "24",
                        "-b:v", "0", "-deadline", "good", "-cpu-used", "4", "-row-mt", "1", "-threads", "16",
                        "-tile-columns", "2", "-g", "60", "-f", "ivf", dst + ".tmp"], check=True)
        os.replace(dst + ".tmp", dst)
        if prime:
            os.replace(dst[:-4] + ".thm.tmp", dst[:-4] + ".thm")
        print(name, "done", flush=True)
        for d in (lo, hi):
            shutil.rmtree(d)
        os.remove(ivf)


if __name__ == "__main__":
    main(*sys.argv[1:6])
