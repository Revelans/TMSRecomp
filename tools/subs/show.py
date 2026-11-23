"""Print transcripts of one group for translating: key|seconds|Japanese (python tools/subs/show.py <json> BTL_ACT [id]).
Lines without words (grunts, shouts, laughs: only the kana in GRUNT) and lines already in en/<group>.txt are skipped."""
import json, os, re, sys

GRUNT = set('あぁいぃうぅえぇおぉはふへほんくぐゃやゅゆょよっッーァィゥェォアイウエオハフヘホンクグ!！?？、。…〜~ 　')


def main():
    d = json.load(open(sys.argv[1], encoding='utf-8'))
    group, who = sys.argv[2] + '_', sys.argv[3] if len(sys.argv) > 3 else ''
    en = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'en', sys.argv[2] + '.txt')
    done = set()
    for f in os.listdir(os.path.dirname(en)):  # <group>.txt and <group>_<n>.txt
        if re.fullmatch(re.escape(sys.argv[2]) + r'(_\d+)?\.txt', f):
            done |= {l.split('|')[0] for l in open(os.path.join(os.path.dirname(en), f), encoding='utf-8')}
    for k, v in d.items():
        key = k[len(group):]
        if not k.startswith(group) or key in done or who not in key or key.endswith('_mix'):  # mixes: build.py
            continue
        jp = v['jp']
        if not jp or set(jp) <= GRUNT:
            continue
        jp = re.sub(r'(.)\1{4,}', r'\1\1\1', jp)[:50]  # whisper repetition loops
        print(f"{key}|{v['sec']}|{jp}")


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
