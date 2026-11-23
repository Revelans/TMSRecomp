"""Battle voice subtitles, step 2: data/subtitles_en.tsv from the hand translations in tools/subs/en/<GROUP>.txt.

Usage: python tools/subs/build.py <transcripts_jp.json from transcribe.py>
en/<GROUP>.txt (or <GROUP>_<n>.txt, more of the same group) lines: <key>|English, the file stem being <GROUP>_<key>
(e.g. BTL_OPEN.txt "0001_pc1001|First strike!" -> BTL_OPEN_0001_pc1001). Output lines: stem, seconds (voice length,
from the transcripts), speaker, English. Speaker comes from the stem's character id (pc = party, mr = Mirage, em/np =
others: SPEAKERS below, else none). *_mix clips without their own line are made from the two single lines.
"""
import json, os, re, sys

SPEAKERS = {
    'pc1001': 'Itsuki', 'pc1002': 'Tsubasa', 'pc1003': 'Touma', 'pc1004': 'Maiko', 'pc1005': 'Barry',
    'pc1006': 'Eleonora', 'pc1007': 'Mamori', 'pc1008': 'Yashiro', 'pc1009': 'Kiria', 'pc1010': 'Tiki',
    'mr1051': 'Chrom', 'mr1052': 'Caeda', 'mr1053': 'Cain', 'mr1054': 'Tharja', 'mr1055': 'Virion', 'mr1056': 'Draug',
    'em1057': 'Navarre', 'em1008': 'Yashiro',
    'em2307': 'Dark Tsubasa', 'em2308': 'Dark Kiria', 'em2309': 'Dark Yashiro',  # by their lines ("I am the real Kiria")
}

# *_mix clips (party member + Mirage in one file): en text "A // B" is Mirage then party member, ">A // B" the reverse
MIRAGE_OF = {'pc1001': 'Chrom', 'pc1002': 'Caeda', 'pc1003': 'Cain', 'pc1006': 'Virion', 'pc1007': 'Draug',
             'pc1008': 'Navarre', 'pc1009': 'Tharja'}
MIRAGE_ID = {'pc1001': 'mr1051', 'pc1002': 'mr1052', 'pc1003': 'mr1053', 'pc1006': 'mr1055', 'pc1007': 'mr1056',
             'pc1008': 'em1057', 'pc1009': 'mr1054'}


def compose_mix(stem, jp, en):
    """English for an untranslated *_mix clip: its party line (same number) + the Mirage line next to it, in the order
    the Japanese transcript has them; None when either single line is missing."""
    m = re.match(r'(.*_)(\d{4})_(pc\d{4})_mix$', stem)
    if not m or m.group(1) + m.group(2) + '_' + m.group(3) not in en:
        return None
    pre, n, pc = m.group(1), int(m.group(2)), m.group(3)
    party = en[f'{pre}{n:04d}_{pc}']
    for k in (f'{pre}{n - 1:04d}_{MIRAGE_ID[pc]}', f'{pre}{n + 1:04d}_{MIRAGE_ID[pc]}'):
        if k in en and jp.get(k):
            first = jp[stem].replace(' ', '').startswith(jp[k].replace(' ', '')[:3])
            return f'{en[k]} // {party}' if first else f'>{party} // {en[k]}'
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    data = json.load(open(sys.argv[1], encoding='utf-8'))
    secs = {k: v['sec'] for k, v in data.items()}
    en = {}
    for f in sorted(os.listdir(os.path.join(here, 'en'))):
        group = re.sub(r'_\d+$', '', f[:-4])
        for line in open(os.path.join(here, 'en', f), encoding='utf-8'):
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            key, text = line.split('|', 1)
            stem = f'{group}_{key}'
            if stem not in secs:
                sys.exit(f'{f}: {key}: no such voice file')
            en[stem] = text.strip()
    if MIRAGE_ID:
        jp = {k: v['jp'] for k, v in data.items()}
        groups = {re.match(r'BTL_[A-Z]+', s).group(0) for s in en}
        for stem in secs:
            if stem.endswith('_mix') and stem not in en and stem.startswith(tuple(groups)) and stem.split('_')[-2] in MIRAGE_ID:
                text = compose_mix(stem, jp, en)
                if text:
                    en[stem] = text
    rows = []
    for stem, text in sorted(en.items()):
        m = re.search(r'(pc|mr|em|np)\d{4}', stem)
        who = SPEAKERS.get(m.group(0), '') if m else ''
        if ' // ' in text and m and m.group(0).startswith('pc'):  # *_mix: the party member and their Mirage
            mirage = MIRAGE_OF.get(m.group(0), '')
            who = f"{who} / {mirage}" if text.startswith('>') else f"{mirage} / {who}"
        rows.append(f"{stem}\t{secs[stem]}\t{who}\t{text.lstrip('>').strip()}")
    out = os.path.join(here, '..', '..', 'data', 'subtitles_en.tsv')
    with open(out, 'w', encoding='utf-8', newline='\n') as o:
        o.write('# TMSRecomp battle voice subtitles (built by tools/subs/build.py): stem, seconds, speaker, English\n')
        o.write('\n'.join(rows) + '\n')
    print(f'{out}: {len(rows)} lines')


if __name__ == '__main__':
    main()
