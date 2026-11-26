"""Make runtime/src/request_hints.inc from tools/lua/request_hints.txt and the game's flag names.
python tools/lua/request_hints.py <flags.txt (tools/lua/flagnames.py output)>"""
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
flags = {n: int(v, 16) for v, n in (l.split() for l in open(sys.argv[1]) if l.strip())}
esc = lambda s: s.replace('\\', '\\\\').replace('"', '\\"')
out = []
for l in open(os.path.join(here, 'request_hints.txt'), encoding='utf-8'):
    if not l.strip() or l.startswith('#'):
        continue
    q, name, giver, how = l.rstrip('\n').split('|')
    ids = [flags['FLG_MAP_QUEST_%02d_%s' % (int(q), s)] for s in ('AVAILABLE', 'START', 'END')]
    out.append('{%s, 0x%x, 0x%x, 0x%x, L"%s", L"%s", L"%s"},' % (q, *ids, esc(name), esc(giver), esc(how)))
open(os.path.join(here, '..', '..', 'runtime', 'src', 'request_hints.inc'), 'w', encoding='utf-8', newline='\n').write(
    '// made by tools/lua/request_hints.py from tools/lua/request_hints.txt: {quest, available, started, done flag, name, giver, how}\n'
    + '\n'.join(out) + '\n')
print(len(out), 'requests')
