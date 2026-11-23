r"""Battle voice subtitles, step 1: Japanese transcripts of the game's battle voice files.

Usage: python tools/subs/transcribe.py <Sound/Voice/Jp dir> <out dir> [prefix ...]
Decodes every <prefix>*.adx (default BTL_) with vgmstream-cli to <out>/wav, transcribes it with faster-whisper
large-v3 (the whisper venv, CUDA) and writes <out>/transcripts_jp.json {file stem: {"jp": text, "sec": length}}.
Resumable: stems already in the json are skipped. Run with the whisper venv python (Tools/whisper-venv).
"""
import glob, json, os, subprocess, site, sys, wave
for sp in site.getsitepackages():
    for b in glob.glob(os.path.join(sp, 'nvidia', '*', 'bin')):
        os.add_dll_directory(b)
        os.environ['PATH'] = b + ';' + os.environ['PATH']
import numpy as np
from faster_whisper import WhisperModel

VGM = r'C:\Users\user\Tools\vgmstream\vgmstream-cli.exe'


def load16k(path):
    # stdlib WAV read + FFT resample (PyAV in this venv does not work with faster-whisper)
    w = wave.open(path)
    sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
    a = np.frombuffer(w.readframes(n), np.int16).astype(np.float32).reshape(-1, ch).mean(1) / 32768
    m = int(round(len(a) * 16000 / sr))
    return np.fft.irfft(np.fft.rfft(a)[:m // 2 + 1], m).astype(np.float32) * (m / len(a)), n / sr


def main():
    src, out = sys.argv[1], sys.argv[2]
    prefixes = sys.argv[3:] or ['BTL_']
    os.makedirs(os.path.join(out, 'wav'), exist_ok=True)
    outp = os.path.join(out, 'transcripts_jp.json')
    done = json.load(open(outp, encoding='utf-8')) if os.path.exists(outp) else {}
    files = sorted(f for f in os.listdir(src) if f.endswith('.adx') and f.startswith(tuple(prefixes)))
    model = WhisperModel('large-v3', device='cuda', compute_type='float16')
    for i, f in enumerate(files):
        stem = f[:-4]
        if stem in done:
            continue
        wav = os.path.join(out, 'wav', stem + '.wav')
        if not os.path.exists(wav):
            subprocess.run([VGM, '-o', wav, os.path.join(src, f)], check=True, capture_output=True)
        a, sec = load16k(wav)
        segs, _ = model.transcribe(a, language='ja', beam_size=5, condition_on_previous_text=False, vad_filter=False)
        done[stem] = {'jp': ''.join(s.text for s in segs).strip(), 'sec': round(sec, 2)}
        if i % 50 == 49 or i == len(files) - 1:
            json.dump(done, open(outp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
            print(f'{i + 1} / {len(files)}', flush=True)
    json.dump(done, open(outp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)


if __name__ == '__main__':
    main()
